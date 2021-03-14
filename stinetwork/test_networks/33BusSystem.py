from stinetwork.network.components import Bus, CircuitBreaker, Disconnector, Line
from stinetwork.network.systems import Distribution, PowerSystem, Transmission
from stinetwork.visualization.plotting import plot_topology


def initialize_33Bus_network():
    ps = PowerSystem()

    B1 = Bus("B1", coordinate=[0, 0], fail_rate_per_year=0)
    B2 = Bus("B2", coordinate=[0, -1], fail_rate_per_year=365)
    B3 = Bus("B3", coordinate=[0, -2], fail_rate_per_year=365)
    B4 = Bus("B4", coordinate=[0, -3], fail_rate_per_year=365)
    B5 = Bus("B5", coordinate=[0, -4], fail_rate_per_year=365)
    B6 = Bus("B6", coordinate=[0, -5], fail_rate_per_year=365)
    B7 = Bus("B7", coordinate=[0, -6], fail_rate_per_year=365)
    B8 = Bus("B8", coordinate=[0, -7], fail_rate_per_year=365)
    B9 = Bus("B9", coordinate=[0, -8], fail_rate_per_year=365)
    B10 = Bus("B10", coordinate=[0, -9], fail_rate_per_year=365)
    B11 = Bus("B11", coordinate=[0, -10], fail_rate_per_year=365)
    B12 = Bus("B12", coordinate=[0, -11], fail_rate_per_year=365)
    B13 = Bus("B13", coordinate=[0, -12], fail_rate_per_year=365)
    B14 = Bus("B14", coordinate=[0, -13], fail_rate_per_year=365)
    B15 = Bus("B15", coordinate=[0, -14], fail_rate_per_year=365)
    B16 = Bus("B16", coordinate=[0, -15], fail_rate_per_year=365)
    B17 = Bus("B17", coordinate=[0, -16], fail_rate_per_year=365)
    B18 = Bus("B18", coordinate=[0, -17], fail_rate_per_year=365)
    B19 = Bus("B19", coordinate=[-1, -2], fail_rate_per_year=365)
    B20 = Bus("B20", coordinate=[-1, -3], fail_rate_per_year=365)
    B21 = Bus("B21", coordinate=[-1, -4], fail_rate_per_year=365)
    B22 = Bus("B22", coordinate=[-1, -5], fail_rate_per_year=365)
    B23 = Bus("B23", coordinate=[1, -3], fail_rate_per_year=365)
    B24 = Bus("B24", coordinate=[1, -4], fail_rate_per_year=365)
    B25 = Bus("B25", coordinate=[1, -5], fail_rate_per_year=365)
    B26 = Bus("B26", coordinate=[-1, -6], fail_rate_per_year=365)
    B27 = Bus("B27", coordinate=[-1, -7], fail_rate_per_year=365)
    B28 = Bus("B28", coordinate=[-1, -8], fail_rate_per_year=365)
    B29 = Bus("B29", coordinate=[-1, -9], fail_rate_per_year=365)
    B30 = Bus("B30", coordinate=[-1, -10], fail_rate_per_year=365)
    B31 = Bus("B31", coordinate=[-1, -11], fail_rate_per_year=365)
    B32 = Bus("B32", coordinate=[-1, -12], fail_rate_per_year=365)
    B33 = Bus("B33", coordinate=[-1, -13], fail_rate_per_year=365)

    L1 = Line(
        "L1",
        B1,
        B2,
        0.057526629463617,
        0.029324854498807,
        fail_rate_density_per_year=365,
    )
    L2 = Line(
        "L2",
        B2,
        B3,
        0.307599005700253,
        0.156669594992563,
        fail_rate_density_per_year=365,
    )
    L3 = Line(
        "L3",
        B3,
        B4,
        0.228359505246029,
        0.11630112507612,
        fail_rate_density_per_year=365,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        0.237780894670114,
        0.121105409749329,
        fail_rate_density_per_year=365,
    )
    L5 = Line(
        "L5",
        B5,
        B6,
        0.511001187968574,
        0.441120683630991,
        fail_rate_density_per_year=365,
    )
    L6 = Line(
        "L6",
        B6,
        B7,
        0.116800271535674,
        0.386089786465145,
        fail_rate_density_per_year=365,
    )
    L7 = Line(
        "L7",
        B7,
        B8,
        1.06779906360124,
        0.770619740244183,
        fail_rate_density_per_year=365,
    )
    L8 = Line(
        "L8", B8, B9, 0.642651066675984, 0.4617104750876, fail_rate_density_per_year=365
    )
    L9 = Line(
        "L9",
        B9,
        B10,
        0.651386129718182,
        0.4617104750876,
        fail_rate_density_per_year=365,
    )
    L10 = Line(
        "L10",
        B10,
        B11,
        0.122665242435435,
        0.040555649838776,
        fail_rate_density_per_year=365,
    )
    L11 = Line(
        "L11",
        B11,
        B12,
        0.233600543071348,
        0.077242914616007,
        fail_rate_density_per_year=365,
    )
    L12 = Line(
        "L12",
        B12,
        B13,
        0.915933753281888,
        0.720642700981322,
        fail_rate_density_per_year=365,
    )
    L13 = Line(
        "L13",
        B13,
        B14,
        0.337922153118168,
        0.444801888770203,
        fail_rate_density_per_year=365,
    )
    L14 = Line(
        "L14",
        B14,
        B15,
        0.368744446995637,
        0.328188797156862,
        fail_rate_density_per_year=365,
    )
    L15 = Line(
        "L15",
        B15,
        B16,
        0.465641253456589,
        0.340043525571273,
        fail_rate_density_per_year=365,
    )
    L16 = Line(
        "L16",
        B16,
        B17,
        0.804249732956644,
        1.07378882111589,
        fail_rate_density_per_year=365,
    )
    L17 = Line(
        "L17",
        B17,
        B18,
        0.456719010492059,
        0.358137584730111,
        fail_rate_density_per_year=365,
    )
    L18 = Line(
        "L18",
        B2,
        B19,
        0.102325024208603,
        0.097645526150283,
        fail_rate_density_per_year=365,
    )
    L19 = Line(
        "L19",
        B19,
        B20,
        0.938520130576714,
        0.84567888909964,
        fail_rate_density_per_year=365,
    )
    L20 = Line(
        "L20",
        B20,
        B21,
        0.255500593984287,
        0.298489582813389,
        fail_rate_density_per_year=365,
    )
    L21 = Line(
        "L21",
        B21,
        B22,
        0.442306156472432,
        0.584812470675146,
        fail_rate_density_per_year=365,
    )
    L22 = Line(
        "L22",
        B3,
        B23,
        0.281518603188548,
        0.192358566850685,
        fail_rate_density_per_year=365,
    )
    L23 = Line(
        "L23",
        B23,
        B24,
        0.560291900849547,
        0.442430943087321,
        fail_rate_density_per_year=365,
    )
    L24 = Line(
        "L24",
        B24,
        B25,
        0.559044034700662,
        0.437439478491779,
        fail_rate_density_per_year=365,
    )
    L25 = Line(
        "L25",
        B6,
        B26,
        0.126658414111869,
        0.064514679897376,
        fail_rate_density_per_year=365,
    )
    L26 = Line(
        "L26",
        B26,
        B27,
        0.177321779756616,
        0.090283115871859,
        fail_rate_density_per_year=365,
    )
    L27 = Line(
        "L27",
        B27,
        B28,
        0.660745125834823,
        0.582566311607152,
        fail_rate_density_per_year=365,
    )
    L28 = Line(
        "L28",
        B28,
        B29,
        0.501766978466822,
        0.437127511954558,
        fail_rate_density_per_year=365,
    )
    L29 = Line(
        "L29",
        B29,
        B30,
        0.316646035279672,
        0.161286699743439,
        fail_rate_density_per_year=365,
    )
    L30 = Line(
        "L30",
        B30,
        B31,
        0.60796038773697,
        0.600847550688323,
        fail_rate_density_per_year=365,
    )
    L31 = Line(
        "L31",
        B31,
        B32,
        0.193731219614459,
        0.225801379640814,
        fail_rate_density_per_year=365,
    )
    L32 = Line(
        "L32",
        B32,
        B33,
        0.212761178384962,
        0.330809316069521,
        fail_rate_density_per_year=365,
    )

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
        ]
    )

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_33Bus_network()
    fig = plot_topology(ps.buses, ps.lines, figsize=(40, 40))

    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test33.pdf"))
