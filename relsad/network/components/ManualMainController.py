import matplotlib.lines as mlines
import numpy as np

from relsad.Time import Time, TimeUnit
from relsad.utils import convert_yearly_fail_rate, random_choice

from .Component import Component
from .Controller import Controller


class ManualMainController(Component):

    """
    Common class for manual main controller

    ...

    Attributes
    ----------
    name : string
        Name of the manual main controller
    sectioning_time : Time
        The average sectioning time of the system
    power_system : PowerSystem
        The associated power system
    distribution_controllers : list
        List of controllers from the distribution systems in the power system
    microgrid_controllers : list
        List of controllers from the microgrids in the power system


    Methods
    ----------
    add_distribution_controller(controller)
        Adds distribution controllers from connected distribution systems to a list and sets the manual sectioning time for the controller
    add_microgrid_controller(controller)
        Adds microgird controllers from connected microgrids to a list and sets the manual sectioning time for the controller
    run_control_loop(curr_time, dt)
        Runs the manual control loop for the distribution system controllers and the microgird controllers
    update_fail_status(dt)
        Updates the failure status
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

    def __init__(
        self,
        name: str,
        sectioning_time: Time,
    ):

        self.name = name
        self.sectioning_time = sectioning_time
        self.power_system = None

        self.distribution_controllers = list()
        self.microgrid_controllers = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ManualMainController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, ManualMainController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_distribution_controller(self, controller):
        """
        Adds distribution controllers from connected distribution systems to a list
        and sets the manual sectioning time for the controller

        Parameters
        ----------
        controller : Controller
            Distribution system controller

        Returns
        ----------
        None

        """
        self.distribution_controllers.append(controller)
        controller.manual_sectioning_time = self.sectioning_time

    def add_microgrid_controller(self, controller):
        """
        Adds microgird controllers from connected microgrids to a list and sets the manual sectioning time for the controller

        Parameters
        ----------
        controller : Controller
            Microgrid controller

        Returns
        ----------
        None

        """
        self.microgrid_controllers.append(controller)
        controller.manual_sectioning_time = self.sectioning_time

    def run_control_loop(self, curr_time: Time, dt: Time):
        """
        Runs the manual control loop for the distribution system controllers and the microgird controllers

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
        for controller in self.distribution_controllers:
            controller.run_manual_control_loop(curr_time, dt)
        for controller in self.microgrid_controllers:
            controller.run_manual_control_loop(curr_time, dt)

    def update_fail_status(self, dt: Time):
        """
        Updates the failure status

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        pass

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
        pass

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute

        Parameters
        ----------
        attribute : str
            Manual controller attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        pass

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
        pass

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
        pass

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
        pass
