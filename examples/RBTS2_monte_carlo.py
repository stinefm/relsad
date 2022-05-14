from relsad.test_networks.RBTS2 import initialize_network
from relsad.simulation import Simulation
from relsad.load.bus import CostFunction
from load_and_gen_data import (
    WeatherGen,
    LoadGen,
    windGen,
    PVgeneration,
)
import time
import numpy as np
import os
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    start = time.time()

    ps = initialize_network()

    # Fetching bus-objects
    B0 = ps.get_comp("B0")
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
    B17 = ps.get_comp("B17")
    B18 = ps.get_comp("B18")
    B19 = ps.get_comp("B19")
    B20 = ps.get_comp("B20")
    B21 = ps.get_comp("B21")
    B22 = ps.get_comp("B22")
    BF11 = ps.get_comp("BF11")
    BF12 = ps.get_comp("BF12")
    BF13 = ps.get_comp("BF13")
    BF14 = ps.get_comp("BF14")
    BF21 = ps.get_comp("BF21")
    BF22 = ps.get_comp("BF22")
    BF31 = ps.get_comp("BF31")
    BF32 = ps.get_comp("BF32")
    BF33 = ps.get_comp("BF33")
    BF34 = ps.get_comp("BF34")
    BF41 = ps.get_comp("BF41")
    BF42 = ps.get_comp("BF42")
    BF43 = ps.get_comp("BF43")
    BF44 = ps.get_comp("BF44")

    load_res1 = np.ones(8760) * (0.535 / 210)
    load_res2 = np.ones(8760) * (0.450 / 200)
    load_small1 = np.ones(8760) * (1 / 1)
    load_small2 = np.ones(8760) * (1.15 / 1)
    load_gov = np.ones(8760) * (0.566 / 1)
    load_com = np.ones(8760) * (0.454 / 10)

    # load_res1 = np.ones(8760) * (0.8668 / 210)
    # load_res2 = np.ones(8760) * (0.7291 / 200)
    # load_small1 = np.ones(8760) * (1.6279 / 1)
    # load_small2 = np.ones(8760) * (1.8721 / 1)
    # load_gov = np.ones(8760) * (0.9167 / 1)
    # load_com = np.ones(8760) * (0.7500 / 10)

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

    # save_dir = r"test_RBTS2"

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
