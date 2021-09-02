import os
from stinetwork.visualization.plotting import plot_topology
from stinetwork.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    Battery,
    Production,
    MainController,
    Sensor,
    Router,
)
from stinetwork.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
    Microgrid,
)


def initialize_network():
    C1 = MainController("C1")

    ps = PowerSystem(C1)

    ## Transmission network
    T = Bus("T", n_customers=0, coordinate=[0, 0], fail_rate_per_year=0)

    fail_rate_trafo = 0.007
    fail_rate_line = 0.07

    ## Distribution network
    B1 = Bus(
        "B1",
        n_customers=1,
        coordinate=[0, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B2 = Bus(
        "B2",
        n_customers=100,
        coordinate=[1, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B3 = Bus(
        "B3",
        n_customers=50,
        coordinate=[0, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B4 = Bus(
        "B4",
        n_customers=90,
        coordinate=[0, -3],
        fail_rate_per_year=fail_rate_trafo,
    )
    B5 = Bus(
        "B5",
        n_customers=3,
        coordinate=[1, -3],
        fail_rate_per_year=fail_rate_trafo,
    )

    ## Microgridn_customers=,
    M1 = Bus(
        "M1",
        n_customers=0,
        coordinate=[-1, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    M2 = Bus(
        "M2",
        n_customers=0,
        coordinate=[-2, -3],
        fail_rate_per_year=fail_rate_trafo,
    )
    M3 = Bus(
        "M3",
        n_customers=40,
        coordinate=[-1, -3],
        fail_rate_per_year=fail_rate_trafo,
    )

    Battery("Bat1", M1)
    Production("P1", M2)

    L1 = Line(
        "L1",
        T,
        B1,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B1,
        B2,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B1,
        B3,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B3,
        B4,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B2,
        B5,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L6 = Line(
        "L6",
        B3,
        B5,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        capacity=6,
    )
    L7 = Line(
        "L7",
        B1,
        M1,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )
    ML1 = Line(
        "ML1",
        M1,
        M2,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )
    ML2 = Line(
        "ML2",
        M1,
        M3,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )

    E1 = CircuitBreaker("E1", L1)
    E2 = CircuitBreaker("E2", L7)

    DL1a = Disconnector("L1a", L1, T, E1)
    DL1b = Disconnector("L1b", L1, B1, E1)
    DL1c = Disconnector("L1c", L1, B1)
    DL2a = Disconnector("L2a", L2, B1)
    DL2b = Disconnector("L2b", L2, B2)
    DL3a = Disconnector("L3a", L3, B1)
    DL3b = Disconnector("L3b", L3, B3)
    DL4a = Disconnector("L4a", L4, B3)
    DL4b = Disconnector("L4b", L4, B4)
    DL5a = Disconnector("L5a", L5, B2)
    DL5b = Disconnector("L5b", L5, B5)
    DL6a = Disconnector("L6a", L6, B3)
    DL6b = Disconnector("L6b", L6, B5)
    DL7a = Disconnector("L7a", L7, B1, E2)
    DL7b = Disconnector("L7b", L7, M1, E2)
    DL7c = Disconnector("L7c", L7, M1)

    DML1a = Disconnector("ML1a", ML1, M1)
    DML1b = Disconnector("ML1b", ML1, M2)
    DML2a = Disconnector("ML2a", ML2, M1)
    DML2b = Disconnector("ML2b", ML2, M3)

    Sensor("SL1", L1)
    Sensor("SL2", L2)
    Sensor("SL3", L3)
    Sensor("SL4", L4)
    Sensor("SL5", L5)
    Sensor("SL6", L6)
    Sensor("SL7", L7)

    Sensor("SML1", ML1)
    Sensor("SML2", ML2)

    Router("RL1a", DL1a)
    Router("RL1b", DL1b)
    Router("RL1c", DL1c)
    Router("RL2a", DL2a)
    Router("RL2b", DL2b)
    Router("RL3a", DL3a)
    Router("RL3b", DL3b)
    Router("RL4a", DL4a)
    Router("RL4b", DL4b)
    Router("RL5a", DL5a)
    Router("RL5b", DL5b)
    Router("RL6a", DL6a)
    Router("RL6b", DL6b)
    Router("RL7a", DL7a)
    Router("RL7b", DL7b)
    Router("RL7c", DL7c)

    Router("RML1a", DML1a)
    Router("RML1b", DML1b)
    Router("RML2a", DML2a)
    Router("RML2b", DML2b)

    L6.set_backup()

    tn = Transmission(ps, T)

    dn = Distribution(tn, L1)

    dn.add_buses([B1, B2, B3, B4, B5])
    dn.add_lines([L2, L3, L4, L5, L6])

    m = Microgrid(dn, L7, mode="survival")

    m.add_buses([M1, M2, M3])
    m.add_lines([ML1, ML2])

    return ps


if __name__ == "__main__":
    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "CINELDI_testnetwork.pdf",
        )
    )

    # def print_sections(section, level=0):
    #     print("\nSection: (level {})".format(level))
    #     print("Lines: ", section.comp_list)
    #     print("Disconnectors: ", section.disconnectors)
    #     level += 1
    #     for child_section in section.child_sections:
    #         print_sections(child_section, level)

    # for network in ps.child_network_list:
    #     print("\n\n", network)
    #     if not isinstance(network, Transmission):
    #         parent_section = create_sections(network.connected_line)
    #         print_sections(parent_section)
