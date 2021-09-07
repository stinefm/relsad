from stinetwork.test_networks.CINELDI import initialize_network
from stinetwork.simulation import Simulation
from stinetwork.utils import (
    TimeUnit,
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

    # Fetching bus-objects
    T = ps.get_comp("T")
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    M1 = ps.get_comp("M1")
    M2 = ps.get_comp("M2")
    M3 = ps.get_comp("M3")

    # Fetching line-objects
    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")
    L6 = ps.get_comp("L6")
    L7 = ps.get_comp("L7")
    ML1 = ps.get_comp("ML1")
    ML2 = ps.get_comp("ML2")

    # Fetching disconnector objects
    L1a = ps.get_comp("L1a")
    L1b = ps.get_comp("L1b")
    L1c = ps.get_comp("L1c")
    L2a = ps.get_comp("L2a")
    L3a = ps.get_comp("L3a")
    L3b = ps.get_comp("L3b")
    L4a = ps.get_comp("L4a")
    L5a = ps.get_comp("L5a")
    L6a = ps.get_comp("L6a")
    L7a = ps.get_comp("L7a")
    L7b = ps.get_comp("L7b")

    # Fetching battery and production objects
    Bat1 = M1.get_battery()
    P1 = M2.get_production()
    # P2 = B5.get_production()

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

    load_dict = dict()

    load_dict[B1] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0},
    }
    load_dict[B2] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict[B3] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict[B4] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict[B5] = {
        "Husholdning": {"pload": load_office, "qload": load_house * 0}
    }
    load_dict[M1] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict[M2] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict[M3] = {
        "Microgrid": {"pload": load_microgrid, "qload": load_microgrid * 0}
    }

    prod_dict = dict()

    prod_dict[P1] = {"pprod": (PV + wind), "qprod": PV * 0}

    ps.add_load_dict(load_dict)
    ps.add_prod_dict(prod_dict)

    save_dir = r"test_CINELDI"

    sim = Simulation(ps, random_seed=3)
    sim.run_monte_carlo(
        iterations=50,
        increments=8760,
        time_unit=TimeUnit.HOUR,
        save_iterations=[1, 10, 20, 30, 40, 50],
        save_dir=save_dir,
        n_procs=4,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
