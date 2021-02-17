from stinetwork.network.components import Bus, Line, Disconnector, CircuitBreaker, Battery, Production
from stinetwork.network.systems import PowerSystem, Transmission, Distribution, Microgrid

def initialize_test_network():
    ps = PowerSystem()

    ## Transmission network
    T = Bus("T", coordinate=[0, 0], fail_rate_per_year=0)

    ## Distribution network
    B1 = Bus("B1", coordinate=[0, -1], fail_rate_per_year=20)#0.2)
    B2 = Bus("B2", coordinate=[1, -2], fail_rate_per_year=20)#0.2)
    B3 = Bus("B3", coordinate=[0, -2], fail_rate_per_year=20)#0.2)
    B4 = Bus("B4", coordinate=[0, -3], fail_rate_per_year=20)#0.2)
    B5 = Bus("B5", coordinate=[1, -3], fail_rate_per_year=20)#0.2)

    ## Microgrid
    M1 = Bus("M1", coordinate=[-1, -2], fail_rate_per_year=20)#0.2)
    M2 = Bus("M2", coordinate=[-2, -3], fail_rate_per_year=20)#0.2)
    M3 = Bus("M3", coordinate=[-1, -3], fail_rate_per_year=20)#0.2)

    Battery("Bat1",M1)
    Production("P1",M2)
    Production("P2",B5)

    L1 = Line("L1", T, B1, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    L2 = Line("L2", B1, B2, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    L3 = Line("L3", B1, B3, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    L4 = Line("L4", B3, B4, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    L5 = Line("L5", B2, B5, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    L6 = Line("L6", B3, B5, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    L7 = Line("L7", B1, M1, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    ML1 = Line("ML1", M1, M2, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)
    ML2 = Line("ML2", M1, M3, 0.057526629463617, 0.029324854498807, fail_rate_density_per_year=20)#0.2)

    E1 = CircuitBreaker("E1", L1)

    Disconnector("L1a", L1, T, E1)
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

    L6.set_backup()

    tn = Transmission(ps,T)

    dn = Distribution(tn,L1)

    dn.add_buses({B1,B2,B3,B4,B5})
    dn.add_lines({L2,L3,L4,L5,L6})

    m = Microgrid(dn,L7)

    m.add_buses({M1,M2,M3})
    m.add_lines({ML1,ML2})

    ps.add_transmission_network(tn)
    ps.add_distribution_network(dn)
    ps.add_microgrid_network(m)

    return ps

if __name__=="__main__":
    pass
