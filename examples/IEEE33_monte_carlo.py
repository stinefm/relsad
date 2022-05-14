from relsad.test_networks.IEEE33 import initialize_network
from relsad.visualization.plotting import plot_topology
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

os.chdir(os.path.dirname(os.path.abspath(__file__)))

include_microgrid = True
include_production = True

start = time.time()

ps = initialize_network(
    include_microgrid=include_microgrid,
    include_production=include_production,
)

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


for bus in [B3, B9, B10, B11, B15, B16, B17, B19, B20, B23, B26, B27]:
    bus.add_load_data(
        pload_data=load_house,
        cost_function=household,
    )
for bus in [B2, B29]:
    bus.add_load_data(
        pload_data=load_trade,
        cost_function=trade,
    )
for bus in [B4, B14, B31]:
    bus.add_load_data(
        pload_data=load_office,
        cost_function=trade,
    )
for bus in [B5, B6, B12, B13, B18, B21, B22, B28, B33]:
    bus.add_load_data(
        pload_data=load_farm,
        cost_function=farm,
    )
for bus in [B7, B8, B24, B25, B30, B32]:
    bus.add_load_data(
        pload_data=load_industry2,
        cost_function=industry,
    )


if include_microgrid:

    BM1 = ps.get_comp("BM1")
    BM2 = ps.get_comp("BM2")
    BM3 = ps.get_comp("BM3")
    BM4 = ps.get_comp("BM4")

    Bat1 = BM1.get_battery()
    P1 = BM3.get_production()
    P2 = BM4.get_production()

    P1.add_prod_data(
        pprod_data=wind,
    )
    P2.add_prod_data(
        pprod_data=PV,
    )

    BM2.add_load_data(
        pload_data=load_farm,
        cost_function=microgrid,
    )

if include_production:

    Battery = B30.get_battery()
    P3 = B15.get_production()

    P3.add_prod_data(
        pprod_data=wind * 2,
    )

# save_dir = r"test_IEEE33"

# fig = plot_topology(ps.buses, ps.lines, figsize=(6.5, 4.5))
# fig.savefig(os.path.join(save_dir, "topology.pdf"))

sim = Simulation(ps, random_seed=0)

sim.run_monte_carlo(
    iterations=1,  # 5000,
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
    time_step=Time(30, TimeUnit.MINUTE),
    time_unit=TimeUnit.HOUR,
    save_iterations=[1, 2, 3, 4, 5],
    # save_dir=save_dir,
    n_procs=4,
    debug=True,
)

end = time.time()
print("Time elapsed: {}".format(end - start))
