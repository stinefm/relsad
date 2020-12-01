from stinetwork.network.components import Bus, Line, Disconnector, CircuitBreaker
from stinetwork.network.systems import PowerSystem, Distribution, Microgrid
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow, ForwardSearch, BackwardSearch
from stinetwork.visualization.plotting import plot_topology

def initialize_test_network():

    ps = PowerSystem()

    B0 = Bus("B0", coordinate=[0, 0], is_slack=True) #Slack bus
    B1 = Bus("B1", coordinate=[0, -1], is_slack=False)
    B2 = Bus("B2", coordinate=[1, -2], is_slack=False)
    B3 = Bus("B3", coordinate=[0, -2])
    B4 = Bus("B4", coordinate=[0, -3], is_slack=False)
    B5 = Bus("B5", coordinate=[1, -3]) # Production
    M1 = Bus("M1", coordinate=[-1, -2], is_slack=False) # Microgrid
    M2 = Bus("M2", coordinate=[-2, -3], is_slack=False)
    M3 = Bus("M3", coordinate=[-1, -3])

    # B0.set_load(0.001,0.0006)
    B1.set_load(0.001,0.0006)
    B2.set_load(0.001,0.0006)
    B3.set_load(0.001,0.0006)
    B4.set_load(0.001,0.0006)
    B5.set_load(0.001,0.0006)
    M1.set_load(0.001,0.0006)
    M2.set_load(0.001,0.0006)
    M3.set_load(0.001,0.0006)

    L1 = Line(1, B0, B1, 0.057526629463617, 0.029324854498807)
    L2 = Line(2, B1, B2, 0.057526629463617, 0.029324854498807)
    L3 = Line(3, B1, B3, 0.057526629463617, 0.029324854498807)
    L4 = Line(4, B3, B4, 0.057526629463617, 0.029324854498807)
    L5 = Line(5, B2, B5, 0.057526629463617, 0.029324854498807)
    L6 = Line(6, B3, B5, 0.057526629463617, 0.029324854498807)
    L7 = Line(7, B1, M1, 0.057526629463617, 0.029324854498807)
    ML1 = Line(8, M1, M2, 0.057526629463617, 0.029324854498807)
    ML2 = Line(9, M1, M3, 0.057526629463617, 0.029324854498807)

    E1 = CircuitBreaker("E1", L1)

    Disconnector("L1a", L1, B0, E1)
    Disconnector("L1b", L1, B1, E1)
    Disconnector("L1c", L1, B1)
    L2a = Disconnector("L2a", L2, B1)
    Disconnector("L3a", L3, B1)
    Disconnector("L3b", L3, B3)
    Disconnector("L4a", L4, B3)
    Disconnector("L5a", L5, B2)
    L6a = Disconnector("L6a", L6, B3)
    Disconnector("L7a", L7, B1)
    L7b = Disconnector("L7b", L7, M1)

    # L2a.open()
    L6a.open()
    # L7b.open()

    dn = Distribution(ps)

    dn.add_buses([B0,B1,B2,B3,B4,B5])
    dn.add_lines([L1,L2,L3,L4,L5,L6])

    m = Microgrid(ps,L7)

    m.add_buses([M1,M2,M3])
    m.add_lines([ML1,ML2])

    # ps.update()

    # ps.find_sub_systems()

    # for sub_system in ps.sub_systems:
    #     plot_topology(sub_system["buses"],sub_system["lines"])
    #     buses = DistLoadFlow(sub_system["buses"],sub_system["lines"])

    #     dispVolt(buses,tpres=False)
    #     dispFlow(buses, sub_system["lines"],tpres=False)


    return ps

if __name__=="__main__":

    ps = initialize_test_network()

    plot_topology(ps.active_buses,ps.active_lines)

    ps.active_buses = DistLoadFlow(ps.active_buses,ps.active_lines)

    dispVolt(ps.active_buses,tpres=False)
    dispFlow(ps.active_buses, ps.active_lines,tpres=False)
