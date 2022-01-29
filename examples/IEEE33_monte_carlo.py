from relsad.test_networks.IEEE33 import initialize_network
from relsad.visualization.plotting import plot_topology
from relsad.simulation import Simulation
from relsad.Time import (
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
    B23 = ps.get_comp("B23")
    B24 = ps.get_comp("B24")
    B25 = ps.get_comp("B25")
    B26 = ps.get_comp("B26")
    B27 = ps.get_comp("B27")
    B28 = ps.get_comp("B28")
    B29 = ps.get_comp("B29")
    B30 = ps.get_comp("B30")
    B31 = ps.get_comp("B31")
    B32 = ps.get_comp("B32")
    B33 = ps.get_comp("B33")

    # Fetching battery and production objects

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

    load_dict["load"][B2] = {
        "Handel og tjenester": {"pload": load_trade, "qload": load_trade * 0}
    }
    load_dict["load"][B3] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B4] = {
        "Offentlig virksomhet": {
            "pload": load_office,
            "qload": load_office * 0,
        }
    }
    load_dict["load"][B5] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B6] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B7] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
    }
    load_dict["load"][B8] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
    }
    load_dict["load"][B9] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B10] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B11] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B12] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B13] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B14] = {
        "Offentlig virksomhet": {
            "pload": load_office,
            "qload": load_office * 0,
        }
    }
    load_dict["load"][B15] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B16] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B17] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B18] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B19] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B20] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B21] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B22] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B23] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B24] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
    }
    load_dict["load"][B25] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
    }
    load_dict["load"][B26] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B27] = {
        "Husholdning": {"pload": load_house, "qload": load_house * 0}
    }
    load_dict["load"][B28] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }
    load_dict["load"][B29] = {
        "Handel og tjenester": {"pload": load_trade, "qload": load_trade * 0}
    }
    load_dict["load"][B30] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
    }
    load_dict["load"][B31] = {
        "Offentlig virksomhet": {
            "pload": load_office,
            "qload": load_office * 0,
        }
    }
    load_dict["load"][B32] = {
        "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
    }
    load_dict["load"][B33] = {
        "Jordbruk": {"pload": load_farm, "qload": load_farm * 0}
    }

    prod_dict = dict()

    if include_microgrid:

        BM1 = ps.get_comp("BM1")
        BM2 = ps.get_comp("BM2")
        BM3 = ps.get_comp("BM3")
        BM4 = ps.get_comp("BM4")

        Bat1 = BM1.get_battery()
        P1 = BM3.get_production()
        P2 = BM4.get_production()

        prod_dict[P1] = {"pprod": wind, "qprod": PV * 0}
        prod_dict[P2] = {"pprod": PV, "qprod": PV * 0}

        load_dict["load"][BM2] = {
            "Microgrid": {"pload": load_farm, "qload": load_farm * 0}
        }

    if include_production:

        Battery = B30.get_battery()
        Wind_Plant = B15.get_production()
        prod_dict[Wind_Plant] = {"pprod": wind * 2, "qprod": wind * 0}

    save_dir = r"test_IEEE33"

    # fig = plot_topology(ps.buses, ps.lines, figsize=(6.5, 4.5))
    # fig.savefig(os.path.join(save_dir, "topology.pdf"))

    sim = Simulation(ps, random_seed=0)

    sim.run_monte_carlo(
        iterations=5,
        increments=100,
        time_step=Time(1, TimeUnit.HOUR),
        time_unit=TimeUnit.HOUR,
        load_dict=load_dict,
        prod_dict=prod_dict,
        save_iterations=[1, 2, 3, 4, 5],
        save_dir=save_dir,
        n_procs=4,
        debug=True,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
