from stinetwork.test_networks.IEEE69 import initialize_network
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
    B34 = ps.get_comp("B34")
    B35 = ps.get_comp("B35")
    B36 = ps.get_comp("B36")
    B37 = ps.get_comp("B37")
    B38 = ps.get_comp("B38")
    B39 = ps.get_comp("B39")
    B40 = ps.get_comp("B40")
    B41 = ps.get_comp("B41")
    B42 = ps.get_comp("B42")
    B43 = ps.get_comp("B43")
    B44 = ps.get_comp("B44")
    B45 = ps.get_comp("B45")
    B46 = ps.get_comp("B46")
    B47 = ps.get_comp("B47")
    B48 = ps.get_comp("B48")
    B49 = ps.get_comp("B49")
    B50 = ps.get_comp("B50")
    B51 = ps.get_comp("B51")
    B52 = ps.get_comp("B52")
    B53 = ps.get_comp("B53")
    B54 = ps.get_comp("B54")
    B55 = ps.get_comp("B55")
    B56 = ps.get_comp("B56")
    B57 = ps.get_comp("B57")
    B58 = ps.get_comp("B58")
    B59 = ps.get_comp("B59")
    B60 = ps.get_comp("B60")
    B61 = ps.get_comp("B61")
    B62 = ps.get_comp("B62")
    B63 = ps.get_comp("B63")
    B64 = ps.get_comp("B64")
    B65 = ps.get_comp("B65")
    B66 = ps.get_comp("B66")
    B67 = ps.get_comp("B67")

    B68 = ps.get_comp("B68")
    B69 = ps.get_comp("B69")
    B70 = ps.get_comp("B70")
    B71 = ps.get_comp("B71")

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
    L33 = ps.get_comp("L33")
    L34 = ps.get_comp("L34")
    L35 = ps.get_comp("L35")
    L36 = ps.get_comp("L36")
    L37 = ps.get_comp("L37")
    L38 = ps.get_comp("L38")
    L39 = ps.get_comp("L39")
    L40 = ps.get_comp("L40")
    L41 = ps.get_comp("L41")
    L42 = ps.get_comp("L42")
    L43 = ps.get_comp("L43")
    L44 = ps.get_comp("L44")
    L45 = ps.get_comp("L45")
    L46 = ps.get_comp("L46")
    L47 = ps.get_comp("L47")
    L48 = ps.get_comp("L48")
    L49 = ps.get_comp("L49")
    L50 = ps.get_comp("L50")
    L51 = ps.get_comp("L51")
    L52 = ps.get_comp("L52")
    L53 = ps.get_comp("L53")
    L54 = ps.get_comp("L54")
    L55 = ps.get_comp("L55")
    L56 = ps.get_comp("L56")
    L57 = ps.get_comp("L57")
    L58 = ps.get_comp("L58")
    L59 = ps.get_comp("L59")
    L60 = ps.get_comp("L60")
    L61 = ps.get_comp("L61")
    L62 = ps.get_comp("L62")
    L63 = ps.get_comp("L63")
    L64 = ps.get_comp("L64")
    L65 = ps.get_comp("L65")
    L66 = ps.get_comp("L66")

    L67 = ps.get_comp("L67")
    L68 = ps.get_comp("L68")
    ML3 = ps.get_comp("ML3")
    ML4 = ps.get_comp("ML4")

    L69 = ps.get_comp("L69")
    L70 = ps.get_comp("L70")
    # L71 = ps.get_comp("L71")
    L72 = ps.get_comp("L72")
    # L73 = ps.get_comp("L73")


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
    L33a = ps.get_comp("L33a")
    L33b = ps.get_comp("L33b")
    L34a = ps.get_comp("L34a")
    L34b = ps.get_comp("L34b")
    L35a = ps.get_comp("L35a")
    L35b = ps.get_comp("L35b")
    L36a = ps.get_comp("L36a")
    L36b = ps.get_comp("L36b")
    L37a = ps.get_comp("L37a")
    L37b = ps.get_comp("L37b")
    L38a = ps.get_comp("L38a")
    L38b = ps.get_comp("L38b")
    L39a = ps.get_comp("L39a")
    L39b = ps.get_comp("L39b")
    L40a = ps.get_comp("L40a")
    L40b = ps.get_comp("L40b")
    L41a = ps.get_comp("L41a")
    L41b = ps.get_comp("L41b")
    L42a = ps.get_comp("L42a")
    L42b = ps.get_comp("L42b")
    L43a = ps.get_comp("L43a")
    L43b = ps.get_comp("L43b")
    L44a = ps.get_comp("L44a")
    L44b = ps.get_comp("L44b")
    L45a = ps.get_comp("L45a")
    L45b = ps.get_comp("L45b")
    L46a = ps.get_comp("L46a")
    L46b = ps.get_comp("L46b")
    L47a = ps.get_comp("L47a")
    L47b = ps.get_comp("L47b")
    L48a = ps.get_comp("L48a")
    L48b = ps.get_comp("L48b")
    L49a = ps.get_comp("L49a")
    L49b = ps.get_comp("L49b")
    L50a = ps.get_comp("L50a")
    L50b = ps.get_comp("L50b")
    L51a = ps.get_comp("L51a")
    L51b = ps.get_comp("L51b")
    L52a = ps.get_comp("L52a")
    L52b = ps.get_comp("L52b")
    L53a = ps.get_comp("L53a")
    L53b = ps.get_comp("L53b")
    L54a = ps.get_comp("L54a")
    L54b = ps.get_comp("L54b")
    L55a = ps.get_comp("L55a")
    L55b = ps.get_comp("L55b")
    L56a = ps.get_comp("L56a")
    L56b = ps.get_comp("L56b")
    L57a = ps.get_comp("L57a")
    L57b = ps.get_comp("L57b")
    L58a = ps.get_comp("L58a")
    L58b = ps.get_comp("L58b")
    L59a = ps.get_comp("L59a")
    L59b = ps.get_comp("L59b")
    L60a = ps.get_comp("L60a")
    L60b = ps.get_comp("L60b")
    L61a = ps.get_comp("L61a")
    L61b = ps.get_comp("L61b")
    L62a = ps.get_comp("L62a")
    L62b = ps.get_comp("L62b")
    L63a = ps.get_comp("L63a")
    L63b = ps.get_comp("L63b")
    L64a = ps.get_comp("L64a")
    L64b = ps.get_comp("L64b")
    L65a = ps.get_comp("L65a")
    L65b = ps.get_comp("L65b")
    L66a = ps.get_comp("L66a")
    L66b = ps.get_comp("L66b")

    L67a = ps.get_comp("L67a")
    L67b = ps.get_comp("L67b")
    L67c = ps.get_comp("L67c")
    L68a = ps.get_comp("L68a")
    L68b = ps.get_comp("L68b")
    ML3a = ps.get_comp("ML3a")
    ML3b = ps.get_comp("ML3b")
    ML4a = ps.get_comp("ML4a")
    ML4b = ps.get_comp("ML4b")

    L69a = ps.get_comp("L69a")
    L69b = ps.get_comp("L69b")
    L70a = ps.get_comp("L70a")
    L70b = ps.get_comp("L70b")
    # L71a = ps.get_comp("L71a")
    # L71b = ps.get_comp("L71b")
    L72a = ps.get_comp("L72a")
    L72b = ps.get_comp("L72b")
    # L73a = ps.get_comp("L73a")
    # L73b = ps.get_comp("L73b")


# Fetching battery and production objects
Bat1 = B68.get_battery()
P1 = B70.get_production()
P2 = B71.get_production()

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

# load_dict[B2] = {
#     "Husholdning": {"pload": load_house * 50, "qload": load_house * 0}
# }
# load_dict[B3] = {
#     "Husholdning": {"pload": load_house * 60, "qload": load_house * 0}
# }
# load_dict[B4] = {
#     "Husholdning": {"pload": load_house * 52, "qload": load_house * 0}
# }
load_dict[B5] = {
    "Husholdning": {"pload": load_house * 50, "qload": load_house * 0}
}
load_dict[B6] = {
    "Husholdning": {"pload": load_house * 35, "qload": load_house * 0}
}
load_dict[B7] = {
    "Husholdning": {"pload": load_house * 55, "qload": load_house * 0}
}
load_dict[B8] = {
    "Husholdning": {"pload": load_house * 40, "qload": load_house * 0}
}
load_dict[B9] = {
    "Husholdning": {"pload": load_house * 53, "qload": load_house * 0}
}
load_dict[B10] = {
    "Husholdning": {"pload": load_house * 56, "qload": load_house * 0}
}
load_dict[B11] = {
    "Husholdning": {"pload": load_house * 45, "qload": load_house * 0}
}
load_dict[B12] = {
    "Husholdning": {"pload": load_house * 53, "qload": load_house * 0}
}
load_dict[B13] = {
    "Husholdning": {"pload": load_house * 62, "qload": load_house * 0}
}
load_dict[B14] = {
    "Husholdning": {"pload": load_house * 59, "qload": load_house * 0}
}
load_dict[B15] = {
    "Husholdning": {"pload": load_house * 49, "qload": load_house * 0}
}
load_dict[B16] = {
    "Husholdning": {"pload": load_house * 0, "qload": load_house * 0}
}
load_dict[B17] = {
    "Husholdning": {"pload": load_house * 42, "qload": load_house * 0}
}
load_dict[B18] = {
    "Jordbruk": {"pload": load_farm * 40, "qload": load_farm * 0}
}
load_dict[B19] = {
    "Jordbruk": {"pload": load_farm * 36, "qload": load_farm * 0}
}
load_dict[B20] = {
    "Jordbruk": {"pload": load_farm * 40, "qload": load_farm * 0}
}
load_dict[B21] = {
    "Jordbruk": {"pload": load_farm * 20, "qload": load_farm * 0}
}
load_dict[B22] = {
    "Jordbruk": {"pload": load_farm * 22, "qload": load_farm * 0}
}
load_dict[B23] = {
    "Jordbruk": {"pload": load_farm * 35, "qload": load_farm * 0}
}
load_dict[B24] = {
    "Jordbruk": {"pload": load_farm * 32, "qload": load_farm * 0}
}
load_dict[B25] = {
    "Jordbruk": {"pload": load_farm * 25, "qload": load_farm * 0}
}
load_dict[B26] = {
    "Jordbruk": {"pload": load_farm * 36, "qload": load_farm * 0}
}
load_dict[B27] = {
    "Jordbruk": {"pload": load_farm * 20, "qload": load_farm * 0}
}
load_dict[B28] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B29] = {
    "Offentlig virksomhet": {
        "pload": load_office * 1,
        "qload": load_office * 0,
    }
}
load_dict[B30] = {
    "Offentlig virksomhet": {
        "pload": load_office * 1,
        "qload": load_office * 0,
    }
}
load_dict[B31] = {
    "Handel og tjenester": {
        "pload": load_trade * 2,
        "qload": load_trade * 0,
    }
}
load_dict[B32] = {
    "Handel og tjenester": {
        "pload": load_trade * 1,
        "qload": load_trade * 0,
    }
}
load_dict[B33] = {
    "Husholdning": {"pload": load_house * 55, "qload": load_house * 0}
}
load_dict[B34] = {
    "Husholdning": {"pload": load_house * 42, "qload": load_house * 0}
}
load_dict[B35] = {
    "Husholdning": {"pload": load_house * 52, "qload": load_house * 0}
}
load_dict[B36] = {
    "Industri": {"pload": load_industry2 * 2, "qload": load_industry2 * 0}
}
load_dict[B37] = {
    "Industri": {"pload": load_industry2 * 1, "qload": load_industry2 * 0}
}
load_dict[B38] = {
    "Offentlig virksomhet": {
        "pload": load_office * 1,
        "qload": load_office * 0,
    }
}
load_dict[B39] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B40] = {
    "Husholdning": {"pload": load_house * 36, "qload": load_house * 0}
}
load_dict[B41] = {
    "Husholdning": {"pload": load_house * 42, "qload": load_house * 0}
}
load_dict[B42] = {
    "Handel og tjenester": {
        "pload": load_trade * 3,
        "qload": load_trade * 0,
    }
}
load_dict[B43] = {
    "Handel og tjenester": {
        "pload": load_trade * 2,
        "qload": load_trade * 0,
    }
}
load_dict[B44] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B45] = {
    "Jordbruk": {"pload": load_farm * 40, "qload": load_farm * 0}
}
load_dict[B46] = {
    "Jordbruk": {"pload": load_farm * 45, "qload": load_farm * 0}
}
load_dict[B47] = {
    "Husholdning": {"pload": load_house * 50, "qload": load_house * 0}
}
load_dict[B48] = {
    "Husholdning": {"pload": load_house * 42, "qload": load_house * 0}
}
load_dict[B49] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B50] = {
    "Offentlig virksomhet": {
        "pload": load_office * 1,
        "qload": load_office * 0,
    }
}
load_dict[B51] = {
    "Offentlig virksomhet": {
        "pload": load_office * 1,
        "qload": load_office * 0,
    }
}
load_dict[B52] = {
    "Offentlig virksomhet": {
        "pload": load_office * 2,
        "qload": load_office * 0,
    }
}
load_dict[B53] = {
    "Husholdning": {"pload": load_house * 55, "qload": load_house * 0}
}
load_dict[B54] = {
    "Husholdning": {"pload": load_house * 41, "qload": load_house * 0}
}
load_dict[B55] = {
    "Husholdning": {"pload": load_house * 42, "qload": load_house * 0}
}
load_dict[B56] = {
    "Jordbruk": {"pload": load_farm * 50, "qload": load_farm * 0}
}
load_dict[B57] = {
    "Jordbruk": {"pload": load_farm * 45, "qload": load_farm * 0}
}
load_dict[B58] = {
    "Jordbruk": {"pload": load_farm * 40, "qload": load_farm * 0}
}
load_dict[B59] = {
    "Industri": {"pload": load_industry2 * 2, "qload": load_industry2 * 0}
}
load_dict[B60] = {
    "Industri": {"pload": load_industry2 * 1, "qload": load_industry2 * 0}
}
load_dict[B61] = {
    "Industri": {"pload": load_industry2 * 2, "qload": load_industry2 * 0}
}
load_dict[B62] = {
    "Handel og tjenester": {
        "pload": load_trade * 2,
        "qload": load_trade * 0,
    }
}
load_dict[B63] = {
    "Handel og tjenester": {
        "pload": load_trade * 2,
        "qload": load_trade * 0,
    }
}
load_dict[B64] = {
    "Handel og tjenester": {
        "pload": load_trade * 1,
        "qload": load_trade * 0,
    }
}
load_dict[B65] = {
    "Industri": {"pload": load_industry2 * 1, "qload": load_industry2 * 0}
}
load_dict[B66] = {
    "Husholdning": {"pload": load_house * 40, "qload": load_house * 0}
}
load_dict[B67] = {
    "Jordbruk": {"pload": load_farm * 30, "qload": load_farm * 0}
}

# Microgrid:
load_dict[B69] = {
    "Microgrid": {"pload": load_farm * 40, "qload": load_farm * 0}
}

prod_dict = dict()

prod_dict[P1] = {"pprod": wind, "qprod": PV * 0}
prod_dict[P2] = {"pprod": PV, "qprod": PV * 0}

ps.add_load_dict(load_dict)
ps.add_prod_dict(prod_dict)

save_dir = r"C:\Users\stinefm\Documents\results69"

fig = plot_topology(ps.buses, ps.lines, figsize=(6.5, 4.5))
fig.savefig(os.path.join(save_dir, "topology.pdf"))

sim = Simulation(ps, random_seed=0)

sim.run_monte_carlo(
    iterations=1500,
    increments=8760,
    save_iterations=[1, 500, 1500],
    save_dir=save_dir,
)

end = time.time()
print("Time elapsed: {}".format(end - start))
