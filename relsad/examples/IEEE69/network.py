from relsad.network.components import (
    Battery,
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
    ManualMainController,
    MicrogridMode,
    Production,
)
from relsad.network.systems import (
    Distribution,
    Microgrid,
    PowerSystem,
    Transmission,
)
from relsad.StatDist import NormalParameters, StatDist, StatDistType
from relsad.Table import Table
from relsad.Time import Time, TimeUnit
from relsad.visualization.plotting import plot_topology


def initialize_network(
    fail_rate_trafo: float = 0.007,
    fail_rate_line: float = 0.7,
    outage_time_trafo: Time = Time(8, TimeUnit.HOUR),
    microgrid_mode: MicrogridMode = MicrogridMode.SURVIVAL,
):

    line_stat_dist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    )

    C1 = ManualMainController(
        name="C1",
        sectioning_time=Time(1, TimeUnit.HOUR),
    )

    ps = PowerSystem(C1)

    B1 = Bus(
        name="B1",
        coordinate=[0, 0],
        fail_rate_per_year=0,
    )
    B2 = Bus(
        name="B2",
        coordinate=[1, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B3 = Bus(
        name="B3",
        coordinate=[2, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B4 = Bus(
        name="B4",
        coordinate=[3, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B5 = Bus(
        name="B5",
        coordinate=[4, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B6 = Bus(
        name="B6",
        coordinate=[5, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B7 = Bus(
        name="B7",
        coordinate=[6, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B8 = Bus(
        name="B8",
        coordinate=[7, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B9 = Bus(
        name="B9",
        coordinate=[8, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B10 = Bus(
        name="B10",
        coordinate=[9, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B11 = Bus(
        name="B11",
        coordinate=[10, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B12 = Bus(
        name="B12",
        coordinate=[11, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B13 = Bus(
        name="B13",
        coordinate=[12, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B14 = Bus(
        name="B14",
        coordinate=[13, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B15 = Bus(
        name="B15",
        coordinate=[14, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B16 = Bus(
        name="B16",
        coordinate=[15, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B17 = Bus(
        name="B17",
        coordinate=[16, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B18 = Bus(
        name="B18",
        coordinate=[17, 0.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B19 = Bus(
        name="B19",
        coordinate=[18, 0.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B20 = Bus(
        name="B20",
        coordinate=[19, 0.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B21 = Bus(
        name="B21",
        coordinate=[20, 0.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B22 = Bus(
        name="B22",
        coordinate=[21, 0.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B23 = Bus(
        name="B23",
        coordinate=[22, 0.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B24 = Bus(
        name="B24",
        coordinate=[23, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B25 = Bus(
        name="B25",
        coordinate=[24, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B26 = Bus(
        name="B26",
        coordinate=[25, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B27 = Bus(
        name="B27",
        coordinate=[26, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B28 = Bus(
        name="B28",
        coordinate=[3, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B29 = Bus(
        name="B29",
        coordinate=[4, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B30 = Bus(
        name="B30",
        coordinate=[5, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B31 = Bus(
        name="B31",
        coordinate=[6, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B32 = Bus(
        name="B32",
        coordinate=[7, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B33 = Bus(
        name="B33",
        coordinate=[8, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B34 = Bus(
        name="B34",
        coordinate=[9, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B35 = Bus(
        name="B35",
        coordinate=[10, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B36 = Bus(
        name="B36",
        coordinate=[3, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B37 = Bus(
        name="B37",
        coordinate=[4, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B38 = Bus(
        name="B38",
        coordinate=[5, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B39 = Bus(
        name="B39",
        coordinate=[6, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B40 = Bus(
        name="B40",
        coordinate=[7, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B41 = Bus(
        name="B41",
        coordinate=[8, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B42 = Bus(
        name="B42",
        coordinate=[9, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B43 = Bus(
        name="B43",
        coordinate=[10, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B44 = Bus(
        name="B44",
        coordinate=[11, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B45 = Bus(
        name="B45",
        coordinate=[12, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B46 = Bus(
        name="B46",
        coordinate=[13, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B47 = Bus(
        name="B47",
        coordinate=[4, -1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B48 = Bus(
        name="B48",
        coordinate=[5, -1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B49 = Bus(
        name="B49",
        coordinate=[6, -1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B50 = Bus(
        name="B50",
        coordinate=[7, -1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B51 = Bus(
        name="B51",
        coordinate=[8, 1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B52 = Bus(
        name="B52",
        coordinate=[9, 1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B53 = Bus(
        name="B53",
        coordinate=[9, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B54 = Bus(
        name="B54",
        coordinate=[10, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B55 = Bus(
        name="B55",
        coordinate=[11, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B56 = Bus(
        name="B56",
        coordinate=[12, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B57 = Bus(
        name="B57",
        coordinate=[13, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B58 = Bus(
        name="B58",
        coordinate=[14, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B59 = Bus(
        name="B59",
        coordinate=[15, -1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B60 = Bus(
        name="B60",
        coordinate=[16, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B61 = Bus(
        name="B61",
        coordinate=[17, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B62 = Bus(
        name="B62",
        coordinate=[18, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B63 = Bus(
        name="B63",
        coordinate=[19, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B64 = Bus(
        name="B64",
        coordinate=[20, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B65 = Bus(
        name="B65",
        coordinate=[21, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B66 = Bus(
        name="B66",
        coordinate=[11, 1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B67 = Bus(
        name="B67",
        coordinate=[12, 1],
        fail_rate_per_year=fail_rate_trafo,
    )

    # Microgrid:
    B68 = Bus(
        name="B68",
        coordinate=[16, 1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B69 = Bus(
        name="B69",
        coordinate=[17, 1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    B70 = Bus(
        name="B70",
        coordinate=[17, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B71 = Bus(
        name="B71",
        coordinate=[17, 1],
        fail_rate_per_year=fail_rate_trafo,
    )

    Battery(name="Bat1", bus=B68)
    Production(name="P1", bus=B70)
    Production(name="P2", bus=B71)

    # Lines, connections and impedances
    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=0.0005,
        x=0.0012,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=0.0005,
        x=0.0012,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B3,
        tbus=B4,
        r=0.0015,
        x=0.0036,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=0.0251,
        x=0.0294,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B5,
        tbus=B6,
        r=0.3660,
        x=0.1864,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L6 = Line(
        name="L6",
        fbus=B6,
        tbus=B7,
        r=0.3811,
        x=0.1941,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L7 = Line(
        name="L7",
        fbus=B7,
        tbus=B8,
        r=0.0922,
        x=0.0470,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L8 = Line(
        name="L8",
        fbus=B8,
        tbus=B9,
        r=0.0493,
        x=0.0251,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L9 = Line(
        name="L9",
        fbus=B9,
        tbus=B10,
        r=0.8190,
        x=0.2707,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L10 = Line(
        name="L10",
        fbus=B10,
        tbus=B11,
        r=0.1872,
        x=0.0619,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L11 = Line(
        name="L11",
        fbus=B11,
        tbus=B12,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L12 = Line(
        name="L12",
        fbus=B12,
        tbus=B13,
        r=1.0300,
        x=0.3400,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L13 = Line(
        name="L13",
        fbus=B13,
        tbus=B14,
        r=1.0440,
        x=0.3450,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L14 = Line(
        name="L14",
        fbus=B14,
        tbus=B15,
        r=1.0580,
        x=0.3496,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L15 = Line(
        name="L15",
        fbus=B15,
        tbus=B16,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L16 = Line(
        name="L16",
        fbus=B16,
        tbus=B17,
        r=0.3744,
        x=0.1238,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L17 = Line(
        name="L17",
        fbus=B17,
        tbus=B18,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L18 = Line(
        name="L18",
        fbus=B18,
        tbus=B19,
        r=0.3276,
        x=0.1083,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L19 = Line(
        name="L19",
        fbus=B19,
        tbus=B20,
        r=0.2106,
        x=0.0690,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L20 = Line(
        name="L20",
        fbus=B20,
        tbus=B21,
        r=0.3416,
        x=0.1129,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L21 = Line(
        name="L21",
        fbus=B21,
        tbus=B22,
        r=0.0140,
        x=0.0046,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L22 = Line(
        name="L22",
        fbus=B22,
        tbus=B23,
        r=0.1591,
        x=0.0526,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L23 = Line(
        name="L23",
        fbus=B23,
        tbus=B24,
        r=0.3463,
        x=0.1145,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L24 = Line(
        name="L24",
        fbus=B24,
        tbus=B25,
        r=0.7488,
        x=0.2475,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L25 = Line(
        name="L25",
        fbus=B25,
        tbus=B26,
        r=0.3089,
        x=0.1021,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L26 = Line(
        name="L26",
        fbus=B26,
        tbus=B27,
        r=0.1732,
        x=0.0572,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L27 = Line(
        name="L27",
        fbus=B3,
        tbus=B28,
        r=0.0044,
        x=0.0108,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L28 = Line(
        name="L28",
        fbus=B28,
        tbus=B29,
        r=0.0640,
        x=0.1565,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L29 = Line(
        name="L29",
        fbus=B29,
        tbus=B30,
        r=0.3978,
        x=0.1315,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L30 = Line(
        name="L30",
        fbus=B30,
        tbus=B31,
        r=0.0702,
        x=0.0232,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L31 = Line(
        name="L31",
        fbus=B31,
        tbus=B32,
        r=0.3510,
        x=0.1160,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L32 = Line(
        name="L32",
        fbus=B32,
        tbus=B33,
        r=0.8390,
        x=0.2816,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L33 = Line(
        name="L33",
        fbus=B33,
        tbus=B34,
        r=1.7080,
        x=0.5646,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L34 = Line(
        name="L34",
        fbus=B34,
        tbus=B35,
        r=1.4740,
        x=0.4873,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L35 = Line(
        name="L35",
        fbus=B3,
        tbus=B36,
        r=0.0044,
        x=0.0108,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L36 = Line(
        name="L36",
        fbus=B36,
        tbus=B37,
        r=0.0640,
        x=0.11565,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L37 = Line(
        name="L37",
        fbus=B37,
        tbus=B38,
        r=0.1053,
        x=0.1230,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L38 = Line(
        name="L38",
        fbus=B38,
        tbus=B39,
        r=0.0304,
        x=0.0355,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L39 = Line(
        name="L39",
        fbus=B39,
        tbus=B40,
        r=0.0018,
        x=0.0021,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L40 = Line(
        name="L40",
        fbus=B40,
        tbus=B41,
        r=0.7283,
        x=0.8509,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L41 = Line(
        name="L41",
        fbus=B41,
        tbus=B42,
        r=0.31,
        x=0.3623,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L42 = Line(
        name="L42",
        fbus=B42,
        tbus=B43,
        r=0.0410,
        x=0.0478,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L43 = Line(
        name="L43",
        fbus=B43,
        tbus=B44,
        r=0.0092,
        x=0.0116,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L44 = Line(
        name="L44",
        fbus=B44,
        tbus=B45,
        r=0.1089,
        x=0.1373,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L45 = Line(
        name="L45",
        fbus=B45,
        tbus=B46,
        r=0.0009,
        x=0.0012,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L46 = Line(
        name="L46",
        fbus=B4,
        tbus=B47,
        r=0.0034,
        x=0.0084,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L47 = Line(
        name="L47",
        fbus=B47,
        tbus=B48,
        r=0.0851,
        x=0.2083,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L48 = Line(
        name="L48",
        fbus=B48,
        tbus=B49,
        r=0.2898,
        x=0.7091,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L49 = Line(
        name="L49",
        fbus=B49,
        tbus=B50,
        r=0.0822,
        x=0.2011,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L50 = Line(
        name="L50",
        fbus=B8,
        tbus=B51,
        r=0.0928,
        x=0.0473,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L51 = Line(
        name="L51",
        fbus=B51,
        tbus=B52,
        r=0.3319,
        x=0.1114,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L52 = Line(
        name="L52",
        fbus=B9,
        tbus=B53,
        r=0.1740,
        x=0.0886,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L53 = Line(
        name="L53",
        fbus=B53,
        tbus=B54,
        r=0.2030,
        x=0.1034,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L54 = Line(
        name="L54",
        fbus=B54,
        tbus=B55,
        r=0.2842,
        x=0.1447,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L55 = Line(
        name="L55",
        fbus=B55,
        tbus=B56,
        r=0.2813,
        x=0.1433,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L56 = Line(
        name="L56",
        fbus=B56,
        tbus=B57,
        r=1.5900,
        x=0.5337,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L57 = Line(
        name="L57",
        fbus=B57,
        tbus=B58,
        r=0.7837,
        x=0.2630,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L58 = Line(
        name="L58",
        fbus=B58,
        tbus=B59,
        r=0.3042,
        x=0.1006,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L59 = Line(
        name="L59",
        fbus=B59,
        tbus=B60,
        r=0.3861,
        x=0.1172,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L60 = Line(
        name="L60",
        fbus=B60,
        tbus=B61,
        r=0.5075,
        x=0.2585,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L61 = Line(
        name="L61",
        fbus=B61,
        tbus=B62,
        r=0.0974,
        x=0.0496,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L62 = Line(
        name="L62",
        fbus=B62,
        tbus=B63,
        r=0.1450,
        x=0.0738,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L63 = Line(
        name="L63",
        fbus=B63,
        tbus=B64,
        r=0.7105,
        x=0.3619,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L64 = Line(
        name="L64",
        fbus=B64,
        tbus=B65,
        r=1.0410,
        x=0.5302,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L65 = Line(
        name="L65",
        fbus=B11,
        tbus=B66,
        r=0.2012,
        x=0.0611,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L66 = Line(
        name="L66",
        fbus=B66,
        tbus=B67,
        r=0.0047,
        x=0.0014,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )

    # Microgrid:
    L67 = Line(
        name="L67",
        fbus=B16,
        tbus=B68,
        r=0.7394,
        x=0.2444,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L68 = Line(
        name="L68",
        fbus=B68,
        tbus=B69,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    ML3 = Line(
        name="ML3",
        fbus=B68,
        tbus=B70,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    ML4 = Line(
        name="ML4",
        fbus=B68,
        tbus=B71,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )

    # Backup lines:
    L69 = Line(
        name="L69",
        fbus=B11,
        tbus=B43,
        r=0.3042,
        x=0.1006,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
        capacity=5,
    )
    L70 = Line(
        name="L70",
        fbus=B17,
        tbus=B24,
        r=0.8390,
        x=0.2816,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
        capacity=5,
    )
    # L71 = Line(
    #     "L71",
    #     B15,
    #     B46,
    #     r=0.0,
    #     x=0.0,
    #     fail_rate_density_per_year=fail_rate_line,
    #     capacity=3,
    # )
    L72 = Line(
        name="L72",
        fbus=B50,
        tbus=B59,
        r=0.2012,
        x=0.0611,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
        capacity=5,
    )
    # L73 = Line(
    #     "L73",
    #     B27,
    #     B65,
    #     r=0.0,
    #     x=0.0,
    #     fail_rate_density_per_year=fail_rate_line,
    #     capacity=3,
    # )

    CircuitBreaker("E1", L1)
    CircuitBreaker("E2", L67)

    Disconnector("L1a", L1, B1)
    Disconnector("L1b", L1, B2)
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
    Disconnector("L67a", L67, B16)
    Disconnector("L67b", L67, B68)
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

    m = Microgrid(dn, L67, mode=microgrid_mode)
    m.add_buses([B68, B69, B70, B71])
    m.add_lines([L68, ML3, ML4])

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "IEEE69.pdf")
    )
