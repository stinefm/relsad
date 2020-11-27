from stinetwork.network.components import Bus, Line, Disconnector, CircuitBreaker
from stinetwork.network.systems import Distribution
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow
from stinetwork.visualization.plotting import plot_topology

def initialize_test_network():
    B0 = Bus(0, 0, 0, coordinate=[0, 0]) #Slack bus
    B1 = Bus(1, 5, 0, coordinate=[0, -1])
    B2 = Bus(2, 4, 0, coordinate=[1, -2])
    B3 = Bus(3, 3, 0, coordinate=[0, -2])
    B4 = Bus(4, 2, 0, coordinate=[0, -3])
    B5 = Bus(5, 0, 0, coordinate=[1, -3]) # Microgrid
    B6 = Bus(6, -10, 0, coordinate=[-1, -2]) # Production

    L1 = Line(1, B0, B1, 0.057526629463617, 0.029324854498807)
    L2 = Line(2, B1, B2, 0.057526629463617, 0.029324854498807)
    L3 = Line(3, B1, B3, 0.057526629463617, 0.029324854498807)
    L4 = Line(4, B3, B4, 0.057526629463617, 0.029324854498807)
    L5 = Line(5, B2, B5, 0.057526629463617, 0.029324854498807)
    L6 = Line(6, B3, B5, 0.057526629463617, 0.029324854498807)
    L7 = Line(7, B1, B6, 0.057526629463617, 0.029324854498807)

    E1 = CircuitBreaker("E1", L1)

    Disconnector("L1a", L1, B0, E1)
    Disconnector("L1b", L1, B1, E1)
    Disconnector("L1c", L1, B1)
    Disconnector("L2a", L2, B1)
    Disconnector("L3a", L3, B1)
    Disconnector("L3b", L3, B3)
    Disconnector("L4a", L4, B3)
    Disconnector("L5a", L5, B2)
    Disconnector("L6a", L6, B3)
    Disconnector("L7a", L7, B1)
    Disconnector("L7b", L7, B6)

    dn = Distribution()

    dn.add_buses([B0,B1,B2,B3,B4,B5,B6])
    dn.add_lines([L1,L2,L3,L4,L5,L6,L7])

    return dn

if __name__=="__main__":

    dn = initialize_test_network()
    plot_topology(dn.buses,dn.lines)