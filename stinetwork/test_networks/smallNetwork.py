from stinetwork.network.components import Bus, Line, Disconnector, CircuitBreaker, Battery, Production
from stinetwork.network.systems import PowerSystem, Distribution, Microgrid

def initialize_test_network():
    ps = PowerSystem()

    B0 = Bus("B0", coordinate=[0, 0], is_slack=True) #Slack bus
    B1 = Bus("B1", coordinate=[0, -1])
    B2 = Bus("B2", coordinate=[1, -2])
    B3 = Bus("B3", coordinate=[0, -2])
    B4 = Bus("B4", coordinate=[0, -3])
    B5 = Bus("B5", coordinate=[1, -3])
    M1 = Bus("M1", coordinate=[-1, -2])
    M2 = Bus("M2", coordinate=[-2, -3])
    M3 = Bus("M3", coordinate=[-1, -3])

    Battery("Bat1",M1)
    Production("P1",M2)
    Production("P2",B5)

    L1 = Line("L1", B0, B1, 0.057526629463617, 0.029324854498807)
    L2 = Line("L2", B1, B2, 0.057526629463617, 0.029324854498807)
    L3 = Line("L3", B1, B3, 0.057526629463617, 0.029324854498807)
    L4 = Line("L4", B3, B4, 0.057526629463617, 0.029324854498807)
    L5 = Line("L5", B2, B5, 0.057526629463617, 0.029324854498807)
    L6 = Line("L6", B3, B5, 0.057526629463617, 0.029324854498807)
    L7 = Line("L7", B1, M1, 0.057526629463617, 0.029324854498807)
    ML1 = Line("ML1", M1, M2, 0.057526629463617, 0.029324854498807)
    ML2 = Line("ML2", M1, M3, 0.057526629463617, 0.029324854498807)

    E1 = CircuitBreaker("E1", L1)

    Disconnector("L1a", L1, B0, E1)
    Disconnector("L1b", L1, B1, E1)
    Disconnector("L1c", L1, B1)
    Disconnector("L2a", L2, B1)
    Disconnector("L2b", L2, B2)
    Disconnector("L3a", L3, B1)
    Disconnector("L3b", L3, B3)
    Disconnector("L4a", L4, B3)
    Disconnector("L4b", L4, B4)
    Disconnector("L5a", L5, B2)
    Disconnector("L5b", L5, B5)
    Disconnector("L6a", L6, B3)
    Disconnector("L6b", L6, B5)
    Disconnector("L7a", L7, B1)
    Disconnector("L7b", L7, M1)

    Disconnector("ML1a", ML1, M1)
    Disconnector("ML1b", ML1, M2)
    Disconnector("ML2a", ML2, M1)
    Disconnector("ML2b", ML2, M3)

    dn = Distribution(ps)

    dn.add_buses([B0,B1,B2,B3,B4,B5])
    dn.add_lines([L1,L2,L3,L4,L5,L6])

    m = Microgrid(dn,L7)

    m.add_buses([M1,M2,M3])
    m.add_lines([ML1,ML2])

    return ps

if __name__=="__main__":
    pass
