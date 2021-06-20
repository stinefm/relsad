from stinetwork.visualization.printing import dispFlow, dispVolt
import numpy as np
from stinetwork.topology.paths import configure
from stinetwork.network.systems.Network import Network


def run_bfs_load_flow(network: Network, maxit: int = 5):
    """
    Solves the load flow with a specified number of iterations
    The two first septs are to set up additions topology information and to build the main structure
    Next, it is switched between forward sweeps (Voltage updates) and backward sweeps(load update and loss calcuation)
    Input:
        network      - Network
    Returns:
        network.buses - List of network buses
    """
    topology_list, network.buses, network.lines = configure(
        network.buses, network.lines
    )
    for _ in range(maxit):
        accumulate_load(topology_list)
        update_voltage(topology_list)
        dispFlow(network.lines)
        dispVolt(network.buses)
    return network.buses


def accumulate_load(topology_list):
    """Calculates the accumulated downstream active and reactive load at all buses
    and calculates the active and reactive losses of lines and make an accumulated equivalent load at the buses
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
        p_load_local, q_load_local, dPdV_local, dQdV_local = get_load(
            parent_bus
        )
        p_load += p_load_local
        q_load += q_load_local
        # Add accumulated descriptions to the branching node
        parent_bus.p_load_downstream = p_load
        parent_bus.q_load_downstream = q_load
        if parent_bus.calc_sensitivities:
            # Weighting accumulated and parent_bus DPDV
            if p_load != 0:
                parent_bus.dPdV = (
                    parent_bus.dPdV * (p_load - p_load_local)
                    + dPdV_local * p_load_local
                ) / p_load
            if q_load != 0:
                parent_bus.dQdV = (
                    parent_bus.dQdV * (q_load - q_load_local)
                    + dQdV_local * q_load_local
                ) / q_load
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
                    * (pto ** 2 + qto ** 2)
                    / parent_bus.vomag ** 2
                )
                to_line.qloss = (
                    to_line.x_pu
                    * (pto ** 2 + qto ** 2)
                    / parent_bus.vomag ** 2
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
    :param fbus:
    :param tbus:
    :param tline:
    :param branch:
    :return:
    """

    vk2 = fbus.vomag ** 2
    # Find the accumulated loads and losses flowing on the branch
    tpload = branch[0].p_load_downstream + branch[0].p_loss_downstream
    tqload = branch[0].q_load_downstream + branch[0].q_loss_downstream
    # Voltage calculation
    term2 = 2 * (tpload * tline.r_pu + tqload * tline.x_pu)
    term3 = (
        (tpload ** 2 + tqload ** 2)
        * (tline.r_pu ** 2 + tline.x_pu ** 2)
        / fbus.vomag ** 2
    )
    # Update the bus voltage magnitude on the down-stream bus
    tbus.vomag = np.sqrt(vk2 - term2 + term3)
    if tbus.calc_sensitivities:
        # Calculate the sensitivities for changing the load
        dvdp = (
            -tline.r_pu
            + tpload * (tline.r_pu ** 2 + tline.x_pu ** 2) / fbus.vomag ** 2
        ) / tbus.vomag
        dpdq = (2 * tline.r_pu * tqload / tbus.vomag ** 2) * (
            1 + 2 * tline.r_pu * tpload / tbus.vomag ** 2
        )
        dvdq = (
            -tline.x_pu
            + tqload * (tline.r_pu ** 2 + tline.x_pu ** 2) / fbus.vomag ** 2
        ) / tbus.vomag
        dqdp = (2 * tline.x_pu * tpload / tbus.vomag ** 2) * (
            1 + 2 * tline.x_pu * tqload / tbus.vomag ** 2
        )
        dpldp = (2 * tline.r_pu * tpload / tbus.vomag ** 2) * (
            1 + 2 * tline.x_pu * tqload / tbus.vomag ** 2
        )

        tbus.dVdP = fbus.dVdP + dvdp + dvdq * dqdp
        tbus.dVdQ = fbus.dVdQ + dvdq + dvdp * dpdq
        # Calculate sensitivities for change in losses
        tbus.dPlossdP = fbus.dPlossdP + dpldp
        tbus.dPlossdQ = fbus.dPlossdQ + dpdq
        tbus.dQlossdP = fbus.dQlossdP + dqdp
        tbus.dQlossdQ = (
            fbus.dQlossdQ
            + 2 * tline.x_pu * tqload / tbus.vomag ** 2
            + 2 * tline.x_pu * tpload * tbus.dPlossdQ / tbus.vomag ** 2
        )
        # Calculate the second-order derivatives
        tbus.dP2lossdQ2 = (
            fbus.dP2lossdQ2
            + dpdq / max(tqload, 1e-9)
            + (2 * tline.r_pu * tqload / tbus.vomag ** 2)
            * 2
            * tline.r_pu
            * dpdq
            / tbus.vomag ** 2
        )
        tbus.dP2lossdP2 = (
            fbus.dP2lossdQ2
            + dpldp / max(tpload, 1e-9)
            + (2 * tline.r_pu * tpload / tbus.vomag ** 2)
            * 2
            * tline.x_pu
            * dqdp
            / tbus.vomag ** 2
        )
        tbus.lossRatioQ = tbus.dPlossdQ / tbus.dP2lossdQ2
        tbus.lossRatioP = tbus.dPlossdP / tbus.dP2lossdP2

        # Update the voltage for the purpose of loss minimization
        # - adjust the sensitivity acording to the chosen step.
        if tbus.iloss:
            # Equivalent to that the dP cost more than pqcostRatio times dQ
            if np.abs(tbus.dPlossdQ) >= 1.0 / tbus.pqcostRatio:
                qcomp = tbus.dPlossdQ / tbus.dP2lossdQ2
                tbus.qload -= qcomp
                tbus.dPlossdQ = 0.0
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
    """Update the voltage profile based on the accumulated load on each bus"""
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
    """Calculates the net voltage corrected load at the bus - currently a simple ZIP model is applied.
    Input: The busect
    Returns: p_load_act, q_load_act
    """
    # load - production [PU]
    relative_pload = bus.pload_pu - bus.pprod_pu
    relative_qload = bus.qload_pu - bus.qprod_pu

    p_load_act = relative_pload * (
        bus.ZIP[0] * bus.vomag ** 2 + bus.ZIP[1] * bus.vomag + bus.ZIP[2]
    )
    q_load_act = relative_qload * (
        bus.ZIP[0] * bus.vomag ** 2 + bus.ZIP[1] * bus.vomag + bus.ZIP[2]
    )
    if bus.calc_sensitivities:
        dPdV = relative_pload * (bus.ZIP[0] * 2 * bus.vomag + bus.ZIP[1])
        dQdV = relative_qload * (bus.ZIP[0] * 2 * bus.vomag + bus.ZIP[1])
        return p_load_act, q_load_act, dPdV, dQdV
    return p_load_act, q_load_act, 0, 0
