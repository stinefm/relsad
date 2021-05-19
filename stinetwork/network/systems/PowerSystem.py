import os
import numpy as np
from numpy.lib.npyio import save
from scipy.optimize import linprog, OptimizeWarning
from stinetwork.network.components import (
    Bus,
    Line,
    CircuitBreaker,
    Disconnector,
    Component,
)
from .Transmission import Transmission
from stinetwork.utils import eq
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.topology.paths import find_backup_lines_between_sub_systems
from stinetwork.visualization.plotting import (
    plot_topology,
    plot_history,
    plot_history_last_state,
    plot_monte_carlo_history,
)
from stinetwork.results.storage import save_history, save_monte_carlo_history
from stinetwork.utils import unique, subtract

np.set_printoptions(suppress=True, linewidth=np.nan)


class PowerSystem:

    ## Visual attributes
    color = "black"

    ## Counter
    counter = 0

    ## Load shed configurations
    shed_configs = list()

    ## Load shedding
    p_load_shed = 0
    acc_p_load_shed = 0
    q_load_shed = 0
    acc_q_load_shed = 0

    ## Random instance
    ps_random = None

    ## History
    all_comp_list = list()
    all_buses = list()
    all_batteries = list()
    all_productions = list()
    all_lines = list()
    history = {}

    monte_carlo_history = {}

    def __init__(self):
        """Initializing power system content
        Content:
            buses(set): List of buses
            lines(set): List of lines
            comp_dict(dict): Dictionary of components
        """
        PowerSystem.counter += 1
        self.name = "ps{:d}".format(PowerSystem.counter)

        self.slack = None

        self.sub_systems = list()

        self.buses = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()

        self.comp_list = list()
        self.comp_dict = dict()

        self.child_network_list = list()

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

    def add_random_instance(self, random_instance):
        """
        Adds a global numpy random instance
        """
        PowerSystem.ps_random = random_instance
        for comp in PowerSystem.all_comp_list:
            comp.add_random_seed(PowerSystem.ps_random)

    def add_bus(self, bus: Bus):
        """
        Adding bus to power system
        Input: bus(Bus)
        """
        self.comp_dict[bus.name] = bus
        self.comp_list.append(bus)
        PowerSystem.all_comp_list.append(bus)
        self.buses.append(bus)
        self.buses = unique(self.buses)
        PowerSystem.all_buses.append(bus)
        PowerSystem.all_buses = unique(PowerSystem.all_buses)
        if bus.battery is not None:
            self.comp_dict[bus.battery.name] = bus.battery
            self.comp_list.append(bus.battery)
            self.batteries.append(bus.battery)
            self.batteries = unique(self.batteries)
            PowerSystem.all_comp_list.append(bus.battery)
            PowerSystem.all_batteries.append(bus.battery)
            PowerSystem.all_batteries = unique(PowerSystem.all_batteries)
        if bus.prod is not None:
            self.comp_dict[bus.prod.name] = bus.prod
            self.comp_list.append(bus.prod)
            self.productions.append(bus.prod)
            self.productions = unique(self.productions)
            PowerSystem.all_comp_list.append(bus.prod)
            PowerSystem.all_productions.append(bus.prod)
            PowerSystem.all_productions = unique(PowerSystem.all_productions)

        self.comp_list = unique(self.comp_list)
        PowerSystem.all_comp_list = unique(PowerSystem.all_comp_list)

    def add_buses(self, buses: set):
        """Adding buses to power system
        Input: buses(list(Bus))"""
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding line to power system
        Input: line(Line)
        """
        self.comp_dict[line.name] = line
        self.comp_list.append(line)
        PowerSystem.all_comp_list.append(line)
        self.lines.append(line)
        PowerSystem.all_lines.append(line)
        PowerSystem.all_lines = unique(PowerSystem.all_lines)
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
            self.comp_list.append(discon)
            PowerSystem.all_comp_list.append(discon)
        if line.circuitbreaker is not None:
            c_b = line.circuitbreaker
            self.comp_dict[c_b.name] = c_b
            self.comp_list.append(c_b)
            PowerSystem.all_comp_list.append(c_b)
            for discon in c_b.disconnectors:
                self.comp_dict[discon.name] = discon
                self.comp_list.append(discon)
                PowerSystem.all_comp_list.append(discon)

        PowerSystem.all_comp_list = unique(PowerSystem.all_comp_list)
        self.comp_list = unique(self.comp_list)

    def add_lines(self, lines: set):
        """Adding lines to power system
        Input: lines(list(Line))"""
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the power system
        """
        return self.lines

    def get_comp(self, name: str):
        """
        Returns component based on given name
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
        """
        return self.comp_list

    def add_child_network(self, network):
        """
        Adding child network to power system
        """
        self.child_network_list.append(network)

    def reset_slack_bus(self):
        """
        Resets the slack bus of the child networks
        """
        for child_network in self.child_network_list:
            child_network.reset_slack_bus()

    def print_status(self):
        """
        Prints the status of the buses and lines in the power system
        """
        print("Buses:")
        for bus in self.buses:
            bus.print_status()
        print("Lines:")
        for line in self.lines:
            line.print_status()

    # flake8: noqa: C901
    def shed_loads(self):
        """
        Sheds the unsupplied loads of the power system using a linear minimization
        problem solved with linear programming
        """

        if len(self.sub_systems) <= 1:
            buses = list(self.buses)
            cost = [x.get_cost() for x in buses]
            lines = [x for x in self.lines if x.connected]
            N_D = len(buses)
            N_L = len(lines)
            c = cost + [0] * N_L + [0] * N_D
            A = np.zeros((N_D, N_D + N_L + N_D))
            p_b = list()  # Active bus load
            q_b = list()  # Reactive bus load
            p_gen = list()  # Active bus generation
            q_gen = list()  # Reactive bus generation
            # Building A-matrix
            for j, bus in enumerate(buses):
                A[j, j] = 1  # lambda_md
                A[j, N_D + N_L + j] = 1  # mu_md
                for line in bus.connected_lines:
                    if line.connected:
                        index = lines.index(line)
                        if bus == line.fbus:
                            A[j, N_D + index] = -1
                        else:
                            A[j, N_D + index] = 1
                p_b.append(max(0, bus.pload))
                q_b.append(max(0, bus.qload))
                flag = False
                for child_network in self.child_network_list:
                    if isinstance(child_network, Transmission):
                        if bus == child_network.get():
                            p_gen.append(np.inf)
                            q_gen.append(np.inf)
                            flag = True
                if flag is False:
                    p_gen.append(max(0, bus.pprod))
                    q_gen.append(max(0, bus.qprod))
            p_bounds = list()
            q_bounds = list()
            for n in range(N_D + N_L + N_D):
                if n < N_D:
                    p_bounds.append((0, p_b[n]))
                    q_bounds.append((0, q_b[n]))
                elif n >= N_D and n < N_D + N_L:
                    line = lines[n - N_D]
                    (
                        max_available_p_flow,
                        max_available_q_flow,
                    ) = line.get_line_load()[:2]
                    PL_p_max = min(line.capacity, abs(max_available_p_flow))
                    PL_q_max = min(line.capacity, abs(max_available_q_flow))
                    p_bounds.append((-PL_p_max, PL_p_max))
                    q_bounds.append((-PL_q_max, PL_q_max))
                else:
                    p_bounds.append((0, p_gen[n - (N_D + N_L)]))
                    q_bounds.append((0, q_gen[n - (N_D + N_L)]))
            try:
                p_res = linprog(
                    c,
                    A_eq=A,
                    b_eq=p_b,
                    bounds=p_bounds,
                    # options={
                    #     "cholesky": False,
                    #     "sym_pos": False,
                    #     "lstsq": True,
                    #     "rr": False,
                    # },
                )
            except OptimizeWarning:
                p_res = linprog(
                    c,
                    A_eq=A,
                    b_eq=p_b,
                    bounds=p_bounds,
                    # options={
                    #     "cholesky": False,
                    #     "sym_pos": False,
                    #     "lstsq": True,
                    #     "rr": False,
                    # },
                )
                print(buses, lines)
                self.print_status()
                print("Active:\n")
                print("c:\n", c)
                print("A_eq:\n", A)
                print("rank A:", np.linalg.matrix_rank(A), A.shape[0], A.size)
                print("b_eq_p:\n", p_b)
                print("Bounds_p:\n", p_bounds)
                print("Results_p:", p_res)

                fig = plot_topology(buses, lines)
                fig.show()
                raise OptimizeWarning
            try:
                q_res = linprog(
                    c,
                    A_eq=A,
                    b_eq=q_b,
                    bounds=q_bounds,
                    # options={
                    #     "cholesky": False,
                    #     "sym_pos": False,
                    #     "lstsq": True,
                    #     "rr": False,
                    # },
                )
            except OptimizeWarning:
                q_res = linprog(
                    c,
                    A_eq=A,
                    b_eq=q_b,
                    bounds=q_bounds,
                    # options={
                    #     "cholesky": False,
                    #     "sym_pos": False,
                    #     "lstsq": True,
                    #     "rr": False,
                    # },
                )
                print(buses, lines)
                self.print_status()
                print("Active:\n")
                print("c:\n", c)
                print("A_eq:\n", A)
                print("rank A:", np.linalg.matrix_rank(A), A.shape[0], A.size)
                print("b_eq_q:\n", q_b)
                print("Bounds_q:\n", q_bounds)
                print("Results_q:", q_res)

                fig = plot_topology(buses, lines)
                fig.show()
                raise OptimizeWarning

            if p_res.fun > 0 or q_res.fun > 0:
                for i, bus in enumerate(buses):
                    bus.add_to_load_shed_stack(p_res.x[i], q_res.x[i])
                if len(PowerSystem.shed_configs) == 0:
                    PowerSystem.shed_configs.append(self)
                add = True
                for shed_config in PowerSystem.shed_configs:
                    if self == shed_config:
                        add = False
                        break
                if add:
                    PowerSystem.shed_configs.append(self)

        else:
            raise Exception("More than one sub system")

    def get_system_load_balance(self):
        """
        Returns the load balance of the system
        """
        system_load_balance_p, system_load_balance_q = 0, 0
        for bus in self.buses:
            for child_network in self.child_network_list:
                if type(child_network) == Transmission:
                    if bus == child_network.get():
                        system_load_balance_p = -np.inf
                        system_load_balance_q = 0
                        return system_load_balance_p, system_load_balance_q
            system_load_balance_p += bus.pload - bus.pprod
            system_load_balance_q += bus.qload - bus.qprod
        return system_load_balance_p, system_load_balance_q

    def update_batteries(self):
        """
        Updates the batteries in the power system
        """
        p, q = self.get_system_load_balance()
        for battery in self.batteries:
            p, q = battery.update_bus_load_and_prod(p, q)

    def plot_bus_history(self, save_dir: str):
        """
        Plots the history of the buses in the power system
        """
        plot_history(self.buses, "pload", save_dir)
        plot_history(self.buses, "qload", save_dir)
        plot_history(self.buses, "pprod", save_dir)
        plot_history(self.buses, "qprod", save_dir)
        plot_history(self.buses, "remaining_outage_time", save_dir)
        plot_history(self.buses, "trafo_failed", save_dir)
        plot_history(self.buses, "p_load_shed_stack", save_dir)
        plot_history_last_state(self.buses, "acc_p_load_shed", save_dir)
        plot_history(self.buses, "q_load_shed_stack", save_dir)
        plot_history_last_state(self.buses, "acc_q_load_shed", save_dir)
        plot_history(self.buses, "voang", save_dir)
        plot_history(self.buses, "vomag", save_dir)
        plot_history_last_state(self.buses, "avg_fail_rate", save_dir)
        plot_history_last_state(self.buses, "avg_outage_time", save_dir)

    def save_bus_history(self, save_dir: str):
        """
        saves the history of the buses in the power system
        """
        save_history(self.buses, "pload", save_dir)
        save_history(self.buses, "qload", save_dir)
        save_history(self.buses, "pprod", save_dir)
        save_history(self.buses, "qprod", save_dir)
        save_history(self.buses, "remaining_outage_time", save_dir)
        save_history(self.buses, "trafo_failed", save_dir)
        save_history(self.buses, "p_load_shed_stack", save_dir)
        save_history(self.buses, "acc_p_load_shed", save_dir)
        save_history(self.buses, "q_load_shed_stack", save_dir)
        save_history(self.buses, "acc_q_load_shed", save_dir)
        save_history(self.buses, "voang", save_dir)
        save_history(self.buses, "vomag", save_dir)
        save_history(self.buses, "avg_fail_rate", save_dir)
        save_history(self.buses, "avg_outage_time", save_dir)

    def plot_battery_history(self, save_dir: str):
        """
        Plots the history of the battery in the power system
        """
        plot_history(self.batteries, "SOC", save_dir)
        plot_history(self.batteries, "SOC_min", save_dir)
        plot_history(self.batteries, "remaining_survival_time", save_dir)

    def save_battery_history(self, save_dir: str):
        """
        Saves the history of the battery in the power system
        """
        save_history(self.batteries, "SOC", save_dir)
        save_history(self.batteries, "SOC_min", save_dir)
        save_history(self.batteries, "remaining_survival_time", save_dir)

    def plot_power_system_history(self, save_dir: str):
        """
        Plots the history of the power system
        """
        plot_history([self], "p_load_shed", save_dir)
        plot_history_last_state([self], "acc_p_load_shed", save_dir)
        plot_history([self], "q_load_shed", save_dir)
        plot_history_last_state([self], "acc_q_load_shed", save_dir)
        plot_history([self], "p_load", save_dir)
        plot_history([self], "q_load", save_dir)

    def save_power_system_history(self, save_dir: str):
        """
        Saves the history of the power system
        """
        save_history([self], "p_load_shed", save_dir)
        save_history([self], "acc_p_load_shed", save_dir)
        save_history([self], "q_load_shed", save_dir)
        save_history([self], "acc_q_load_shed", save_dir)
        save_history([self], "p_load", save_dir)
        save_history([self], "q_load", save_dir)

    def plot_monte_carlo_history(self, save_dir: str):
        """
        Plots the history of the load shedding in the power system
        """
        plot_monte_carlo_history([self], "acc_p_load_shed", save_dir)
        plot_monte_carlo_history([self], "acc_q_load_shed", save_dir)
        for bus in PowerSystem.all_buses:
            bus_save_dir = os.path.join(save_dir, bus.name)
            self.plot_monte_carlo_comp_history(
                bus, "acc_p_load_shed", bus_save_dir
            )
            self.plot_monte_carlo_comp_history(
                bus, "acc_q_load_shed", bus_save_dir
            )
            self.plot_monte_carlo_comp_history(
                bus, "avg_outage_time", bus_save_dir
            )

    def save_monte_carlo_history(self, save_dir: str):
        """
        Saves the history of the load shedding in the power system
        """
        save_monte_carlo_history([self], "acc_p_load_shed", save_dir)
        save_monte_carlo_history([self], "acc_q_load_shed", save_dir)
        for bus in PowerSystem.all_buses:
            bus_save_dir = os.path.join(save_dir, bus.name)
            self.save_monte_carlo_comp_history(
                bus, "acc_p_load_shed", bus_save_dir
            )
            self.save_monte_carlo_comp_history(
                bus, "acc_q_load_shed", bus_save_dir
            )
            self.save_monte_carlo_comp_history(
                bus, "avg_outage_time", bus_save_dir
            )

    def plot_monte_carlo_comp_history(
        self, comp: Component, attribute: str, bus_save_dir: str
    ):
        plot_monte_carlo_history(
            [self], comp.name + "_" + attribute, bus_save_dir
        )

    def save_monte_carlo_comp_history(
        self, comp: Component, attribute: str, bus_save_dir: str
    ):
        save_monte_carlo_history(
            [self], comp.name + "_" + attribute, bus_save_dir
        )

    def plot_line_history(self, save_dir: str):
        """
        Plots the history of the line in the power system
        """
        plot_history(self.lines, "p_from", save_dir)
        plot_history(self.lines, "q_from", save_dir)
        plot_history(self.lines, "p_to", save_dir)
        plot_history(self.lines, "q_to", save_dir)
        plot_history(self.lines, "remaining_outage_time", save_dir)
        plot_history(self.lines, "failed", save_dir)
        plot_history(self.lines, "line_loading", save_dir)

    def save_line_history(self, save_dir: str):
        """
        Saves the history of the line in the power system
        """
        save_history(self.lines, "p_from", save_dir)
        save_history(self.lines, "q_from", save_dir)
        save_history(self.lines, "p_to", save_dir)
        save_history(self.lines, "q_to", save_dir)
        save_history(self.lines, "remaining_outage_time", save_dir)
        save_history(self.lines, "failed", save_dir)
        save_history(self.lines, "line_loading", save_dir)

    def plot_circuitbreaker_history(self, save_dir: str):
        """
        Plots the history of the circuitbreakers in the power system
        """
        plot_history(
            [x for x in self.comp_list if type(x) == CircuitBreaker],
            "is_open",
            save_dir,
        )
        plot_history(
            [x for x in self.comp_list if type(x) == CircuitBreaker],
            "remaining_section_time",
            save_dir,
        )
        plot_history(
            [x for x in self.comp_list if type(x) == CircuitBreaker],
            "prev_section_time",
            save_dir,
        )

    def save_circuitbreaker_history(self, save_dir: str):
        """
        Saves the history of the circuitbreakers in the power system
        """
        save_history(
            [x for x in self.comp_list if type(x) == CircuitBreaker],
            "is_open",
            save_dir,
        )
        save_history(
            [x for x in self.comp_list if type(x) == CircuitBreaker],
            "remaining_section_time",
            save_dir,
        )
        save_history(
            [x for x in self.comp_list if type(x) == CircuitBreaker],
            "prev_section_time",
            save_dir,
        )

    def plot_disconnector_history(self, save_dir: str):
        """
        Plots the history of the disconnectors in the power system
        """
        plot_history(
            [x for x in self.comp_list if type(x) == Disconnector],
            "is_open",
            save_dir,
        )

    def save_disconnector_history(self, save_dir: str):
        """
        Saves the history of the disconnectors in the power system
        """
        save_history(
            [x for x in self.comp_list if type(x) == Disconnector],
            "is_open",
            save_dir,
        )

    def update_history(self, curr_time, save_flag: bool):
        """
        Updates the history variables in the power system
        """
        for bus in PowerSystem.all_buses:
            PowerSystem.p_load_shed += bus.p_load_shed_stack
            PowerSystem.q_load_shed += bus.q_load_shed_stack
        PowerSystem.acc_p_load_shed += PowerSystem.p_load_shed
        PowerSystem.acc_q_load_shed += PowerSystem.q_load_shed
        if save_flag:
            PowerSystem.history["p_load_shed"][
                curr_time
            ] = PowerSystem.p_load_shed
            PowerSystem.history["acc_p_load_shed"][
                curr_time
            ] = PowerSystem.acc_p_load_shed
            PowerSystem.history["q_load_shed"][
                curr_time
            ] = PowerSystem.q_load_shed
            PowerSystem.history["acc_q_load_shed"][
                curr_time
            ] = PowerSystem.acc_q_load_shed
            (
                PowerSystem.history["p_load"][curr_time],
                PowerSystem.history["q_load"][curr_time],
            ) = PowerSystem.get_system_load(PowerSystem)
        PowerSystem.p_load_shed = 0
        PowerSystem.q_load_shed = 0
        for comp in PowerSystem.all_comp_list:
            comp.update_history(curr_time, save_flag)
        # for bus in PowerSystem.all_buses:
        #     bus.reset_load_and_prod_attributes()

    def get_history(self, attribute):
        """
        Returns the specified history variable
        """
        return PowerSystem.history[attribute]

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable
        """
        return PowerSystem.monte_carlo_history[attribute]

    def get_system_load(self):
        """
        Returns the system load at curr_time in MW/MVar
        """
        pload, qload = 0, 0
        for bus in PowerSystem.all_buses:
            p, q = bus.get_load()
            pload += p
            qload += q
        return pload, qload

    def get_max_load(self):
        """
        Get the maximum load of the power system for the entire loading history in MW/MVar

        Parameters
        ----------
        None

        Returns
        ----------
        p_load_max : float
            The maximum active load of the power system for the entire loading history

        q_load_max : float
            The maximum reactive load of the power system for the entire loading history

        """
        p_load_max, q_load_max = 0, 0
        for bus in self.buses:
            if bus.load_dict != dict():
                d_bus = bus  # Dummy bus used to find number of increments
                n_increments = len(
                    d_bus.load_dict[list(d_bus.load_dict.keys())[0]][
                        "pload"
                    ].flatten()
                )  # Number of increments
                break
        for increment in range(n_increments):
            p_load, q_load = 0, 0
            for bus in self.buses:
                for load_type in bus.load_dict:
                    p_load += bus.load_dict[load_type]["pload"].flatten()[
                        increment
                    ]
                    q_load += bus.load_dict[load_type]["qload"].flatten()[
                        increment
                    ]
            p_load_max = max(p_load_max, p_load)
            q_load_max = max(q_load_max, q_load)
        return p_load_max, q_load_max

    def run_load_flow(self):
        """
        Runs load flow in power system
        """

        ## Run load flow
        self.buses = DistLoadFlow(list(self.buses), list(self.lines))

    def update_fail_status(self, curr_time):
        for bus in self.buses:
            bus.update_fail_status(curr_time)
        for line in self.lines:
            line.update_fail_status(curr_time)
        for comp in self.get_comp_list():
            if comp not in self.buses + self.lines:
                comp.update_fail_status(curr_time)

    def run_increment(self, curr_time, save_flag: bool):
        """
        Runs power system at current state for one time increment
        """
        # print("curr_time: {}".format(curr_time))

        if PowerSystem.ps_random is None:
            print(
                "Warning! No random instance was detected, creating a new one."
            )
            self.add_random_instance(np.random.default_rng())

        ## Set loads
        self.set_load(curr_time)

        ## Set productions
        self.set_prod(curr_time)

        ## Set fail status
        self.update_fail_status(curr_time)

        if self.failed_comp():
            ## Find sub systems
            find_sub_systems(self, curr_time)
            update_sub_system_slack(self)

            ## Load flow
            for sub_system in self.sub_systems:
                ## Update batteries and history
                sub_system.update_batteries()
                ## Run load flow
                if sub_system.slack is not None:
                    sub_system.reset_load_flow_data()
                    sub_system.run_load_flow()
                ## Shed load
                sub_system.shed_loads()

        elif not self.full_batteries():
            self.sub_systems = list()
            ## Load flow
            ## Update batteries and history
            self.update_batteries()
            ## Run load flow
            if self.slack is not None:
                self.reset_load_flow_data()
                self.run_load_flow()
            ## Shed load
            self.shed_loads()

        ## Log results
        self.update_history(curr_time, save_flag)

    def run_sequence(self, increments: int, save_flag: bool):
        """
        Runs power system for a sequence of increments
        """
        for curr_time in range(increments):
            if curr_time % 100 == 0:
                print("inc: {}".format(curr_time), flush=True)
            self.run_increment(curr_time, save_flag)

    def run_monte_carlo(
        self,
        iterations: int,
        increments: int,
        save_iterations: list = [],
        save_dir: str = "results",
    ):
        self.initialize_history(increments)
        self.initialize_monte_carlo_history(iterations)
        for it in range(iterations):
            save_flag = it in save_iterations
            self.reset_system(increments, save_flag)
            print("it: {}".format(it), flush=True)
            self.run_sequence(increments, save_flag)
            self.update_monte_carlo_history(it, increments)
            self.save_monte_carlo_history(
                os.path.join(save_dir, "monte_carlo")
            )

            if save_flag:
                self.save_iteration_history(it, save_dir)

    def initialize_history(self, increments: int):
        PowerSystem.history["p_load_shed"] = np.zeros(increments)
        PowerSystem.history["acc_p_load_shed"] = np.zeros(increments)
        PowerSystem.history["q_load_shed"] = np.zeros(increments)
        PowerSystem.history["acc_q_load_shed"] = np.zeros(increments)
        PowerSystem.history["p_load"] = np.zeros(increments)
        PowerSystem.history["q_load"] = np.zeros(increments)

    def initialize_monte_carlo_history(self, iterations: int):
        PowerSystem.monte_carlo_history["acc_p_load_shed"] = np.zeros(
            iterations
        )
        PowerSystem.monte_carlo_history["acc_q_load_shed"] = np.zeros(
            iterations
        )
        for bus in PowerSystem.all_buses:
            PowerSystem.monte_carlo_history[
                bus.name + "_" + "acc_p_load_shed"
            ] = np.zeros(iterations)
            PowerSystem.monte_carlo_history[
                bus.name + "_" + "acc_q_load_shed"
            ] = np.zeros(iterations)
            PowerSystem.monte_carlo_history[
                bus.name + "_" + "avg_outage_time"
            ] = np.zeros(iterations)

    def save_iteration_history(self, it: int, save_dir: str):
        if not os.path.isdir(os.path.join(save_dir, str(it))):
            os.mkdir(os.path.join(save_dir, str(it)))
        # self.plot_bus_history(os.path.join(save_dir, str(it), "bus"))
        # self.plot_battery_history(os.path.join(save_dir, str(it), "battery"))
        # self.plot_power_system_history(
        #     os.path.join(save_dir, str(it), "power_system")
        # )
        # self.plot_line_history(os.path.join(save_dir, str(it), "line"))
        # self.plot_circuitbreaker_history(
        #     os.path.join(save_dir, str(it), "circuitbreaker")
        # )
        # self.plot_disconnector_history(
        #     os.path.join(save_dir, str(it), "disconnector")
        # )

        self.save_bus_history(os.path.join(save_dir, str(it), "bus"))
        self.save_battery_history(os.path.join(save_dir, str(it), "battery"))
        self.save_power_system_history(
            os.path.join(save_dir, str(it), "power_system")
        )
        self.save_line_history(os.path.join(save_dir, str(it), "line"))
        self.save_circuitbreaker_history(
            os.path.join(save_dir, str(it), "circuitbreaker")
        )
        self.save_disconnector_history(
            os.path.join(save_dir, str(it), "disconnector")
        )

    def update_monte_carlo_history(self, it: int, increments: int):
        PowerSystem.monte_carlo_history["acc_p_load_shed"][
            it
        ] = PowerSystem.acc_p_load_shed
        PowerSystem.monte_carlo_history["acc_q_load_shed"][
            it
        ] = PowerSystem.acc_q_load_shed
        PowerSystem.update_monte_carlo_comp_history(PowerSystem, it)

    def update_monte_carlo_comp_history(self, it: int):
        for bus in PowerSystem.all_buses:
            PowerSystem.monte_carlo_history[
                bus.name + "_" + "acc_p_load_shed"
            ][it] = bus.acc_p_load_shed
            PowerSystem.monte_carlo_history[
                bus.name + "_" + "acc_q_load_shed"
            ][it] = bus.acc_q_load_shed
            PowerSystem.monte_carlo_history[
                bus.name + "_" + "avg_outage_time"
            ][it] = bus.avg_outage_time

    def reset_system(self, increments: int, save_flag: bool):
        PowerSystem.p_load_shed = 0
        PowerSystem.acc_p_load_shed = 0
        PowerSystem.q_load_shed = 0
        PowerSystem.acc_q_load_shed = 0
        PowerSystem.initialize_history(PowerSystem, increments)

        for comp in PowerSystem.all_comp_list:
            comp.reset_status(increments)

        ## Find sub systems
        find_sub_systems(self, 0)
        update_sub_system_slack(self)

    def add_load_dict(self, load_dict: dict):
        for bus in self.buses:
            if bus in load_dict:
                bus.add_load_dict(load_dict[bus])

    def add_prod_dict(self, prod_dict: dict):
        for prod in self.productions:
            if prod in prod_dict:
                prod.add_prod_dict(prod_dict[prod])

    def set_load(self, curr_time):
        for bus in self.buses:
            bus.set_load(curr_time)

    def set_prod(self, curr_time):
        for prod in self.productions:
            prod.set_prod(curr_time)
        for bus in self.buses:
            if bus.battery is not None:
                bus.reset_prod()

    def failed_comp(self):
        """
        Returns True if the power system contains a failed component, and False otherwise
        """
        return any(
            [
                True if bus.trafo_failed else False
                for bus in PowerSystem.all_buses
            ]
        ) or any(
            [True if line.failed else False for line in PowerSystem.all_lines]
        )

    def full_batteries(self):
        """
        Returns True if the batteries of the power system are full, and False otherwise
        """
        return all(
            [
                True if eq(battery.SOC, battery.SOC_max) else False
                for battery in PowerSystem.all_batteries
            ]
        )

    def reset_load_flow_data(self):
        """
        Reset the variables used in the load flow analysis
        """
        for bus in self.buses:
            bus.reset_load_flow_data()


def find_sub_systems(p_s: PowerSystem, curr_time):
    """
    Function that find the independent sub systems of the given power system
    and adds them to the sub_systems list of the power system
    """

    p_s.sub_systems = list()
    # Will only include connected lines
    active_lines = [line for line in p_s.lines if line.connected]
    used_buses = list()
    used_lines = list()
    sub_system = PowerSystem()

    def try_to_add_connected_lines(bus, sub_system, used_buses, used_lines):
        for line in subtract(bus.connected_lines, used_lines):
            if line.connected:
                sub_system.add_line(line)
                used_lines.append(line)
                used_lines = unique(used_lines)
                if line.tbus == bus:
                    sub_system, used_buses = add_bus(
                        line.fbus, sub_system, used_buses
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        line.fbus, sub_system, used_buses, used_lines
                    )
                else:
                    sub_system, used_buses = add_bus(
                        line.tbus, sub_system, used_buses
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        line.tbus, sub_system, used_buses, used_lines
                    )
        return sub_system, used_buses, used_lines

    def add_bus(bus, sub_system, used_buses):
        if bus not in unique(used_buses + sub_system.buses):
            sub_system.add_bus(bus)
            used_buses.append(bus)
            used_buses = unique(used_buses)
            for child_network in p_s.child_network_list:
                if bus in child_network.buses:
                    sub_system.add_child_network(child_network)
        return sub_system, used_buses

    while not (len(used_buses) + len(used_lines)) == (
        len(p_s.buses) + len(active_lines)
    ):
        for bus in p_s.buses:
            if bus not in unique(used_buses + sub_system.buses):
                if (len(sub_system.buses) + len(sub_system.lines)) == 0:
                    sub_system, used_buses = add_bus(
                        bus, sub_system, used_buses
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        bus, sub_system, used_buses, used_lines
                    )
                    p_s.sub_systems.append(sub_system)
                    p_s.sub_systems = unique(p_s.sub_systems)
                    if (len(used_buses) + len(used_lines)) == (
                        len(p_s.buses) + len(active_lines)
                    ):
                        break
                    sub_system = PowerSystem()

    if len(p_s.sub_systems) > 1:
        update_backup_lines_between_sub_systems(p_s, curr_time)


def update_backup_lines_between_sub_systems(p_s: PowerSystem, curr_time):
    """
    Function that updates the backup lines between the sub systems of the
    power system if they exist and are not failed
    """
    update = False
    for s_1 in p_s.sub_systems:
        for s_2 in p_s.sub_systems:
            if s_1 != s_2:
                external_backup_lines = find_backup_lines_between_sub_systems(
                    s_1, s_2
                )
                for line in external_backup_lines:
                    if not line.connected and not line.failed:
                        for discon in line.get_disconnectors():
                            if discon.is_open:
                                discon.close(curr_time)
                        update = True
                        break
            if update:
                break
        if update:
            break
    if update:
        find_sub_systems(p_s, curr_time)


def update_sub_system_slack(p_s: PowerSystem):
    """
    Function that updates the current slack bus of the sub systems of the
    power system
    """
    possible_sub_systems = list(p_s.sub_systems)
    for sub_system in possible_sub_systems:
        sub_system.slack = None
        for bus in sub_system.buses:
            bus.is_slack = False
            if set_slack(sub_system):
                break
        # if not set_slack(sub_system): # Remove sub system if slack is not found
        #     p_s.sub_systems.remove(sub_system)


def set_slack(p_s: PowerSystem):
    """
    Function that sets the slack bus of the power system
    """
    ## Transmission network slack buses in sub_system
    for bus in p_s.buses:
        for child_network in p_s.child_network_list:
            if type(child_network) == Transmission:
                if bus == child_network.get():
                    bus.set_slack()
                    p_s.slack = bus
                    return True
    ## Buses with battery
    if p_s.slack is None:
        for bus in p_s.buses:
            if (
                bus.battery is not None and bus.battery.mode is None
            ):  # Battery in Distribution network
                bus.set_slack()
                p_s.slack = bus
                return True
        for bus in p_s.buses:
            if (
                bus.battery is not None and bus.battery.mode is not None
            ):  # Battery in Microgrid
                if (
                    bus.battery.mode == 3
                    and bus.battery.remaining_survival_time == 0
                    and not bus.is_slack
                ):
                    bus.battery.start_survival_time()
                bus.set_slack()
                p_s.slack = bus
                return True
    ## Buses with production
    if p_s.slack is None:
        for bus in p_s.buses:
            if bus.prod is not None:
                bus.set_slack()
                p_s.slack = bus
                return True
    ## Not slack material
    return False


if __name__ == "__main__":
    pass
