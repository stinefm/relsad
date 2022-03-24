import numpy as np
from relsad.network.components import (
    Bus,
    Line,
)
from relsad.network.systems import Network
from .Transmission import Transmission
from relsad.utils import (
    eq,
    unique,
    interpolate,
    INF,
)
from relsad.Time import Time
from relsad.topology.paths import (
    create_sections,
    get_section_list,
)


class PowerSystem(Network):
    """
    Class defining a power system type

    ...

    Attributes
    ----------
    name : str
        Name of the power system
    slack : Bus ? 
    p_load_shed : float
        The active power load shed in the power system
    acc_p_load_shed : float
        The accumulated active power load shedding in the power system
    q_load_shed : float
        The reactive power load shed in the power system
    acc_q_load_shed : float
        The accumulated reactive power load shedding in the power system
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
        Adding a bus including elements on the bus (battery, generation unit, EV parkt) to the power system 
    add_buses(buses)
        Adding buses to the power system bus list
    add_line(line)
        Adding a line including elements on the line (sensor, circuit breaker, disconnector) to the power system
    add_lines(lines)
        Adding lines to the power system 
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
    update_ev_parks(fail_duration, dt)
        Updates the EV parks in the power system     
    update_fail_status(dt)
        Updates the failure status for each component that can fail in the power system 
    get_system_load()
        Returns the system load at the current time in MW and MVar
    get_max_load()
        Get the maximum load of the power system for the entire load history in MW and MVar
    add_load_dict(load_dict, time_indices)
    add_prod_dict(prod_dict, time_indices)
    set_load(inc_idx)
        Sets the load at the buses in the power system 
    set_prod(inc_idx)
        Sets the generation (generation units, batteries, EV parks) at the buses in the power system
    failes_comp()
        Returns True if the power system contains a failed compoent, False otherwise
    full_batteries()
        Returns True if the batteries in the power system are full, and False otherwise
    reset_load_flow_data()
        Resets the variables used in the load flow analysis
    get_monte_carlo_history(attribute)
        Returns the specified history variable from the Monte Carlo simulation
    get_history(attribute)
        Returns the specified history variable
    reset_load_shed_variables()
        Resets the load shed variables

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
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0
        # Sub-systems
        self.sub_systems = list()
        # Components
        self.buses = list()
        self.ev_parks = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()
        self.sensors = list()
        self.circuitbreakers = list()
        self.disconnectors = list()
        self.intelligent_switches = list()
        self.controller = controller
        self.comp_list = list()
        self.comp_dict = dict()
        ## Child networks
        self.child_network_list: list = list()
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
        Adding a bus to the power system
 
        Paramters
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
        Adding a bus including elements on the bus (battery, generation unit, EV parkt) to the power system
        
        Paramters
        ----------
        buses : list 
            A list of Bus elements in the power system 

        Returns
        ----------
        None

        """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding a line including elements on the line (sensor, circuit breaker, disconnector) to the power system
 
        Paramters
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
            for discon in c_b.disconnectors:
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
                    self.intelligent_switches = unique(
                        self.intelligent_switches
                    )
        self.comp_list = unique(self.comp_list)

    def add_lines(self, lines: list):
        """
        Adding lines to the power system
       
        Paramters
        ----------
        lines : list 
            A list of Line elements in the power system 

        Returns
        ----------
        None

        """
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the power system

        Paramters
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
        
        Paramters
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
        
        Paramters
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
        
        Paramters
        ----------
        network : Network 
            A list of Line elements in the power system 

        Returns
        ----------
        None

        """
        self.child_network_list.append(network)

    def reset_slack_bus(self):
        """
        Resets the slack bus of the child networks
        
        Paramters
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
        
        Paramters
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
        
        Paramters
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
        
        Paramters
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
                    if bus == child_network.get():
                        system_load_balance_p = -INF
                        system_load_balance_q = 0
                        return system_load_balance_p, system_load_balance_q
            system_load_balance_p += bus.pload - bus.pprod
            system_load_balance_q += bus.qload - bus.qprod
        return system_load_balance_p, system_load_balance_q

    def update_batteries(self, fail_duration: Time, dt: Time):
        """
        Updates the batteries in the power system
        
        Paramters
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

    def update_ev_parks(self, fail_duration: Time, dt: Time):
        """
        Updates the EV parks in the power system
        
        Paramters
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
        for ev_park in self.ev_parks:
            p, q = ev_park.update(p, q, fail_duration, dt)


    def update_fail_status(self, dt: Time):
        """
        Updates the failure status for each component that can fail in the power system 
        
        Paramters
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
        self.controller.update_fail_status(dt)

    def get_system_load(self):
        """
        Returns the system load at the current time in MW and MVar
        
        Paramters
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

    def get_max_load(self):
        """
        Get the maximum load of the power system for the entire load history in MW and MVar

        Parameters
        ----------
        None

        Returns
        ----------
        p_load_max : float
            The maximum active power load of the power system for the entire load history

        q_load_max : float
            The maximum reactive power load of the power system for the entire load history

        """
        p_load_max, q_load_max = 0, 0
        for bus in self.buses:
            if bus.load_dict != dict():
                d_bus = bus  # Dummy bus used to find number of increments
                n_increments = len(
                    d_bus.load_dict["load"][
                        list(d_bus.load_dict["load"].keys())[0]
                    ]["pload"].flatten()
                )  # Number of increments
                break
        for increment in range(n_increments):
            p_load, q_load = 0, 0
            for bus in self.buses:
                if bus.load_dict != dict():
                    for load_type in bus.load_dict["load"]:
                        p_load += (
                            bus.load_dict["load"][load_type][
                                "pload"
                            ].flatten()[increment]
                            * bus.n_customers
                        )
                        q_load += (
                            bus.load_dict["load"][load_type][
                                "qload"
                            ].flatten()[increment]
                            * bus.n_customers
                        )
            p_load_max = max(p_load_max, p_load)
            q_load_max = max(q_load_max, q_load)
        return p_load_max, q_load_max

    def add_load_dict(self, load_dict: dict, time_indices: np.ndarray):
        """
        Returns the system load at the current time in MW and MVar
        
        Paramters
        ----------
        load_dict : dict
        time_indices ? 

        Returns
        ----------
        None

        """
        for bus in self.buses:
            if bus in load_dict["load"]:
                bus_load_dict = {}
                bus_load_dict["load"] = {}
                bus_load_dict["cost"] = load_dict["cost"]
                for load_type in load_dict["load"][bus]:
                    bus_load_dict["load"][load_type] = {}
                    bus_load_dict["load"][load_type]["pload"] = interpolate(
                        array=load_dict["load"][bus][load_type]["pload"],
                        time_indices=time_indices,
                    )
                    bus_load_dict["load"][load_type]["qload"] = interpolate(
                        array=load_dict["load"][bus][load_type]["qload"],
                        time_indices=time_indices,
                    )
                bus.add_load_dict(bus_load_dict)

    def add_prod_dict(self, prod_dict: dict, time_indices: np.ndarray):
        """
        Returns the system load at the current time in MW and MVar
        
        Paramters
        ----------
        prod_dict : dict
        time_indices ? 

        Returns
        ----------
        None

        """
        for prod in self.productions:
            if prod in prod_dict:
                bus_prod_dict = {}
                for prod_type in prod_dict[prod]:
                    bus_prod_dict[prod_type] = interpolate(
                        array=prod_dict[prod][prod_type],
                        time_indices=time_indices,
                    )
                prod.add_prod_dict(bus_prod_dict)

    def set_load(self, inc_idx: int):
        """
        Sets the load at the buses in the power system 
        
        Paramters
        ----------
        inc_idx : int
            Increment index

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.set_load(inc_idx)

    def set_prod(self, inc_idx: int):
        """
        Sets the generation (generation units, batteries, EV parks) at the buses in the power system 
        
        Paramters
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
        Returns True if the power system contains a failed component, and False otherwise
        
        Paramters
        ----------
        None

        Returns
        ----------
        True/False

        """
        return any(
            [True if bus.trafo_failed else False for bus in self.buses]
        ) or any([True if line.failed else False for line in self.lines])

    def full_batteries(self):
        """
        Returns True if the batteries in the power system are full, and False otherwise
        
        Paramters
        ----------
        None

        Returns
        ----------
        True/False

        """
        return all(
            [
                True if eq(battery.SOC, battery.SOC_max) else False
                for battery in self.batteries
            ]
        )

    def reset_load_flow_data(self):
        """
        Reset the variables used in the load flow analysis
        
        Paramters
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

    def reset_load_shed_variables(self):
        """
        Resets the load shed variables
        
        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0
