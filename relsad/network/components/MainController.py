import matplotlib.lines as mlines
import numpy as np

from relsad.Time import Time, TimeUnit
from relsad.utils import convert_yearly_fail_rate, random_choice

from .Component import Component
from .Controller import Controller, ControllerState
from .ICTNode import ICTNode


class MainController(Component, Controller):

    """
    Common class for main controller

    ...

    Attributes
    ----------
    name : string
        Name of the main controller
    ict_node : ICTNode
        The ICT node connected to the controller
    harware_fail_rate_per_year : float
        The failure rate per year for hardware failuers of the controller
    software_fail_rate_per_year : float
        The failure rate per year for software failures of the controller
    p_fail_repair_new_signal : float
        The probability tuat a new signal cannot be sent
    p_fail_reboot : float
        The probability that a reboot of the controller will fail to fix the failure
    new_signal_time : Time
        The time it takes to send a new signal
    reboot_time : Time
        The time it takes to reboot the controller
    remaining_repair_time : Time
        The remaining time of the repair
    manual_software_repair_time : Time
        The time it takes to manually repair a software failure
    manual_hardware_repair_time : Time
        The time it takes to manually repair a hardware failure
    state : enum
        The state of the controller
    sectioning_time : Time
        The sectioning time of the system (can differ based on if the controller is OK or not)
    manual_sectioning_time : Time
        The sectioning time of a passive system without controller (controller is failed)
    distribution_controllers : list
        List of controllers from the distribution systems in the power system
    microgrid_controllers : list
        List of controllers from the microgrids in the power system
    history : dict
        Dictonary attribute that stores the historic variables
    monte_carlo_history : dict
        Dictonary attribute that stores the historic variables from the Monte Carlo simulation


    Methods
    ----------
    fail_software()
        Sets the controller state to software fail
    fail_hardware()
        Sets the controller state to hardware fail
    not_fail()
        Sets the controller state to ok (not fail)
    draw_fail_status(dt)
        Draws the failure status of the controller
    draw_hardware_status(prob)
        Draws if a hardware failure has occured and sets the fail status of the controller
    draw_software_status(prob)
        Draws if a software failure has occured and sets the fail status of the controller
    repair_software_fail(dt)
        Goes through the repair sequence of a software failure, draws the repair mechanism, returns the repair time and updates the state of the controller
    update_fail_status(dt)
        Updates the failure status of the controller based on the remaining outage time
    add_distribution_controller(controller)
        Adds distribution controllers from connected distribution systems to a list and
        sets the sectioning time for the controller. Assignes the
        ICT node to the distribution system controller.
    add_microgrid_controller(controller)
        Adds microgird controllers from connected microgrids to a list and
        sets the sectioning time for the controller. Assignes the
        ICT node to the microgrid controller.
    run_control_loop(curr_time, dt)
        Runs the control loop for the distribution system controllers and the microgird controllers
    spread_sectioning_time_to_sub_controllers()
        Sets the sectioning time for the controllers in the connected distribution systems and microgrids
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_instance(random_gen)
        Adds global random seed
    print_status()
        Prints the status
    reset_status(save_flag)
        Resets and sets the status of the class parameters
    initialize_history()
        Initializes the history variables
    """

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        ict_node: ICTNode = None,
        hardware_fail_rate_per_year: float = 0.2,
        software_fail_rate_per_year: float = 12,
        p_fail_repair_new_signal: float = 1 - 0.95,
        p_fail_repair_reboot: float = 0.9,
        new_signal_time: Time = Time(2, TimeUnit.SECOND),
        reboot_time: Time = Time(5, TimeUnit.MINUTE),
        manual_software_repair_time: Time = Time(0.3, TimeUnit.HOUR),
        manual_hardware_repair_time: Time = Time(2.5, TimeUnit.HOUR),
        manual_sectioning_time: Time = Time(1, TimeUnit.HOUR),
        state: ControllerState = ControllerState.OK,
    ):

        self.name = name
        self.ict_node = ict_node
        self.hardware_fail_rate_per_year = hardware_fail_rate_per_year
        self.software_fail_rate_per_year = software_fail_rate_per_year
        self.p_fail_repair_new_signal = p_fail_repair_new_signal
        self.p_fail_repair_reboot = p_fail_repair_reboot
        self.new_signal_time = new_signal_time
        self.reboot_time = reboot_time
        self.remaining_repair_time = Time(0)
        self.manual_software_repair_time = manual_software_repair_time
        self.manual_hardware_repair_time = manual_hardware_repair_time
        self.state = state
        self.sectioning_time = Time(0)
        self.manual_sectioning_time = manual_sectioning_time

        self.distribution_controllers = list()
        self.microgrid_controllers = list()

        ## History
        self.history = {}
        self.monte_carlo_history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"MainController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, MainController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def fail_software(self):
        """
        Sets the controller state to software fail

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = ControllerState.SOFTWARE_FAIL

    def fail_hardware(self):
        """
        Sets the controller state to hardware fail

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = ControllerState.HARDWARE_FAIL

    def not_fail(self):
        """
        Sets the controller state to ok (not fail)

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = ControllerState.OK

    def draw_fail_status(self, dt: Time):
        """
        Draws the failure status of the controller

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        p_hardware_fail = convert_yearly_fail_rate(
            self.hardware_fail_rate_per_year, dt
        )
        self.draw_hardware_status(p_hardware_fail)
        if self.state == ControllerState.OK:
            p_software_fail = convert_yearly_fail_rate(
                self.software_fail_rate_per_year, dt
            )
            self.draw_software_status(p_software_fail)

    def draw_hardware_status(self, prob):
        """
        Draws if a hardware failure has occured and sets the fail status of the controller

        Parameters
        ----------
        prob : float
            The probability of a hardware failure

        Returns
        ----------
        None

        """
        if random_choice(self.ps_random, prob):
            self.fail_hardware()
        else:
            self.not_fail()

    def draw_software_status(self, prob):
        """
        Draws if a software failure has occured and sets the fail status of the controller

        Parameters
        ----------
        prob : float
            The probability of a software failure

        Returns
        ----------
        None

        """
        if random_choice(self.ps_random, prob):
            self.fail_software()
        else:
            self.not_fail()

    def repair_software_fail(self, dt: Time):
        """
        Goes through the repair sequence of a software failure, draws the repair mechanism, returns the repair time and updates the state of the controller

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        repair_time : Time
            The repair time of the software failure

        """

        repair_time = self.new_signal_time
        self.draw_software_status(self.p_fail_repair_new_signal)
        if self.state == ControllerState.OK:
            return repair_time
        elif self.state == ControllerState.SOFTWARE_FAIL:
            repair_time += self.reboot_time
            self.draw_software_status(self.p_fail_repair_reboot)
            if self.state == ControllerState.SOFTWARE_FAIL:
                self.remaining_repair_time = self.manual_software_repair_time
                self.state = ControllerState.REPAIR
            return repair_time

    def update_fail_status(self, dt: Time):
        """
        Updates the failure status of the controller based on the remaining outage time

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.state == ControllerState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time <= Time(0):
                self.not_fail()
        elif self.state == ControllerState.OK:
            self.draw_fail_status(dt)
            if self.state == ControllerState.HARDWARE_FAIL:
                self.remaining_repair_time = self.manual_hardware_repair_time
                self.state = ControllerState.REPAIR
            elif self.state == ControllerState.SOFTWARE_FAIL:
                self.sectioning_time = self.repair_software_fail(dt)
                self.spread_sectioning_time_to_sub_controllers()

    def add_distribution_controller(self, controller):
        """
        Adds distribution controllers from connected distribution systems to a list and
        sets the sectioning time for the controller. Assignes the
        ICT node to the distribution system controller.

        Parameters
        ----------
        controller : Controller
            Distribution system controller

        Returns
        ----------
        None

        """
        self.distribution_controllers.append(controller)
        controller.manual_sectioning_time = self.manual_sectioning_time
        controller.ict_node = self.ict_node
        if self.ict_node is not None:
            controller.ict_network = self.ict_node.parent_network

    def add_microgrid_controller(self, controller):
        """
        Adds microgird controllers from connected microgrids to a list and
        sets the sectioning time for the controller. Assignes the
        ICT node to the microgrid controller.

        Parameters
        ----------
        controller : Controller
            Microgird controller

        Returns
        ----------
        None

        """
        self.microgrid_controllers.append(controller)
        controller.manual_sectioning_time = self.manual_sectioning_time
        controller.ict_node = self.ict_node
        if self.ict_node is not None:
            controller.ict_network = self.ict_node.parent_network

    def run_control_loop(self, curr_time: Time, dt: Time):
        """
        Runs the control loop for the distribution system controllers and the microgird controllers

        Parameters
        ----------
        curr_time : Time
            The current time
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.state == ControllerState.OK:
            for controller in self.distribution_controllers:
                controller.run_control_loop(curr_time, dt)
            for controller in self.microgrid_controllers:
                controller.run_control_loop(curr_time, dt)
        elif self.state == ControllerState.REPAIR:
            for controller in self.distribution_controllers:
                controller.run_manual_control_loop(curr_time, dt)
            for controller in self.microgrid_controllers:
                controller.run_manual_control_loop(curr_time, dt)

    def spread_sectioning_time_to_sub_controllers(self):
        """
        Sets the sectioning time for the controllers in the connected distribution systems and microgrids

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for controller in self.distribution_controllers:
            if controller.power_network.connected_line.circuitbreaker.is_open:
                controller.set_sectioning_time(self.sectioning_time)
        for controller in self.microgrid_controllers:
            if controller.power_network.connected_line.circuitbreaker.is_open:
                controller.set_sectioning_time(self.sectioning_time)

    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        """
        Updates the history variables

        Parameters
        ----------
        prev_time : Time
            The previous time
        curr_time : Time
            Current time
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["sectioning_time"][
                time
            ] = self.sectioning_time.get_unit_quantity(curr_time.unit)
            self.history["remaining_repair_time"][
                time
            ] = self.remaining_repair_time.get_unit_quantity(curr_time.unit)
            self.history["state"][time] = self.state.value

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute

        Parameters
        ----------
        attribute : str
            Controller attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def add_random_instance(self, random_gen):
        """
        Adds global random seed

        Parameters
        ----------
        random_gen : int
            Random number generator

        Returns
        ----------
        None

        """
        self.ps_random = random_gen

    def print_status(self):
        """
        Prints the status

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        pass

    def reset_status(self, save_flag: bool):
        """
        Resets and sets the status of the class parameters

        Parameters
        ----------
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        self.state = ControllerState.OK
        self.sectioning_time = Time(0)
        self.remaining_repair_time = Time(0)
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        """
        Initializes the history variables

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.history["sectioning_time"] = {}
        self.history["remaining_repair_time"] = {}
        self.history["state"] = {}
