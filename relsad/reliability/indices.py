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
    Returns the current EV Index, which indicates how much power an EV are unable to charge

    Parameters
    ----------
    network : Network 
        A Network element

    Returns
    ----------
    sum([ev_park.get_ev_index() for ev_park in network.ev_parks]) : float
        Index telling how much power an EV are unable to charge

    """
    return sum([ev_park.get_ev_index() for ev_park in network.ev_parks])
    

def EV_Interruption(network: Network):
    """
    Returns the current EV Interruption. Tells how many EVs that get interrupted/used for grid support
    
    Parameters
    ----------
    network : Network 
        A Network element

    Returns
    ----------
    interrupted_cars/total_cars : float
        An average number of how many EVs that get used for grid support

    """
    interrupted_cars = sum(
        [ev_park.acc_interruptions * ev_park.num_cars for ev_park in network.ev_parks]
    )
    total_cars = sum([ev_park.num_cars for ev_park in network.ev_parks])
    if total_cars == 0:
        return 0
    return interrupted_cars / total_cars

def EV_Duration(network: Network, time_unit: TimeUnit):
    """
    Returns the current EV Duration. Tells the average duration of the interrupted/used EVs for grid support
    
    Parameters
    ----------
    network : Network 
        A Network element
    time_unit : TimeUnit
        A time unit (hour, seconds, ect.)

    Returns
    ----------
    sum_interruption_duration_x_num_cars/total_cars : float
        The average duration of the interruptions/an EV is being used for grid support

    """
    sum_interruption_duration_x_num_cars = sum(
        [
            ev_park.acc_interruption_duration.get_unit_quantity(time_unit) * ev_park.num_cars
            for ev_park in network.ev_parks
            if ev_park.acc_interruptions > 0
        ]
    )
    total_cars = sum(
        [ev_park.num_cars for ev_park in network.ev_parks if ev_park.acc_interruptions > 0]
    )
    if total_cars == 0:
        return 0
    return sum_interruption_duration_x_num_cars / total_cars