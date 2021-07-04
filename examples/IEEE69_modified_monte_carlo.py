from stinetwork.test_networks.IEEE69_modified import (
    initialize_network,
)
from stinetwork.visualization.plotting import plot_topology
from stinetwork.utils import random_instance
from stinetwork.simulation import Simulation
from load_and_gen_data import (
    WeatherGen,
    LoadGen,
    windGen,
    PVgeneration,
)
import time
import os

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
    load_house,
    load_farm,
    load_microgrid,
    load_industry2,
    load_trade,
    load_office,
) = LoadGen(temp_profiles)

load_dict = dict()

load_dict[B2] = {
    "Husholdning": {"pload": load_house * 60, "qload": load_house * 0}
}
load_dict[B3] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B4] = {
    "Husholdning": {"pload": load_house * 60, "qload": load_house * 0}
}
load_dict[B5] = {
    "Industri": {"pload": load_industry2 * 2, "qload": load_industry2 * 0}
}
load_dict[B6] = {"Jordbruk": {"pload": load_farm * 90, "qload": load_farm * 0}}
load_dict[B7] = {"Jordbruk": {"pload": load_farm * 90, "qload": load_farm * 0}}
load_dict[B8] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B9] = {
    "Handel og tjenester": {
        "pload": load_trade * 3,
        "qload": load_trade * 0,
    }
}

load_dict[B10] = {
    "Industri": {"pload": load_industry2 * 2, "qload": load_industry2 * 0}
}
load_dict[B11] = {
    "Jordbruk": {"pload": load_farm * 80, "qload": load_farm * 0}
}
load_dict[B12] = {
    "Handel og tjenester": {
        "pload": load_trade * 3,
        "qload": load_trade * 0,
    }
}
load_dict[B13] = {
    "Husholdning": {"pload": load_house * 60, "qload": load_house * 0}
}
load_dict[B14] = {
    "Husholdning": {"pload": load_house * 60, "qload": load_house * 0}
}
load_dict[B15] = {
    "Jordbruk": {"pload": load_farm * 80, "qload": load_farm * 0}
}

load_dict[B16] = {
    "Husholdning": {"pload": load_house * 60, "qload": load_house * 0}
}


# Microgrid:
load_dict[BM2] = {
    "Microgrid": {"pload": load_farm * 40, "qload": load_farm * 0}
}

prod_dict = dict()

prod_dict[P1] = {"pprod": wind, "qprod": wind * 0}
prod_dict[P2] = {"pprod": PV, "qprod": PV * 0}

ps.add_load_dict(load_dict)
ps.add_prod_dict(prod_dict)

save_dir = r"C:\Users\stinefm\Documents\IEEE69_modified_21-05-2021\s3"

fig = plot_topology(ps.buses, ps.lines, figsize=(6.5, 4.5))
fig.savefig(os.path.join(save_dir, "topology.pdf"))

sim = Simulation(ps, random_seed=0)

sim.run_monte_carlo(
    iterations=54,
    increments=8760,
    save_iterations=[
        0,
        6,
        19,
        27,
        29,
        31,
        35,
        39,
        52,
    ],
    save_dir=save_dir,
)

end = time.time()
print("Time elapsed: {}".format(end - start))
