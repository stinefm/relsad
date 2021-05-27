from stinetwork.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    Battery,
    Production,
)
from stinetwork.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
    Microgrid,
)
from stinetwork.visualization.plotting import plot_topology


def initialize_69Bus_network():
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
    B17 = Bus("B17", coordinate=[16, 0], fail_rate_per_year=fail_rate_trafo)
    B18 = Bus("B18", coordinate=[17, 0.5], fail_rate_per_year=fail_rate_trafo)
    B19 = Bus("B19", coordinate=[18, 0.5], fail_rate_per_year=fail_rate_trafo)
    B20 = Bus("B20", coordinate=[19, 0.5], fail_rate_per_year=fail_rate_trafo)
    B21 = Bus("B21", coordinate=[20, 0.5], fail_rate_per_year=fail_rate_trafo)
    B22 = Bus("B22", coordinate=[21, 0.5], fail_rate_per_year=fail_rate_trafo)
    B23 = Bus("B23", coordinate=[22, 0.5], fail_rate_per_year=fail_rate_trafo)
    B24 = Bus("B24", coordinate=[23, 0], fail_rate_per_year=fail_rate_trafo)
    B25 = Bus("B25", coordinate=[24, 0], fail_rate_per_year=fail_rate_trafo)
    B26 = Bus("B26", coordinate=[25, 0], fail_rate_per_year=fail_rate_trafo)
    B27 = Bus("B27", coordinate=[26, 0], fail_rate_per_year=fail_rate_trafo)
    B28 = Bus("B28", coordinate=[3, -2], fail_rate_per_year=fail_rate_trafo)
    B29 = Bus("B29", coordinate=[4, -2], fail_rate_per_year=fail_rate_trafo)
    B30 = Bus("B30", coordinate=[5, -2], fail_rate_per_year=fail_rate_trafo)
    B31 = Bus("B31", coordinate=[6, -2], fail_rate_per_year=fail_rate_trafo)
    B32 = Bus("B32", coordinate=[7, -2], fail_rate_per_year=fail_rate_trafo)
    B33 = Bus("B33", coordinate=[8, -2], fail_rate_per_year=fail_rate_trafo)
    B34 = Bus("B34", coordinate=[9, -2], fail_rate_per_year=fail_rate_trafo)
    B35 = Bus("B35", coordinate=[10, -2], fail_rate_per_year=fail_rate_trafo)
    B36 = Bus("B36", coordinate=[3, 2], fail_rate_per_year=fail_rate_trafo)
    B37 = Bus("B37", coordinate=[4, 2], fail_rate_per_year=fail_rate_trafo)
    B38 = Bus("B38", coordinate=[5, 2], fail_rate_per_year=fail_rate_trafo)
    B39 = Bus("B39", coordinate=[6, 2], fail_rate_per_year=fail_rate_trafo)
    B40 = Bus("B40", coordinate=[7, 2], fail_rate_per_year=fail_rate_trafo)
    B41 = Bus("B41", coordinate=[8, 2], fail_rate_per_year=fail_rate_trafo)
    B42 = Bus("B42", coordinate=[9, 2], fail_rate_per_year=fail_rate_trafo)
    B43 = Bus("B43", coordinate=[10, 2], fail_rate_per_year=fail_rate_trafo)
    B44 = Bus("B44", coordinate=[11, 2], fail_rate_per_year=fail_rate_trafo)
    B45 = Bus("B45", coordinate=[12, 2], fail_rate_per_year=fail_rate_trafo)
    B46 = Bus("B46", coordinate=[13, 2], fail_rate_per_year=fail_rate_trafo)
    B47 = Bus("B47", coordinate=[4, -1.5], fail_rate_per_year=fail_rate_trafo)
    B48 = Bus("B48", coordinate=[5, -1.5], fail_rate_per_year=fail_rate_trafo)
    B49 = Bus("B49", coordinate=[6, -1.5], fail_rate_per_year=fail_rate_trafo)
    B50 = Bus("B50", coordinate=[7, -1.5], fail_rate_per_year=fail_rate_trafo)
    B51 = Bus("B51", coordinate=[8, 1], fail_rate_per_year=fail_rate_trafo)
    B52 = Bus("B52", coordinate=[9, 1], fail_rate_per_year=fail_rate_trafo)
    B53 = Bus("B53", coordinate=[9, -1], fail_rate_per_year=fail_rate_trafo)
    B54 = Bus("B54", coordinate=[10, -1], fail_rate_per_year=fail_rate_trafo)
    B55 = Bus("B55", coordinate=[11, -1], fail_rate_per_year=fail_rate_trafo)
    B56 = Bus("B56", coordinate=[12, -1], fail_rate_per_year=fail_rate_trafo)
    B57 = Bus("B57", coordinate=[13, -1], fail_rate_per_year=fail_rate_trafo)
    B58 = Bus("B58", coordinate=[14, -1], fail_rate_per_year=fail_rate_trafo)
    B59 = Bus("B59", coordinate=[15, -1.5], fail_rate_per_year=fail_rate_trafo)
    B60 = Bus("B60", coordinate=[16, -2], fail_rate_per_year=fail_rate_trafo)
    B61 = Bus("B61", coordinate=[17, -2], fail_rate_per_year=fail_rate_trafo)
    B62 = Bus("B62", coordinate=[18, -2], fail_rate_per_year=fail_rate_trafo)
    B63 = Bus("B63", coordinate=[19, -2], fail_rate_per_year=fail_rate_trafo)
    B64 = Bus("B64", coordinate=[20, -2], fail_rate_per_year=fail_rate_trafo)
    B65 = Bus("B65", coordinate=[21, -2], fail_rate_per_year=fail_rate_trafo)
    B66 = Bus("B66", coordinate=[11, 1], fail_rate_per_year=fail_rate_trafo)
    B67 = Bus("B67", coordinate=[12, 1], fail_rate_per_year=fail_rate_trafo)

    # Microgrid:
    B68 = Bus("B68", coordinate=[16, 1.5], fail_rate_per_year=fail_rate_trafo)
    B69 = Bus("B69", coordinate=[17, 1.5], fail_rate_per_year=fail_rate_trafo)
    B70 = Bus("B70", coordinate=[17, 2], fail_rate_per_year=fail_rate_trafo)
    B71 = Bus("B71", coordinate=[17, 1], fail_rate_per_year=fail_rate_trafo)

    Battery("Bat1", B68)
    Production("P1", B70)
    Production("P2", B71)

    # Lines, connections and impedances
    L1 = Line(
        "L1",
        B1,
        B2,
        0.0005,
        0.0012,
        length=0.001887,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B2,
        B3,
        0.0005,
        0.0012,
        length=0.001887,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B3,
        B4,
        0.0015,
        0.0036,
        length=0.00566,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        0.0251,
        0.0294,
        length=0.094705,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B5,
        B6,
        0.3660,
        0.1864,
        length=1.380954,
        fail_rate_density_per_year=fail_rate_line,
    )
    L6 = Line(
        "L6",
        B6,
        B7,
        0.3811,
        0.1941,
        length=1.437928,
        fail_rate_density_per_year=fail_rate_line,
    )
    L7 = Line(
        "L7",
        B7,
        B8,
        0.0922,
        0.0470,
        length=0.34788,
        fail_rate_density_per_year=fail_rate_line,
    )
    L8 = Line(
        "L8",
        B8,
        B9,
        0.0493,
        0.0251,
        length=0.186014,
        fail_rate_density_per_year=fail_rate_line,
    )
    L9 = Line(
        "L9",
        B9,
        B10,
        0.8190,
        0.2707,
        length=3.090168,
        fail_rate_density_per_year=fail_rate_line,
    )
    L10 = Line(
        "L10",
        B10,
        B11,
        0.1872,
        0.0619,
        length=0.706324,
        fail_rate_density_per_year=fail_rate_line,
    )
    L11 = Line(
        "L11",
        B11,
        B12,
        0.7114,
        0.2351,
        length=2.684183,
        fail_rate_density_per_year=fail_rate_line,
    )
    L12 = Line(
        "L12",
        B12,
        B13,
        1.0300,
        0.3400,
        length=3.886292,
        fail_rate_density_per_year=fail_rate_line,
    )
    L13 = Line(
        "L13",
        B13,
        B14,
        1.0440,
        0.3450,
        length=3.939116,
        fail_rate_density_per_year=fail_rate_line,
    )
    L14 = Line(
        "L14",
        B14,
        B15,
        1.0580,
        0.3496,
        length=3.991939,
        fail_rate_density_per_year=fail_rate_line,
    )
    L15 = Line(
        "L15",
        B15,
        B16,
        0.1966,
        0.0650,
        length=0.794615,
        fail_rate_density_per_year=fail_rate_line,
    )
    L16 = Line(
        "L16",
        B16,
        B17,
        0.3744,
        0.1238,
        length=1.412648,
        fail_rate_density_per_year=fail_rate_line,
    )
    L17 = Line(
        "L17",
        B17,
        B18,
        0.0047,
        0.0016,
        length=0.017734,
        fail_rate_density_per_year=fail_rate_line,
    )
    L18 = Line(
        "L18",
        B18,
        B19,
        0.3276,
        0.1083,
        length=1.236067,
        fail_rate_density_per_year=fail_rate_line,
    )
    L19 = Line(
        "L19",
        B19,
        B20,
        0.2106,
        0.0690,
        length=0.794615,
        fail_rate_density_per_year=fail_rate_line,
    )
    L20 = Line(
        "L20",
        B20,
        B21,
        0.3416,
        0.1129,
        length=1.288891,
        fail_rate_density_per_year=fail_rate_line,
    )
    L21 = Line(
        "L21",
        B21,
        B22,
        0.0140,
        0.0046,
        length=0.052823,
        fail_rate_density_per_year=fail_rate_line,
    )
    L22 = Line(
        "L22",
        B22,
        B23,
        0.1591,
        0.0526,
        length=0.6003,
        fail_rate_density_per_year=fail_rate_line,
    )
    L23 = Line(
        "L23",
        B23,
        B24,
        0.3463,
        0.1145,
        length=1.306624,
        fail_rate_density_per_year=fail_rate_line,
    )
    L24 = Line(
        "L24",
        B24,
        B25,
        0.7488,
        0.2475,
        length=2.825297,
        fail_rate_density_per_year=fail_rate_line,
    )
    L25 = Line(
        "L25",
        B25,
        B26,
        0.3089,
        0.1021,
        length=1.16551,
        fail_rate_density_per_year=fail_rate_line,
    )
    L26 = Line(
        "L26",
        B26,
        B27,
        0.1732,
        0.0572,
        length=0.653501,
        fail_rate_density_per_year=fail_rate_line,
    )
    L27 = Line(
        "L27",
        B3,
        B28,
        0.0044,
        0.0108,
        length=0.016602,
        fail_rate_density_per_year=fail_rate_line,
    )
    L28 = Line(
        "L28",
        B28,
        B29,
        0.0640,
        0.1565,
        length=0.241478,
        fail_rate_density_per_year=fail_rate_line,
    )
    L29 = Line(
        "L29",
        B29,
        B30,
        0.3978,
        0.1315,
        length=1.5,
        fail_rate_density_per_year=fail_rate_line,
    )
    L30 = Line(
        "L30",
        B30,
        B31,
        0.0702,
        0.0232,
        length=0.264872,
        fail_rate_density_per_year=fail_rate_line,
    )
    L31 = Line(
        "L31",
        B31,
        B32,
        0.3510,
        0.1160,
        length=1.324358,
        fail_rate_density_per_year=fail_rate_line,
    )
    L32 = Line(
        "L32",
        B32,
        B33,
        0.8390,
        0.2816,
        length=3.16563,
        fail_rate_density_per_year=fail_rate_line,
    )
    L33 = Line(
        "L33",
        B33,
        B34,
        1.7080,
        0.5646,
        length=6.44,
        fail_rate_density_per_year=fail_rate_line,
    )
    L34 = Line(
        "L34",
        B34,
        B35,
        1.4740,
        0.4873,
        length=5.561549,
        fail_rate_density_per_year=fail_rate_line,
    )
    L35 = Line(
        "L35",
        B3,
        B36,
        0.0044,
        0.0108,
        length=0.016602,
        fail_rate_density_per_year=fail_rate_line,
    )
    L36 = Line(
        "L36",
        B36,
        B37,
        0.0640,
        0.11565,
        length=0.241478,
        fail_rate_density_per_year=fail_rate_line,
    )
    L37 = Line(
        "L37",
        B37,
        B38,
        0.1053,
        0.1230,
        length=0.397307,
        fail_rate_density_per_year=fail_rate_line,
    )
    L38 = Line(
        "L38",
        B38,
        B39,
        0.0304,
        0.0355,
        length=0.114702,
        fail_rate_density_per_year=fail_rate_line,
    )
    L39 = Line(
        "L39",
        B39,
        B40,
        0.0018,
        0.0021,
        length=0.006792,
        fail_rate_density_per_year=fail_rate_line,
    )
    L40 = Line(
        "L40",
        B40,
        B41,
        0.7283,
        0.8509,
        length=2.747948,
        fail_rate_density_per_year=fail_rate_line,
    )
    L41 = Line(
        "L41",
        B41,
        B42,
        0.31,
        0.3623,
        length=1.169661,
        fail_rate_density_per_year=fail_rate_line,
    )
    L42 = Line(
        "L42",
        B42,
        B43,
        0.0410,
        0.0478,
        length=0.154697,
        fail_rate_density_per_year=fail_rate_line,
    )
    L43 = Line(
        "L43",
        B43,
        B44,
        0.0092,
        0.0116,
        length=0.034713,
        fail_rate_density_per_year=fail_rate_line,
    )
    L44 = Line(
        "L44",
        B44,
        B45,
        0.1089,
        0.1373,
        length=0.410891,
        fail_rate_density_per_year=fail_rate_line,
    )
    L45 = Line(
        "L45",
        B45,
        B46,
        0.0009,
        0.0012,
        length=0.003396,
        fail_rate_density_per_year=fail_rate_line,
    )
    L46 = Line(
        "L46",
        B4,
        B47,
        0.0034,
        0.0084,
        length=0.012829,
        fail_rate_density_per_year=fail_rate_line,
    )
    L47 = Line(
        "L47",
        B47,
        B48,
        0.0851,
        0.2083,
        length=0.321091,
        fail_rate_density_per_year=fail_rate_line,
    )
    L48 = Line(
        "L48",
        B48,
        B49,
        0.2898,
        0.7091,
        length=1.093444,
        fail_rate_density_per_year=fail_rate_line,
    )
    L49 = Line(
        "L49",
        B49,
        B50,
        0.0822,
        0.2011,
        length=0.310149,
        fail_rate_density_per_year=fail_rate_line,
    )
    L50 = Line(
        "L50",
        B8,
        B51,
        0.0928,
        0.0473,
        length=0.350144,
        fail_rate_density_per_year=fail_rate_line,
    )
    L51 = Line(
        "L51",
        B51,
        B52,
        0.3319,
        0.1114,
        length=1.252292,
        fail_rate_density_per_year=fail_rate_line,
    )
    L52 = Line(
        "L52",
        B9,
        B53,
        0.1740,
        0.0886,
        length=0.656519,
        fail_rate_density_per_year=fail_rate_line,
    )
    L53 = Line(
        "L53",
        B53,
        B54,
        0.2030,
        0.1034,
        length=0.765939,
        fail_rate_density_per_year=fail_rate_line,
    )
    L54 = Line(
        "L54",
        B54,
        B55,
        0.2842,
        0.1447,
        length=1.072315,
        fail_rate_density_per_year=fail_rate_line,
    )
    L55 = Line(
        "L55",
        B55,
        B56,
        0.2813,
        0.1433,
        length=1.061373,
        fail_rate_density_per_year=fail_rate_line,
    )
    L56 = Line(
        "L56",
        B56,
        B57,
        1.5900,
        0.5337,
        length=6.0,
        fail_rate_density_per_year=fail_rate_line,
    )
    L57 = Line(
        "L57",
        B57,
        B58,
        0.7837,
        0.2630,
        length=2.96,
        fail_rate_density_per_year=fail_rate_line,
    )
    L58 = Line(
        "L58",
        B58,
        B59,
        0.3042,
        0.1006,
        length=1.148,
        fail_rate_density_per_year=fail_rate_line,
    )
    L59 = Line(
        "L59",
        B59,
        B60,
        0.3861,
        0.1172,
        length=1.4568,
        fail_rate_density_per_year=fail_rate_line,
    )
    L60 = Line(
        "L60",
        B60,
        B61,
        0.5075,
        0.2585,
        length=1.9148,
        fail_rate_density_per_year=fail_rate_line,
    )
    L61 = Line(
        "L61",
        B61,
        B62,
        0.0974,
        0.0496,
        length=0.3675,
        fail_rate_density_per_year=fail_rate_line,
    )
    L62 = Line(
        "L62",
        B62,
        B63,
        0.1450,
        0.0738,
        length=0.5471,
        fail_rate_density_per_year=fail_rate_line,
    )
    L63 = Line(
        "L63",
        B63,
        B64,
        0.7105,
        0.3619,
        length=2.6808,
        fail_rate_density_per_year=fail_rate_line,
    )
    L64 = Line(
        "L64",
        B64,
        B65,
        1.0410,
        0.5302,
        length=3.9278,
        fail_rate_density_per_year=fail_rate_line,
    )
    L65 = Line(
        "L65",
        B11,
        B66,
        0.2012,
        0.0611,
        length=0.75915,
        fail_rate_density_per_year=fail_rate_line,
    )
    L66 = Line(
        "L66",
        B66,
        B67,
        0.0047,
        0.0014,
        length=0.017734,
        fail_rate_density_per_year=fail_rate_line,
    )

    # Microgrid:
    L67 = Line(
        "L67",
        B16,
        B68,
        0.7394,
        0.2444,
        length=2.78983,
        fail_rate_density_per_year=fail_rate_line,
    )
    L68 = Line(
        "L68",
        B68,
        B69,
        0.0047,
        0.0016,
        length=0.017734,
        fail_rate_density_per_year=fail_rate_line,
    )
    ML3 = Line(
        "ML3",
        B68,
        B70,
        0.0047,
        0.0016,
        length=0.017734,
        fail_rate_density_per_year=fail_rate_line,
    )
    ML4 = Line(
        "ML4",
        B68,
        B71,
        0.0047,
        0.0016,
        length=0.017734,
        fail_rate_density_per_year=fail_rate_line,
    )

    # Backup lines:
    L69 = Line(
        "L69",
        B11,
        B43,
        0.3042,
        0.1006,
        length=1.148,
        fail_rate_density_per_year=fail_rate_line,
        capacity=5,
    )
    L70 = Line(
        "L70",
        B17,
        B24,
        0.8390,
        0.2816,
        length=3.16563,
        fail_rate_density_per_year=fail_rate_line,
        capacity=5,
    )
    # L71 = Line(
    #     "L71",
    #     B15,
    #     B46,
    #     0.0,
    #     length=1.0e-08,
    #     fail_rate_density_per_year=fail_rate_line,
    #     capacity=3,
    # )
    L72 = Line(
        "L72",
        B50,
        B59,
        0.2012,
        0.0611,
        length=0.75915,
        fail_rate_density_per_year=fail_rate_line,
        capacity=5,
    )
    # L73 = Line(
    #     "L73",
    #     B27,
    #     B65,
    #     0.0,
    #     length=1.0e-08,
    #     fail_rate_density_per_year=fail_rate_line,
    #     capacity=3,
    # )

    E1 = CircuitBreaker("E1", L1)
    E2 = CircuitBreaker("E2", L67)

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
    Disconnector("L18a", L18, B18)
    Disconnector("L18b", L18, B19)
    Disconnector("L19a", L19, B19)
    Disconnector("L19b", L19, B20)
    Disconnector("L20a", L20, B20)
    Disconnector("L20b", L20, B21)
    Disconnector("L21a", L21, B21)
    Disconnector("L21b", L21, B22)
    Disconnector("L22a", L22, B22)
    Disconnector("L22b", L22, B23)
    Disconnector("L23a", L23, B23)
    Disconnector("L23b", L23, B24)
    Disconnector("L24a", L24, B24)
    Disconnector("L24b", L24, B25)
    Disconnector("L25a", L25, B25)
    Disconnector("L25b", L25, B26)
    Disconnector("L26a", L26, B26)
    Disconnector("L26b", L26, B27)

    Disconnector("L27a", L27, B3)
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
    Disconnector("L33a", L33, B33)
    Disconnector("L33b", L33, B34)
    Disconnector("L34a", L34, B34)
    Disconnector("L34b", L34, B35)

    Disconnector("L35a", L35, B3)
    Disconnector("L35b", L35, B36)
    Disconnector("L36a", L36, B36)
    Disconnector("L36b", L36, B37)
    Disconnector("L37a", L37, B37)
    Disconnector("L37b", L37, B38)
    Disconnector("L38a", L38, B38)
    Disconnector("L38b", L38, B39)
    Disconnector("L39a", L39, B39)
    Disconnector("L39b", L39, B40)
    Disconnector("L40a", L40, B40)
    Disconnector("L40b", L40, B41)
    Disconnector("L41a", L41, B41)
    Disconnector("L41b", L41, B42)
    Disconnector("L42a", L42, B42)
    Disconnector("L42b", L42, B43)
    Disconnector("L43a", L43, B43)
    Disconnector("L43b", L43, B44)
    Disconnector("L44a", L44, B44)
    Disconnector("L44b", L44, B45)
    Disconnector("L45a", L45, B45)
    Disconnector("L45b", L45, B46)

    Disconnector("L46a", L46, B4)
    Disconnector("L46b", L46, B47)
    Disconnector("L47a", L47, B47)
    Disconnector("L47b", L47, B48)
    Disconnector("L48a", L48, B48)
    Disconnector("L48b", L48, B49)
    Disconnector("L49a", L49, B49)
    Disconnector("L49b", L49, B50)

    Disconnector("L50a", L50, B8)
    Disconnector("L50b", L50, B51)
    Disconnector("L51a", L51, B51)
    Disconnector("L51b", L51, B52)

    Disconnector("L52a", L52, B9)
    Disconnector("L52b", L52, B53)
    Disconnector("L53a", L53, B53)
    Disconnector("L53b", L53, B54)
    Disconnector("L54a", L54, B54)
    Disconnector("L54b", L54, B55)
    Disconnector("L55a", L55, B55)
    Disconnector("L55b", L55, B56)
    Disconnector("L56a", L56, B56)
    Disconnector("L56b", L56, B57)
    Disconnector("L57a", L57, B57)
    Disconnector("L57b", L57, B58)

    Disconnector("L58a", L58, B58)
    Disconnector("L58b", L58, B59)
    Disconnector("L59a", L59, B59)
    Disconnector("L59b", L59, B60)
    Disconnector("L60a", L60, B60)
    Disconnector("L60b", L60, B61)
    Disconnector("L61a", L61, B61)
    Disconnector("L61b", L61, B62)
    Disconnector("L62a", L62, B62)
    Disconnector("L62b", L62, B63)
    Disconnector("L63a", L63, B63)
    Disconnector("L63b", L63, B64)
    Disconnector("L64a", L64, B64)
    Disconnector("L64b", L64, B65)

    Disconnector("L65a", L65, B11)
    Disconnector("L65b", L65, B66)
    Disconnector("L66a", L66, B66)
    Disconnector("L66b", L66, B67)

    # Microgrid:
    Disconnector("L67a", L67, B16, E2)
    Disconnector("L67b", L67, B68, E2)
    Disconnector("L67c", L67, B68)
    Disconnector("L68a", L68, B68)
    Disconnector("L68b", L68, B69)
    Disconnector("ML3a", ML3, B68)
    Disconnector("ML3b", ML3, B70)
    Disconnector("ML4a", ML4, B68)
    Disconnector("ML4b", ML4, B71)

    # Backup lines:
    Disconnector("L69a", L69, B11)
    Disconnector("L69b", L69, B43)
    Disconnector("L70a", L70, B17)
    Disconnector("L70b", L70, B24)
    # Disconnector("L71a", L71, B15)
    # Disconnector("L71b", L71, B46)
    Disconnector("L72a", L72, B50)
    Disconnector("L72b", L72, B59)
    # Disconnector("L73a", L73, B27)
    # Disconnector("L73b", L73, B65)

    L69.set_backup()
    L70.set_backup()
    # L71.set_backup()
    L72.set_backup()
    # L73.set_backup()

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
            B34,
            B35,
            B36,
            B37,
            B38,
            B39,
            B40,
            B41,
            B42,
            B43,
            B44,
            B45,
            B46,
            B47,
            B48,
            B49,
            B50,
            B51,
            B52,
            B53,
            B54,
            B55,
            B56,
            B57,
            B58,
            B59,
            B60,
            B61,
            B62,
            B63,
            B64,
            B65,
            B66,
            B67,
            # B68,
            # B69,
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
            L33,
            L34,
            L35,
            L36,
            L37,
            L38,
            L39,
            L40,
            L41,
            L42,
            L43,
            L44,
            L45,
            L46,
            L47,
            L48,
            L49,
            L50,
            L51,
            L52,
            L53,
            L54,
            L55,
            L56,
            L57,
            L58,
            L59,
            L60,
            L61,
            L62,
            L63,
            L64,
            L65,
            L66,
            # L67,
            # L68,
            L69,
            L70,
            # L71,
            L72,
            # L73,
        ]
    )

    m = Microgrid(dn, L67, mode=1)
    m.add_buses([B68, B69, B70, B71])
    m.add_lines([L68, ML3, ML4])

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_69Bus_network()
    fig = plot_topology(ps.buses, ps.lines, figsize=(40, 40))

    fig.savefig(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "test69.pdf")
    )
