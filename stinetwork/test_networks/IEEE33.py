from stinetwork.network.components import (
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
    Battery,
    Production,
    MainController,
    ManualMainController,
    Sensor,
    IntelligentSwitch,
    MicrogridMode,
)
from stinetwork.network.systems import (
    Distribution,
    PowerSystem,
    Transmission,
    Microgrid,
)
from stinetwork.visualization.plotting import plot_topology
from stinetwork.utils import (
    Time,
    TimeUnit,
)


def initialize_network():

    include_microgrid = True
    include_production = True
    include_ICT = True

    if include_ICT:
        C1 = MainController(
            name="C1",
        )
    else:
        C1 = ManualMainController(
            name="C1",
            section_time=Time(1, TimeUnit.HOUR),
        )

    ps = PowerSystem(C1)

    fail_rate_trafo = 0.007  # fails per year
    fail_rate_line = 0.07  # fails per year
    outage_time_trafo = Time(8, TimeUnit.HOUR)  # hours
    outage_time_line = Time(4, TimeUnit.HOUR)  # hours

    B1 = Bus("B1", n_customers=0, coordinate=[0, 0], fail_rate_per_year=0)
    B2 = Bus(
        "B2",
        n_customers=1,
        coordinate=[1, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B3 = Bus(
        "B3",
        n_customers=39,
        coordinate=[2, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B4 = Bus(
        "B4",
        n_customers=1,
        coordinate=[3, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B5 = Bus(
        "B5",
        n_customers=26,
        coordinate=[4, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B6 = Bus(
        "B6",
        n_customers=26,
        coordinate=[5, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B7 = Bus(
        "B7",
        n_customers=1,
        coordinate=[6, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B8 = Bus(
        "B8",
        n_customers=1,
        coordinate=[7, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B9 = Bus(
        "B9",
        n_customers=26,
        coordinate=[8, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B10 = Bus(
        "B10",
        n_customers=26,
        coordinate=[9, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B11 = Bus(
        "B11",
        n_customers=19,
        coordinate=[10, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B12 = Bus(
        "B12",
        n_customers=26,
        coordinate=[11, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B13 = Bus(
        "B13",
        n_customers=26,
        coordinate=[12, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B14 = Bus(
        "B14",
        n_customers=1,
        coordinate=[13, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B15 = Bus(
        "B15",
        n_customers=26,
        coordinate=[14, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B16 = Bus(
        "B16",
        n_customers=26,
        coordinate=[15, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B17 = Bus(
        "B17",
        n_customers=26,
        coordinate=[16, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B18 = Bus(
        "B18",
        n_customers=39,
        coordinate=[17, 0],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B19 = Bus(
        "B19",
        n_customers=39,
        coordinate=[2, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B20 = Bus(
        "B20",
        n_customers=39,
        coordinate=[3, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B21 = Bus(
        "B21",
        n_customers=39,
        coordinate=[4, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B22 = Bus(
        "B22",
        n_customers=39,
        coordinate=[5, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B23 = Bus(
        "B23",
        n_customers=39,
        coordinate=[3, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B24 = Bus(
        "B24",
        n_customers=2,
        coordinate=[4, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B25 = Bus(
        "B25",
        n_customers=2,
        coordinate=[5, -1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B26 = Bus(
        "B26",
        n_customers=26,
        coordinate=[6, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B27 = Bus(
        "B27",
        n_customers=26,
        coordinate=[7, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B28 = Bus(
        "B28",
        n_customers=26,
        coordinate=[8, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B29 = Bus(
        "B29",
        n_customers=1,
        coordinate=[9, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B30 = Bus(
        "B30",
        n_customers=1,
        coordinate=[10, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B31 = Bus(
        "B31",
        n_customers=1,
        coordinate=[11, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B32 = Bus(
        "B32",
        n_customers=1,
        coordinate=[12, 1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B33 = Bus(
        "B33",
        n_customers=26,
        coordinate=[13, 1],
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
        B5,
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
        B12,
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
        B15,
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
        B2,
        B19,
        r=0.1640,
        x=0.1565,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L19 = Line(
        "L19",
        B19,
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
        B21,
        B22,
        r=0.7089,
        x=0.9373,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L22 = Line(
        "L22",
        B3,
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
        B6,
        B26,
        r=0.2030,
        x=0.1034,
        fail_rate_density_per_year=fail_rate_line,
        outage_time=outage_time_line,
    )
    L26 = Line(
        "L26",
        B26,
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
        B31,
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

    DL1a = Disconnector("L1a", L1, B1, E1)
    DL1b = Disconnector("L1b", L1, B2, E1)
    DL1c = Disconnector("L1c", L1, B2)
    DL2a = Disconnector("L2a", L2, B2)
    DL2b = Disconnector("L2b", L2, B3)
    DL3a = Disconnector("L3a", L3, B3)
    DL3b = Disconnector("L3b", L3, B4)
    DL4a = Disconnector("L4a", L4, B4)
    DL4b = Disconnector("L4b", L4, B5)
    DL5a = Disconnector("L5a", L5, B5)
    DL5b = Disconnector("L5b", L5, B6)
    DL6a = Disconnector("L6a", L6, B6)
    DL6b = Disconnector("L6b", L6, B7)
    DL7a = Disconnector("L7a", L7, B7)
    DL7b = Disconnector("L7b", L7, B8)
    DL8a = Disconnector("L8a", L8, B8)
    DL8b = Disconnector("L8b", L8, B9)
    DL9a = Disconnector("L9a", L9, B9)
    DL9b = Disconnector("L9b", L9, B10)
    DL10a = Disconnector("L10a", L10, B10)
    DL10b = Disconnector("L10b", L10, B11)
    DL11a = Disconnector("L11a", L11, B11)
    DL11b = Disconnector("L11b", L11, B12)
    DL12a = Disconnector("L12a", L12, B12)
    DL12b = Disconnector("L12b", L12, B13)
    DL13a = Disconnector("L13a", L13, B13)
    DL13b = Disconnector("L13b", L13, B14)
    DL14a = Disconnector("L14a", L14, B14)
    DL14b = Disconnector("L14b", L14, B15)
    DL15a = Disconnector("L15a", L15, B15)
    DL15b = Disconnector("L15b", L15, B16)
    DL16a = Disconnector("L16a", L16, B16)
    DL16b = Disconnector("L16b", L16, B17)
    DL17a = Disconnector("L17a", L17, B17)
    DL17b = Disconnector("L17b", L17, B18)

    DL18a = Disconnector("L18a", L18, B2)
    DL18b = Disconnector("L18b", L18, B19)
    DL19a = Disconnector("L19a", L19, B19)
    DL19b = Disconnector("L19b", L19, B20)
    DL20a = Disconnector("L20a", L20, B20)
    DL20b = Disconnector("L20b", L20, B21)
    DL21a = Disconnector("L21a", L21, B21)
    DL21b = Disconnector("L21b", L21, B22)

    DL22a = Disconnector("L22a", L22, B3)
    DL22b = Disconnector("L22b", L22, B23)
    DL23a = Disconnector("L23a", L23, B23)
    DL23b = Disconnector("L23b", L23, B24)
    DL24a = Disconnector("L24a", L24, B24)
    DL24b = Disconnector("L24b", L24, B25)

    DL25a = Disconnector("L25a", L25, B6)
    DL25b = Disconnector("L25b", L25, B26)
    DL26a = Disconnector("L26a", L26, B26)
    DL26b = Disconnector("L26b", L26, B27)
    DL27a = Disconnector("L27a", L27, B27)
    DL27b = Disconnector("L27b", L27, B28)
    DL28a = Disconnector("L28a", L28, B28)
    DL28b = Disconnector("L28b", L28, B29)
    DL29a = Disconnector("L29a", L29, B29)
    DL29b = Disconnector("L29b", L29, B30)
    DL30a = Disconnector("L30a", L30, B30)
    DL30b = Disconnector("L30b", L30, B31)
    DL31a = Disconnector("L31a", L31, B31)
    DL31b = Disconnector("L31b", L31, B32)
    DL32a = Disconnector("L32a", L32, B32)
    DL32b = Disconnector("L32b", L32, B33)

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

    # # Backup
    # DL33a = Disconnector("L33a", L33, B9)
    # DL33b = Disconnector("L33b", L33, B15)
    # DL34a = Disconnector("L34a", L34, B12)
    # DL34b = Disconnector("L34b", L34, B22)
    # DL35a = Disconnector("L35a", L35, B18)
    # DL35b = Disconnector("L35b", L35, B33)
    # DL36a = Disconnector("L36a", L36, B25)
    # DL36b = Disconnector("L36b", L36, B29)
    # DL37a = Disconnector("L37a", L37, B8)
    # DL37b = Disconnector("L37b", L37, B21)

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

    if include_production:

        battery_capacity = 1  # MWh

        Battery("Battery", B30, E_max=battery_capacity)
        Production("Wind_Plant", B15)

    if include_microgrid:

        # Micorgrid:

        microgrid_mode = MicrogridMode.LIMITED_SUPPORT
        battery_capacity = 1  # MWh

        BM1 = Bus(
            "BM1",
            n_customers=0,
            coordinate=[14, 2],
            fail_rate_per_year=fail_rate_trafo,
            outage_time=outage_time_trafo,
        )
        BM2 = Bus(
            "BM2",
            n_customers=40,
            coordinate=[15, 2],
            fail_rate_per_year=fail_rate_trafo,
            outage_time=outage_time_trafo,
        )
        BM3 = Bus(
            "BM3",
            n_customers=0,
            coordinate=[15, 2.5],
            fail_rate_per_year=fail_rate_trafo,
            outage_time=outage_time_trafo,
        )
        BM4 = Bus(
            "BM4",
            n_customers=0,
            coordinate=[15, 1.5],
            fail_rate_per_year=fail_rate_trafo,
            outage_time=outage_time_trafo,
        )

        Battery("Bat1", BM1, E_max=battery_capacity)
        Production("P1", BM3)
        Production("P2", BM4)

        # Microgrid

        ML1 = Line(
            "ML1",
            B33,
            BM1,
            r=0.1872,  # 0.7394,
            x=0.0619,  # 0.2444,
            fail_rate_density_per_year=fail_rate_line,
            outage_time=outage_time_line,
        )

        ML2 = Line(
            "ML2",
            BM1,
            BM2,
            r=0.0047,
            x=0.0016,
            fail_rate_density_per_year=fail_rate_line,
            outage_time=outage_time_line,
        )
        ML3 = Line(
            "ML3",
            BM1,
            BM3,
            r=0.0047,
            x=0.0016,
            fail_rate_density_per_year=fail_rate_line,
            outage_time=outage_time_line,
        )
        ML4 = Line(
            "ML4",
            BM1,
            BM4,
            r=0.0047,
            x=0.0016,
            fail_rate_density_per_year=fail_rate_line,
            outage_time=outage_time_line,
        )

        E2 = CircuitBreaker("E2", ML1)

        DML1a = Disconnector("ML1a", ML1, B33, E2)
        DML1b = Disconnector("ML1b", ML1, BM1, E2)
        DML1c = Disconnector("ML1c", ML1, BM1)
        DML2a = Disconnector("ML2a", ML2, BM1)
        DML2b = Disconnector("ML2b", ML2, BM2)
        DML3a = Disconnector("ML3a", ML3, BM1)
        DML3b = Disconnector("ML3b", ML3, BM3)
        DML4a = Disconnector("ML4a", ML4, BM1)
        DML4b = Disconnector("ML4b", ML4, BM4)

        m = Microgrid(dn, ML1, mode=microgrid_mode)
        m.add_buses([BM1, BM2, BM3, BM4])
        m.add_lines([ML2, ML3, ML4])

    if include_ICT:

        Sensor("SL1", L1)
        Sensor("SL2", L2)
        Sensor("SL3", L3)
        Sensor("SL4", L4)
        Sensor("SL5", L5)
        Sensor("SL6", L6)
        Sensor("SL7", L7)
        Sensor("SL8", L8)
        Sensor("SL9", L9)
        Sensor("SL10", L10)
        Sensor("SL11", L11)
        Sensor("SL12", L12)
        Sensor("SL13", L13)
        Sensor("SL14", L14)
        Sensor("SL15", L15)
        Sensor("SL16", L16)
        Sensor("SL17", L17)
        Sensor("SL18", L18)
        Sensor("SL19", L19)
        Sensor("SL20", L20)
        Sensor("SL21", L21)
        Sensor("SL22", L22)
        Sensor("SL23", L23)
        Sensor("SL24", L24)
        Sensor("SL25", L25)
        Sensor("SL26", L26)
        Sensor("SL27", L27)
        Sensor("SL28", L28)
        Sensor("SL29", L29)
        Sensor("SL30", L30)
        Sensor("SL31", L31)
        Sensor("SL32", L32)

        # Backup lines
        # Sensor("SL33", L33)
        # Sensor("SL34", L34)
        # Sensor("SL35", L35)
        # Sensor("SL36", L36)
        # Sensor("SL37", L37)

        IntelligentSwitch("ISwL1a", DL1a)
        IntelligentSwitch("ISwL1b", DL1b)
        IntelligentSwitch("ISwL1c", DL1c)
        IntelligentSwitch("ISwL2a", DL2a)
        IntelligentSwitch("ISwL2b", DL2b)
        IntelligentSwitch("ISwL3a", DL3a)
        IntelligentSwitch("ISwL3b", DL3b)
        IntelligentSwitch("ISwL4a", DL4a)
        IntelligentSwitch("ISwL4b", DL4b)
        IntelligentSwitch("ISwL5a", DL5a)
        IntelligentSwitch("ISwL5b", DL5b)
        IntelligentSwitch("ISwL6a", DL6a)
        IntelligentSwitch("ISwL6b", DL6b)
        IntelligentSwitch("ISwL7a", DL7a)
        IntelligentSwitch("ISwL7b", DL7b)
        IntelligentSwitch("ISwL8a", DL8a)
        IntelligentSwitch("ISwL8b", DL8b)
        IntelligentSwitch("ISwL9a", DL9a)
        IntelligentSwitch("ISwL9b", DL9b)
        IntelligentSwitch("ISwL10a", DL10a)
        IntelligentSwitch("ISwL10b", DL10b)
        IntelligentSwitch("ISwL11a", DL11a)
        IntelligentSwitch("ISwL11b", DL11b)
        IntelligentSwitch("ISwL12a", DL12a)
        IntelligentSwitch("ISwL12b", DL12b)
        IntelligentSwitch("ISwL13a", DL13a)
        IntelligentSwitch("ISwL13b", DL13b)
        IntelligentSwitch("ISwL14a", DL14a)
        IntelligentSwitch("ISwL14b", DL14b)
        IntelligentSwitch("ISwL15a", DL15a)
        IntelligentSwitch("ISwL15b", DL15b)
        IntelligentSwitch("ISwL16a", DL16a)
        IntelligentSwitch("ISwL16b", DL16b)
        IntelligentSwitch("ISwL17a", DL17a)
        IntelligentSwitch("ISwL17b", DL17b)
        IntelligentSwitch("ISwL18a", DL18a)
        IntelligentSwitch("ISwL18b", DL18b)
        IntelligentSwitch("ISwL19a", DL19a)
        IntelligentSwitch("ISwL19b", DL19b)
        IntelligentSwitch("ISwL20a", DL20a)
        IntelligentSwitch("ISwL20b", DL20b)
        IntelligentSwitch("ISwL21a", DL21a)
        IntelligentSwitch("ISwL21b", DL21b)
        IntelligentSwitch("ISwL22a", DL22a)
        IntelligentSwitch("ISwL22b", DL22b)
        IntelligentSwitch("ISwL23a", DL23a)
        IntelligentSwitch("ISwL23b", DL23b)
        IntelligentSwitch("ISwL24a", DL24a)
        IntelligentSwitch("ISwL24b", DL24b)
        IntelligentSwitch("ISwL25a", DL25a)
        IntelligentSwitch("ISwL25b", DL25b)
        IntelligentSwitch("ISwL26a", DL26a)
        IntelligentSwitch("ISwL26b", DL26b)
        IntelligentSwitch("ISwL27a", DL27a)
        IntelligentSwitch("ISwL27b", DL27b)
        IntelligentSwitch("ISwL28a", DL28a)
        IntelligentSwitch("ISwL28b", DL28b)
        IntelligentSwitch("ISwL29a", DL29a)
        IntelligentSwitch("ISwL29b", DL29b)
        IntelligentSwitch("ISwL30a", DL30a)
        IntelligentSwitch("ISwL30b", DL30b)
        IntelligentSwitch("ISwL31a", DL31a)
        IntelligentSwitch("ISwL31b", DL31b)
        IntelligentSwitch("ISwL32a", DL32a)
        IntelligentSwitch("ISwL32b", DL32b)

        # Backup lines:
        # IntelligentSwitch("ISwL33a", DL33a)
        # IntelligentSwitch("ISwL33b", DL33b)
        # IntelligentSwitch("ISwL34a", DL34a)
        # IntelligentSwitch("ISwL34b", DL34b)
        # IntelligentSwitch("ISwL35a", DL35a)
        # IntelligentSwitch("ISwL35b", DL35b)
        # IntelligentSwitch("ISwL36a", DL36a)
        # IntelligentSwitch("ISwL36b", DL36b)
        # IntelligentSwitch("ISwL37a", DL37a)
        # IntelligentSwitch("ISwL37b", DL37b)

        if include_microgrid:
            Sensor("SML1", ML1)
            Sensor("SML2", ML2)
            Sensor("SML3", ML3)
            Sensor("SML4", ML4)

            IntelligentSwitch("ISwML1a", DML1a)
            IntelligentSwitch("ISwML1b", DML1b)
            IntelligentSwitch("ISwML1c", DML1c)
            IntelligentSwitch("ISwML2a", DML2a)
            IntelligentSwitch("ISwML2b", DML2b)
            IntelligentSwitch("ISwML3a", DML3a)
            IntelligentSwitch("ISwML3b", DML3b)
            IntelligentSwitch("ISwML4a", DML4a)
            IntelligentSwitch("ISwML4b", DML4b)

    return ps, include_microgrid, include_production


if __name__ == "__main__":
    import os

    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "IEEE33_testnetwork.pdf",
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
