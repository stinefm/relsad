from stinetwork.network.components import (
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
)
from stinetwork.network.systems import Distribution, PowerSystem, Transmission
from stinetwork.visualization.plotting import plot_topology


def initialize_network():
    ps = PowerSystem()
    fail_rate_trafo = 0.007  # 0.008
    fail_rate_line = 0.07  # 0.08

    B1 = Bus("B1", coordinate=[0, 0], fail_rate_per_year=0)
    B2 = Bus("B2", coordinate=[0, -1], fail_rate_per_year=fail_rate_trafo)
    B3 = Bus("B3", coordinate=[0, -2], fail_rate_per_year=fail_rate_trafo)
    B4 = Bus("B4", coordinate=[0, -3], fail_rate_per_year=fail_rate_trafo)
    B5 = Bus("B5", coordinate=[0, -4], fail_rate_per_year=fail_rate_trafo)
    B6 = Bus("B6", coordinate=[0, -5], fail_rate_per_year=fail_rate_trafo)
    B7 = Bus("B7", coordinate=[0, -6], fail_rate_per_year=fail_rate_trafo)
    B8 = Bus("B8", coordinate=[0, -7], fail_rate_per_year=fail_rate_trafo)
    B9 = Bus("B9", coordinate=[0, -8], fail_rate_per_year=fail_rate_trafo)
    B10 = Bus("B10", coordinate=[0, -9], fail_rate_per_year=fail_rate_trafo)
    B11 = Bus("B11", coordinate=[0, -10], fail_rate_per_year=fail_rate_trafo)
    B12 = Bus("B12", coordinate=[0, -11], fail_rate_per_year=fail_rate_trafo)
    B13 = Bus("B13", coordinate=[0, -12], fail_rate_per_year=fail_rate_trafo)
    B14 = Bus("B14", coordinate=[0, -13], fail_rate_per_year=fail_rate_trafo)
    B15 = Bus("B15", coordinate=[0, -14], fail_rate_per_year=fail_rate_trafo)
    B16 = Bus("B16", coordinate=[0, -15], fail_rate_per_year=fail_rate_trafo)
    B17 = Bus("B17", coordinate=[0, -16], fail_rate_per_year=fail_rate_trafo)
    B18 = Bus("B18", coordinate=[0, -17], fail_rate_per_year=fail_rate_trafo)
    B19 = Bus("B19", coordinate=[-1, -2], fail_rate_per_year=fail_rate_trafo)
    B20 = Bus("B20", coordinate=[-1, -3], fail_rate_per_year=fail_rate_trafo)
    B21 = Bus("B21", coordinate=[-1, -4], fail_rate_per_year=fail_rate_trafo)
    B22 = Bus("B22", coordinate=[-1, -5], fail_rate_per_year=fail_rate_trafo)
    B23 = Bus("B23", coordinate=[1, -3], fail_rate_per_year=fail_rate_trafo)
    B24 = Bus("B24", coordinate=[1, -4], fail_rate_per_year=fail_rate_trafo)
    B25 = Bus("B25", coordinate=[1, -5], fail_rate_per_year=fail_rate_trafo)
    B26 = Bus("B26", coordinate=[-1, -6], fail_rate_per_year=fail_rate_trafo)
    B27 = Bus("B27", coordinate=[-1, -7], fail_rate_per_year=fail_rate_trafo)
    B28 = Bus("B28", coordinate=[-1, -8], fail_rate_per_year=fail_rate_trafo)
    B29 = Bus("B29", coordinate=[-1, -9], fail_rate_per_year=fail_rate_trafo)
    B30 = Bus("B30", coordinate=[-1, -10], fail_rate_per_year=fail_rate_trafo)
    B31 = Bus("B31", coordinate=[-1, -11], fail_rate_per_year=fail_rate_trafo)
    B32 = Bus("B32", coordinate=[-1, -12], fail_rate_per_year=fail_rate_trafo)
    B33 = Bus("B33", coordinate=[-1, -13], fail_rate_per_year=fail_rate_trafo)

    L1 = Line(
        "L1",
        B1,
        B2,
        r=0.0922,
        x=0.0470,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B2,
        B3,
        r=0.4930,
        x=0.2511,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B3,
        B4,
        r=0.3660,
        x=0.1864,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        r=0.3811,
        x=0.1941,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B5,
        B6,
        r=0.8190,
        x=0.7070,
        fail_rate_density_per_year=fail_rate_line,
    )
    L6 = Line(
        "L6",
        B6,
        B7,
        r=0.1872,
        x=0.6188,
        fail_rate_density_per_year=fail_rate_line,
    )
    L7 = Line(
        "L7",
        B7,
        B8,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L8 = Line(
        "L8",
        B8,
        B9,
        r=1.0300,
        x=0.7400,
        fail_rate_density_per_year=fail_rate_line,
    )
    L9 = Line(
        "L9",
        B9,
        B10,
        r=1.0440,
        x=0.7400,
        fail_rate_density_per_year=fail_rate_line,
    )
    L10 = Line(
        "L10",
        B10,
        B11,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
    )
    L11 = Line(
        "L11",
        B11,
        B12,
        r=0.3744,
        x=0.1238,
        fail_rate_density_per_year=fail_rate_line,
    )
    L12 = Line(
        "L12",
        B12,
        B13,
        r=1.4680,
        x=1.1550,
        fail_rate_density_per_year=fail_rate_line,
    )
    L13 = Line(
        "L13",
        B13,
        B14,
        r=0.5416,
        x=0.7129,
        fail_rate_density_per_year=fail_rate_line,
    )
    L14 = Line(
        "L14",
        B14,
        B15,
        r=0.5910,
        x=0.5260,
        fail_rate_density_per_year=fail_rate_line,
    )
    L15 = Line(
        "L15",
        B15,
        B16,
        r=0.7463,
        x=0.5450,
        fail_rate_density_per_year=fail_rate_line,
    )
    L16 = Line(
        "L16",
        B16,
        B17,
        r=1.2890,
        x=1.72010,
        fail_rate_density_per_year=fail_rate_line,
    )
    L17 = Line(
        "L17",
        B17,
        B18,
        r=0.7320,
        x=0.5740,
        fail_rate_density_per_year=fail_rate_line,
    )
    L18 = Line(
        "L18",
        B2,
        B19,
        r=0.1640,
        x=0.1565,
        fail_rate_density_per_year=fail_rate_line,
    )
    L19 = Line(
        "L19",
        B19,
        B20,
        r=1.5042,
        x=1.3554,
        fail_rate_density_per_year=fail_rate_line,
    )
    L20 = Line(
        "L20",
        B20,
        B21,
        r=0.4095,
        x=0.4784,
        fail_rate_density_per_year=fail_rate_line,
    )
    L21 = Line(
        "L21",
        B21,
        B22,
        r=0.7089,
        x=0.9373,
        fail_rate_density_per_year=fail_rate_line,
    )
    L22 = Line(
        "L22",
        B3,
        B23,
        r=0.4512,
        x=0.3083,
        fail_rate_density_per_year=fail_rate_line,
    )
    L23 = Line(
        "L23",
        B23,
        B24,
        r=0.8980,
        x=0.7091,
        fail_rate_density_per_year=fail_rate_line,
    )
    L24 = Line(
        "L24",
        B24,
        B25,
        r=0.8960,
        x=0.7011,
        fail_rate_density_per_year=fail_rate_line,
    )
    L25 = Line(
        "L25",
        B6,
        B26,
        r=0.2030,
        x=0.1034,
        fail_rate_density_per_year=fail_rate_line,
    )
    L26 = Line(
        "L26",
        B26,
        B27,
        r=0.2842,
        x=0.1447,
        fail_rate_density_per_year=fail_rate_line,
    )
    L27 = Line(
        "L27",
        B27,
        B28,
        r=1.0590,
        x=0.9337,
        fail_rate_density_per_year=fail_rate_line,
    )
    L28 = Line(
        "L28",
        B28,
        B29,
        r=0.8042,
        x=0.7006,
        fail_rate_density_per_year=fail_rate_line,
    )
    L29 = Line(
        "L29",
        B29,
        B30,
        r=0.5075,
        x=0.2585,
        fail_rate_density_per_year=fail_rate_line,
    )
    L30 = Line(
        "L30",
        B30,
        B31,
        r=0.9744,
        x=0.9630,
        fail_rate_density_per_year=fail_rate_line,
    )
    L31 = Line(
        "L31",
        B31,
        B32,
        r=0.3105,
        x=0.3619,
        fail_rate_density_per_year=fail_rate_line,
    )
    L32 = Line(
        "L32",
        B32,
        B33,
        r=0.3410,
        x=0.5320,
        fail_rate_density_per_year=fail_rate_line,
    )

    # Backup lines

    # L33 = Line(
    #     "L33",
    #     B9,
    #     B15,
    #     r=2.0000,
    #     x=2.0000,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    # L34 = Line(
    #     "L34",
    #     B12,
    #     B22,
    #     r=2.0000,
    #     x=2.0000,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    # L35 = Line(
    #     "L35",
    #     B18,
    #     B33,
    #     r=0.5000,
    #     x=0.5000,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    # L36 = Line(
    #     "L36",
    #     B25,
    #     B29,
    #     r=0.5000,
    #     x=0.5000,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    # L37 = Line(
    #     "L37",
    #     B8,
    #     B21,
    #     r=2.0000,
    #     x=2.0000,
    #     fail_rate_density_per_year=fail_rate_line,
    # )

    E1 = CircuitBreaker("E1", L1)

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
    Disconnector("L16a", L16, B16)
    Disconnector("L16b", L16, B17)
    Disconnector("L17a", L17, B17)
    Disconnector("L17b", L17, B18)

    Disconnector("L18a", L18, B2)
    Disconnector("L18b", L18, B19)
    Disconnector("L19a", L19, B19)
    Disconnector("L19b", L19, B20)
    Disconnector("L20a", L20, B20)
    Disconnector("L20b", L20, B21)
    Disconnector("L21a", L21, B21)
    Disconnector("L21b", L21, B22)

    Disconnector("L22a", L22, B3)
    Disconnector("L22b", L22, B23)
    Disconnector("L23a", L23, B23)
    Disconnector("L23b", L23, B24)
    Disconnector("L24a", L24, B24)
    Disconnector("L24b", L24, B25)

    Disconnector("L25a", L25, B6)
    Disconnector("L25b", L25, B26)
    Disconnector("L26a", L26, B26)
    Disconnector("L26b", L26, B27)
    Disconnector("L27a", L27, B27)
    Disconnector("L27b", L27, B28)
    Disconnector("L28a", L28, B28)
    Disconnector("L28b", L28, B29)
    Disconnector("L29a", L29, B29)
    Disconnector("L29b", L29, B30)
    Disconnector("L30a", L30, B30)
    Disconnector("L30b", L30, B31)
    Disconnector("L31a", L31, B31)
    Disconnector("L31b", L31, B32)
    Disconnector("L32a", L32, B32)
    Disconnector("L32b", L32, B33)

    # # Backup
    # Disconnector("L33a", L33, B9)
    # Disconnector("L33b", L33, B15)
    # Disconnector("L34a", L34, B12)
    # Disconnector("L34b", L34, B22)
    # Disconnector("L35a", L35, B18)
    # Disconnector("L35b", L35, B33)
    # Disconnector("L36a", L36, B25)
    # Disconnector("L36b", L36, B29)
    # Disconnector("L37a", L37, B8)
    # Disconnector("L37b", L37, B21)

    # L33.set_backup()
    # L34.set_backup()
    # L35.set_backup()
    # L36.set_backup()
    # L37.set_backup()

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
            B17,
            B18,
            B19,
            B20,
            B21,
            B22,
            B23,
            B24,
            B25,
            B26,
            B27,
            B28,
            B29,
            B30,
            B31,
            B32,
            B33,
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
            L26,
            L27,
            L28,
            L29,
            L30,
            L31,
            L32,
            # L33,
            # L34,
            # L35,
            # L36,
            # L37,
        ]
    )

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines, figsize=(40, 40))

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "IEEE33_testnetwork.pdf",
        )
    )
