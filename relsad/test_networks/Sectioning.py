from relsad.network.components import (
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
    Battery,
    Production,
    MicrogridMode,
)
from relsad.network.systems import (
    Distribution,
    PowerSystem,
    Transmission,
    Microgrid,
)
from relsad.visualization.plotting import plot_topology


def initialize_network():
    ps = PowerSystem()

    fail_rate_trafo = 0.007  # fails per year
    fail_rate_line = 0.07  # fails per year
    outage_time_trafo = 8  # hours
    outage_time_line = 4  # hours
    # battery_capacity = 1  # MWh
    # microgrid_mode = MicrogridMode.LIMITED_SUPPORT

    B1 = Bus("B1", n_customers=0, coordinate=[0, 0], fail_rate_per_year=0)
    B2 = Bus(
        "B2",
        n_customers=1,
        coordinate=[1, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B3 = Bus(
        "B3",
        n_customers=39,
        coordinate=[2, 2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B4 = Bus(
        "B4",
        n_customers=1,
        coordinate=[3, 2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B5 = Bus(
        "B5",
        n_customers=26,
        coordinate=[4, 2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B6 = Bus(
        "B6",
        n_customers=26,
        coordinate=[2, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B7 = Bus(
        "B7",
        n_customers=1,
        coordinate=[3, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B8 = Bus(
        "B8",
        n_customers=1,
        coordinate=[4, 1.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B9 = Bus(
        "B9",
        n_customers=26,
        coordinate=[5, 1.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B10 = Bus(
        "B10",
        n_customers=26,
        coordinate=[6, 2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B11 = Bus(
        "B11",
        n_customers=19,
        coordinate=[7, 2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B12 = Bus(
        "B12",
        n_customers=26,
        coordinate=[8, 2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B13 = Bus(
        "B13",
        n_customers=26,
        coordinate=[6, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B14 = Bus(
        "B14",
        n_customers=1,
        coordinate=[7, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B15 = Bus(
        "B15",
        n_customers=26,
        coordinate=[8, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B16 = Bus(
        "B16",
        n_customers=26,
        coordinate=[4, 0.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B17 = Bus(
        "B17",
        n_customers=26,
        coordinate=[5, 0.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B18 = Bus(
        "B18",
        n_customers=39,
        coordinate=[6, 0.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B19 = Bus(
        "B19",
        n_customers=39,
        coordinate=[7, 0.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B20 = Bus(
        "B20",
        n_customers=39,
        coordinate=[2, 0.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B21 = Bus(
        "B21",
        n_customers=39,
        coordinate=[3, 0.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B22 = Bus(
        "B22",
        n_customers=39,
        coordinate=[1, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B23 = Bus(
        "B23",
        n_customers=39,
        coordinate=[2, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B24 = Bus(
        "B24",
        n_customers=2,
        coordinate=[3, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B25 = Bus(
        "B25",
        n_customers=2,
        coordinate=[4, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B26 = Bus(
        "B26",
        n_customers=26,
        coordinate=[5, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B27 = Bus(
        "B27",
        n_customers=26,
        coordinate=[1, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B28 = Bus(
        "B28",
        n_customers=26,
        coordinate=[2, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B29 = Bus(
        "B29",
        n_customers=1,
        coordinate=[3, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B30 = Bus(
        "B30",
        n_customers=1,
        coordinate=[4, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B31 = Bus(
        "B31",
        n_customers=1,
        coordinate=[5, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B32 = Bus(
        "B32",
        n_customers=1,
        coordinate=[3, -1.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B33 = Bus(
        "B33",
        n_customers=26,
        coordinate=[4, -1.5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )

    L1 = Line(
        "L1",
        B1,
        B2,
        r=0.0922,
        x=0.0470,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L2 = Line(
        "L2",
        B2,
        B3,
        r=0.4930,
        x=0.2511,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L3 = Line(
        "L3",
        B3,
        B4,
        r=0.3660,
        x=0.1864,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        r=0.3811,
        x=0.1941,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L5 = Line(
        "L5",
        B2,
        B6,
        r=0.8190,
        x=0.7070,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L6 = Line(
        "L6",
        B6,
        B7,
        r=0.1872,
        x=0.6188,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L7 = Line(
        "L7",
        B7,
        B8,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L8 = Line(
        "L8",
        B8,
        B9,
        r=1.0300,
        x=0.7400,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L9 = Line(
        "L9",
        B9,
        B10,
        r=1.0440,
        x=0.7400,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L10 = Line(
        "L10",
        B10,
        B11,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L11 = Line(
        "L11",
        B11,
        B12,
        r=0.3744,
        x=0.1238,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L12 = Line(
        "L12",
        B9,
        B13,
        r=1.4680,
        x=1.1550,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L13 = Line(
        "L13",
        B13,
        B14,
        r=0.5416,
        x=0.7129,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L14 = Line(
        "L14",
        B14,
        B15,
        r=0.5910,
        x=0.5260,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L15 = Line(
        "L15",
        B7,
        B16,
        r=0.7463,
        x=0.5450,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L16 = Line(
        "L16",
        B16,
        B17,
        r=1.2890,
        x=1.72010,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L17 = Line(
        "L17",
        B17,
        B18,
        r=0.7320,
        x=0.5740,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L18 = Line(
        "L18",
        B18,
        B19,
        r=0.1640,
        x=0.1565,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L19 = Line(
        "L19",
        B2,
        B20,
        r=1.5042,
        x=1.3554,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L20 = Line(
        "L20",
        B20,
        B21,
        r=0.4095,
        x=0.4784,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L21 = Line(
        "L21",
        B1,
        B22,
        r=0.7089,
        x=0.9373,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L22 = Line(
        "L22",
        B22,
        B23,
        r=0.4512,
        x=0.3083,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L23 = Line(
        "L23",
        B23,
        B24,
        r=0.8980,
        x=0.7091,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L24 = Line(
        "L24",
        B24,
        B25,
        r=0.8960,
        x=0.7011,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L25 = Line(
        "L25",
        B25,
        B26,
        r=0.2030,
        x=0.1034,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L26 = Line(
        "L26",
        B1,
        B27,
        r=0.2842,
        x=0.1447,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L27 = Line(
        "L27",
        B27,
        B28,
        r=1.0590,
        x=0.9337,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L28 = Line(
        "L28",
        B28,
        B29,
        r=0.8042,
        x=0.7006,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L29 = Line(
        "L29",
        B29,
        B30,
        r=0.5075,
        x=0.2585,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L30 = Line(
        "L30",
        B30,
        B31,
        r=0.9744,
        x=0.9630,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L31 = Line(
        "L31",
        B28,
        B32,
        r=0.3105,
        x=0.3619,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L32 = Line(
        "L32",
        B32,
        B33,
        r=0.3410,
        x=0.5320,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )

    E1 = CircuitBreaker("E1", L1)
    E2 = CircuitBreaker("E2", L21)
    E3 = CircuitBreaker("E3", L26)

    Disconnector("DL1a", L1, B1, E1)
    Disconnector("DL1b", L1, B2, E1)
    Disconnector("DL3", L3, B3)
    Disconnector("DL6", L6, B6)
    Disconnector("DL9", L9, B9)
    Disconnector("DL16", L16, B16)

    Disconnector("DL21a", L21, B1, E2)
    Disconnector("DL21b", L21, B22, E2)
    Disconnector("DL23a", L23, B23)
    Disconnector("DL23b", L23, B24)

    Disconnector("DL26a", L26, B1, E3)
    Disconnector("DL26b", L26, B27, E3)
    Disconnector("DL31", L31, B28)

    tn = Transmission(ps, B1)

    dn1 = Distribution(tn, L1)

    dn1.add_buses(
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
            B17,
            B18,
            B19,
            B20,
            B21,
        ]
    )
    dn2 = Distribution(tn, L21)

    dn2.add_buses(
        [
            B22,
            B23,
            B24,
            B25,
            B26,
        ]
    )
    dn3 = Distribution(tn, L26)

    dn3.add_buses(
        [
            B27,
            B28,
            B29,
            B30,
            B31,
            B32,
            B33,
        ]
    )

    dn1.add_lines(
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
            L16,
            L17,
            L18,
            L19,
            L20,
        ]
    )
    dn2.add_lines(
        [
            L21,
            L22,
            L23,
            L24,
            L25,
        ]
    )
    dn3.add_lines(
        [
            L26,
            L27,
            L28,
            L29,
            L30,
            L31,
            L32,
        ]
    )

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_network()

    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "Sectioning_testnetwork.pdf",
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
