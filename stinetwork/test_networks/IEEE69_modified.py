from stinetwork.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    Battery,
    Production,
    MicrogridMode,
)
from stinetwork.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
    Microgrid,
)
from stinetwork.visualization.plotting import plot_topology


def initialize_network():
    ps = PowerSystem()
    fail_rate_trafo = 0.007  # 0.008
    fail_rate_line = 0.07  # 0.08

    B1 = Bus("B1", coordinate=[0, 0], fail_rate_per_year=0)
    B2 = Bus("B2", coordinate=[1, 0], fail_rate_per_year=fail_rate_trafo)
    B3 = Bus("B3", coordinate=[2, 0], fail_rate_per_year=fail_rate_trafo)
    B4 = Bus("B4", coordinate=[3, 0], fail_rate_per_year=fail_rate_trafo)
    B5 = Bus("B5", coordinate=[4, 0], fail_rate_per_year=fail_rate_trafo)
    B6 = Bus("B6", coordinate=[5, 0], fail_rate_per_year=fail_rate_trafo)
    B7 = Bus("B7", coordinate=[6, 0], fail_rate_per_year=fail_rate_trafo)
    B8 = Bus("B8", coordinate=[7, 0], fail_rate_per_year=fail_rate_trafo)
    B9 = Bus("B9", coordinate=[8, 0], fail_rate_per_year=fail_rate_trafo)
    B10 = Bus("B10", coordinate=[9, 0], fail_rate_per_year=fail_rate_trafo)
    B11 = Bus("B11", coordinate=[10, 0], fail_rate_per_year=fail_rate_trafo)
    B12 = Bus("B12", coordinate=[11, 0], fail_rate_per_year=fail_rate_trafo)
    B13 = Bus("B13", coordinate=[12, 0], fail_rate_per_year=fail_rate_trafo)
    B14 = Bus("B14", coordinate=[13, 0], fail_rate_per_year=fail_rate_trafo)
    B15 = Bus("B15", coordinate=[14, 0], fail_rate_per_year=fail_rate_trafo)
    B16 = Bus("B16", coordinate=[15, 0], fail_rate_per_year=fail_rate_trafo)

    # Microgrid:
    BM1 = Bus("BM1", coordinate=[13, 1.5], fail_rate_per_year=fail_rate_trafo)
    BM2 = Bus("BM2", coordinate=[14, 1.5], fail_rate_per_year=fail_rate_trafo)
    BM3 = Bus("BM3", coordinate=[14, 2], fail_rate_per_year=fail_rate_trafo)
    BM4 = Bus("BM4", coordinate=[14, 1], fail_rate_per_year=fail_rate_trafo)

    Battery("Bat1", BM1)
    Production("P1", BM3)
    Production("P2", BM4)

    # Lines, connections and impedances
    L1 = Line(
        "L1",
        B1,
        B2,
        r=0.0922,  # 0.3660,
        x=0.0470,  # 0.1864,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B2,
        B3,
        r=0.0922,  # 0.3811,
        x=0.0470,  # 0.1941,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B3,
        B4,
        r=0.0922,
        x=0.0470,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        r=0.0493,
        x=0.0251,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B5,
        B6,
        r=0.1872,  # 0.8190,
        x=0.0619,  # 0.2707,
        fail_rate_density_per_year=fail_rate_line,
    )
    L6 = Line(
        "L6",
        B6,
        B7,
        r=0.1872,
        x=0.0619,
        fail_rate_density_per_year=fail_rate_line,
    )
    L7 = Line(
        "L7",
        B7,
        B8,
        r=0.1872,  # 0.7114,
        x=0.0619,  # 0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L8 = Line(
        "L8",
        B8,
        B9,
        r=0.1872,  # 1.0300,
        x=0.0619,  # 0.3400,
        fail_rate_density_per_year=fail_rate_line,
    )
    L9 = Line(
        "L9",
        B9,
        B10,
        r=0.1872,  # 1.0440,
        x=0.0619,  # 0.3450,
        fail_rate_density_per_year=fail_rate_line,
    )
    L10 = Line(
        "L10",
        B10,
        B11,
        r=0.1872,  # 1.0580,
        x=0.0619,  # 0.3496,
        fail_rate_density_per_year=fail_rate_line,
    )
    L11 = Line(
        "L11",
        B11,
        B12,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
    )
    L12 = Line(
        "L12",
        B12,
        B13,
        r=0.1872,  # 1.0300,
        x=0.0619,  # 0.3400,
        fail_rate_density_per_year=fail_rate_line,
    )
    L13 = Line(
        "L13",
        B13,
        B14,
        r=0.1872,  # 1.0440,
        x=0.0619,  # 0.3450,
        fail_rate_density_per_year=fail_rate_line,
    )
    L14 = Line(
        "L14",
        B14,
        B15,
        r=0.1872,  # 1.0580,
        x=0.0619,  # 0.3496,
        fail_rate_density_per_year=fail_rate_line,
    )
    L15 = Line(
        "L15",
        B15,
        B16,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
    )

    # Microgrid

    ML1 = Line(
        "ML1",
        B13,
        BM1,
        r=0.1872,  # 0.7394,
        x=0.0619,  # 0.2444,
        fail_rate_density_per_year=fail_rate_line,
    )

    ML2 = Line(
        "ML2",
        BM1,
        BM2,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
    )
    ML3 = Line(
        "ML3",
        BM1,
        BM3,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
    )
    ML4 = Line(
        "ML4",
        BM1,
        BM4,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
    )

    E1 = CircuitBreaker("E1", L1)
    E2 = CircuitBreaker("E2", ML1)

    Disconnector("L1a", L1, B1, E1)
    Disconnector("L1b", L1, B2, E1)
    Disconnector("L1c", L1, B2)
    Disconnector("L2a", L2, B2)
    Disconnector("L2b", L2, B3)
    Disconnector("L3a", L3, B3)
    Disconnector("L3b", L3, B4)
    Disconnector("L4a", L4, B4)
    Disconnector("L4b", L4, B5)
    Disconnector("L5a", L5, B5)
    Disconnector("L5b", L5, B6)
    Disconnector("L6a", L6, B6)
    Disconnector("L6b", L6, B7)
    Disconnector("L7a", L7, B7)
    Disconnector("L7b", L7, B8)
    Disconnector("L8a", L8, B8)
    Disconnector("L8b", L8, B9)
    Disconnector("L9a", L9, B9)
    Disconnector("L9b", L9, B10)
    Disconnector("L10a", L10, B10)
    Disconnector("L10b", L10, B11)
    Disconnector("L11a", L11, B11)
    Disconnector("L11b", L11, B12)
    Disconnector("L12a", L12, B12)
    Disconnector("L12b", L12, B13)
    Disconnector("L13a", L13, B13)
    Disconnector("L13b", L13, B14)
    Disconnector("L14a", L14, B14)
    Disconnector("L14b", L14, B15)
    Disconnector("L15a", L15, B15)
    Disconnector("L15b", L15, B16)

    # Microgrid:

    Disconnector("ML1a", ML1, B13, E2)
    Disconnector("ML1b", ML1, BM1, E2)
    Disconnector("ML1c", ML1, BM1)
    Disconnector("ML2a", ML2, BM1)
    Disconnector("ML2b", ML2, BM2)
    Disconnector("ML3a", ML3, BM1)
    Disconnector("ML3b", ML3, BM3)
    Disconnector("ML4a", ML4, BM1)
    Disconnector("ML4b", ML4, BM4)

    tn = Transmission(ps, B1)

    dn = Distribution(tn, L1)

    dn.add_buses(
        [
            B2,
            B3,
            B4,
            B5,
            B6,
            B7,
            B8,
            B9,
            B10,
            B11,
            B12,
            B13,
            B14,
            B15,
            B16,
        ]
    )

    dn.add_lines(
        [
            L2,
            L3,
            L4,
            L5,
            L6,
            L7,
            L8,
            L9,
            L10,
            L11,
            L12,
            L13,
            L14,
            L15,
        ]
    )

    m = Microgrid(dn, ML1, mode=MicrogridMode.FULL_SUPPORT)
    m.add_buses([BM1, BM2, BM3, BM4])
    m.add_lines([ML2, ML3, ML4])

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test69modified.pdf"
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
