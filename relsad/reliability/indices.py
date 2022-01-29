from relsad.network.systems import Network
from relsad.utils import eq
from relsad.Time import TimeUnit


def SAIFI(network: Network):
    """
    Returns the current SAIFI (System average interruption failure index)
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
    """
    saifi = SAIFI(network)
    if not eq(saifi, 0):
        return SAIDI(network, time_unit) / saifi
    else:
        return 0


def EENS(network):
    """
    Returns the current EENS (Expected energy not supplied)
    """
    dt = 1  # Time increment
    sum_outage_time_x_load_shed = sum(
        [dt * bus.acc_p_load_shed for bus in network.buses]
    )
    total_customers = sum([bus.n_customers for bus in network.buses])
    if total_customers == 0:
        return 0
    return sum_outage_time_x_load_shed / total_customers
