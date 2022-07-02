import numpy as np
from relsad.network.systems import Network
from relsad.utils import eq
from relsad.Time import TimeUnit


def SAIFI(network: Network):
    """
    Returns the current SAIFI (System average interruption failure index)

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    interrupted_customers/total_customers : float
        The SAIFI value

    """
    interrupted_customers = sum(
        [bus.acc_interruptions * bus.n_customers for bus in network.buses]
    )
    total_customers = sum([bus.n_customers for bus in network.buses])
    if total_customers == 0:
        return 0
    return interrupted_customers / total_customers


def SAIDI(network: Network, time_unit: TimeUnit):
    """
    Returns the current SAIDI (System average interruption duration index)

    Parameters
    ----------
    network : Network
        A Network element
    time_unit : TimeUnit
        A time unit (hour, seconds, ect)

    Returns
    ----------
    sum_outage_time_x_n_customer/total_customers : float
        The SAIDI value

    """
    sum_outage_time_x_n_customer = sum(
        [
            bus.acc_outage_time.get_unit_quantity(time_unit) * bus.n_customers
            for bus in network.buses
            if bus.acc_interruptions > 0
        ]
    )
    total_customers = sum(
        [bus.n_customers for bus in network.buses if bus.acc_interruptions > 0]
    )
    if total_customers == 0:
        return 0
    return sum_outage_time_x_n_customer / total_customers


def CAIDI(network: Network, time_unit: TimeUnit):
    """
    Returns the current CAIFI (Customer average interruption duration index)

    Parameters
    ----------
    network : Network
        A Network element
    time_unit : TimeUnit
        A time unit (hour, seconds, ect)

    Returns
    ----------
    SAIDI(network, time_unit)/SAIFI(network) : float
        The CAIDI value

    """
    saifi = SAIFI(network)
    if not eq(saifi, 0):
        return SAIDI(network, time_unit) / saifi
    else:
        return 0


def EENS(network):
    """
    Returns the current ENS (Energy not Supplied)

    Parameters
    ----------
    network : Network
        A Network element

    Returns
    ----------
    sum_outage_time_x_load_shed/total_customers : float
        The ENS value

    """
    dt = 1  # Time increment
    sum_outage_time_x_load_shed = sum(
        [dt * bus.acc_p_load_shed for bus in network.buses]
    )
    total_customers = sum([bus.n_customers for bus in network.buses])
    if total_customers == 0:
        return 0
    return sum_outage_time_x_load_shed / total_customers


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
        [
            ev_park.acc_exp_car_interruptions
            for ev_park in network.ev_parks
        ]
    )
    total_num_cars = sum(
        [
            ev_park.acc_num_cars
            for ev_park in network.ev_parks
        ]
    )
    if total_num_cars == 0:
        return 0
    ev_interruption = interrupted_cars / total_num_cars
    return ev_interruption


def EV_Duration(network: Network, time_unit: TimeUnit):
    """
    Returns the current EV Duration. Reflects the average duration of an EV car
    interruption for grid support

    Parameters
    ----------
    network : Network
        A Network element
    time_unit : TimeUnit
        A time unit (hour, seconds, ect.)

    Returns
    ----------
    ev_duration : float
        The average duration of an EV car interruption for grid support

    """
    sum_interruption_duration = sum(
        [
            ev_park.acc_interruption_duration.get_unit_quantity(time_unit)
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
