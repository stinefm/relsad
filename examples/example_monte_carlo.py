from stinetwork.test_networks.smallNetwork import initialize_test_network
from stinetwork.network.systems import find_sub_systems, update_sub_system_slack, PowerSystem
from stinetwork.visualization.plotting import plot_topology
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow, ForwardSearch, BackwardSearch, dispLoads
from load_and_gen_data import WeatherGen,LoadGen,windGen,PVgeneration
import time, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

start = time.time()

ps = initialize_test_network()

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
P2 = B5.get_production()

temp_profiles, wind_profiles, solar_profiles = WeatherGen()

wind = windGen(wind_profiles)
PV = PVgeneration(temp_profiles, solar_profiles)

load_house, load_farm, load_industry2, load_trade, load_office = LoadGen(temp_profiles)

N = 1 # Size of Monte Carlo simulation

for i in range(N):
    for day in range(1):
        for hour in range(24):
            print("hour: {}".format(day*24+hour))
            ## Set load
            B1.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0},
                                    "Industri":{"pload":load_industry2[day,hour]*10,"qload":0.0}})
            B2.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})
            B3.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})
            B4.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})
            B5.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})
            M2.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})
            M3.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})


            ## Set production
            P1.set_prod(pprod=PV[day,hour]+wind[day,hour], qprod=0)
            P2.set_prod(pprod=wind[day,hour], qprod=0)

            ps.run()
                          
end = time.time()
print("Time elapsed: {}".format(end - start))

# ps.plot_battery_history()
# ps.plot_bus_history()
# ps.plot_load_shed_history()

ps.save_bus_history(r"C:\Users\stinefm\Desktop\results")
ps.save_battery_history(r"C:\Users\stinefm\Desktop\results")
ps.save_load_shed_history(r"C:\Users\stinefm\Desktop\results")

for sub_system in PowerSystem.shed_configs:
    fig = plot_topology(list(sub_system.buses),list(sub_system.lines))
    fig.show()
try:
    input("Press enter to continue")
except SyntaxError:
    pass
