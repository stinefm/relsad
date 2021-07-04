from stinetwork.test_networks.IEEE33 import initialize_network
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
    L16 = ps.get_comp("L16")
    L17 = ps.get_comp("L17")
    L18 = ps.get_comp("L18")
    L19 = ps.get_comp("L19")
    L20 = ps.get_comp("L20")
    L21 = ps.get_comp("L21")
    L22 = ps.get_comp("L22")
    L23 = ps.get_comp("L23")
    L24 = ps.get_comp("L24")
    L25 = ps.get_comp("L25")
    L26 = ps.get_comp("L26")
    L27 = ps.get_comp("L27")
    L28 = ps.get_comp("L28")
    L29 = ps.get_comp("L29")
    L30 = ps.get_comp("L30")
    L31 = ps.get_comp("L31")
    L32 = ps.get_comp("L32")
    # L33 = ps.get_comp("L33")
    # L34 = ps.get_comp("L34")
    # L35 = ps.get_comp("L35")
    # L36 = ps.get_comp("L36")
    # L37 = ps.get_comp("L37")

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
    L16a = ps.get_comp("L16a")
    L16b = ps.get_comp("L16b")
    L17a = ps.get_comp("L17a")
    L17b = ps.get_comp("L17b")
    L18a = ps.get_comp("L18a")
    L18b = ps.get_comp("L18b")
    L19a = ps.get_comp("L19a")
    L19b = ps.get_comp("L19b")
    L20a = ps.get_comp("L20a")
    L20b = ps.get_comp("L20b")
    L21a = ps.get_comp("L21a")
    L21b = ps.get_comp("L21b")
    L22a = ps.get_comp("L22a")
    L22b = ps.get_comp("L22b")
    L23a = ps.get_comp("L23a")
    L23b = ps.get_comp("L23b")
    L24a = ps.get_comp("L24a")
    L24b = ps.get_comp("L24b")
    L25a = ps.get_comp("L25a")
    L25b = ps.get_comp("L25b")
    L26a = ps.get_comp("L26a")
    L26b = ps.get_comp("L26b")
    L27a = ps.get_comp("L27a")
    L27b = ps.get_comp("L27b")
    L28a = ps.get_comp("L28a")
    L28b = ps.get_comp("L28b")
    L29a = ps.get_comp("L29a")
    L29b = ps.get_comp("L29b")
    L30a = ps.get_comp("L30a")
    L30b = ps.get_comp("L30b")
    L31a = ps.get_comp("L31a")
    L31b = ps.get_comp("L31b")
    L32a = ps.get_comp("L32a")
    L32b = ps.get_comp("L32b")
    # L33a = ps.get_comp("L33a")
    # L33b = ps.get_comp("L33b")
    # L34a = ps.get_comp("L34a")
    # L34b = ps.get_comp("L34b")
    # L35a = ps.get_comp("L35a")
    # L35b = ps.get_comp("L35b")
    # L36a = ps.get_comp("L36a")
    # L36b = ps.get_comp("L36b")
    # L37a = ps.get_comp("L37a")
    # L37b = ps.get_comp("L37b")

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
    "Handel og tjenester": {"pload": load_trade, "qload": load_trade * 0}
}
load_dict[B3] = {"Husholdning": {"pload": load_house, "qload": load_house * 0}}
load_dict[B4] = {
    "Offentlig virksomhet": {
        "pload": load_office,
        "qload": load_office * 0,
    }
}
load_dict[B5] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B6] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B7] = {
    "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
}
load_dict[B8] = {
    "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
}
load_dict[B9] = {"Husholdning": {"pload": load_house, "qload": load_house * 0}}
load_dict[B10] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B11] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B12] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B13] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B14] = {
    "Offentlig virksomhet": {
        "pload": load_office,
        "qload": load_office * 0,
    }
}
load_dict[B15] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B16] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B17] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B18] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B19] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B20] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B21] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B22] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B23] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B24] = {
    "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
}
load_dict[B25] = {
    "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
}
load_dict[B26] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B27] = {
    "Husholdning": {"pload": load_house, "qload": load_house * 0}
}
load_dict[B28] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}
load_dict[B29] = {
    "Handel og tjenester": {"pload": load_trade, "qload": load_trade * 0}
}
load_dict[B30] = {
    "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
}
load_dict[B31] = {
    "Offentlig virksomhet": {
        "pload": load_office,
        "qload": load_office * 0,
    }
}
load_dict[B32] = {
    "Industri": {"pload": load_industry2, "qload": load_industry2 * 0}
}
load_dict[B33] = {"Jordbruk": {"pload": load_farm, "qload": load_farm * 0}}

# Microgrid:
load_dict[BM2] = {"Microgrid": {"pload": load_farm, "qload": load_farm * 0}}


prod_dict = dict()

prod_dict[P1] = {"pprod": wind, "qprod": PV * 0}
prod_dict[P2] = {"pprod": PV, "qprod": PV * 0}

ps.add_load_dict(load_dict)
ps.add_prod_dict(prod_dict)

save_dir = "res"

fig = plot_topology(ps.buses, ps.lines, figsize=(6.5, 4.5))
fig.savefig(os.path.join(save_dir, "topology.pdf"))

sim = Simulation(ps, random_seed=0)

sim.run_monte_carlo(
    iterations=1500,
    increments=8760,
    save_iterations=[1, 250, 500, 750, 1000, 1250, 1500],
    save_dir=save_dir,
)

end = time.time()
print("Time elapsed: {}".format(end - start))
