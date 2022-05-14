from relsad.test_networks.IEEE16_modified import (
    initialize_network,
)
from relsad.visualization.plotting import plot_topology
from relsad.utils import random_instance
from relsad.load.bus import CostFunction
from relsad.simulation import Simulation
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

    ps = initialize_network()

    if True:
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
        B11 = ps.get_comp("B11")
        B12 = ps.get_comp("B12")
        B13 = ps.get_comp("B13")
        B14 = ps.get_comp("B14")
        B15 = ps.get_comp("B15")
        B16 = ps.get_comp("B16")

        BM1 = ps.get_comp("BM1")
        BM2 = ps.get_comp("BM2")
        BM3 = ps.get_comp("BM3")
        BM4 = ps.get_comp("BM4")

    if True:
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
        L10 = ps.get_comp("L10")
        L11 = ps.get_comp("L11")
        L12 = ps.get_comp("L12")
        L13 = ps.get_comp("L13")
        L14 = ps.get_comp("L14")
        L15 = ps.get_comp("L15")

        ML1 = ps.get_comp("ML1")
        ML2 = ps.get_comp("ML2")
        ML3 = ps.get_comp("ML3")
        ML4 = ps.get_comp("ML4")

    if True:
        # Fetching disconnector objects
        L1a = ps.get_comp("L1a")
        L1b = ps.get_comp("L1b")
        L1c = ps.get_comp("L1c")
        L2a = ps.get_comp("L2a")
        L2b = ps.get_comp("L2b")
        L3a = ps.get_comp("L3a")
        L3b = ps.get_comp("L3b")
        L4a = ps.get_comp("L4a")
        L4b = ps.get_comp("L4b")
        L5a = ps.get_comp("L5a")
        L5b = ps.get_comp("L5b")
        L6a = ps.get_comp("L6a")
        L6b = ps.get_comp("L6b")
        L7a = ps.get_comp("L7a")
        L7b = ps.get_comp("L7b")
        L8a = ps.get_comp("L8a")
        L8b = ps.get_comp("L8b")
        L9a = ps.get_comp("L9a")
        L9b = ps.get_comp("L9b")
        L10a = ps.get_comp("L10a")
        L10b = ps.get_comp("L10b")
        L11a = ps.get_comp("L11a")
        L11b = ps.get_comp("L11b")
        L12a = ps.get_comp("L12a")
        L12b = ps.get_comp("L12b")
        L13a = ps.get_comp("L13a")
        L13b = ps.get_comp("L13b")
        L14a = ps.get_comp("L14a")
        L14b = ps.get_comp("L14b")
        L15a = ps.get_comp("L15a")
        L15b = ps.get_comp("L15b")

        ML1a = ps.get_comp("ML1a")
        ML1b = ps.get_comp("ML1b")
        ML1c = ps.get_comp("ML1c")
        ML2a = ps.get_comp("ML2a")
        ML2b = ps.get_comp("ML2b")
        ML3a = ps.get_comp("ML3a")
        ML3b = ps.get_comp("ML3b")
        ML4a = ps.get_comp("ML4a")
        ML4b = ps.get_comp("ML4b")

    # Fetching battery and production objects
    Bat1 = BM1.get_battery()
    P1 = BM3.get_production()
    P2 = BM4.get_production()

    temp_profiles, wind_profiles, solar_profiles = WeatherGen()

    wind = windGen(wind_profiles)
    PV = PVgeneration(temp_profiles, solar_profiles)

    (
        load_household,
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

    for bus in [B2, B4, B13, B14, B16]:
        bus.add_load_data(pload_data=load_household, cost_function=household)

    for bus in [B6, B7, B11, B15, BM2]:
        bus.add_load_data(pload_data=load_farm, cost_function=farm)

    for bus in [B5, B10]:
        bus.add_load_data(pload_data=load_industry2, cost_function=industry)

    for bus in [B3, B8]:
        bus.add_load_data(pload_data=load_office, cost_function=public)

    for bus in [B9, B12]:
        bus.add_load_data(pload_data=load_trade, cost_function=trade)

    P1.add_prod_data(
        pprod_data=PV,
    )
    P2.add_prod_data(
        pprod_data=wind,
    )

    # save_dir = r"C:\Users\stinefm\Documents\IEEE69_modified_21-05-2021\s3"

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
        # save_dir=save_dir,
        n_procs=1,
        debug=True,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
