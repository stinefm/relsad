import os
import numpy as np
from relsad.visualization.plotting import plot_topology
from relsad.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    EVPark,
    Battery,
    Production,
    MainController,
    ManualMainController,
    Sensor,
    IntelligentSwitch,
    MicrogridMode,
)
from relsad.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
    Microgrid,
)
from relsad.Time import (
    Time,
    TimeUnit,
)

from relsad.StatDist import (
    StatDist,
    StatDistType,
    NormalParameters,
)
from relsad.Table import Table


def initialize_network(
    fail_rate_trafo: float = 0.007,
    fail_rate_line: float = 0.7,
    fail_rate_intelligent_switch: float = 1000,
    fail_rate_hardware: float = 0.2,
    fail_rate_software: float = 12,
    fail_rate_sensor: float = 0.023,
    p_fail_repair_new_signal: float = 1 - 0.95,
    p_fail_repair_reboot: float = 1 - 0.9,
    outage_time_trafo: Time = Time(8, TimeUnit.HOUR),
    include_microgrid: bool = True,
    include_production: bool = True,
    include_ICT: bool = True,
    include_ev: bool = True,
    v2g_flag: bool = True,
    include_backup: bool = True,
    microgrid_mode: MicrogridMode = MicrogridMode.SURVIVAL,
    line_stat_dist: StatDist = StatDist(
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
            sectioning_time=Time(1, TimeUnit.HOUR),
        )

    ps = PowerSystem(C1)

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
        repair_time_dist=line_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B2,
        tbus=B4,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B3,
        tbus=B6,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )

    if include_backup:
        L6 = Line(
            name="L6",
            fbus=B4,
            tbus=B6,
            r=0.7114,
            x=0.2351,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_stat_dist,
            capacity=6,
        )

    E1 = CircuitBreaker("E1", L1)

    DL1a = Disconnector("L1a", L1, B1, E1)
    DL1b = Disconnector("L1b", L1, B2, E1)
    DL1c = Disconnector("L1c", L1, B2)
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
            repair_time_dist=line_stat_dist,
        )
        ML2 = Line(
            name="ML2",
            fbus=M1,
            tbus=M3,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_stat_dist,
        )

        L7 = Line(
            name="L7",
            fbus=B2,
            tbus=M1,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
            repair_time_dist=line_stat_dist,
        )

        E2 = CircuitBreaker(name="E2", line=L7)

        DL7a = Disconnector(
            name="L7a",
            line=L7,
            bus=B2,
            circuitbreaker=E2,
        )
        DL7b = Disconnector(
            name="L7b",
            line=L7,
            bus=M1,
            circuitbreaker=E2,
        )
        DL7c = Disconnector(
            name="L7c",
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

        m = Microgrid(
            distribution_network=dn,
            connected_line=L7,
            mode=microgrid_mode,
        )

        m.add_buses([M1, M2, M3])
        m.add_lines([ML1, ML2])

    if include_ICT:

        Sensor(
            name="SL1",
            line=L1,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL2",
            line=L2,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL3",
            line=L3,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL4",
            line=L4,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )
        Sensor(
            name="SL5",
            line=L5,
            fail_rate_per_year=fail_rate_sensor,
            p_fail_repair_new_signal=p_fail_repair_new_signal,
            p_fail_repair_reboot=p_fail_repair_reboot,
        )

        if include_backup:
            Sensor(
                name="SL6",
                line=L6,
                fail_rate_per_year=fail_rate_sensor,
                p_fail_repair_new_signal=p_fail_repair_new_signal,
                p_fail_repair_reboot=p_fail_repair_reboot,
            )

        IntelligentSwitch(
            name="RL1a",
            disconnector=DL1a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL1b",
            disconnector=DL1b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL1c",
            disconnector=DL1c,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL2a",
            disconnector=DL2a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL2b",
            disconnector=DL2b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL3a",
            disconnector=DL3a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL3b",
            disconnector=DL3b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL4a",
            disconnector=DL4a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL4b",
            disconnector=DL4b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL5a",
            disconnector=DL5a,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )
        IntelligentSwitch(
            name="RL5b",
            disconnector=DL5b,
            fail_rate_per_year=fail_rate_intelligent_switch,
        )

        if include_backup:
            IntelligentSwitch(
                name="RL6a",
                disconnector=DL6a,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )
            IntelligentSwitch(
                name="RL6b",
                disconnector=DL6b,
                fail_rate_per_year=fail_rate_intelligent_switch,
            )

        if include_microgrid:

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
                name="RL7c",
                disconnector=DL7c,
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

    if include_ev:
        EVPark(
            name="EV1",
            bus=B5,
            num_ev_dist=num_ev_table_func(B3.n_customers),
            v2g_flag=v2g_flag,
        )

    dn.add_buses([B2, B3, B4, B5, B6])
    if include_backup:
        dn.add_lines([L2, L3, L4, L5, L6])
    else:
        dn.add_lines([L2, L3, L4, L5])

    return ps


if __name__ == "__main__":
    ps = initialize_network(
        include_microgrid=True,
        include_production=False,
        include_ICT=False,
        include_ev=False,
    )
    fig = plot_topology(
        buses=ps.buses,
        lines=ps.lines,
        bus_text=True,
        line_text=True,
    )

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "CINELDI_testnetwork.pdf",
        )
    )
    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "CINELDI_testnetwork.png",
        ),
        dpi=600,
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
