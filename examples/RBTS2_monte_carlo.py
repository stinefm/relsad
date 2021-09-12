from stinetwork.test_networks.RBTS2 import initialize_network
from stinetwork.simulation import Simulation
from load_and_gen_data import (
    WeatherGen,
    LoadGen,
    windGen,
    PVgeneration,
)
import time
import numpy as np
import os
from stinetwork.utils import (
    Time,
    TimeUnit,
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

    if False:
        pass
        # # Fetching line-objects
        # L1 = ps.get_comp("L1")
        # L2 = ps.get_comp("L2")
        # L3 = ps.get_comp("L3")
        # L4 = ps.get_comp("L4")
        # L5 = ps.get_comp("L5")
        # L6 = ps.get_comp("L6")
        # L7 = ps.get_comp("L7")
        # L8 = ps.get_comp("L8")
        # L9 = ps.get_comp("L9")
        # L10 = ps.get_comp("L10")
        # L11 = ps.get_comp("L11")
        # L12 = ps.get_comp("L12")
        # L13 = ps.get_comp("L13")
        # L14 = ps.get_comp("L14")
        # L15 = ps.get_comp("L15")
        # L16 = ps.get_comp("L16")
        # L17 = ps.get_comp("L17")
        # L18 = ps.get_comp("L18")
        # L19 = ps.get_comp("L19")
        # L20 = ps.get_comp("L20")
        # L21 = ps.get_comp("L21")
        # L22 = ps.get_comp("L22")
        # L23 = ps.get_comp("L23")
        # L24 = ps.get_comp("L24")
        # L25 = ps.get_comp("L25")
        # L26 = ps.get_comp("L26")
        # L27 = ps.get_comp("L27")
        # L28 = ps.get_comp("L28")
        # L29 = ps.get_comp("L29")
        # L30 = ps.get_comp("L30")
        # L31 = ps.get_comp("L31")
        # L32 = ps.get_comp("L32")
        # L33 = ps.get_comp("L33")
        # L34 = ps.get_comp("L34")
        # L35 = ps.get_comp("L35")
        # L36 = ps.get_comp("L36")
        # LB1 = ps.get_comp("LB1")
        # LB2 = ps.get_comp("LB2")

        # # Fetching disconnector objects
        # DL4 = ps.get_comp("DL4")
        # DL7 = ps.get_comp("DL7")
        # DL10 = ps.get_comp("DL10")
        # DLB1a = ps.get_comp("DLB1a")
        # DL14 = ps.get_comp("DL14")
        # DLB1b = ps.get_comp("DLB1b")
        # DL18 = ps.get_comp("DL18")
        # DL21 = ps.get_comp("DL21")
        # DL24 = ps.get_comp("DL24")
        # DLB2a = ps.get_comp("DLB2a")
        # DL29 = ps.get_comp("DL29")
        # DL32 = ps.get_comp("DL32")
        # DL34 = ps.get_comp("DL34")
        # DLB2b = ps.get_comp("DLB2b")

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
        "Husholdning": {"pload": load_res1, "qload": load_res1 * 0},
    }
    load_dict["load"][B2] = {
        "Husholdning": {"pload": load_res1, "qload": load_res1 * 0}
    }
    load_dict["load"][B3] = {
        "Husholdning": {"pload": load_res1, "qload": load_res1 * 0}
    }
    load_dict["load"][B4] = {
        "Husholdning": {"pload": load_gov, "qload": load_gov * 0}
    }
    load_dict["load"][B5] = {
        "Husholdning": {"pload": load_gov, "qload": load_gov * 0}
    }
    load_dict["load"][B6] = {
        "Husholdning": {"pload": load_com, "qload": load_com * 0}
    }
    load_dict["load"][B7] = {
        "Husholdning": {"pload": load_com, "qload": load_com * 0}
    }
    load_dict["load"][B8] = {
        "Husholdning": {"pload": load_small1, "qload": load_gov * 0}
    }
    load_dict["load"][B9] = {
        "Husholdning": {"pload": load_small2, "qload": load_gov * 0}
    }
    load_dict["load"][B10] = {
        "Husholdning": {"pload": load_res1, "qload": load_gov * 0}
    }
    load_dict["load"][B11] = {
        "Husholdning": {"pload": load_res1, "qload": load_gov * 0}
    }
    load_dict["load"][B12] = {
        "Husholdning": {"pload": load_res2, "qload": load_gov * 0}
    }
    load_dict["load"][B13] = {
        "Husholdning": {"pload": load_gov, "qload": load_gov * 0}
    }
    load_dict["load"][B14] = {
        "Husholdning": {"pload": load_gov, "qload": load_gov * 0}
    }
    load_dict["load"][B15] = {
        "Husholdning": {"pload": load_com, "qload": load_gov * 0}
    }
    load_dict["load"][B16] = {
        "Husholdning": {"pload": load_com, "qload": load_gov * 0}
    }
    load_dict["load"][B17] = {
        "Husholdning": {"pload": load_res2, "qload": load_gov * 0}
    }
    load_dict["load"][B18] = {
        "Husholdning": {"pload": load_res2, "qload": load_gov * 0}
    }
    load_dict["load"][B19] = {
        "Husholdning": {"pload": load_res2, "qload": load_gov * 0}
    }
    load_dict["load"][B20] = {
        "Husholdning": {"pload": load_gov, "qload": load_gov * 0}
    }
    load_dict["load"][B21] = {
        "Husholdning": {"pload": load_gov, "qload": load_gov * 0}
    }
    load_dict["load"][B22] = {
        "Husholdning": {"pload": load_com, "qload": load_gov * 0}
    }

    save_dir = r"test_RBTS2"

    sim = Simulation(ps, random_seed=3)
    sim.run_monte_carlo(
        iterations=200,
        increments=8760,
        time_step=Time(1, TimeUnit.HOUR),
        time_unit=TimeUnit.HOUR,
        load_dict=load_dict,
        prod_dict={},
        save_iterations=[
            1,
            50,
            100,
            150,
            200,
        ],  # , 250, 300, 350, 400, 450, 499],
        save_dir=save_dir,
        n_procs=4,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
