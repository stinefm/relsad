from relsad.test_networks.CINELDI import initialize_network
from relsad.simulation import Simulation
from relsad.utils import (
    Time,
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

    ps, include_microgrid, include_production = initialize_network()

    # Fetching bus-objects
    T = ps.get_comp("T")
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    if include_microgrid:
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
    if include_microgrid:
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
    if include_microgrid:
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

    cost_functions = {
        "Jordbruk": {"A": 21.4 - 17.5, "B": 17.5},
        "Microgrid": {"A": (21.4 - 17.5) * 1000, "B": 17.5 * 1000},
        "Industri": {"A": 132.6 - 92.5, "B": 92.5},
        "Handel og tjenester": {"A": 220.3 - 102.4, "B": 102.4},
        "Offentlig virksomhet": {"A": 194.5 - 31.4, "B": 31.4},
        "Husholdning": {"A": 8.8, "B": 14.7},
    }

    load_dict = dict()
    load_dict["load"] = {}

    load_dict["cost"] = cost_functions

    load_dict["load"][B1] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0},
    }
    load_dict["load"][B2] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B3] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B4] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B5] = {
        "Husholdning": {"pload": load_office, "qload": load_house * 0}
    }

    prod_dict = dict()

    if include_microgrid:
        load_dict["load"][M1] = {
            "Husholdning": {"pload": load_house, "qload": load_house * 0}
        }
        load_dict["load"][M2] = {
            "Husholdning": {"pload": load_house, "qload": load_house * 0}
        }
        load_dict["load"][M3] = {
            "Microgrid": {"pload": load_microgrid, "qload": load_microgrid * 0}
        }
        
        if include_production:
            prod_dict[P1] = {"pprod": (PV + wind), "qprod": PV * 0}

    save_dir = r"test_CINELDI"

    sim = Simulation(ps, random_seed=3)
    sim.run_monte_carlo(
        iterations=1,
        increments=8760,
        time_step=Time(1, TimeUnit.HOUR),
        time_unit=TimeUnit.HOUR,
        load_dict=load_dict,
        prod_dict=prod_dict,
        save_iterations=[1],
        save_dir=save_dir,
        n_procs=1,
        debug=True,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
