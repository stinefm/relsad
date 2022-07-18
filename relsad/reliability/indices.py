import numpy as np
from relsad.network.systems import Network
from relsad.utils import eq
from relsad.Time import Time


def SAIFI(network: Network):
    """
    Returns the current SAIFI (System average interruption failure index)

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    saifi : float
        The SAIFI value

    """
    interrupted_customers = sum(
        [bus.acc_interruptions * bus.n_customers for bus in network.buses]
    )
    total_customers = sum([bus.n_customers for bus in network.buses])
    if total_customers == 0:
        saifi = 0
    else:
        saifi = interrupted_customers / total_customers
    return saifi


def SAIDI(network: Network):
    """
    Returns the current SAIDI (System average interruption duration index)

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    saidi : float
        The SAIDI value

    """
    sum_outage_time_x_n_customer = sum(
        [
            bus.acc_outage_time.get_hours() * bus.n_customers
            for bus in network.buses
            if bus.acc_interruptions > 0
        ]
    )
    total_customers = sum(
        [bus.n_customers for bus in network.buses if bus.acc_interruptions > 0]
    )
    if total_customers == 0:
        saidi = 0
    else:
        saidi = sum_outage_time_x_n_customer / total_customers
    return saidi


def CAIDI(network: Network):
    """
    Returns the current CAIFI (Customer average interruption duration index)

    Parameters
    ----------
    network : Network
        A Network element

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


def ASUI(network: Network, current_time: Time):
    """
    Returns the current ASUI (average service unavailability index)

    Parameters
    ----------
    network : Network
        A Network element
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


def ASAI(network: Network, current_time: Time):
    """
    Returns the current ASAI (average service avaialbility index)

    Parameters
    ----------
    network : Network
        A Network element
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
    network : Network
        A Network element

    Returns
    ----------
    ens : float
        The ENS value

    """
    dt = 1  # Time increment
    sum_outage_time_x_load_shed = sum(
        [dt * bus.acc_p_load_shed for bus in network.buses]
    )
    total_customers = sum([bus.n_customers for bus in network.buses])
    if total_customers == 0:
        ens = 0
    else:
        ens = sum_outage_time_x_load_shed / total_customers
    return ens


def EV_Index(network: Network):
    """
    Returns the current EV Index, which is the current power demand from
    all the EV parks in the system.

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    ev_index : float
        Index reflecting the current power demand from all the EV parks in
        the system

    """
    ev_index = sum([ev_park.get_ev_index() for ev_park in network.ev_parks])
    return ev_index


def EV_Interruption(network: Network):
    """
    Returns the current EV Interruption. Reflects the average number of
    interruptions per EV car for grid support

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    ev_interruption : float
        The average number of interruptions per EV car for grid support

    """
    interrupted_cars = sum(
        [ev_park.acc_exp_car_interruptions for ev_park in network.ev_parks]
    )
    total_num_cars = sum(
        [ev_park.acc_num_cars for ev_park in network.ev_parks]
    )
    if total_num_cars == 0:
        return 0
    ev_interruption = interrupted_cars / total_num_cars
    return ev_interruption


def EV_Duration(network: Network):
    """
    Returns the current EV Duration. Reflects the average duration of an EV car
    interruption for grid support

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    ev_duration : float
        The average duration of an EV car interruption for grid support

    """
    sum_interruption_duration = sum(
        [
            ev_park.acc_interruption_duration.get_hours()
            for ev_park in network.ev_parks
        ]
    )
    sum_interruptions = sum(
        [ev_park.acc_num_interruptions for ev_park in network.ev_parks]
    )
    if sum_interruptions == 0:
        return 0
    ev_duration = sum_interruption_duration / sum_interruptions
    return ev_duration
