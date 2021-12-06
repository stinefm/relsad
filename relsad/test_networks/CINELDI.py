import os
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
from relsad.utils import (
    Time,
    TimeUnit,
)


def initialize_network():
    fail_rate_trafo = 0.007
    fail_rate_line = 0.07
    fail_rate_intelligent_switch = 1000
    fail_rate_hardware = 0.2
    fail_rate_software = 12
    fail_rate_sensor = 0.023
    p_fail_repair_new_signal = 1 - 0.95
    p_fail_repair_reboot = 1 - 0.9

    include_microgrid = False
    include_production = False
    include_ICT = False
    include_ev = True
    include_backup = False


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
            section_time=Time(1, TimeUnit.HOUR),
        )

    

    ps = PowerSystem(C1)

    ## Transmission network
    T = Bus("T", n_customers=0, coordinate=[0, 0], fail_rate_per_year=0)

    ## Distribution network
    B1 = Bus(
        "B1",
        n_customers=1,
        coordinate=[0, -1],
        fail_rate_per_year=fail_rate_trafo,
    )
    B2 = Bus(
        "B2",
        n_customers=100,
        coordinate=[1, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B3 = Bus(
        "B3",
        n_customers=50,
        coordinate=[0, -2],
        fail_rate_per_year=fail_rate_trafo,
    )
    B4 = Bus(
        "B4",
        n_customers=90,
        coordinate=[0, -3],
        fail_rate_per_year=fail_rate_trafo,
    )
    B5 = Bus(
        "B5",
        n_customers=3,
        coordinate=[1, -3],
        fail_rate_per_year=fail_rate_trafo,
    )

    
    L1 = Line(
        "L1",
        T,
        B1,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B1,
        B2,
        r=0.057526629463617,
        x=0.029324854498807,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B1,
        B3,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B3,
        B4,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B2,
        B5,
        r=0.7114,
        x=0.2351,
        fail_rate_density_per_year=fail_rate_line,
    )

    if include_backup: 
        L6 = Line(
            "L6",
            B3,
            B5,
            r=0.7114,
            x=0.2351,
            fail_rate_density_per_year=fail_rate_line,
            capacity=6,
        )
        
    

    E1 = CircuitBreaker("E1", L1)
    

    DL1a = Disconnector("L1a", L1, T, E1)
    DL1b = Disconnector("L1b", L1, B1, E1)
    DL1c = Disconnector("L1c", L1, B1)
    DL2a = Disconnector("L2a", L2, B1)
    DL2b = Disconnector("L2b", L2, B2)
    DL3a = Disconnector("L3a", L3, B1)
    DL3b = Disconnector("L3b", L3, B3)
    DL4a = Disconnector("L4a", L4, B3)
    DL4b = Disconnector("L4b", L4, B4)
    DL5a = Disconnector("L5a", L5, B2)
    DL5b = Disconnector("L5b", L5, B5)

    if include_backup:
        DL6a = Disconnector("L6a", L6, B3)
        DL6b = Disconnector("L6b", L6, B5)

        L6.set_backup()

    tn = Transmission(ps, T)

    dn = Distribution(tn, L1)

    
    
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
            fail_rate_density_per_year=fail_rate_line,
        )
        ML2 = Line(
            "ML2",
            M1,
            M3,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
        )

        L7 = Line(
            "L7",
            B1,
            M1,
            r=0.057526629463617,
            x=0.029324854498807,
            fail_rate_density_per_year=fail_rate_line,
        )

        E2 = CircuitBreaker("E2", L7)

        DL7a = Disconnector("L7a", L7, B1, E2)
        DL7b = Disconnector("L7b", L7, M1, E2)
        DL7c = Disconnector("L7c", L7, M1)
        DML1a = Disconnector("ML1a", ML1, M1)
        DML1b = Disconnector("ML1b", ML1, M2)
        DML2a = Disconnector("ML2a", ML2, M1)
        DML2b = Disconnector("ML2b", ML2, M3)

        m = Microgrid(dn, L7, mode=MicrogridMode.SURVIVAL)

        m.add_buses([M1, M2, M3])
        m.add_lines([ML1, ML2])

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

        if include_backup: 
            Sensor(
                "SL6",
                L6,
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
            "RL1c", DL1c, fail_rate_per_year=fail_rate_intelligent_switch
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

        if include_backup: 
            IntelligentSwitch(
                "RL6a", DL6a, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RL6b", DL6b, fail_rate_per_year=fail_rate_intelligent_switch
            )

        if include_microgrid:

            Sensor(
                "SL7",
                L7,
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
                "RL7a", DL7a, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RL7b", DL7b, fail_rate_per_year=fail_rate_intelligent_switch
            )
            IntelligentSwitch(
                "RL7c", DL7c, fail_rate_per_year=fail_rate_intelligent_switch
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
            name="EV1",
            bus=B5,
            min_num_ev=0,
            max_num_ev=5,
        )
    
    dn.add_buses([B1, B2, B3, B4, B5])
    if include_backup:
        dn.add_lines([L2, L3, L4, L5, L6])
    else: 
        dn.add_lines([L2, L3, L4, L5])

    return ps, include_microgrid, include_production, include_backup


if __name__ == "__main__":
    ps, _, _ = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "CINELDI_testnetwork.pdf",
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
