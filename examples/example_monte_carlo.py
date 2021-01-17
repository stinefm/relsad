from stinetwork.test_networks.smallNetwork import initialize_test_network
from stinetwork.visualization.plotting import plot_topology
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow, ForwardSearch, BackwardSearch
from load_and_gen_data import WeatherGen,LoadGen,windGen,PVgeneration
import time

start = time.time()

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

plot_topology(ps.all_buses, ps.all_lines)

N = 1 # Size of Monte Carlo simulation

for i in range(N):
    for day in range(1):
        for hour in range(5):
            print("hour: {}".format(day*24+hour))
            ## Set load
            B1.set_load(pload=load_house[day,hour]*10,qload=0.0)
            B2.set_load(pload=load_house[day,hour]*10,qload=0.0)
            B3.set_load(pload=load_house[day,hour]*10,qload=0.0)
            B4.set_load(pload=load_house[day,hour]*10,qload=0.0)
            B5.set_load(pload=load_house[day,hour]*10,qload=0.0)
            M1.set_load(pload=load_house[day,hour]*10,qload=0.0)
            M2.set_load(pload=load_house[day,hour]*10,qload=0.0)
            M3.set_load(pload=load_house[day,hour]*10,qload=0.0)
            
            ## Set fail status
            for comp in ps.get_comp_list():
                comp.update_fail_status()

            ps.update()
                
            ps.find_sub_systems()
            ps.update_sub_system_slack()
            
            ## Load flow
            for sub_system in ps.sub_systems:
                if len(ps.sub_systems) > 0:
                    # Print status
                    ps.print_status()
                    plot_topology(sub_system["buses"],sub_system["lines"])
                buses = DistLoadFlow(sub_system["buses"],sub_system["lines"])
            
            
            
            

end = time.time()
print("Time elapsed: {}".format(end - start))