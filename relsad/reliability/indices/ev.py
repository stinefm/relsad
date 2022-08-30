from relsad.network.systems import PowerNetwork


def EV_Index(network: PowerNetwork):
    """
    Returns the current EV Index, which is the current power demand from
    all the EV parks in the system.

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    ev_index : float
        Index reflecting the current power demand from all the EV parks in
        the system

    """
    ev_index = sum(ev_park.get_ev_index() for ev_park in network.ev_parks)
    return ev_index


def EV_Interruption(network: PowerNetwork):
    """
    Returns the current EV Interruption. Reflects the average number of
    interruptions per EV car for grid support

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    ev_interruption : float
        The average number of interruptions per EV car for grid support

    """
    interruptions_x_num_cars = sum(
        ev_park.acc_exp_interruptions * ev_park.num_cars
        for ev_park in network.ev_parks
    )
    total_num_cars = sum(ev_park.num_cars for ev_park in network.ev_parks)
    if total_num_cars == 0:
        ev_interruption = 0
    else:
        ev_interruption = interruptions_x_num_cars / total_num_cars
    return ev_interruption


def EV_Duration(network: PowerNetwork):
    """
    Returns the current EV Duration. Reflects the average duration of an EV car
    interruption for grid support

    Parameters
    ----------
    network : PowerNetwork
        A PowerNetwork element

    Returns
    ----------
    ev_duration : float
        The average duration of an EV car interruption for grid support

    """
    sum_interruption_duration = sum(
        ev_park.acc_interruption_duration.get_hours()
        for ev_park in network.ev_parks
    )
    sum_interruptions = sum(
        ev_park.acc_num_interruptions for ev_park in network.ev_parks
    )
    if sum_interruptions == 0:
        ev_duration = 0
    else:
        ev_duration = sum_interruption_duration / sum_interruptions
    return ev_duration
