import numpy as np

from relsad.network.systems.PowerNetwork import PowerNetwork
from relsad.topology.load_flow.bfs import configure_bfs_load_flow_setup


def run_bfs_load_flow(network: PowerNetwork, maxit: int = 5):
    """
    Solves the load flow with a specified number of iterations
    The two first septs are to set up additions topology information and to build the main structure
    Next, it is switched between forward sweeps (Voltage updates) and backward sweeps(load update and loss calcuation)

    See :doc:`/theory/bfs` for more details.

    Parameters
    ----------
    network : PowerNetwork
        The analyzed network
    maxit : int
        The number of iterations

    Returns
    -------
    network.buses : list
        List of network buses
    """
    topology_list, network.buses = configure_bfs_load_flow_setup(
        network.buses, network.lines
    )
    for _ in range(maxit):
        accumulate_load(topology_list)
        update_voltage(topology_list)
    return network.buses


def accumulate_load(topology_list):
    """
    Calculates the accumulated downstream active and reactive load at all buses
    and calculates the active and reactive losses of lines and make an accumulated equivalent load at the buses
    The function returns the accumulated loads and the accumulated power losses from a branch in the system

    Parameters
    ----------
    topology_list : list
        List containing the system topology

    Returns
    -------
    p_load : float
        Active accumulated power load of a branch
    q_load : float
        Reactive accumulated power load of a branch
    p_loss : float
        Active accumulated power loss of a branch
    q_loss : float
        Reactive accumulated power loss of a branch
    """
    p_load = 0.0
    q_load = 0.0
    p_loss = 0.0
    q_loss = 0.0
    for branch in reversed(topology_list):  # Start on last node
        if len(branch) > 1:
            for child_branch in branch[1:]:  # Do for all child branches
                (
                    p_load_child,
                    q_load_child,
                    p_loss_child,
                    q_loss_child,
                ) = accumulate_load(child_branch)
                # Add accumulated powers and losses in a branch to
                # the node where the brancing accurs.
                p_load += p_load_child
                q_load += q_load_child
                p_loss += p_loss_child
                q_loss += q_loss_child
        parent_bus = branch[0]
        # Add local loads
        p_load_local, q_load_local = get_load(parent_bus)
        p_load += p_load_local
        q_load += q_load_local
        # Add accumulated descriptions to the branching node
        parent_bus.p_load_downstream = p_load
        parent_bus.q_load_downstream = q_load

        # Add line loss
        if parent_bus.toline:
            to_line = parent_bus.toline
            if to_line.connected:
                # Find the flow to the downstream bus
                pto = parent_bus.p_load_downstream + p_loss
                qto = parent_bus.q_load_downstream + q_loss
                # Estimate the losses of the branch
                to_line.ploss = (
                    to_line.r_pu
                    * (pto**2 + qto**2)
                    / parent_bus.vomag**2
                )
                to_line.qloss = (
                    to_line.x_pu
                    * (pto**2 + qto**2)
                    / parent_bus.vomag**2
                )
                p_loss += to_line.ploss
                q_loss += to_line.qloss
                # Add the losses to the downstream bus
                parent_bus.p_loss_downstream = p_loss
                parent_bus.q_loss_downstream = q_loss

    # Return the accumulated loads and losses from the current branch
    return p_load, q_load, p_loss, q_loss


#
# Function for calculating the voltages and sensitivities in the single phase case
#
def calc_bus_voltage_sensitivity_single_phase(fbus, tbus, tline, branch: list):
    """
    Calculate the node voltages and sensitivities in the single phase case

    Parameters
    ----------
    fbus : Bus
        The sending Bus element
    tbus : Bus
        The recieving Bus element
    tline : Line
        The recieving Line element
    branch : list
        List of branches in the system

    Returns
    -------
    None

    """

    vk2 = fbus.vomag**2
    # Find the accumulated loads and losses flowing on the branch
    tpload = branch[0].p_load_downstream + branch[0].p_loss_downstream
    tqload = branch[0].q_load_downstream + branch[0].q_loss_downstream
    # Voltage calculation
    term2 = 2 * (tpload * tline.r_pu + tqload * tline.x_pu)
    term3 = (
        (tpload**2 + tqload**2)
        * (tline.r_pu**2 + tline.x_pu**2)
        / fbus.vomag**2
    )
    # Update the bus voltage magnitude on the down-stream bus
    tbus.vomag = np.sqrt(vk2 - term2 + term3)

    # Voltage angle calculation
    busvoltreal = (
        fbus.vomag - (tpload * tline.r_pu + tqload * tline.x_pu) / fbus.vomag
    )
    busvoltimag = (tqload * tline.r_pu - tpload * tline.x_pu) / fbus.vomag
    tbus.voang = fbus.voang + np.arctan2(
        busvoltimag, busvoltreal
    )  # Update voltage angles


#
# Update the voltage profile starting on the top node
#
def update_voltage(topology_list):
    """
    Update the voltage profile based on the accumulated load on each bus

    Parameters
    ----------
    topology_list : list
        List containing the system topology

    Returns
    -------
    None
    """
    for branch in topology_list:
        if branch[0].toline:
            tline = branch[0].toline
            fbus = tline.fbus
            tbus = tline.tbus
            # Update voltages and sensitivities Single Phase
            calc_bus_voltage_sensitivity_single_phase(
                fbus, tbus, tline, branch
            )
        if len(branch) > 1:
            for bus in branch[1:]:  # Update voltages along the branches
                update_voltage(bus)


#
# Calculates the load for the actual volage at the bus
#
def get_load(bus):
    """
    Calculates the net voltage corrected load at the bus - currently a simple ZIP model is applied.

    Parameters
    ----------
    bus : Bus
        A Bus element

    Returns
    -------
    p_load_corr : float
        Corrected active power load
    q_load_corr : float
        Corrected reactive power load

    """
    # load - production [PU]
    relative_pload = bus.pload_pu - bus.pprod_pu
    relative_qload = bus.qload_pu - bus.qprod_pu

    p_load_corr = relative_pload * (
        bus.ZIP[0] * bus.vomag**2 + bus.ZIP[1] * bus.vomag + bus.ZIP[2]
    )
    q_load_corr = relative_qload * (
        bus.ZIP[0] * bus.vomag**2 + bus.ZIP[1] * bus.vomag + bus.ZIP[2]
    )
    return p_load_corr, q_load_corr
