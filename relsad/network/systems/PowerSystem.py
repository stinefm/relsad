import numpy as np

from relsad.network.components import Bus, ICTLine, ICTNode, Line
from relsad.reliability.indices import (
    ASAI,
    ASUI,
    CAIDI,
    ENS,
    SAIDI,
    SAIFI,
    EV_Duration,
    EV_Index,
    EV_Interruption,
)
from relsad.Time import Time, TimeStamp
from relsad.topology.sectioning import create_sections, get_section_list
from relsad.utils import INF, eq, unique

from .PowerNetwork import PowerNetwork
from .Transmission import Transmission


class PowerSystem(PowerNetwork):
    """
    Class defining a power system type

    ...

    Attributes
    ----------
    name : str
        Name of the power system
    slack : Bus
        Slack bus of the power system
    p_energy_shed : float
        The active power energy.shed in the power system
    acc_p_energy_shed : float
        The accumulated active power energy.shedding in the power system
    q_energy_shed : float
        The reactive power energy.shed in the power system
    acc_q_energy_shed : float
        The accumulated reactive power energy.shedding in the power system
    sub_systems : list
        List of all sub systems in the power system
    buses : list
        List of all buses in the power system
    ev_parks : list
        List of all EV parks in the power system
    batteries : list
        List of all batteries in the power system
    production : list
        List of all generation units in the power system
    ict_nodes : list
        List of all ICT nodes in the power system
    lines : list
        List of all lines in the power system
    sensors : list
        List of all sensors in the power system
    circuitbreaker : list
        List of all circuit breakers in the power system
    disconnectors : list
        List of all disconnectors in the power system
    intelligent_switch : list
        List of all intelligent switches in the power system
    ict_lines : list
        List of all ICT lines in the power system
    controller : MainController
        The controller for the power system, either MainController or ManualMainController
    comp_list : list
        List containing the components in the power system
    comp_dict : dict
        Dictionary containing the components in the power system
    child_network_list : list
        List containing all the networks in the power system
    history : dict
        Dictionary containing the history variables of the power system
    monte_carlo_history : dict
        Dictionary containing the history variables from the monte carlo simulation



    Methods
    ----------
    add_bus(bus)
        Adding a bus including elements on the bus
        (battery, generation unit, EV park) to the power system
    add_buses(buses)
        Adding buses to the power system
    add_ict_node(ict_node)
        Adding an ICT node to the power system
    add_line(line)
        Adding a line including elements on the line
        (sensor, circuit breaker, disconnector) to the power system
    add_lines(lines)
        Adding lines to the power system
    add_ict_line(ict_line)
        Adding an ICT line to the power system
    get_lines()
        Returns the lines in the power system
    get_comp(name)
        Returns component based on given name
    get_comp_list()
        Returns list of the components in the power system
    add_child_network(network)
        Adding child network to the power system
    reset_slack_bus()
        Resets the slack bus of the child networks
    create_sections()
        Creates sections in the power system
    print_status()
        Prints the status of the buses and lines in the power system
    get_system_load_balance()
        Returns the load balance of the system in MW and MVar
    update_batteries(fail_duration, dt)
        Updates the batteries in the power system
    update_ev_parks(fail_duration, dt, start_time, curr_time)
        Updates the EV parks in the power system
    update_fail_status(dt)
        Updates the failure status for each component that
        can fail in the power system
    get_system_load()
        Returns the system load at the current time in MW and MVar
    prepare_load_data(time_indices)
        Prepares the load data for the buses in the power system
    prepare_prod_data(time_indices)
        Prepares the production data for the production components
        in the power system
    set_load_and_cost(inc_idx)
        Sets the bus load and cost in MW based on load and cost profiles
        in the current increment for the power system
    set_prod(inc_idx)
        Sets the generation (generation units, batteries, EV parks)
        at the buses in the power system
    failes_comp()
        Returns True if the power system contains a
        failed compoent, False otherwise
    full_batteries()
        Returns True if the batteries in the power system
        are full, and False otherwise
    reset_load_flow_data()
        Resets the variables used in the load flow analysis
    get_monte_carlo_history(attribute)
        Returns the specified history variable
        from the Monte Carlo simulation
    initialize_sequence_history()
        Initializes the dictionaries used for sequence history variables
    update_sequence_history()
        Updates the sequence history variables of the power system
    initialize_monte_carlo_history()
        Initializes the lists used for history variable
        from the Monte Carlo simulation
    update_monte_carlo_history()
        Updates the history dictionary from the Monte Carlo simulation
    update_monte_carlo_child_network_history()
        Updates the history dictionary for the child networks
        in the Monte Carlo simulation
    update_monte_carlo_comp_history()
        Updates the component values for the system
        from the Monte Carlo simulation
    get_history(attribute)
        Returns the specified history variable
    reset_energy_shed_variables()
        Resets the energy.shed variables
    verify_component_setup()
        Verifies the component setup in the power system

    """

    ## Visual attributes
    color = "black"

    ## Counter
    counter = 0

    ## Load shed configurations
    shed_configs: list = list()

    def __init__(self, controller):
        """Initializing power system content
        Content:
            buses(set): List of buses
            lines(set): List of lines
            comp_dict(dict): Dictionary of components
        """
        # Info
        PowerSystem.counter += 1
        self.name = "ps{:d}".format(PowerSystem.counter)
        # Load flow
        self.slack = None
        # Load shedding
        self.p_energy_shed = 0
        self.acc_p_energy_shed = 0
        self.q_energy_shed = 0
        self.acc_q_energy_shed = 0
        # Sub-systems
        self.sub_systems: list = []
        # Components
        self.buses: list = []
        self.ev_parks: list = []
        self.batteries: list = []
        self.productions: list = []
        self.ict_nodes: list = []
        self.lines: list = []
        self.sensors: list = []
        self.circuitbreakers: list = []
        self.disconnectors: list = []
        self.intelligent_switches: list = []
        self.ict_lines: list = []
        self.controller = controller
        self.comp_list: list = []
        self.comp_dict: dict = {}
        ## Child networks
        self.child_network_list: list = []
        ## History
        self.history: dict = {}
        self.monte_carlo_history: dict = {}
        ## Random instance
        self.random_instance: np.random.Generator = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PowerSystem(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "buses") and hasattr(other, "lines"):
            return set(unique(self.buses + self.lines)) == set(
                unique(other.buses + other.lines)
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus: Bus):
        """
        Adding a bus including elements on the bus
        (battery, generation unit, EV park) to the power system

        Parameters
        ----------
        bus : Bus
            A bus element

        Returns
        ----------
        None

        """
        self.comp_dict[bus.name] = bus
        self.comp_list.append(bus)
        self.buses.append(bus)
        self.buses = unique(self.buses)
        if bus.ev_park is not None:
            self.comp_dict[bus.ev_park.name] = bus.ev_park
            self.comp_list.append(bus.ev_park)
            self.ev_parks.append(bus.ev_park)
            self.ev_parks = unique(self.ev_parks)
        if bus.battery is not None:
            self.comp_dict[bus.battery.name] = bus.battery
            self.comp_list.append(bus.battery)
            self.batteries.append(bus.battery)
            self.batteries = unique(self.batteries)
        if bus.prod is not None:
            self.comp_dict[bus.prod.name] = bus.prod
            self.comp_list.append(bus.prod)
            self.productions.append(bus.prod)
            self.productions = unique(self.productions)
        self.comp_list = unique(self.comp_list)

    def add_buses(self, buses: list):
        """
        Adding buses to the power system

        Parameters
        ----------
        buses : list
            A list of Bus elements in the power system

        Returns
        ----------
        None

        """
        for bus in buses:
            self.add_bus(bus)

    def add_ict_node(self, ict_node: ICTNode):
        """
        Adding an ICT node to the power system

        Parameters
        ----------
        ict_node : ICTNode
            An ICT node element

        Returns
        ----------
        None

        """
        self.comp_dict[ict_node.name] = ict_node
        self.comp_list.append(ict_node)
        self.ict_nodes.append(ict_node)
        self.ict_nodes = unique(self.ict_nodes)
        self.comp_list = unique(self.comp_list)

    def add_line(self, line: Line):
        """
        Adding a line including elements on the line
        (sensor, circuit breaker, disconnector) to the power system

        Parameters
        ----------
        line : Line
            A line element

        Returns
        ----------
        None

        """
        self.comp_dict[line.name] = line
        self.comp_list.append(line)
        self.lines.append(line)
        self.lines = unique(self.lines)
        if line.sensor:
            self.comp_dict[line.sensor.name] = line.sensor
            self.comp_list.append(line.sensor)
            self.sensors.append(line.sensor)
            self.sensors = unique(self.sensors)
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
            self.comp_list.append(discon)
            self.disconnectors.append(discon)
            self.disconnectors = unique(self.disconnectors)
            if discon.intelligent_switch:
                self.comp_dict[
                    discon.intelligent_switch.name
                ] = discon.intelligent_switch
                self.comp_list.append(discon.intelligent_switch)
                self.intelligent_switches.append(discon.intelligent_switch)
                self.intelligent_switches = unique(self.intelligent_switches)
        if line.circuitbreaker is not None:
            c_b = line.circuitbreaker
            self.comp_dict[c_b.name] = c_b
            self.comp_list.append(c_b)
            self.circuitbreakers.append(c_b)
            self.circuitbreakers = unique(self.circuitbreakers)
        self.comp_list = unique(self.comp_list)

    def add_lines(self, lines: list):
        """
        Adding lines to the power system

        Parameters
        ----------
        lines : list
            A list of Line elements in the power system

        Returns
        ----------
        None

        """
        for line in lines:
            self.add_line(line)

    def add_ict_line(self, ict_line: ICTLine):
        """
        Adding an ICT line to the power system

        Parameters
        ----------
        ict_line : ICTLine
            An ICT line element

        Returns
        ----------
        None

        """
        self.comp_dict[ict_line.name] = ict_line
        self.comp_list.append(ict_line)
        self.ict_lines.append(ict_line)
        self.ict_lines = unique(self.ict_lines)
        self.comp_list = unique(self.comp_list)

    def get_lines(self):
        """
        Returns the lines in the power system

        Parameters
        ----------
        lines : list
            A list of Line elements in the power system

        Returns
        ----------
        lines : list
            List of Line elements

        """
        return self.lines

    def get_comp(self, name: str):
        """
        Returns component based on given name

        Parameters
        ----------
        name : str
           Name of the component

        Returns
        ----------
        comp_dict[name] : dict
            Dictionary containing information about the component

        """
        try:
            return self.comp_dict[name]
        except KeyError:
            print(name)
            print("Component is not part of the network")
            exit()

    def get_comp_list(self):
        """
        Returns list of the components in the power system

        Parameters
        ----------
        None

        Returns
        ----------
        comp_list : list
            List of the components in the power system

        """
        return self.comp_list

    def add_child_network(self, network):
        """
        Adding child network to the power system

        Parameters
        ----------
        network : PowerNetwork
            The child network of the power system

        Returns
        ----------
        None

        """
        self.child_network_list.append(network)

    def reset_slack_bus(self):
        """
        Resets the slack bus of the child networks

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for child_network in self.child_network_list:
            child_network.reset_slack_bus()

    def create_sections(self):
        """
        Creates sections in the power system

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for network in self.child_network_list:
            if not isinstance(network, Transmission):
                parent_section = create_sections(network.connected_line)
                network.sections = get_section_list(parent_section, [])

    def print_status(self):
        """
        Prints the status of the buses and lines in the power system

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        print("Buses:")
        for bus in self.buses:
            bus.print_status()
        print("Lines:")
        for line in self.lines:
            line.print_status()

    def get_system_load_balance(self):
        """
        Returns the load balance of the system in MW and MVar

        Parameters
        ----------
        None

        Returns
        ----------
        system_load_balance_p : float
            The active power load balance in the power system (load - generation)
        system_load_balance_q : float
            The reactive power load balance in the power system (load - generation)

        """
        system_load_balance_p, system_load_balance_q = 0, 0
        for bus in self.buses:
            for child_network in self.child_network_list:
                if isinstance(child_network, Transmission):
                    if bus == child_network.get_trafo_bus():
                        system_load_balance_p = -INF
                        system_load_balance_q = 0
                        return system_load_balance_p, system_load_balance_q
            system_load_balance_p += bus.pload - bus.pprod
            system_load_balance_q += bus.qload - bus.qprod
        return system_load_balance_p, system_load_balance_q

    def update_batteries(self, fail_duration: Time, dt: Time):
        """
        Updates the batteries in the power system

        Parameters
        ----------
        fail_duration : Time
            The failure duration
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        p, q = self.get_system_load_balance()
        for battery in self.batteries:
            p, q = battery.update(p, q, fail_duration, dt)

    def update_ev_parks(
        self,
        fail_duration: Time,
        dt: Time,
        start_time: TimeStamp,
        curr_time: Time,
    ):
        """
        Updates the EV parks in the power system

        Parameters
        ----------
        fail_duration : Time
            The failure duration
        dt : Time
            The current time step
        start_time : TimeStamp
            Start time
        curr_time : Time
            The current time

        Returns
        ----------
        None

        """
        hour_of_day = start_time.get_hour_of_day(curr_time)
        p, q = self.get_system_load_balance()
        for ev_park in self.ev_parks:
            p, q = ev_park.update(
                p=p,
                q=q,
                fail_duration=fail_duration,
                dt=dt,
                hour_of_day=hour_of_day,
            )

    def update_fail_status(self, dt: Time):
        """
        Updates the failure status for each component that
        can fail in the power system

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.update_fail_status(dt)
        for battery in self.batteries:
            battery.update_fail_status(dt)
        for line in self.lines:
            line.update_fail_status(dt)
        for circuitbreaker in self.circuitbreakers:
            circuitbreaker.update_fail_status(dt)
        for sensor in self.sensors:
            sensor.update_fail_status(dt)
        for intelligent_switch in self.intelligent_switches:
            intelligent_switch.update_fail_status(dt)
        for ict_line in self.ict_lines:
            ict_line.update_fail_status(dt)
        for ict_node in self.ict_nodes:
            ict_node.update_fail_status(dt)
        self.controller.update_fail_status(dt)

    def get_system_load(self):
        """
        Returns the system load at the current time in MW and MVar

        Parameters
        ----------
        None

        Returns
        ----------
        pload : float
            The active power load in the power system
        qload : float
            The reactive power load in the power system

        """
        pload, qload = 0, 0
        for bus in self.buses:
            p, q = bus.get_load()
            pload += p
            qload += q
        return pload, qload

    def prepare_load_data(self, time_indices: np.ndarray):
        """
        Prepares the load data for the buses in the power system

        Parameters
        ----------
        time_indices : np.ndarray
            Time indices used to discretize the load data

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.prepare_load_data(time_indices)

    def prepare_prod_data(self, time_indices: np.ndarray):
        """
        Prepares the production data for the production components
        in the power system

        Parameters
        ----------
        time_indices : np.ndarray
            Time indices used to discretize the load data

        Returns
        ----------
        None

        """
        for prod in self.productions:
            prod.prepare_prod_data(time_indices)

    def set_load_and_cost(self, inc_idx: int):
        """
        Sets the bus load and cost in MW based on load and cost profiles
        in the current increment for the power system

        Parameters
        ----------
        inc_idx : int
            Increment index

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.set_load_and_cost(inc_idx)

    def set_prod(self, inc_idx: int):
        """
        Sets the generation (generation units, batteries, EV parks)
        at the buses in the power system

        Parameters
        ----------
        inc_idx : int
            Increment index

        Returns
        ----------
        None

        """
        for prod in self.productions:
            prod.set_prod(inc_idx)
        for bus in self.buses:
            if bus.battery is not None:
                bus.reset_prod()
            elif bus.ev_park is not None:
                bus.reset_prod()

    def failed_comp(self):
        """
        Returns True if the power system contains a
        failed component, False otherwise

        Parameters
        ----------
        None

        Returns
        ----------
        True/False

        """
        return any(
            bus.trafo_failed for bus in self.buses
        ) or any(line.failed for line in self.lines)

    def full_batteries(self):
        """
        Returns True if the batteries in the power system
        are full, and False otherwise

        Parameters
        ----------
        None

        Returns
        ----------
        True/False

        """
        return all(
            eq(battery.SOC, battery.SOC_max)
            for battery in self.batteries
        )

    def reset_load_flow_data(self):
        """
        Reset the variables used in the load flow analysis

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.reset_load_flow_data()
        for line in self.lines:
            line.reset_load_flow_data()

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable

        Parameters
        ----------
        attribute : str
            Power system attribute

        Returns
        ----------
        monte_carlo_history[attribute] : dict
            Returns the history variables of an attribute from the Monte Carlo simulation

        """
        return self.monte_carlo_history[attribute]

    def initialize_sequence_history(self):
        """
        Initializes the dictionaries used for sequence history variables
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
    
        """
        network_state_list = [
            "p_energy_shed",
            "q_energy_shed",
            "acc_p_energy_shed",
            "acc_q_energy_shed",
            "p_load",
            "q_load",
            "SAIFI",
            "SAIDI",
            "CAIDI",
            "ASAI",
            "ASUI",
            "ENS",
            "EV_Index",
            "EV_Interruption",
            "EV_Duration",
        ]
        for state_var in network_state_list:
            self.history[state_var] = {}
        for network in self.child_network_list:
            for state_var in network_state_list:
                network.history[state_var] = {}
        self.controller.initialize_history()

    def update_sequence_history(
        self,
        prev_time: Time,
        curr_time: Time,
        save_flag: bool,
    ):
        """
        Updates the sequence history variables of the power system

        Parameters
        ----------
        prev_time : Time
            The previous time
        curr_time : Time
            The current time
        save_flag : bool
            Indicates if saving is on/off

        Returns
        ----------
        None

        """
        time = curr_time.get_unit_quantity(curr_time.unit)
        for comp in self.comp_list:
            comp.update_history(prev_time, curr_time, save_flag)
        self.controller.update_history(prev_time, curr_time, save_flag)
        for network in self.child_network_list:
            for bus in network.buses:
                network.p_energy_shed += bus.p_energy_shed_stack
                network.q_energy_shed += bus.q_energy_shed_stack
            self.p_energy_shed += network.p_energy_shed
            self.q_energy_shed += network.q_energy_shed
            network.acc_p_energy_shed += network.p_energy_shed
            network.acc_q_energy_shed += network.q_energy_shed
        self.acc_p_energy_shed += self.p_energy_shed
        self.acc_q_energy_shed += self.q_energy_shed
        if save_flag:
            self_state_dict = {
                "p_energy_shed": self.p_energy_shed,
                "q_energy_shed": self.p_energy_shed,
                "acc_p_energy_shed": self.acc_p_energy_shed,
                "acc_q_energy_shed": self.acc_q_energy_shed,
                "p_load": self.get_system_load()[0],
                "q_load": self.get_system_load()[1],
                "SAIFI": SAIFI(self),
                "SAIDI": SAIDI(self),
                "CAIDI": CAIDI(self),
                "ASAI": ASAI(self, curr_time),
                "ASUI": ASUI(self, curr_time),
                "ENS": ENS(self),
                "EV_Index": EV_Index(self),
                "EV_Interruption": EV_Interruption(self),
                "EV_Duration": EV_Duration(self),
            }
            for state_var, value in self_state_dict.items():
                self.history[state_var][time] = value
            for network in self.child_network_list:
                network_state_dict = {
                    "p_energy_shed": network.p_energy_shed,
                    "q_energy_shed": network.q_energy_shed,
                    "acc_p_energy_shed": network.acc_p_energy_shed,
                    "acc_q_energy_shed": network.acc_q_energy_shed,
                    "p_load": network.get_system_load()[0],
                    "q_load": network.get_system_load()[1],
                    "SAIFI": SAIFI(network),
                    "SAIDI": SAIDI(network),
                    "CAIDI": CAIDI(network),
                    "ASAI": ASAI(network, curr_time),
                    "ASUI": ASUI(network, curr_time),
                    "ENS": ENS(network),
                    "EV_Index": EV_Index(network),
                    "EV_Interruption": EV_Interruption(network),
                    "EV_Duration": EV_Duration(network),
                }
                for state_var, value in network_state_dict.items():
                    network.history[state_var][time] = value
        self.p_energy_shed = 0
        self.q_energy_shed = 0
        for network in self.child_network_list:
            network.p_energy_shed = 0
            network.q_energy_shed = 0

    def initialize_monte_carlo_history(self):
        """
        Initializes the lists used for history variables
        from the Monte Carlo simulation
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        save_dict : dict
            Dictionary with simulation results
    
        """
        network_state_list = [
            "acc_p_energy_shed",
            "acc_q_energy_shed",
            "SAIFI",
            "SAIDI",
            "CAIDI",
            "ASAI",
            "ASUI",
            "ENS",
            "EV_Index",
            "EV_Interruption",
            "EV_Duration",
        ]
        save_dict = {}
        save_dict[self.name] = {}
        for state_var in network_state_list:
            save_dict[self.name][state_var] = {}
        for network in self.child_network_list:
            save_dict[network.name] = {}
            for state_var in network_state_list:
                save_dict[network.name][state_var] = {}
        bus_state_list = [
            "acc_p_energy_shed",
            "acc_q_energy_shed",
            "avg_outage_time",
            "acc_outage_time",
            "interruption_fraction",
            "acc_interruptions",
        ]
        ev_park_state_list = [
            "acc_num_interruptions",
            "acc_exp_interruptions",
            "acc_exp_car_interruptions",
            "acc_interruption_duration",
            "acc_available_num_cars",
            "num_cars",
        ]
        for bus in self.buses:
            save_dict[bus.name] = {}
            for state_var in bus_state_list:
                save_dict[bus.name][state_var] = {}
            if bus.ev_park is not None:
                save_dict[bus.ev_park.name] = {}
                for state_var in ev_park_state_list:
                    save_dict[bus.ev_park.name][state_var] = {}
        return save_dict

    def update_monte_carlo_history(
        self,
        it: int,
        current_time: Time,
        save_dict: dict,
    ):
        """
        Updates the history dictionary from the Monte Carlo simulation
    
        Parameters
        ----------
        it : int
            The iteration number
        current_time : Time
            Current time
        save_dict : dict
            Dictionary with simulation results
    
        Returns
        ----------
        save_dict : dict
            Dictionary with simulation results
    
        """
        network_state_dict = {
            "acc_p_energy_shed": self.acc_p_energy_shed,
            "acc_q_energy_shed": self.acc_q_energy_shed,
            "SAIFI": SAIFI(self),
            "SAIDI": SAIDI(self),
            "CAIDI": CAIDI(self),
            "ASAI": ASAI(self, current_time),
            "ASUI": ASUI(self, current_time),
            "ENS": ENS(self),
            "EV_Index": EV_Index(self),
            "EV_Interruption": EV_Interruption(self),
            "EV_Duration": EV_Duration(self),
        }
        for state_var, value in network_state_dict.items():
            save_dict[self.name][state_var][it] = value
        save_dict = self.update_monte_carlo_child_network_history(
            it, current_time, save_dict
        )
        save_dict = self.update_monte_carlo_comp_history(it, save_dict)
        return save_dict
    
    def update_monte_carlo_child_network_history(
        self,
        it: int,
        current_time: Time,
        save_dict: dict,
    ):
        """
        Updates the history dictionary for the child networks
        in the Monte Carlo simulation
    
        Parameters
        ----------
        it : int
            The iteration number
        current_time : Time
            Current time
        save_dict : dict
            Dictionary with simulation results
    
        Returns
        ----------
        save_dict : dict
            Dictionary with simulation results
    
        """
        for network in self.child_network_list:
            network_state_dict = {
                "acc_p_energy_shed": network.acc_p_energy_shed,
                "acc_q_energy_shed": network.acc_q_energy_shed,
                "SAIFI": SAIFI(network),
                "SAIDI": SAIDI(network),
                "CAIDI": CAIDI(network),
                "ASAI": ASAI(network, current_time),
                "ASUI": ASUI(network, current_time),
                "ENS": ENS(network),
                "EV_Index": EV_Index(network),
                "EV_Interruption": EV_Interruption(network),
                "EV_Duration": EV_Duration(network),
            }
            for state_var, value in network_state_dict.items():
                save_dict[network.name][state_var][it] = value
        return save_dict
    
    def update_monte_carlo_comp_history(
        self,
        it: int,
        save_dict: dict,
    ):
        """
        Updates the component values for the system
        from the Monte Carlo simulation
    
        Parameters
        ----------
        it : int
            The iteration number
        save_dict : dict
            Dictionary with simulation results
    
        Returns
        ----------
        save_dict : dict
            Dictionary with simulation results
    
        """
        for bus in self.buses:
            bus_state_dict = {
                "acc_p_energy_shed": bus.acc_p_energy_shed,
                "acc_q_energy_shed": bus.acc_q_energy_shed,
                "avg_outage_time": bus.avg_outage_time.get_hours(),
                "acc_outage_time": bus.acc_outage_time.get_hours(),
                "interruption_fraction": bus.interruption_fraction,
                "acc_interruptions": bus.acc_interruptions,
            }
            for state_var, value in bus_state_dict.items():
                save_dict[bus.name][state_var][it] = value
            if bus.ev_park is not None:
                ev_park_state_dict = {
                    "acc_num_interruptions": bus.ev_park.acc_num_interruptions,
                    "acc_exp_interruptions": bus.ev_park.acc_exp_interruptions,
                    "acc_exp_car_interruptions": bus.ev_park.acc_exp_car_interruptions,
                    "acc_interruption_duration": bus.ev_park.acc_interruption_duration.get_hours(),
                    "acc_available_num_cars": bus.ev_park.acc_available_num_cars,
                    "num_cars": bus.ev_park.num_cars,
                }
                for state_var, value in ev_park_state_dict.items():
                    save_dict[bus.ev_park.name][state_var][it] = value
        return save_dict

    def get_history(self, attribute):
        """
        Returns the specified history variable

        Parameters
        ----------
        attribute : str
            Power system attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def reset_energy_shed_variables(self):
        """
        Resets the energy.shed variables

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.p_energy_shed = 0
        self.acc_p_energy_shed = 0
        self.q_energy_shed = 0
        self.acc_q_energy_shed = 0

    def verify_component_setup(self):
        """
        Verifies the component setup in the power system

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for bus in self.buses:
            for line in bus.connected_lines:
                if line not in self.lines and line.is_backup:
                    if line.parent_network is None:
                        raise Exception(
                            "Line, {:s}, does not have a parent network".format(
                                line.name
                            )
                        )
