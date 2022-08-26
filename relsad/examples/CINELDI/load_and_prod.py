import os
import sys

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
    include_microgrid: bool = False,
    include_production: bool = False,
    data_dir=os.path.join(
        os.pardir,
        os.pardir,
        "data",
    ),
):

    # Fetching bus-objects
    B2 = power_system.get_comp("B2")
    B3 = power_system.get_comp("B3")
    B4 = power_system.get_comp("B4")
    B5 = power_system.get_comp("B5")
    B6 = power_system.get_comp("B6")
    if include_microgrid:
        M1 = power_system.get_comp("M1")
        M2 = power_system.get_comp("M2")
        M3 = power_system.get_comp("M3")
        # Fetch production objects
        if include_production:
            P1 = M2.get_production()

    temp_profiles, wind_profiles, solar_profiles = weather_generation_data(
        path=os.path.join(data_dir, "weather_data_rygge.csv"),
    )

    wind = wind_power(wind_profiles)
    PV = pv_power(temp_profiles, solar_profiles)

    (
        load_household,
        load_farm,
        load_microgrid,
        load_industry2,
        load_trade,
        load_office,
    ) = load_data(
        temp_profiles,
        path=os.path.join(data_dir, "load_profiles_fasit.csv"),
    )

    microgrid = CostFunction(
        A=(21.4 - 17.5) * 1000,
        B=17.5 * 1000,
    )

    industry = CostFunction(
        A=132.6 - 92.5,
        B=92.5,
    )

    household = CostFunction(
        A=8.8,
        B=14.7,
    )

    B2.add_load_data(
        pload_data=load_industry2,
        cost_function=industry,
    )

    for bus in [B3, B4, B5]:
        bus.add_load_data(
            pload_data=load_household,
            cost_function=household,
        )

    B6.add_load_data(
        pload_data=load_office,
        cost_function=household,
    )

    if include_microgrid:
        for bus in [M1, M2]:
            bus.add_load_data(
                pload_data=load_household,
                cost_function=household,
            )
        M3.add_load_data(
            pload_data=load_microgrid,
            cost_function=microgrid,
        )

        if include_production:
            P1.add_prod_data(
                pprod_data=PV + wind,
            )
    return power_system
