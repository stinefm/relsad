from relsad.test_networks.test_10bus import initialize_network
from relsad.simulation import Simulation
from relsad.load.bus import CostFunction
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)
from load_and_gen_data import (
    WeatherGen,
    LoadGen,
    windGen,
    PVgeneration,
)
import time
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    start = time.time()

    (
        ps,
        include_microgrid,
        include_production,
        include_backup,
    ) = initialize_network()

    # Fetching bus-objects
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    B7 = ps.get_comp("B7")
    B8 = ps.get_comp("B8")
    B9 = ps.get_comp("B9")
    B10 = ps.get_comp("B10")

    # Fetching line-objects
    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")
    L6 = ps.get_comp("L6")
    L7 = ps.get_comp("L7")
    L8 = ps.get_comp("L8")
    L9 = ps.get_comp("L9")

    if include_backup:
        L10 = ps.get_comp("L10")
    if include_microgrid:
        M1 = ps.get_comp("M1")
        M2 = ps.get_comp("M2")
        M3 = ps.get_comp("M3")
        # Fetching battery and production objects
        Bat1 = M1.get_battery()
        P1 = M2.get_production()
        # P2 = B5.get_production()
        L11 = ps.get_comp("L11")
        ML1 = ps.get_comp("ML1")
        ML2 = ps.get_comp("ML2")

    temp_profiles, wind_profiles, solar_profiles = WeatherGen()

    wind = windGen(wind_profiles)
    PV = PVgeneration(temp_profiles, solar_profiles)
    (
        load_house,
        load_farm,
        load_microgrid,
        load_industry2,
        load_trade,
        load_office,
    ) = LoadGen(temp_profiles)

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

    public = CostFunction(
        A=194.5 - 31.4,
        B=31.4,
    )

    household = CostFunction(
        A=8.8,
        B=14.7,
    )

    for bus in [B3, B4, B6, B7, B9]:
        bus.add_load_data(
            pload_data=load_house,
            cost_function=household,
    )
    for bus in [B2, B8, B10]:
        bus.add_load_data(
            pload_data=load_industry2,
            cost_function=industry,
    )
    B5.add_load_data(
        pload_data=load_trade,
        cost_function=trade,
    )


    if include_microgrid:

        for bus in [M1, M2, M3]:
            bus.add_load_data(
                pload_data=load_microgrid,
                cost_function=microgrid,
    )


        if include_production:
            P1.add_prod_data(
                pprod_data=PV+wind,
            )

    #save_dir = r"test_10bus"

    sim = Simulation(ps, random_seed=3)
    sim.run_monte_carlo(
        iterations=5,
        start_time=TimeStamp(
            year=2019,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        ),
        stop_time=TimeStamp(
            year=2020,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        ),
        time_step=Time(1, TimeUnit.HOUR),
        time_unit=TimeUnit.HOUR,
        save_iterations=[1],
        #save_dir=save_dir,
        n_procs=1,
        debug=True,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
