from relsad.network.systems import PowerNetwork
from relsad.Time import Time
from relsad.utils import eq


def SAIFI(network: PowerNetwork):
    """
    Returns the current SAIFI (System average interruption failure index)

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    saifi : float
        The SAIFI value

    """
    interrupted_customers = sum(
        bus.acc_interruptions * bus.n_customers for bus in network.buses
    )
    total_customers = sum(bus.n_customers for bus in network.buses)
    if total_customers == 0:
        saifi = 0
    else:
        saifi = interrupted_customers / total_customers
    return saifi


def SAIDI(network: PowerNetwork):
    """
    Returns the current SAIDI (System average interruption duration index)

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    saidi : float
        The SAIDI value

    """
    sum_outage_time_x_n_customer = sum(
        bus.acc_outage_time.get_hours() * bus.n_customers
        for bus in network.buses
    )
    total_customers = sum(bus.n_customers for bus in network.buses)
    if total_customers == 0:
        saidi = 0
    else:
        saidi = sum_outage_time_x_n_customer / total_customers
    return saidi


def CAIDI(network: PowerNetwork):
    """
    Returns the current CAIFI (Customer average interruption duration index)

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    caidi : float
        The CAIDI value

    """
    saifi = SAIFI(network)
    if not eq(saifi, 0):
        caidi = SAIDI(network) / saifi
    else:
        caidi = 0
    return caidi


def ASUI(network: PowerNetwork, current_time: Time):
    """
    Returns the current ASUI (average service unavailability index)

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element
    current_time : Time
        Current time

    Returns
    ----------
    asui : float
        The ASUI value
    """
    hours = current_time.get_hours()
    asui = SAIDI(network) / hours
    return asui


def ASAI(network: PowerNetwork, current_time: Time):
    """
    Returns the current ASAI (average service avaialbility index)

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element
    current_time : Time
        Current time

    Returns
    ----------
    asai : float
        The ASAI value
    """
    asai = 1 - ASUI(network, current_time)
    return asai


def ENS(network):
    """
    Returns the current ENS (Energy not Supplied)

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    ens : float
        The ENS value

    """
    ens = sum(bus.acc_p_energy_shed for bus in network.buses)
    return ens
