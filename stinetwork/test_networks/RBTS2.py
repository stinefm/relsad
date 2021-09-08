from stinetwork.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    Battery,
    Production,
    ManualMainController,
    Sensor,
    Router,
)
from stinetwork.network.systems import Distribution, PowerSystem, Transmission
from stinetwork.visualization.plotting import plot_topology
from stinetwork.utils import (
    Time,
    TimeUnit,
)


def initialize_network():
    C1 = ManualMainController(name="C1", section_time=Time(1, TimeUnit.HOUR))

    ps = PowerSystem(C1)
    fail_rate_trafo = 0.0150  # 0.008
    fail_rate_line = 0.0650  # 0.08
    outage_time_line = Time(6, TimeUnit.HOUR)
    # repair_time_trafo = 200
    outage_time_trafo = Time(200, TimeUnit.HOUR)
    rho = 1.72e-8
    a = 64.52e-6
    l1 = 0.6  # km
    l2 = 0.75  # km
    l3 = 0.8  # km

    r1 = (rho * l1) / a * 1e3
    r2 = (rho * l2) / a * 1e3
    r3 = (rho * l3) / a * 1e3

    B0 = Bus(
        "B0",
        n_customers=0,
        coordinate=[0, 0],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )

    BF11 = Bus(
        "BF11",
        n_customers=0,
        coordinate=[-4, -1],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B1 = Bus(
        "B1",
        n_customers=210,
        coordinate=[-5, -2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B2 = Bus(
        "B2",
        n_customers=210,
        coordinate=[-5, -3],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF12 = Bus(
        "BF12",
        n_customers=0,
        coordinate=[-4, -4],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B3 = Bus(
        "B3",
        n_customers=210,
        coordinate=[-5, -5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B4 = Bus(
        "B4",
        n_customers=1,
        coordinate=[-5, -6],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF13 = Bus(
        "BF13",
        n_customers=0,
        coordinate=[-4, -7],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B5 = Bus(
        "B5",
        n_customers=1,
        coordinate=[-5, -8],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B6 = Bus(
        "B6",
        n_customers=10,
        coordinate=[-5, -9],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF14 = Bus(
        "BF14",
        n_customers=0,
        coordinate=[-4, -10],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B7 = Bus(
        "B7",
        n_customers=10,
        coordinate=[-5, -11],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )

    B8 = Bus(
        "B8",
        n_customers=1,
        coordinate=[-3, -2],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    BF21 = Bus(
        "BF21",
        n_customers=0,
        coordinate=[-2, -1],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    BF22 = Bus(
        "BF22",
        n_customers=0,
        coordinate=[-2, -3],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B9 = Bus(
        "B9",
        n_customers=1,
        coordinate=[-3, -4],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )

    BF31 = Bus(
        "BF31",
        n_customers=0,
        coordinate=[2, -1],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B10 = Bus(
        "B10",
        n_customers=210,
        coordinate=[3, -2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B11 = Bus(
        "B11",
        n_customers=210,
        coordinate=[3, -3],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF32 = Bus(
        "BF32",
        n_customers=0,
        coordinate=[2, -4],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B12 = Bus(
        "B12",
        n_customers=200,
        coordinate=[3, -5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B13 = Bus(
        "B13",
        n_customers=1,
        coordinate=[3, -6],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF33 = Bus(
        "BF33",
        n_customers=0,
        coordinate=[2, -7],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B14 = Bus(
        "B14",
        n_customers=1,
        coordinate=[3, -8],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF34 = Bus(
        "BF34",
        n_customers=0,
        coordinate=[2, -9],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B15 = Bus(
        "B15",
        n_customers=10,
        coordinate=[3, -10],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )

    BF41 = Bus(
        "BF41",
        n_customers=0,
        coordinate=[4, -1],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B16 = Bus(
        "B16",
        n_customers=10,
        coordinate=[5, -2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B17 = Bus(
        "B17",
        n_customers=200,
        coordinate=[5, -3],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF42 = Bus(
        "BF42",
        n_customers=0,
        coordinate=[4, -4],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B18 = Bus(
        "B18",
        n_customers=200,
        coordinate=[5, -5],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B19 = Bus(
        "B19",
        n_customers=200,
        coordinate=[5, -6],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF43 = Bus(
        "BF43",
        n_customers=0,
        coordinate=[4, -7],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B20 = Bus(
        "B20",
        n_customers=1,
        coordinate=[5, -8],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B21 = Bus(
        "B21",
        n_customers=1,
        coordinate=[5, -9],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    BF44 = Bus(
        "BF44",
        n_customers=0,
        coordinate=[4, -10],
        fail_rate_per_year=0,
        outage_time=outage_time_trafo,
    )
    B22 = Bus(
        "B22",
        n_customers=10,
        coordinate=[5, -11],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )

    L1 = Line(
        "L1",
        B0,
        BF11,
        r=r2,
        x=0.156669594992563,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L2 = Line(
        "L2",
        BF11,
        B1,
        r=r1,
        x=0.156669594992563,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L3 = Line(
        "L3",
        BF11,
        B2,
        r=r3,
        x=0.11630112507612,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L4 = Line(
        "L4",
        BF11,
        BF12,
        r=r2,
        x=0.121105409749329,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L5 = Line(
        "L5",
        BF12,
        B3,
        r=r3,
        x=0.441120683630991,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L6 = Line(
        "L6",
        BF12,
        B4,
        r=r1,
        x=0.386089786465145,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L7 = Line(
        "L7",
        BF12,
        BF13,
        r=r2,
        x=0.770619740244183,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L8 = Line(
        "L8",
        BF13,
        B5,
        r=r3,
        x=0.4617104750876,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L9 = Line(
        "L9",
        BF13,
        B6,
        r=r2,
        x=0.4617104750876,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L10 = Line(
        "L10",
        BF13,
        BF14,
        r=r1,
        x=0.040555649838776,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L11 = Line(
        "L11",
        BF14,
        B7,
        r=r3,
        x=0.077242914616007,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    LB1 = Line(
        "LB1",
        BF14,
        BF22,
        r=r1,
        x=0.077242914616007,
        fail_rate_density_per_year=0,
        outage_time=outage_time_line,
    )

    L12 = Line(
        "L12",
        B0,
        BF21,
        r=r2,
        x=0.720642700981322,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )

    L13 = Line(
        "L13",
        BF21,
        B8,
        r=r3,
        x=0.444801888770203,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L14 = Line(
        "L14",
        BF21,
        BF22,
        r=r1,
        x=0.328188797156862,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L15 = Line(
        "L15",
        BF22,
        B9,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )

    L16 = Line(
        "L16",
        B0,
        BF31,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L17 = Line(
        "L17",
        BF31,
        B10,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L18 = Line(
        "L18",
        BF31,
        BF32,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L19 = Line(
        "L19",
        BF31,
        B11,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L20 = Line(
        "L20",
        BF32,
        B12,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L21 = Line(
        "L21",
        BF32,
        BF33,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L22 = Line(
        "L22",
        BF33,
        B13,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L23 = Line(
        "L23",
        BF33,
        B14,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L24 = Line(
        "L24",
        BF33,
        BF34,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L25 = Line(
        "L25",
        BF34,
        B15,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    LB2 = Line(
        "LB2",
        BF34,
        BF44,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=0,
        outage_time=outage_time_line,
    )

    L26 = Line(
        "L26",
        B0,
        BF41,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L27 = Line(
        "L27",
        BF41,
        B16,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L28 = Line(
        "L28",
        BF41,
        B17,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L29 = Line(
        "L29",
        BF41,
        BF42,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L30 = Line(
        "L30",
        BF42,
        B18,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L31 = Line(
        "L31",
        BF42,
        B19,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L32 = Line(
        "L32",
        BF42,
        BF43,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L33 = Line(
        "L33",
        BF43,
        B20,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L34 = Line(
        "L34",
        BF43,
        BF44,
        r=r1,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L35 = Line(
        "L35",
        BF44,
        B21,
        r=r2,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L36 = Line(
        "L36",
        BF44,
        B22,
        r=r3,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )

    E1 = CircuitBreaker("E1", L1)
    E2 = CircuitBreaker("E2", L12)
    E3 = CircuitBreaker("E3", L16)
    E4 = CircuitBreaker("E4", L26)

    Disconnector("DL1a", L1, B0, E1)
    Disconnector("DL1b", L1, BF11, E1)
    Disconnector("DL4", L4, BF11)
    Disconnector("DL7", L7, BF12)
    Disconnector("DL10", L10, BF13)
    Disconnector("DLB1a", LB1, BF14)

    Disconnector("DL12a", L12, B0, E2)
    Disconnector("DL12b", L12, BF21, E2)
    Disconnector("DL14", L14, BF21)
    Disconnector("DLB1b", LB1, BF22)

    Disconnector("DL16a", L16, B0, E3)
    Disconnector("DL16b", L16, BF31, E3)
    Disconnector("DL18", L18, BF31)
    Disconnector("DL21", L21, BF32)
    Disconnector("DL24", L24, BF33)
    Disconnector("DLB2a", LB2, BF34)

    Disconnector("DL26a", L26, B0, E4)
    Disconnector("DL26b", L26, BF41, E4)
    Disconnector("DL29", L29, BF41)
    Disconnector("DL32", L32, BF42)
    Disconnector("DL34", L34, BF43)
    Disconnector("DLB2b", LB2, BF44)

    LB1.set_backup()
    LB2.set_backup()

    tn = Transmission(ps, B0)

    dn1 = Distribution(tn, L1)
    dn2 = Distribution(tn, L12)
    dn3 = Distribution(tn, L16)
    dn4 = Distribution(tn, L26)

    dn1.add_buses(
        [
            B0,
            BF11,
            B1,
            B2,
            BF12,
            B3,
            B4,
            BF13,
            B5,
            B6,
            BF14,
            B7,
        ]
    )
    dn2.add_buses(
        [
            BF21,
            B8,
            BF22,
            B9,
        ]
    )
    dn3.add_buses(
        [
            BF31,
            B10,
            BF32,
            B11,
            B12,
            BF33,
            B13,
            B14,
            BF34,
            B15,
        ]
    )

    dn4.add_buses(
        [
            BF41,
            B16,
            B17,
            BF42,
            B18,
            B19,
            BF43,
            B20,
            BF44,
            B21,
            B22,
        ]
    )

    dn1.add_lines(
        [
            L1,
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
            LB1,
        ]
    )
    dn2.add_lines(
        [
            L12,
            L13,
            L14,
            L15,
            LB1,
        ]
    )
    dn3.add_lines(
        [
            L16,
            L17,
            L18,
            L19,
            L20,
            L21,
            L22,
            L23,
            L24,
            L25,
            LB2,
        ]
    )
    dn4.add_lines(
        [
            L26,
            L27,
            L28,
            L29,
            L30,
            L31,
            L32,
            L33,
            L34,
            L35,
            L36,
            LB2,
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
            "RBTS2_testnetwork.pdf",
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
