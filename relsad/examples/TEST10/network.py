import os

import numpy as np

from relsad.network.components import (
    Battery,
    Bus,
    CircuitBreaker,
    Disconnector,
    EVPark,
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
    fail_rate_intelligent_switch: float = 1000,
    fail_rate_hardware: float = 0.2,
    fail_rate_software: float = 12,
    fail_rate_sensor: float = 0.023,
    p_fail_repair_new_signal: float = 1 - 0.95,
    p_fail_repair_reboot: float = 1 - 0.9,
    include_microgrid: bool = True,
    include_production: bool = True,
    include_ICT: bool = True,
    include_ev: bool = True,
    v2g_flag: bool = True,
    include_backup: bool = True,
    line_repair_time_stat_dist=StatDist(
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
        ev_percentage=0.47,
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
        C1 = MainController(
            "C1",
            hardware_fail_rate_per_year=fail_rate_hardware,
            software_fail_rate_per_year=fail_rate_software,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
    else:
        C1 = ManualMainController(
            name="C1",
            sectioning_time=Time(0, TimeUnit.HOUR),
        )

    ps = PowerSystem(C1)

    ## Transmission network
    B1 = Bus("B1", n_customers=0, coordinate=[0, 0], fail_rate_per_year=0)

    B2 = Bus(
        "B2",
        n_customers=1,
        coordinate=[1, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B3 = Bus(
        "B3",
        n_customers=26,
        coordinate=[2, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B4 = Bus(
        "B4",
        n_customers=26,
        coordinate=[3, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B5 = Bus(
        "B5",
        n_customers=1,
        coordinate=[4, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B6 = Bus(
        "B6",
        n_customers=26,
        coordinate=[5, 0],
        fail_rate_per_year=fail_rate_trafo,
    )

    B7 = Bus(
        "B7",
        n_customers=26,
        coordinate=[3, 1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B8 = Bus(
        "B8",
        n_customers=1,
        coordinate=[4, 1],
        fail_rate_per_year=fail_rate_trafo,
    )

    B9 = Bus(
        "B9",
        n_customers=26,
        coordinate=[5, 1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B10 = Bus(
        "B10",
        n_customers=1,
        coordinate=[6, 1],
        fail_rate_per_year=fail_rate_trafo,
    )

    L1 = Line(
        "L1",
        B1,
        B2,
        r=0.0922,
        x=0.0470,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B2,
        B3,
        r=0.4930,
        x=0.2511,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B3,
        B4,
        r=0.3660,
        x=0.1864,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        r=0.3811,
        x=0.1941,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B5,
        B6,
        r=0.8190,
        x=0.7070,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )

    L6 = Line(
        "L6",
        B3,
        B7,
        r=0.8190,
        x=0.7070,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )
    L7 = Line(
        "L7",
        B7,
        B8,
        r=0.8190,
        x=0.7070,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )

    L8 = Line(
        "L8",
        B4,
        B9,
        r=0.8190,
        x=0.7070,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )
    L9 = Line(
        "L9",
        B9,
        B10,
        r=0.8190,
        x=0.7070,
        repair_time_dist=line_repair_time_stat_dist,
        fail_rate_density_per_year=fail_rate_line,
    )

    if include_backup:
        L10 = Line(
            "L10",
            B4,
            B8,
            r=0.7114,
            x=0.2351,
            repair_time_dist=line_repair_time_stat_dist,
            fail_rate_density_per_year=fail_rate_line,
            capacity=6,
        )

    CircuitBreaker("E1", L1)

    DL1a = Disconnector("L1a", L1, B1)
    DL1b = Disconnector("L1b", L1, B2)
    DL2a = Disconnector("L2a", L2, B2)
    DL2b = Disconnector("L2b", L2, B3)
    DL3a = Disconnector("L3a", L3, B3)
    DL3b = Disconnector("L3b", L3, B4)
    DL4a = Disconnector("L4a", L4, B4)
    DL4b = Disconnector("L4b", L4, B5)
    DL5a = Disconnector("L5a", L5, B5)
    DL5b = Disconnector("L5b", L5, B6)
    DL6a = Disconnector("L6a", L6, B3)
    DL6b = Disconnector("L6b", L6, B7)
    DL7a = Disconnector("L7a", L7, B7)
    DL7b = Disconnector("L7b", L7, B8)
    DL8a = Disconnector("L8a", L8, B4)
    DL8b = Disconnector("L8b", L8, B9)
    DL9a = Disconnector("L9a", L9, B9)
    DL9b = Disconnector("L9b", L9, B10)

    if include_backup:
        DL10a = Disconnector("L10a", L10, B4)
        DL10b = Disconnector("L10b", L10, B8)

        L10.set_backup()

    if include_microgrid:
        M1 = Bus(
            "M1",
            n_customers=0,
            coordinate=[-1, -2],
            fail_rate_per_year=fail_rate_trafo,
        )
        M2 = Bus(
            "M2",
            n_customers=0,
            coordinate=[-2, -3],
            fail_rate_per_year=fail_rate_trafo,
        )
        M3 = Bus(
            "M3",
            n_customers=40,
            coordinate=[-1, -3],
            fail_rate_per_year=fail_rate_trafo,
        )

        Battery("Bat1", M1)
        Production("P1", M2)

        ML1 = Line(
            "ML1",
            M1,
            M2,
            r=0.057526629463617,
            x=0.029324854498807,
            repair_time_dist=line_repair_time_stat_dist,
            fail_rate_density_per_year=fail_rate_line,
        )
        ML2 = Line(
            "ML2",
            M1,
            M3,
            r=0.057526629463617,
            x=0.029324854498807,
            repair_time_dist=line_repair_time_stat_dist,
            fail_rate_density_per_year=fail_rate_line,
        )

        L11 = Line(
            "L11",
            B6,
            M1,
            r=0.057526629463617,
            x=0.029324854498807,
            repair_time_dist=line_repair_time_stat_dist,
            fail_rate_density_per_year=fail_rate_line,
        )

        CircuitBreaker("E2", L11)

        DL11a = Disconnector("L11a", L11, B6)
        DL11b = Disconnector("L11b", L11, M1)
        DML1a = Disconnector("ML1a", ML1, M1)
        DML1b = Disconnector("ML1b", ML1, M2)
        DML2a = Disconnector("ML2a", ML2, M1)
        DML2b = Disconnector("ML2b", ML2, M3)

    if include_ICT:

        Sensor(
            "SL1",
            L1,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL2",
            L2,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL3",
            L3,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL4",
            L4,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL5",
            L5,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL6",
            L6,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL7",
            L7,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL8",
            L8,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            "SL9",
            L9,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )

        if include_backup:
            Sensor(
                "SL10",
                L10,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

        IntelligentSwitch(
            "RL1a", DL1a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL1b", DL1b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL2a", DL2a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL2b", DL2b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL3a", DL3a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL3b", DL3b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL4a", DL4a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL4b", DL4b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL5a", DL5a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL5b", DL5b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL6a", DL6a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL6b", DL6b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL7a", DL7a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL7b", DL7b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL8a", DL8a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL8b", DL8b, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL9a", DL9a, fail_rate_per_year=fail_rate_intelligent_switch
        )
        IntelligentSwitch(
            "RL9b", DL9b, fail_rate_per_year=fail_rate_intelligent_switch
        )

        if include_backup:
            IntelligentSwitch(
                "RL10a", DL10a, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RL10b", DL10b, fail_rate_per_year=fail_rate_intelligent_switch
            )

        if include_microgrid:

            Sensor(
                "SL11",
                L11,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

            Sensor(
                "SML1",
                ML1,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )
            Sensor(
                "SML2",
                ML2,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

            IntelligentSwitch(
                "RL11a", DL11a, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RL11b", DL11b, fail_rate_per_year=fail_rate_intelligent_switch
            )

            IntelligentSwitch(
                "RML1a", DML1a, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RML1b", DML1b, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RML2a", DML2a, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RML2b", DML2b, fail_rate_per_year=fail_rate_intelligent_switch
            )

    if include_ev:

        EVPark(
            name="EVB3",
            bus=B3,
            num_ev_dist=num_ev_table_func(B3.n_customers),
            v2g_flag=v2g_flag,
        )
        EVPark(
            name="EVB4",
            bus=B4,
            num_ev_dist=num_ev_table_func(B4.n_customers),
            v2g_flag=v2g_flag,
        )
        EVPark(
            name="EVB6",
            bus=B6,
            num_ev_dist=num_ev_table_func(B6.n_customers),
            v2g_flag=v2g_flag,
        )
        EVPark(
            name="EVB7",
            bus=B7,
            num_ev_dist=num_ev_table_func(B7.n_customers),
            v2g_flag=v2g_flag,
        )
        EVPark(
            name="EVB9",
            bus=B9,
            num_ev_dist=num_ev_table_func(B9.n_customers),
            v2g_flag=v2g_flag,
        )

    tn = Transmission(ps, B1)

    dn = Distribution(tn, L1)

    dn.add_buses([B1, B2, B3, B4, B5, B6, B7, B8, B9, B10])
    if include_backup:
        dn.add_lines([L2, L3, L4, L5, L6, L7, L8, L9, L10])
    else:
        dn.add_lines([L2, L3, L4, L5, L6, L7, L8, L9])

    if include_microgrid:
        m = Microgrid(dn, L11, mode=MicrogridMode.SURVIVAL)

        m.add_buses([M1, M2, M3])
        m.add_lines([ML1, ML2])

    return ps


if __name__ == "__main__":
    ps, _, _, _ = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "TEST10.pdf",
        )
    )
