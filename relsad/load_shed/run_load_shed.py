import numpy as np
from scipy.optimize import linprog
import warnings
from relsad.utils import INF
from relsad.Time import Time
from relsad.network.systems import (
    PowerSystem,
    Transmission,
)

np.set_printoptions(suppress=True, linewidth=np.nan)
warnings.filterwarnings("ignore")

# flake8: noqa: C901
def shed_loads(power_system: PowerSystem, dt: Time, alpha: float = 1e-4):
    """
    Sheds the unsupplied loads of the power system using a linear minimization
    problem solved with linear programming

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
    # Building A-matrix
    A = _build_A_matrix(power_system)
    # Gather boundaries
    p_bounds, q_bounds = _gather_boundaries(power_system, alpha)
    if sum(p_b) > alpha:
        # Shed active loads
        _shed_active_loads(
            c,
            A,
            p_b,
            p_bounds,
            buses,
            lines,
            alpha,
            dt,
        )
    if sum(q_b) > alpha:
        # Shed reactive loads
        _shed_reactive_loads(
            c,
            A,
            q_b,
            q_bounds,
            buses,
            lines,
            alpha,
            dt,
        )


def _build_A_matrix(power_system: PowerSystem):

    """
    Builds a matrix

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration
    
    Returns
    -------
    A : array
        Matrix containing 

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


def _get_generation_boundaries(power_system: PowerSystem):
    """
    Returns the generation units boundaries 

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration
    
    Returns
    -------
    p_gen : list
        List of the active power boundary for the generation units
    q_gen : list 
        List of the reactive power boundary for the generation units

    """
    p_gen = list()  # Active bus generation
    q_gen = list()  # Reactive bus generation
    for j, bus in enumerate(power_system.buses):
        # Generation boundaries
        flag = False
        for child_network in power_system.child_network_list:
            if isinstance(child_network, Transmission):
                if bus == child_network.get():
                    p_gen.append(INF)
                    q_gen.append(INF)
                    flag = True
        if flag is False:
            p_gen.append(max(0, bus.pprod))
            q_gen.append(max(0, bus.qprod))
    return p_gen, q_gen


def _gather_boundaries(power_system, alpha):
    """
    Returns the boundaries in the power system. 

    Parameters
    ----------
    power_system : PowerSystem
        The power system that is under consideration
    alpha : float
        Slack variable to cope with numerical noise
    
    Returns
    -------
    p_bounds : list
        The active power boundary for a generation unit
    q_bounds : list 
        The reaactive power boundary for a generation unit

    """

    # Gather bounderies
    buses = list(power_system.buses)
    lines = [x for x in power_system.lines if x.connected]
    N_D = len(buses)
    N_L = len(lines)
    # Get loads
    p_b = [max(0, bus.pload) for bus in buses]  # Active bus load
    q_b = [max(0, bus.qload) for bus in buses]  # Reactive bus load
    p_bounds = list()
    q_bounds = list()
    # Get generation boundaries
    p_gen, q_gen = _get_generation_boundaries(power_system)
    for n in range(N_D + N_L + N_D):
        if n < N_D:
            p_bounds.append((0, p_b[n]))
            q_bounds.append((0, q_b[n]))
        elif N_D <= n < N_D + N_L:
            line = lines[n - N_D]
            # Line load in MW
            max_available_p_flow = line.get_line_load()[0] * line.s_ref
            max_available_q_flow = line.get_line_load()[1] * line.s_ref
            PL_p_max = min(line.capacity, abs(max_available_p_flow))
            PL_q_max = min(line.capacity, abs(max_available_q_flow))
            p_bounds.append((-PL_p_max, PL_p_max))
            q_bounds.append((-PL_q_max, PL_q_max))
        else:
            p_bounds.append((0, p_gen[n - (N_D + N_L)]))
            q_bounds.append((0, q_gen[n - (N_D + N_L)]))
    # alpha bounds
    p_bounds.append((-alpha, alpha))
    q_bounds.append((-alpha, alpha))
    return p_bounds, q_bounds


def _shed_active_loads(
    c,
    A,
    p_b,
    p_bounds,
    buses,
    lines,
    alpha,
    dt: Time,
):
    """
    Sheds active power load

    Parameters
    ----------
    c : 
    A : 
    p_b : list
    p_bounds : list
    buses : list
    lines : list
    alpha : float
        Slack variable to cope with numerical noise
    dt : Time
        The current time step
    
    Returns
    -------
    None

    """
    p_res = linprog(
        c,
        A_eq=A,
        b_eq=p_b,
        bounds=p_bounds,
    )
    if not p_res.success:
        print("Active load shed was not successful, verify the results:")
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
        for i, bus in enumerate(buses):
            bus.add_to_load_shed_stack(
                p_res.x[i] if p_res.x[i] > alpha else 0,
                0,
                dt,
            )
        _add_to_shed_configs()


def _shed_reactive_loads(
    c,
    A,
    q_b,
    q_bounds,
    buses,
    lines,
    alpha,
    dt: Time,
):
    """
    Sheds reactive power load

    Parameters
    ----------
    c : 
    A : 
    p_b : list
    p_bounds : list
    buses : list
    lines : list
    alpha : float
        Slack variable to cope with numerical noise
    dt : Time
        The current time step
    
    Returns
    -------
    None

    """
    q_res = linprog(
        c,
        A_eq=A,
        b_eq=q_b,
        bounds=q_bounds,
    )
    if not q_res.success:
        print("Reactive load shed was not successful, verify the results:")
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
        for i, bus in enumerate(buses):
            bus.add_to_load_shed_stack(
                0,
                q_res.x[i] if q_res.x[i] > alpha else 0,
                dt,
            )
        _add_to_shed_configs()


def _add_to_shed_configs():
    # if len(PowerSystem.shed_configs) == 0:
    #    PowerSystem.shed_configs.append(power_system)
    # add = True
    # for shed_config in PowerSystem.shed_configs:
    #    if power_system == shed_config:
    #        add = False
    #        break
    # if add:
    #    PowerSystem.shed_configs.append(power_system)
    pass
