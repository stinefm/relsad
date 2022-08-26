import warnings

import numpy as np
from scipy.optimize import linprog

from relsad.network.systems import PowerSystem, Transmission
from relsad.Time import Time
from relsad.utils import INF

np.set_printoptions(suppress=True, linewidth=np.nan)
warnings.filterwarnings("ignore")

# flake8: noqa: C901
def shed_energy(
    power_system: PowerSystem,
    dt: Time,
    alpha: float = 1e-4,
):
    """
    Sheds the unsupplied loads of the power system over the
    time period, dt, using a linear minimization
    problem solved with linear programming

    See :doc:`/theory/opt` for more details.

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration
    dt : Time
        The current time step
    alpha : float
        Slack variable to cope with numerical noise

    Problem formulation
    --------------------

    minimize sum(P_shed_n)

    such that
        sum(P_shed_n) - sum(P_line_nl) + sum(P_gen_n) = sum(P_load_n) for all buses n

                     0 <= P_shed_n  <= P_load_n
        -P_line_nl_max <= P_line_nl <= P_line_nl_max
           P_gen_n_min <= P_gen_n   <= P_gen_n_max

    The problem is solved with the following modification to prevent numerical difficulties

    such that
        sum(P_shed_n) - sum(P_line_nl) + sum(P_gen_n) + alpha = sum(P_load_n)  for all buses n

                     0 <= P_shed_n  <= P_load_n
        -P_line_nl_max <= P_line_nl <= P_line_nl_max
           P_gen_n_min <= P_gen_n   <= P_gen_n_max
             alpha_min <= alpha     <= alpha_max

    Returns
    -------
    None

    """
    buses = list(power_system.buses)
    lines = [x for x in power_system.lines if x.connected]
    N_D = len(buses)
    N_L = len(lines)
    # Define cost function
    c = [x.get_cost() for x in buses] + [0] * N_L + [0] * N_D + [0]
    # Get loads
    p_b = [max(0, bus.pload) for bus in buses]  # Active bus load
    q_b = [max(0, bus.qload) for bus in buses]  # Reactive bus load
    # Building lhs contraint matrix
    A = _build_A_matrix(power_system)
    # Gather bounds
    p_bounds, q_bounds = _gather_bounds(power_system, alpha)
    if sum(p_b) > alpha:
        # Shed active loads
        shedded_active_bus_loads = _shed_active_loads(
            c=c,
            A=A,
            p_b=p_b,
            p_bounds=p_bounds,
            buses=buses,
            lines=lines,
            alpha=alpha,
        )
        if shedded_active_bus_loads is not None:
            # Shed active energy
            _shed_active_energy(
                buses=buses,
                shedded_active_bus_loads=shedded_active_bus_loads,
                alpha=alpha,
                dt=dt,
            )
    if sum(q_b) > alpha:
        # Shed reactive loads
        shedded_reactive_bus_loads = _shed_reactive_loads(
            c=c,
            A=A,
            q_b=q_b,
            q_bounds=q_bounds,
            buses=buses,
            lines=lines,
            alpha=alpha,
        )
        if shedded_reactive_bus_loads is not None:
            # Shed reactive energy
            _shed_reactive_energy(
                buses=buses,
                shedded_reactive_bus_loads=shedded_reactive_bus_loads,
                alpha=alpha,
                dt=dt,
            )


def _build_A_matrix(power_system: PowerSystem):

    """
    Builds the LHS constraint matrix

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration

    Returns
    -------
    A : array
        LHS Constraint matrix

    """

    buses = list(power_system.buses)
    lines = [x for x in power_system.lines if x.connected]
    N_D = len(buses)
    N_L = len(lines)
    A = np.zeros((N_D, N_D + N_L + N_D + 1))
    for j, bus in enumerate(buses):
        # Load shed coefficients
        A[j, j] = 1  # mu_md
        # Line load coefficients
        for line in bus.connected_lines:
            if line.connected:
                index = lines.index(line)
                if bus == line.fbus:
                    A[j, N_D + index] = -1
                else:
                    A[j, N_D + index] = 1
        # Generation coefficients
        A[j, N_D + N_L + j] = 1  # lambda_md
        # Slack parameter
        A[j, -1] = 1
    return A


def _get_generation_bounds(power_system: PowerSystem):
    """
    Returns the generation units bounds

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration

    Returns
    -------
    p_gen : list
        List of the active power bounds for the generation units
    q_gen : list
        List of the reactive power bounds for the generation units

    """
    p_gen = list()  # Active bus generation
    q_gen = list()  # Reactive bus generation
    for j, bus in enumerate(power_system.buses):
        # Generation bounds
        flag = False
        for child_network in power_system.child_network_list:
            if isinstance(child_network, Transmission):
                if bus == child_network.get_trafo_bus():
                    p_gen.append(INF)
                    q_gen.append(INF)
                    flag = True
        if flag is False:
            p_gen.append(max(0, bus.pprod))
            q_gen.append(max(0, bus.qprod))
    return p_gen, q_gen


def _gather_bounds(
    power_system: PowerSystem,
    alpha: float,
):
    """
    Returns the flow bounds between the components in the power system.

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration
    alpha : float
        Slack variable to cope with numerical noise

    Returns
    -------
    p_bounds : list
        The active power bounds for a component
    q_bounds : list
        The reactive power bounds for a component
    """

    # Gather bounds
    buses = list(power_system.buses)
    lines = [x for x in power_system.lines if x.connected]
    N_D = len(buses)
    N_L = len(lines)
    # Get loads
    p_b = [max(0, bus.pload) for bus in buses]  # Active bus load
    q_b = [max(0, bus.qload) for bus in buses]  # Reactive bus load
    p_bounds = list()
    q_bounds = list()
    # Get generation bounds
    p_gen, q_gen = _get_generation_bounds(power_system)
    for n in range(N_D + N_L + N_D):
        if n < N_D:
            # Bus load
            p_bounds.append((0, p_b[n]))
            q_bounds.append((0, q_b[n]))
        elif N_D <= n < N_D + N_L:
            # Line flow
            line = lines[n - N_D]
            # Line flow in MW
            max_available_p_flow = line.get_line_load()[0] * line.s_ref
            max_available_q_flow = line.get_line_load()[1] * line.s_ref
            PL_p_max = min(line.capacity, abs(max_available_p_flow))
            PL_q_max = min(line.capacity, abs(max_available_q_flow))
            p_bounds.append((-PL_p_max, PL_p_max))
            q_bounds.append((-PL_q_max, PL_q_max))
        else:
            # Bus generation
            p_bounds.append((0, p_gen[n - (N_D + N_L)]))
            q_bounds.append((0, q_gen[n - (N_D + N_L)]))
    # alpha bounds
    p_bounds.append((-alpha, alpha))
    q_bounds.append((-alpha, alpha))
    return p_bounds, q_bounds


def _shed_active_loads(
    c: list,
    A: list,
    p_b: list,
    p_bounds: list,
    buses: list,
    lines: list,
    alpha: float,
):
    """
    Sheds active power load

    Parameters
    ----------
    c : list
        Coefficients of the objective function
    A : list
        LHS constraint matrix
    p_b : list
        RHS constraint vector
    p_bounds : list
        Variable boundaries
    buses : list
        List containing buses
    lines : list
        List containing lines
    alpha : float
        Slack variable to cope with numerical noise
    dt : Time
        The current time step

    Returns
    -------
    active_shedded_bus_loads: list
        The active shedded bus loads of the current
        time increment

    """
    p_res = linprog(
        c,
        A_eq=A,
        b_eq=p_b,
        bounds=p_bounds,
    )
    if not p_res.success:
        print("Active energy.shed was not successful, verify the results:")
        print("buses: ", buses)
        print("lines: ", lines)
        print("A: ", A)
        print("cost: ", c)
        print("p_b: ", p_b)
        print("p_bounds: ", p_bounds)
        p_res = linprog(
            c,
            A_eq=A,
            b_eq=p_b,
            bounds=p_bounds,
            options={
                "disp": True,
            },
        )
        print(p_res)
    if p_res.fun > 0:
        shedded_active_bus_loads = p_res.x
    else:
        shedded_active_bus_loads = None
    return shedded_active_bus_loads


def _shed_active_energy(
    buses: list,
    shedded_active_bus_loads: list,
    alpha: float,
    dt: Time,
):
    """
    Sheds active energy

    Parameters
    ----------
    buses : list
        List containing buses
    shedded_active_bus_loads : list
        The shedded active bus loads of the current
        time increment
    alpha : float
        Slack variable to cope with numerical noise
    dt : Time
        The current time step

    Returns
    -------
    None

    """
    for i, bus in enumerate(buses):
        bus.add_to_energy_shed_stack(
            shedded_active_bus_loads[i]
            if shedded_active_bus_loads[i] > alpha
            else 0,
            0,
            dt,
        )


def _shed_reactive_loads(
    c: list,
    A: list,
    q_b: list,
    q_bounds: list,
    buses: list,
    lines: list,
    alpha: float,
):
    """
    Sheds reactive power load

    Parameters
    ----------
    c : list
        Coefficients of the objective function
    A : list
        LHS constraint matrix
    q_b : list
        RHS constraint vector
    q_bounds : list
        Variable boundaries
    buses : list
        List containing buses
    lines : list
        List containing lines
    alpha : float
        Slack variable to cope with numerical noise
    dt : Time
        The current time step

    Returns
    -------
    shedded_reactive_bus_loads : list
        The shedded reactive bus loads of the current
        time increment

    """
    q_res = linprog(
        c,
        A_eq=A,
        b_eq=q_b,
        bounds=q_bounds,
    )
    if not q_res.success:
        print("Reactive energy.shed was not successful, verify the results:")
        print("buses: ", buses)
        print("lines: ", lines)
        print("A: ", A)
        print("cost: ", c)
        print("q_b: ", q_b)
        print("q_bounds: ", q_bounds)
        q_res = linprog(
            c,
            A_eq=A,
            b_eq=q_b,
            bounds=q_bounds,
            options={
                "disp": True,
            },
        )
        print(q_res)
    if q_res.fun > 0:
        shedded_reactive_bus_loads = q_res.x
    else:
        shedded_reactive_bus_loads = None
    return shedded_reactive_bus_loads


def _shed_reactive_energy(
    buses: list,
    shedded_reactive_bus_loads: list,
    alpha: float,
    dt: Time,
):
    """
    Sheds reactive energy

    Parameters
    ----------
    buses : list
        List containing buses
    shedded_reactive_bus_loads : list
        The shedded reactive bus loads of the current
        time increment
    alpha : float
        Slack variable to cope with numerical noise
    dt : Time
        The current time step

    Returns
    -------
    None

    """
    for i, bus in enumerate(buses):
        bus.add_to_energy_shed_stack(
            0,
            shedded_reactive_bus_loads[i]
            if shedded_reactive_bus_loads[i] > alpha
            else 0,
            dt,
        )
