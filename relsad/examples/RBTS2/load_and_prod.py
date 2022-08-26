import os
import sys

import numpy as np

from relsad.examples.load.load_and_gen_data import (
    load_data,
    pv_power,
    weather_generation_data,
    wind_power,
)
from relsad.load.bus import CostFunction
from relsad.network.systems import PowerSystem
from relsad.Time import Time, TimeStamp, TimeUnit


def set_network_load_and_prod(
    power_system: PowerSystem,
):

    # Fetching bus-objects

    B1 = power_system.get_comp("B1")
    B2 = power_system.get_comp("B2")
    B3 = power_system.get_comp("B3")
    B4 = power_system.get_comp("B4")
    B5 = power_system.get_comp("B5")

    B7 = power_system.get_comp("B7")
    B8 = power_system.get_comp("B8")
    B9 = power_system.get_comp("B9")
    B10 = power_system.get_comp("B10")
    B11 = power_system.get_comp("B11")
    B12 = power_system.get_comp("B12")
    B13 = power_system.get_comp("B13")
    B14 = power_system.get_comp("B14")
    B15 = power_system.get_comp("B15")
    B16 = power_system.get_comp("B16")
    B17 = power_system.get_comp("B17")
    B18 = power_system.get_comp("B18")
    B19 = power_system.get_comp("B19")
    B20 = power_system.get_comp("B20")
    B21 = power_system.get_comp("B21")
    B22 = power_system.get_comp("B22")

    load_res1 = np.ones(8760) * (0.535 / 210)
    load_res2 = np.ones(8760) * (0.450 / 200)
    load_small1 = np.ones(8760) * (1 / 1)
    load_small2 = np.ones(8760) * (1.15 / 1)
    load_gov = np.ones(8760) * (0.566 / 1)
    load_com = np.ones(8760) * (0.454 / 10)

    household = CostFunction(
        A=8.8,
        B=14.7,
    )

    for bus in [B1, B2, B3, B10, B11]:
        bus.add_load_data(
            pload_data=load_res1,
            cost_function=household,
        )
    for bus in [B4, B5, B13, B14, B20, B21]:
        bus.add_load_data(
            pload_data=load_gov,
            cost_function=household,
        )
    for bus in [B5, B7, B15, B16, B22]:
        bus.add_load_data(
            pload_data=load_com,
            cost_function=household,
        )
    for bus in [B12, B17, B18, B19]:
        bus.add_load_data(
            pload_data=load_res2,
            cost_function=household,
        )
    B8.add_load_data(
        pload_data=load_small1,
        cost_function=household,
    )
    B9.add_load_data(
        pload_data=load_small2,
        cost_function=household,
    )

    return power_system
