import os

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
    B23 = power_system.get_comp("B23")
    B24 = power_system.get_comp("B24")
    B25 = power_system.get_comp("B25")
    B26 = power_system.get_comp("B26")
    B27 = power_system.get_comp("B27")
    B28 = power_system.get_comp("B28")
    B29 = power_system.get_comp("B29")
    B30 = power_system.get_comp("B30")
    B31 = power_system.get_comp("B31")
    B32 = power_system.get_comp("B32")
    B33 = power_system.get_comp("B33")

    # Fetching battery and production objects

    temp_profiles, wind_profiles, solar_profiles = weather_generation_data(
        path=os.path.join(data_dir, "weather_data_rygge.csv"),
    )

    wind = wind_power(wind_profiles)
    PV = pv_power(temp_profiles, solar_profiles)

    (
        load_house,
        load_farm,
        load_microgrid,
        load_industry2,
        load_trade,
        load_office,
    ) = load_data(
        temp_profiles,
        path=os.path.join(data_dir, "load_profiles_fasit.csv"),
    )

    farm = CostFunction(
        A=21.4 - 17.5,
        B=17.5,
    )

    microgrid = CostFunction(
        A=(21.4 - 17.5) * 1000,
        B=17.5 * 1000,
    )

    industry = CostFunction(
        A=132.6 - 92.5,
        B=92.5,
    )

    trade = CostFunction(
        A=220.3 - 102.4,
        B=102.4,
    )

    household = CostFunction(
        A=8.8,
        B=14.7,
    )

    for bus in [B3, B9, B10, B11, B15, B16, B17, B19, B20, B23, B26, B27]:
        bus.add_load_data(
            pload_data=load_house,
            cost_function=household,
        )
    for bus in [B2, B29]:
        bus.add_load_data(
            pload_data=load_trade,
            cost_function=trade,
        )
    for bus in [B4, B14, B31]:
        bus.add_load_data(
            pload_data=load_office,
            cost_function=trade,
        )
    for bus in [B5, B6, B12, B13, B18, B21, B22, B28, B33]:
        bus.add_load_data(
            pload_data=load_farm,
            cost_function=farm,
        )
    for bus in [B7, B8, B24, B25, B30, B32]:
        bus.add_load_data(
            pload_data=load_industry2,
            cost_function=industry,
        )

    if include_microgrid:

        BM2 = power_system.get_comp("BM2")
        BM3 = power_system.get_comp("BM3")
        BM4 = power_system.get_comp("BM4")

        P1 = BM3.get_production()
        P2 = BM4.get_production()

        P1.add_prod_data(
            pprod_data=wind,
        )
        P2.add_prod_data(
            pprod_data=2 * PV,
        )

        BM2.add_load_data(
            pload_data=load_microgrid,
            cost_function=microgrid,
        )
    return power_system
