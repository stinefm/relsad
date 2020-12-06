from stinetwork.test_networks.smallNetwork import initialize_test_network
from stinetwork.visualization.plotting import plot_topology
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow, ForwardSearch, BackwardSearch
from load_and_gen_data import WeatherGen,LoadGen,windGen,PVgeneration

ps = initialize_test_network()

# Fetching bus-objects
B0 = ps.get_comp("B0")
B1 = ps.get_comp("B1")
B2 = ps.get_comp("B2")
B3 = ps.get_comp("B3")
B4 = ps.get_comp("B4")
B5 = ps.get_comp("B5")
M1 = ps.get_comp("M1")
M2 = ps.get_comp("M2")
M3 = ps.get_comp("M3")

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


temp_profiles, wind_profiles, solar_profiles = WeatherGen()

wind = windGen(wind_profiles)
PV = PVgeneration(temp_profiles, solar_profiles)

load_house, load_farm, load_industry2, load_trade, load_office = LoadGen(temp_profiles)

# B0.set_load(0.001,0.0006)
B1.set_load(0.001,0.0006)
B2.set_load(0.001,0.0006)
B3.set_load(0.001,0.0006)
B4.set_load(0.001,0.0006)
B5.set_load(0.001,0.0006)
M1.set_load(0.001,0.0006)
M2.set_load(0.001,0.0006)
M3.set_load(0.001,0.0006)


L2a.open()
L6a.open()
L7b.open()

plot_topology(ps.active_buses,ps.active_lines)
ps.find_sub_systems()

ps.update_sub_system_slack()

for sub_system in ps.sub_systems:
    plot_topology(sub_system["buses"],sub_system["lines"])
    buses = DistLoadFlow(sub_system["buses"],sub_system["lines"])

    dispVolt(buses,tpres=False)
    dispFlow(buses, sub_system["lines"],tpres=False)