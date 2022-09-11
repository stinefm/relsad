import os

import numpy as np

from relsad.network.components import (
    Battery,
    Bus,
    CircuitBreaker,
    Disconnector,
    EVPark,
    ICTLine,
    ICTNode,
    IntelligentSwitch,
    Line,
    MainController,
    ManualMainController,
    MicrogridMode,
    Production,
    Sensor,
)
from relsad.network.systems import (
    Distribution,
    ICTNetwork,
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
    fail_rate_line: float = 0.07,
    fail_rate_intelligent_switch: float = 0.03,
    fail_rate_hardware: float = 0.2,
    fail_rate_software: float = 12,
    fail_rate_sensor: float = 0.023,
    fail_rate_ict_line: float = 0.07,
    p_fail_repair_new_signal: float = 1 - 0.95,
    p_fail_repair_reboot: float = 1 - 0.9,
    outage_time_trafo: Time = Time(8, TimeUnit.HOUR),
    include_microgrid: bool = True,
    include_production: bool = True,
    include_ICT: bool = True,
    include_ev: bool = True,
    v2g_flag: bool = True,
    ev_percentage: float = 0.47,
    ev_E_max: float = 0.07,
    include_backup: bool = True,
    microgrid_mode: MicrogridMode = MicrogridMode.SURVIVAL,
    line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
    ict_line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
):
    def num_ev_table_func(
        n_customers,
        ev_percentage=ev_percentage,
        daily_charge_frac=0.61,
    ):
        return Table(
            x=np.array(
                [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                ],
            ),
            y=np.array(
                [
                    0.52,
                    0.52,
                    0.52,
                    0.52,
                    0.52,
                    0.52,
                    0.52,
                    0.08,
                    0.08,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.28,
                    0.28,
                    0.28,
                    0.28,
                    0.42,
                    0.42,
                    0.42,
                    0.42,
                ]
            )
            * n_customers
            * ev_percentage
            * daily_charge_frac,
        )

    if include_ICT:

        # Controller
        ICTNController = ICTNode(
            name="ICTNController",
            coordinate=[0, 2],
        )
        # Sensors
        ICTNSL1 = ICTNode(
            name="ICTNSL1",
        )
        ICTNSL2 = ICTNode(
            name="ICTNSL2",
        )
        ICTNSL3 = ICTNode(
            name="ICTNSL3",
        )
        ICTNSL4 = ICTNode(
            name="ICTNSL4",
        )
        ICTNSL5 = ICTNode(
            name="ICTNSL5",
        )
        ict_nodes = [
            ICTNController,
            ICTNSL1,
            ICTNSL2,
            ICTNSL3,
            ICTNSL4,
            ICTNSL5,
        ]
        if include_backup:
            ICTNSL6 = ICTNode(
                name="ICTNSL6",
            )
            ict_nodes.append(ICTNSL6)

        # Intelligent switch
        ICTNISW1a = ICTNode(
            name="ICTNISW1a",
        )
        ICTNISW1b = ICTNode(
            name="ICTNISW1b",
        )
        ICTNISW2a = ICTNode(
            name="ICTNISW2a",
        )
        ICTNISW2b = ICTNode(
            name="ICTNISW2b",
        )
        ICTNISW3a = ICTNode(
            name="ICTNISW3a",
        )
        ICTNISW3b = ICTNode(
            name="ICTNISW3b",
        )
        ICTNISW4a = ICTNode(
            name="ICTNISW4a",
        )
        ICTNISW4b = ICTNode(
            name="ICTNISW4b",
        )
        ICTNISW5a = ICTNode(
            name="ICTNISW5a",
        )
        ICTNISW5b = ICTNode(
            name="ICTNISW5b",
        )
        ict_nodes.extend(
            [
                ICTNISW1a,
                ICTNISW1b,
                ICTNISW2a,
                ICTNISW2b,
                ICTNISW3a,
                ICTNISW3b,
                ICTNISW4a,
                ICTNISW4b,
                ICTNISW5a,
                ICTNISW5b,
            ]
        )
        if include_backup:
            ICTNISW6a = ICTNode(
                name="ICTNISW6a",
            )
            ICTNISW6b = ICTNode(
                name="ICTNISW6b",
            )
            ict_nodes.extend(
                [
                    ICTNISW6a,
                    ICTNISW6b,
                ]
            )

        # Auxillary ICT nodes

        ## Access nodes
        ICTNA1 = ICTNode(
            name="ICTNA1",
            coordinate=[0.5, 2.25],
        )
        ICTNA2 = ICTNode(
            name="ICTNA2",
            coordinate=[0.5, 2.0],
        )
        ICTNA3 = ICTNode(
            name="ICTNA3",
            coordinate=[0.75, 2.0],
        )
        ICTNA4 = ICTNode(
            name="ICTNA4",
            coordinate=[0.75, 2.25],
        )
        ICTNA5 = ICTNode(
            name="ICTNA5",
            coordinate=[2.25, 1.5],
        )
        ICTNA6 = ICTNode(
            name="ICTNA6",
            coordinate=[2.5, 1.5],
        )
        ICTNA7 = ICTNode(
            name="ICTNA7",
            coordinate=[2.5, 1.75],
        )
        ICTNA8 = ICTNode(
            name="ICTNA8",
            coordinate=[2.25, 1.75],
        )
        ict_nodes.extend(
            [
                ICTNA1,
                ICTNA2,
                ICTNA3,
                ICTNA4,
                ICTNA5,
                ICTNA6,
                ICTNA7,
                ICTNA8,
            ]
        )

        ## Network nodes
        ICTN1 = ICTNode(
            name="ICTN1",
            coordinate=[1.0, 1.75],
        )
        ICTN2 = ICTNode(
            name="ICTN2",
            coordinate=[1.25, 1.5],
        )
        ICTN3 = ICTNode(
            name="ICTN3",
            coordinate=[1.5, 1.75],
        )
        ICTN4 = ICTNode(
            name="ICTN4",
            coordinate=[1.75, 2.0],
        )
        ICTN5 = ICTNode(
            name="ICTN5",
            coordinate=[2.25, 1.75],
        )
        ICTN6 = ICTNode(
            name="ICTN6",
            coordinate=[2.5, 2.0],
        )
        ICTN7 = ICTNode(
            name="ICTN7",
            coordinate=[2.5, 2.25],
        )
        ICTN8 = ICTNode(
            name="ICTN8",
            coordinate=[2.25, 2.5],
        )
        ICTN9 = ICTNode(
            name="ICTN9",
            coordinate=[1.75, 2.5],
        )
        ICTN10 = ICTNode(
            name="ICTN10",
            coordinate=[1.5, 2.0],
        )
        ICTN11 = ICTNode(
            name="ICTN11",
            coordinate=[1.5, 2.5],
        )
        ICTN12 = ICTNode(
            name="ICTN12",
            coordinate=[1.25, 2.25],
        )
        ict_nodes.extend(
            [
                ICTN1,
                ICTN2,
                ICTN3,
                ICTN4,
                ICTN5,
                ICTN6,
                ICTN7,
                ICTN8,
                ICTN9,
                ICTN10,
                ICTN11,
                ICTN12,
            ]
        )

        ## Lines

        ### Controller
        ICTL1 = ICTLine(
            name="ICTL1",
            fnode=ICTNController,
            tnode=ICTNA1,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )

        ### Sensors
        ICTL2 = ICTLine(
            name="ICTL2",
            fnode=ICTNSL1,
            tnode=ICTNA2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL3 = ICTLine(
            name="ICTL3",
            fnode=ICTNSL2,
            tnode=ICTNA2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL4 = ICTLine(
            name="ICTL4",
            fnode=ICTNSL3,
            tnode=ICTNA5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL5 = ICTLine(
            name="ICTL5",
            fnode=ICTNSL4,
            tnode=ICTNA5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL6 = ICTLine(
            name="ICTL6",
            fnode=ICTNSL5,
            tnode=ICTNA6,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )

        ### Intelligent switches
        ICTL7 = ICTLine(
            name="ICTL7",
            fnode=ICTNISW1a,
            tnode=ICTNA2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL8 = ICTLine(
            name="ICTL8",
            fnode=ICTNISW1b,
            tnode=ICTNA2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL9 = ICTLine(
            name="ICTL9",
            fnode=ICTNISW2a,
            tnode=ICTNA2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL10 = ICTLine(
            name="ICTL10",
            fnode=ICTNISW2b,
            tnode=ICTNA5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL11 = ICTLine(
            name="ICTL11",
            fnode=ICTNISW3a,
            tnode=ICTNA5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL12 = ICTLine(
            name="ICTL12",
            fnode=ICTNISW3b,
            tnode=ICTNA5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL13 = ICTLine(
            name="ICTL13",
            fnode=ICTNISW4a,
            tnode=ICTNA6,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL14 = ICTLine(
            name="ICTL14",
            fnode=ICTNISW4b,
            tnode=ICTNA5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL15 = ICTLine(
            name="ICTL15",
            fnode=ICTNISW5a,
            tnode=ICTNA6,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL16 = ICTLine(
            name="ICTL16",
            fnode=ICTNISW5b,
            tnode=ICTNA6,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ict_lines = [
            ICTL1,
            ICTL2,
            ICTL3,
            ICTL4,
            ICTL5,
            ICTL6,
            ICTL7,
            ICTL8,
            ICTL9,
            ICTL10,
            ICTL11,
            ICTL12,
            ICTL13,
            ICTL14,
            ICTL15,
            ICTL16,
        ]
        if include_backup:
            ICTL17 = ICTLine(
                name="ICTL17",
                fnode=ICTNSL6,
                tnode=ICTNA6,
                repair_time_dist=ict_line_repair_time_stat_dist,
                fail_rate_per_year=fail_rate_ict_line,
            )
            ICTL18 = ICTLine(
                name="ICTL18",
                fnode=ICTNISW6a,
                tnode=ICTNA6,
                repair_time_dist=ict_line_repair_time_stat_dist,
                fail_rate_per_year=fail_rate_ict_line,
            )
            ICTL19 = ICTLine(
                name="ICTL19",
                fnode=ICTNISW6b,
                tnode=ICTNA6,
                repair_time_dist=ict_line_repair_time_stat_dist,
                fail_rate_per_year=fail_rate_ict_line,
            )
            ict_lines.extend(
                [
                    ICTL17,
                    ICTL18,
                    ICTL19,
                ]
            )

        ### Access lines
        ICTL20 = ICTLine(
            name="ICTL20",
            fnode=ICTNA1,
            tnode=ICTNA2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL21 = ICTLine(
            name="ICTL21",
            fnode=ICTNA2,
            tnode=ICTNA3,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL22 = ICTLine(
            name="ICTL22",
            fnode=ICTNA1,
            tnode=ICTNA4,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL23 = ICTLine(
            name="ICTL23",
            fnode=ICTNA5,
            tnode=ICTNA6,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL24 = ICTLine(
            name="ICTL24",
            fnode=ICTNA6,
            tnode=ICTNA7,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL25 = ICTLine(
            name="ICTL25",
            fnode=ICTNA5,
            tnode=ICTNA8,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ict_lines.extend(
            [
                ICTL20,
                ICTL21,
                ICTL22,
                ICTL23,
                ICTL24,
                ICTL25,
            ]
        )

        ### Network lines
        ICTL26 = ICTLine(
            name="ICTL26",
            fnode=ICTNA3,
            tnode=ICTN1,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL27 = ICTLine(
            name="ICTL27",
            fnode=ICTN1,
            tnode=ICTN2,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL28 = ICTLine(
            name="ICTL28",
            fnode=ICTN2,
            tnode=ICTNA8,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL29 = ICTLine(
            name="ICTL29",
            fnode=ICTN2,
            tnode=ICTN3,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL30 = ICTLine(
            name="ICTL30",
            fnode=ICTN2,
            tnode=ICTN10,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL31 = ICTLine(
            name="ICTL31",
            fnode=ICTN3,
            tnode=ICTN4,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL32 = ICTLine(
            name="ICTL32",
            fnode=ICTN4,
            tnode=ICTN5,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL33 = ICTLine(
            name="ICTL33",
            fnode=ICTN4,
            tnode=ICTN7,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL34 = ICTLine(
            name="ICTL34",
            fnode=ICTN4,
            tnode=ICTN8,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL35 = ICTLine(
            name="ICTL35",
            fnode=ICTN4,
            tnode=ICTN10,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL36 = ICTLine(
            name="ICTL36",
            fnode=ICTN5,
            tnode=ICTN6,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL37 = ICTLine(
            name="ICTL37",
            fnode=ICTN5,
            tnode=ICTNA7,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL38 = ICTLine(
            name="ICTL38",
            fnode=ICTN6,
            tnode=ICTN7,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL39 = ICTLine(
            name="ICTL39",
            fnode=ICTN8,
            tnode=ICTN9,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL40 = ICTLine(
            name="ICTL40",
            fnode=ICTN9,
            tnode=ICTN10,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL41 = ICTLine(
            name="ICTL41",
            fnode=ICTN9,
            tnode=ICTN11,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL42 = ICTLine(
            name="ICTL42",
            fnode=ICTN11,
            tnode=ICTN12,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ICTL43 = ICTLine(
            name="ICTL43",
            fnode=ICTN12,
            tnode=ICTNA4,
            repair_time_dist=ict_line_repair_time_stat_dist,
            fail_rate_per_year=fail_rate_ict_line,
        )
        ict_lines.extend(
            [
                ICTL26,
                ICTL27,
                ICTL28,
                ICTL29,
                ICTL30,
                ICTL31,
                ICTL32,
                ICTL33,
                ICTL34,
                ICTL35,
                ICTL36,
                ICTL37,
                ICTL38,
                ICTL39,
                ICTL40,
                ICTL41,
                ICTL42,
                ICTL43,
            ]
        )

    if include_ICT:
        C1 = MainController(
            name="C1",
            ict_node=ICTNController,
            hardware_fail_rate_per_year=fail_rate_hardware,
            software_fail_rate_per_year=fail_rate_software,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
    else:
        C1 = ManualMainController(
            name="C1",
            sectioning_time=Time(1, TimeUnit.HOUR),
        )

    ps = PowerSystem(C1)
    if include_ICT:
        ict_network = ICTNetwork(ps)
        ict_network.add_nodes(ict_nodes)
        ict_network.add_lines(ict_lines)

    ## Transmission network bus
    B1 = Bus(
        name="B1",
        n_customers=0,
        coordinate=[0, 0],
        fail_rate_per_year=0,
    )

    ## Distribution network
    B2 = Bus(
        name="B2",
        n_customers=1,
        coordinate=[1, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B3 = Bus(
        name="B3",
        n_customers=100,
        coordinate=[2, 1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B4 = Bus(
        name="B4",
        n_customers=50,
        coordinate=[2, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B5 = Bus(
        name="B5",
        n_customers=90,
        coordinate=[3, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B6 = Bus(
        name="B6",
        n_customers=3,
        coordinate=[3, 1],
        fail_rate_per_year=fail_rate_trafo,
    )

    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B2,
        tbus=B4,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B3,
        tbus=B6,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )

    if include_backup:
        L6 = Line(
            name="L6",
            fbus=B4,
            tbus=B6,
            r=0.7114,
            x=0.2351,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_repair_time_stat_dist,
            capacity=6,
        )

    CircuitBreaker("E1", L1)

    DL1a = Disconnector("L1a", L1, B1)
    DL1b = Disconnector("L1b", L1, B2)
    DL2a = Disconnector("L2a", L2, B2)
    DL2b = Disconnector("L2b", L2, B3)
    DL3a = Disconnector("L3a", L3, B2)
    DL3b = Disconnector("L3b", L3, B4)
    DL4a = Disconnector("L4a", L4, B4)
    DL4b = Disconnector("L4b", L4, B5)
    DL5a = Disconnector("L5a", L5, B3)
    DL5b = Disconnector("L5b", L5, B6)

    if include_backup:
        DL6a = Disconnector("L6a", L6, B4)
        DL6b = Disconnector("L6b", L6, B6)

        L6.set_backup()

    if include_ICT:

        Sensor(
            name="SL1",
            line=L1,
            ict_node=ICTNSL1,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL2",
            line=L2,
            ict_node=ICTNSL2,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL3",
            line=L3,
            ict_node=ICTNSL3,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL4",
            line=L4,
            ict_node=ICTNSL4,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL5",
            line=L5,
            ict_node=ICTNSL5,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )

        if include_backup:
            Sensor(
                name="SL6",
                line=L6,
                ict_node=ICTNSL6,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

        IntelligentSwitch(
            name="RL1a",
            disconnector=DL1a,
            ict_node=ICTNISW1a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL1b",
            disconnector=DL1b,
            ict_node=ICTNISW1b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL2a",
            disconnector=DL2a,
            ict_node=ICTNISW2a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL2b",
            disconnector=DL2b,
            ict_node=ICTNISW2b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL3a",
            disconnector=DL3a,
            ict_node=ICTNISW3a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL3b",
            disconnector=DL3b,
            ict_node=ICTNISW3b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL4a",
            disconnector=DL4a,
            ict_node=ICTNISW4a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL4b",
            disconnector=DL4b,
            ict_node=ICTNISW4b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL5a",
            disconnector=DL5a,
            ict_node=ICTNISW5a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL5b",
            disconnector=DL5b,
            ict_node=ICTNISW5b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )

        if include_backup:
            IntelligentSwitch(
                name="RL6a",
                disconnector=DL6a,
                ict_node=ICTNISW6a,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )
            IntelligentSwitch(
                name="RL6b",
                disconnector=DL6b,
                ict_node=ICTNISW6b,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )

    if include_ev:
        EVPark(
            name="EV1",
            bus=B5,
            num_ev_dist=num_ev_table_func(B3.n_customers),
            v2g_flag=v2g_flag,
            E_max=ev_E_max,
        )

    tn = Transmission(parent_network=ps, trafo_bus=B1)

    dn = Distribution(parent_network=tn, connected_line=L1)

    if include_microgrid:
        M1 = Bus(
            "M1",
            n_customers=0,
            coordinate=[2, -1],
            fail_rate_per_year=fail_rate_trafo,
        )
        M2 = Bus(
            "M2",
            n_customers=0,
            coordinate=[3, -2],
            fail_rate_per_year=fail_rate_trafo,
        )
        M3 = Bus(
            "M3",
            n_customers=40,
            coordinate=[3, -1],
            fail_rate_per_year=fail_rate_trafo,
        )

        Battery(name="Bat1", bus=M1)
        Production(name="P1", bus=M2)

        ML1 = Line(
            name="ML1",
            fbus=M1,
            tbus=M2,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_repair_time_stat_dist,
        )
        ML2 = Line(
            name="ML2",
            fbus=M1,
            tbus=M3,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_repair_time_stat_dist,
        )

        L7 = Line(
            name="L7",
            fbus=B2,
            tbus=M1,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_repair_time_stat_dist,
        )

        CircuitBreaker(name="E2", line=L7)

        DL7a = Disconnector(
            name="L7a",
            line=L7,
            bus=B2,
        )
        DL7b = Disconnector(
            name="L7b",
            line=L7,
            bus=M1,
        )
        DML1a = Disconnector(
            name="ML1a",
            line=ML1,
            bus=M1,
        )
        DML1b = Disconnector(
            name="ML1b",
            line=ML1,
            bus=M2,
        )
        DML2a = Disconnector(
            name="ML2a",
            line=ML2,
            bus=M1,
        )
        DML2b = Disconnector(
            name="ML2b",
            line=ML2,
            bus=M3,
        )

        if include_ICT:
            Sensor(
                name="SL7",
                line=L7,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

            Sensor(
                name="SML1",
                line=ML1,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )
            Sensor(
                name="SML2",
                line=ML2,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

            IntelligentSwitch(
                name="RL7a",
                disconnector=DL7a,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )
            IntelligentSwitch(
                name="RL7b",
                disconnector=DL7b,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )

            IntelligentSwitch(
                name="RML1a",
                disconnector=DML1a,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )
            IntelligentSwitch(
                name="RML1b",
                disconnector=DML1b,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )
            IntelligentSwitch(
                name="RML2a",
                disconnector=DML2a,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )
            IntelligentSwitch(
                name="RML2b",
                disconnector=DML2b,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )

        m = Microgrid(
            distribution_network=dn,
            connected_line=L7,
            mode=microgrid_mode,
        )

        m.add_buses([M1, M2, M3])
        m.add_lines([ML1, ML2])

    dn.add_buses([B2, B3, B4, B5, B6])
    if include_backup:
        dn.add_lines([L2, L3, L4, L5, L6])
    else:
        dn.add_lines([L2, L3, L4, L5])

    return ps


if __name__ == "__main__":
    ps = initialize_network(
        include_microgrid=False,
        include_production=False,
        include_ICT=True,
        include_ev=False,
        include_backup=True,
    )
    fig = plot_topology(
        buses=ps.buses,
        lines=ps.lines,
        bus_text=True,
        line_text=True,
        ict_nodes=ps.ict_nodes,
        ict_lines=ps.ict_lines,
        text_dx=(0.05, -0.2),
        ncol=4,
    )

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "CINELDI.pdf",
        )
    )
    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "CINELDI.png",
        ),
        dpi=600,
    )
