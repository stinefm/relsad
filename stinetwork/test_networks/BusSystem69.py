from stinetwork.network.components import Bus, CircuitBreaker, Disconnector, Line
from stinetwork.network.systems import Distribution, PowerSystem, Transmission
from stinetwork.visualization.plotting import plot_topology


def initialize_69Bus_network():
    ps = PowerSystem()

    B1 = Bus("B1", coordinate=[0, 0], fail_rate_per_year=0)
    B2 = Bus("B2", coordinate=[0, -1], fail_rate_per_year=0.008)
    B3 = Bus("B3", coordinate=[0, -2], fail_rate_per_year=0.008)
    B4 = Bus("B4", coordinate=[0, -3], fail_rate_per_year=0.008)
    B5 = Bus("B5", coordinate=[0, -4], fail_rate_per_year=0.008)
    B6 = Bus("B6", coordinate=[0, -5], fail_rate_per_year=0.008)
    B7 = Bus("B7", coordinate=[0, -6], fail_rate_per_year=0.008)
    B8 = Bus("B8", coordinate=[0, -7], fail_rate_per_year=0.008)
    B9 = Bus("B9", coordinate=[0, -8], fail_rate_per_year=0.008)
    B10 = Bus("B10", coordinate=[0, -9], fail_rate_per_year=0.008)
    B11 = Bus("B11", coordinate=[0, -10], fail_rate_per_year=0.008)
    B12 = Bus("B12", coordinate=[0, -11], fail_rate_per_year=0.008)
    B13 = Bus("B13", coordinate=[0, -12], fail_rate_per_year=0.008)
    B14 = Bus("B14", coordinate=[0, -13], fail_rate_per_year=0.008)
    B15 = Bus("B15", coordinate=[0, -14], fail_rate_per_year=0.008)
    B16 = Bus("B16", coordinate=[0, -15], fail_rate_per_year=0.008)
    B17 = Bus("B17", coordinate=[0, -16], fail_rate_per_year=0.008)
    B18 = Bus("B18", coordinate=[0, -17], fail_rate_per_year=0.008)
    B19 = Bus("B19", coordinate=[0, -18], fail_rate_per_year=0.008)
    B20 = Bus("B20", coordinate=[0, -19], fail_rate_per_year=0.008)
    B21 = Bus("B21", coordinate=[0, -20], fail_rate_per_year=0.008)
    B22 = Bus("B22", coordinate=[0, -21], fail_rate_per_year=0.008)
    B23 = Bus("B23", coordinate=[0, -22], fail_rate_per_year=0.008)
    B24 = Bus("B24", coordinate=[0, -23], fail_rate_per_year=0.008)
    B25 = Bus("B25", coordinate=[0, -24], fail_rate_per_year=0.008)
    B26 = Bus("B26", coordinate=[0, -25], fail_rate_per_year=0.008)
    B27 = Bus("B27", coordinate=[0, -26], fail_rate_per_year=0.008)
    B28 = Bus("B28", coordinate=[-2, -3], fail_rate_per_year=0.008)
    B29 = Bus("B29", coordinate=[-2, -4], fail_rate_per_year=0.008)
    B30 = Bus("B30", coordinate=[-2, -5], fail_rate_per_year=0.008)
    B31 = Bus("B31", coordinate=[-2, -6], fail_rate_per_year=0.008)
    B32 = Bus("B32", coordinate=[-2, -7], fail_rate_per_year=0.008)
    B33 = Bus("B33", coordinate=[-2, -8], fail_rate_per_year=0.008)
    B34 = Bus("B34", coordinate=[-2, -9], fail_rate_per_year=0.008)
    B35 = Bus("B35", coordinate=[-2, -10], fail_rate_per_year=0.008)
    B36 = Bus("B36", coordinate=[2, -3], fail_rate_per_year=0.008)
    B37 = Bus("B37", coordinate=[2, -4], fail_rate_per_year=0.008)
    B38 = Bus("B38", coordinate=[2, -5], fail_rate_per_year=0.008)
    B39 = Bus("B39", coordinate=[2, -6], fail_rate_per_year=0.008)
    B40 = Bus("B40", coordinate=[2, -7], fail_rate_per_year=0.008)
    B41 = Bus("B41", coordinate=[2, -8], fail_rate_per_year=0.008)
    B42 = Bus("B42", coordinate=[2, -9], fail_rate_per_year=0.008)
    B43 = Bus("B43", coordinate=[2, -10], fail_rate_per_year=0.008)
    B44 = Bus("B44", coordinate=[2, -11], fail_rate_per_year=0.008)
    B45 = Bus("B45", coordinate=[2, -12], fail_rate_per_year=0.008)
    B46 = Bus("B46", coordinate=[2, -13], fail_rate_per_year=0.008)
    B47 = Bus("B47", coordinate=[-1, -4], fail_rate_per_year=0.008)
    B48 = Bus("B48", coordinate=[-1, -5], fail_rate_per_year=0.008)
    B49 = Bus("B49", coordinate=[-1, -6], fail_rate_per_year=0.008)
    B50 = Bus("B50", coordinate=[-1, -7], fail_rate_per_year=0.008)
    B51 = Bus("B51", coordinate=[1, -8], fail_rate_per_year=0.008)
    B52 = Bus("B52", coordinate=[1, -9], fail_rate_per_year=0.008)
    B53 = Bus("B53", coordinate=[-1, -9], fail_rate_per_year=0.008)
    B54 = Bus("B54", coordinate=[-1, -10], fail_rate_per_year=0.008)
    B55 = Bus("B55", coordinate=[-1, -11], fail_rate_per_year=0.008)
    B56 = Bus("B56", coordinate=[-1, -12], fail_rate_per_year=0.008)
    B57 = Bus("B57", coordinate=[-1, -13], fail_rate_per_year=0.008)
    B58 = Bus("B58", coordinate=[-1, -14], fail_rate_per_year=0.008)
    B59 = Bus("B59", coordinate=[-1, -15], fail_rate_per_year=0.008)
    B60 = Bus("B60", coordinate=[-1, -16], fail_rate_per_year=0.008)
    B61 = Bus("B61", coordinate=[-1, -17], fail_rate_per_year=0.008)
    B62 = Bus("B62", coordinate=[-1, -18], fail_rate_per_year=0.008)
    B63 = Bus("B63", coordinate=[-1, -19], fail_rate_per_year=0.008)
    B64 = Bus("B64", coordinate=[-1, -20], fail_rate_per_year=0.008)
    B65 = Bus("B65", coordinate=[-1, -21], fail_rate_per_year=0.008)
    B66 = Bus("B66", coordinate=[1, -11], fail_rate_per_year=0.008)
    B67 = Bus("B67", coordinate=[1, -12], fail_rate_per_year=0.008)
    B68 = Bus("B68", coordinate=[1, -14], fail_rate_per_year=0.008)
    B69 = Bus("B69", coordinate=[1, -15], fail_rate_per_year=0.008)

    # M1 = Bus("M1", coordinate=[], fail_rate_per_year=365)
    # M2 = Bus("M2", coordinate=[], fail_rate_per_year=365)
    # M3 = Bus("M3", coordinate=[], fail_rate_per_year=365)

    # Lines, connections and impedances
    L1 = Line("L1", B1, B2, 3.11963e-06, 7.4871e-06, fail_rate_density_per_year=0.08)
    L2 = Line("L2", B2, B3, 3.11963e-06, 7.4871e-06, fail_rate_density_per_year=0.08)
    L3 = Line("L3", B3, B4, 9.35888e-06, 2.24613e-05, fail_rate_density_per_year=0.08)
    L4 = Line("L4", B4, B5, 0.000156605, 0.000183434, fail_rate_density_per_year=0.08)
    L5 = Line("L5", B5, B6, 0.002283567, 0.001162997, fail_rate_density_per_year=0.08)
    L6 = Line("L6", B6, B7, 0.002377779, 0.001211039, fail_rate_density_per_year=0.08)
    L7 = Line("L7", B7, B8, 0.000575259, 0.000293245, fail_rate_density_per_year=0.08)
    L8 = Line("L8", B8, B9, 0.000307595, 0.000156605, fail_rate_density_per_year=0.08)
    L9 = Line("L9", B9, B10, 0.005109948, 0.001688966, fail_rate_density_per_year=0.08)
    L10 = Line(
        "L10", B10, B11, 0.001167988, 0.000431132, fail_rate_density_per_year=0.08
    )
    L11 = Line(
        "L11", B11, B12, 0.004438605, 0.001466848, fail_rate_density_per_year=0.08
    )
    L12 = Line(
        "L12", B12, B13, 0.00642643, 0.002121346, fail_rate_density_per_year=0.08
    )
    L13 = Line(
        "L13", B13, B14, 0.00651378, 0.002152542, fail_rate_density_per_year=0.08
    )
    L14 = Line(
        "L14", B14, B15, 0.00660113, 0.002181243, fail_rate_density_per_year=0.08
    )
    L15 = Line(
        "L15", B15, B16, 0.001226637, 0.000405551, fail_rate_density_per_year=0.08
    )
    L16 = Line(
        "L16", B16, B17, 0.002335976, 0.00077242, fail_rate_density_per_year=0.08
    )
    L17 = Line(
        "L17", B17, B18, 2.93245e-05, 9.9828e-06, fail_rate_density_per_year=0.08
    )
    L18 = Line(
        "L18", B18, B19, 0.002043979, 0.000675711, fail_rate_density_per_year=0.08
    )
    L19 = Line(
        "L19", B19, B20, 0.001313987, 0.000430508, fail_rate_density_per_year=0.08
    )
    L20 = Line(
        "L20", B20, B21, 0.002131329, 0.000704412, fail_rate_density_per_year=0.08
    )
    L21 = Line(
        "L21", B21, B22, 8.73495e-05, 2.87006e-05, fail_rate_density_per_year=0.08
    )
    L22 = Line(
        "L22", B22, B23, 0.000992665, 0.000328185, fail_rate_density_per_year=0.08
    )
    L23 = Line(
        "L23", B23, B24, 0.002160653, 0.000714394, fail_rate_density_per_year=0.08
    )
    L24 = Line(
        "L24", B24, B25, 0.004671953, 0.001712675, fail_rate_density_per_year=0.08
    )
    L25 = Line(
        "L25", B25, B26, 0.001927305, 0.000637028, fail_rate_density_per_year=0.08
    )
    L26 = Line(
        "L26", B26, B27, 0.001080639, 0.000356885, fail_rate_density_per_year=0.08
    )
    L27 = Line(
        "L27", B3, B28, 2.74527e-05, 6.73839e-05, fail_rate_density_per_year=0.08
    )
    L28 = Line(
        "L28", B28, B29, 0.000399312, 0.000976443, fail_rate_density_per_year=0.08
    )
    L29 = Line(
        "L29", B29, B30, 0.002481975, 0.000820462, fail_rate_density_per_year=0.08
    )
    L30 = Line(
        "L30", B30, B31, 0.000437996, 0.000144751, fail_rate_density_per_year=0.08
    )
    L31 = Line(
        "L31", B31, B32, 0.002189978, 0.000723753, fail_rate_density_per_year=0.08
    )
    L32 = Line(
        "L32", B32, B33, 0.005234733, 0.001756974, fail_rate_density_per_year=0.08
    )
    L33 = Line(
        "L33", B33, B34, 0.010656644, 0.003522682, fail_rate_density_per_year=0.08
    )
    L34 = Line(
        "L34", B34, B35, 0.009196659, 0.002915603, fail_rate_density_per_year=0.08
    )
    L35 = Line(
        "L35", B3, B36, 2.74527e-05, 6.73839e-05, fail_rate_density_per_year=0.08
    )
    L36 = Line(
        "L36", B36, B37, 0.000399312, 0.000976443, fail_rate_density_per_year=0.08
    )
    L37 = Line(
        "L37", B37, B38, 0.000656993, 0.000767428, fail_rate_density_per_year=0.08
    )
    L38 = Line(
        "L38", B38, B39, 0.000189673, 0.000221493, fail_rate_density_per_year=0.08
    )
    L39 = Line(
        "L39", B39, B40, 1.12307e-05, 1.31024e-05, fail_rate_density_per_year=0.08
    )
    L40 = Line(
        "L40", B40, B41, 0.004544048, 0.00530898, fail_rate_density_per_year=0.08
    )
    L41 = Line(
        "L41", B41, B42, 0.001934168, 0.002260481, fail_rate_density_per_year=0.08
    )
    L42 = Line(
        "L42", B42, B43, 0.000255809, 0.000298236, fail_rate_density_per_year=0.08
    )
    L43 = Line(
        "L43", B43, B44, 5.74011e-05, 7.23753e-05, fail_rate_density_per_year=0.08
    )
    L44 = Line(
        "L44", B44, B45, 0.000679455, 0.000856649, fail_rate_density_per_year=0.08
    )
    L45 = Line(
        "L45", B45, B46, 5.61533e-06, 7.4871e-06, fail_rate_density_per_year=0.08
    )
    L46 = Line(
        "L46", B4, B47, 2.12135e-05, 5.24097e-05, fail_rate_density_per_year=0.08
    )
    L47 = Line(
        "L47", B47, B48, 0.00053096, 0.001299636, fail_rate_density_per_year=0.08
    )
    L48 = Line(
        "L48", B48, B49, 0.001808135, 0.004424254, fail_rate_density_per_year=0.08
    )
    L49 = Line(
        "L49", B49, B50, 0.000512867, 0.001254714, fail_rate_density_per_year=0.08
    )
    L50 = Line(
        "L50", B8, B51, 0.000579003, 0.000295117, fail_rate_density_per_year=0.08
    )
    L51 = Line(
        "L51", B51, B52, 0.002070808, 0.000695053, fail_rate_density_per_year=0.08
    )
    L52 = Line("L52", B9, B53, 0.00108563, 0.000552798, fail_rate_density_per_year=0.08)
    L53 = Line(
        "L53", B53, B54, 0.001266568, 0.000645139, fail_rate_density_per_year=0.08
    )
    L54 = Line(
        "L54", B54, B55, 0.001773196, 0.00090282, fail_rate_density_per_year=0.08
    )
    L55 = Line(
        "L55", B55, B56, 0.001755102, 0.000894085, fail_rate_density_per_year=0.08
    )
    L56 = Line(
        "L56", B56, B57, 0.009920412, 0.003329889, fail_rate_density_per_year=0.08
    )
    L57 = Line(
        "L57", B57, B58, 0.004889702, 0.001640924, fail_rate_density_per_year=0.08
    )
    L58 = Line(
        "L58", B58, B59, 0.001897981, 0.000627669, fail_rate_density_per_year=0.08
    )
    L59 = Line(
        "L59", B59, B60, 0.002408976, 0.00073124, fail_rate_density_per_year=0.08
    )
    L60 = Line(
        "L60", B60, B61, 0.003166421, 0.001612847, fail_rate_density_per_year=0.08
    )
    L61 = Line(
        "L61", B61, B62, 0.000607703, 0.000309467, fail_rate_density_per_year=0.08
    )
    L62 = Line(
        "L62", B62, B63, 0.000904692, 0.000460457, fail_rate_density_per_year=0.08
    )
    L63 = Line(
        "L63", B63, B64, 0.004432989, 0.002257986, fail_rate_density_per_year=0.08
    )
    L64 = Line(
        "L64", B64, B65, 0.006495062, 0.003308052, fail_rate_density_per_year=0.08
    )
    L65 = Line(
        "L65", B11, B66, 0.001255338, 0.000381218, fail_rate_density_per_year=0.08
    )
    L66 = Line(
        "L66", B66, B67, 2.93245e-05, 8.73495e-06, fail_rate_density_per_year=0.08
    )
    L67 = Line(
        "L67", B12, B68, 0.004613304, 0.001524873, fail_rate_density_per_year=0.08
    )
    L68 = Line(
        "L68", B68, B69, 2.93245e-05, 9.9828e-06, fail_rate_density_per_year=0.08
    )

    L69 = Line("L69", B11, B43, 0.0, 1.0e-08, fail_rate_density_per_year=0.08)
    L70 = Line("L70", B13, B21, 0.0, 1.0e-08, fail_rate_density_per_year=0.08)
    L71 = Line("L71", B15, B46, 0.0, 1.0e-08, fail_rate_density_per_year=0.08)
    L72 = Line("L72", B50, B59, 0.0, 1.0e-08, fail_rate_density_per_year=0.08)
    L73 = Line("L73", B27, B65, 0.0, 1.0e-08, fail_rate_density_per_year=0.08)

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

    Disconnector("L67a", L67, B12)
    Disconnector("L67b", L67, B68)
    Disconnector("L68a", L68, B68)
    Disconnector("L68b", L68, B69)

    Disconnector("L69a", L69, B11)
    Disconnector("L69b", L69, B43)
    Disconnector("L70a", L70, B13)
    Disconnector("L70b", L70, B21)
    Disconnector("L71a", L71, B15)
    Disconnector("L71b", L71, B46)
    Disconnector("L72a", L72, B50)
    Disconnector("L72b", L72, B59)
    Disconnector("L73a", L73, B27)
    Disconnector("L73b", L73, B65)

    L69.set_backup()
    L70.set_backup()
    L71.set_backup()
    L72.set_backup()
    L73.set_backup()

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
            B68,
            B69,
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
            L67,
            L68,
            L69,
            L70,
            L71,
            L72,
            L73,
        ]
    )

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_69Bus_network()
    fig = plot_topology(ps.buses, ps.lines, figsize=(40, 40))

    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test69.pdf"))
