import os
import copy
import numpy as np
from numpy.random import SeedSequence
from multiprocessing import Pool
from relsad.network.systems import (
    Network,
    PowerSystem,
    Transmission,
)
from relsad.loadflow.ac import run_bfs_load_flow
from relsad.simulation.system_config import (
    find_sub_systems,
    update_sub_system_slack,
    reset_system,
)
from relsad.load_shed.run_load_shed import shed_loads
from relsad.simulation.sequence.history import update_history
from relsad.simulation.monte_carlo.history import (
    initialize_history,
    initialize_monte_carlo_history,
    merge_monte_carlo_history,
    update_monte_carlo_power_system_history,
    save_network_monte_carlo_history,
    save_iteration_history,
)
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)


class Simulation:
    """ 
    Common class for simulation

    ...

    Attributes 
    ----------
    power_system : PowerSystem
        A PowerSystem element
    random_seed : int
        Random seed number
    fail_duration : Time
        The duration of a failure

    Methods
    ----------
    distribute_random_instance(random_intance)
        Adds a global numpy random instance
    run_load_flow(network)
        Runs load flow of a network
    run_increment(inc_idx, start_time, prev_time, curr_time, save_flag)
        Runs power system at current state for on time increment
    run_sequence(start_time, time_increments, time_unit, save_flag)
        Runs power system for a sequence of increments
    run_iteration(it, start_time, time_increments, time_unit, save_dir, save_iterations, random_seed)
        Runs power system for an iteration
    run_monte_carlo(iterations, start_time, stop_time, time_step, time_unit, load_dict, prod_dict, save_iterations, save_dir, n_procs, debug)
        Runs Monte Carlo simulation of the power system
    """
    def __init__(self, power_system: PowerSystem, random_seed: int = None):
        self.power_system = power_system
        self.random_seed = random_seed
        self.fail_duration = Time(0)

    def distribute_random_instance(self, random_instance):
        """
        Adds a global numpy random instance
        
        Parameters
        ----------
        random_instance : 
            A random...

        Returns
        ----------
        None

        """
        self.power_system.random_instance = random_instance
        for comp in self.power_system.comp_list:
            comp.add_random_instance(random_instance)
        self.power_system.controller.add_random_instance(random_instance)

    def run_load_flow(self, network: Network):
        """
        Runs load flow of a network
        
        Parameters
        ----------
        network : Network 
            A Network element

        Returns
        ----------
        None

        """
        run_bfs_load_flow(network)

    def run_increment(
        self,
        inc_idx: int,
        start_time: TimeStamp,
        prev_time: Time,
        curr_time: Time,
        save_flag: bool,
    ):
        """
        Runs power system at current state for one time increment

        Parameters
        ----------
        inc_idx : int 
            Increment index
        start_time : TimeStamp
            The start time of the simulation/iteration
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
        ## Time step
        dt = curr_time - prev_time if prev_time is not None else curr_time
        ## Set loads
        self.power_system.set_load_and_cost(inc_idx)
        ## Set productions
        self.power_system.set_prod(inc_idx)
        ## Set fail status
        self.power_system.update_fail_status(dt)
        ## Run control loop
        self.power_system.controller.run_control_loop(curr_time, dt)
        if (
            self.power_system.failed_comp()
            or not self.power_system.full_batteries()
        ):
            self.fail_duration += dt
            ## Find sub systems
            find_sub_systems(self.power_system, curr_time)
            update_sub_system_slack(self.power_system)
            ## Load flow
            for sub_system in self.power_system.sub_systems:
                ## Update EV parks
                sub_system.update_ev_parks(self.fail_duration, dt, start_time, curr_time)
                ## Update batteries and history
                sub_system.update_batteries(self.fail_duration, dt)
                ## Run load flow
                sub_system.reset_load_flow_data()
                if sub_system.slack is not None:
                    self.run_load_flow(sub_system)
                ## Shed load
                shed_loads(sub_system, dt)
            ## Log results
            update_history(self.power_system, prev_time, curr_time, save_flag)
        else:
            if self.fail_duration > Time(0):
                update_history(
                    self.power_system, prev_time, curr_time, save_flag
                )
                self.fail_duration = Time(0)

    def run_sequence(
        self,
        start_time: TimeStamp,
        time_increments: np.ndarray,
        time_unit: TimeUnit,
        save_flag: bool,
    ):
        """
        Runs power system for a sequence of increments

        Parameters
        ----------
        inc_inx : int 
            Increment index
        start_time : TimeStamp
            The start time of the simulation/iteration
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
        prev_time = Time(0, unit=time_unit)
        curr_time = Time(0, unit=time_unit)
        for inc_idx, time_quantity in enumerate(time_increments):
            curr_time = Time(time_quantity, unit=time_unit)
            self.run_increment(
                inc_idx, 
                start_time,
                prev_time,
                curr_time,
                save_flag,
            )
            prev_time = copy.deepcopy(curr_time)

    def run_iteration(
        self,
        it: int,
        start_time: TimeStamp,
        time_increments: np.ndarray,
        time_unit: TimeUnit,
        save_dir: str,
        save_iterations: list,
        random_seed: int,
    ):
        """
        Runs power system for an iteration 

        Parameters
        ----------
        it : int 
            Iteration numver
        start_time : TimeStamp
            The start time of the simulation/iteration
        time_increment : array?
        time_unit : TimeUnit
            A time unit (hour, seconds, ect.)
        save_dir: str
            The saving path
        save_iteration : list
        random_seed : int
            Random seed number

        Returns
        ----------
        None

        """
        if random_seed is None:
            random_instance = np.random.default_rng()
        else:
            random_instance = np.random.default_rng(random_seed)
        self.distribute_random_instance(random_instance)
        save_dict = initialize_monte_carlo_history(self.power_system)
        print("it: {}".format(it), flush=True)
        save_flag = it in save_iterations
        reset_system(self.power_system, save_flag)
        self.run_sequence(
            start_time,
            time_increments,
            time_unit,
            save_flag)
        save_dict = update_monte_carlo_power_system_history(
            self.power_system, it, time_unit, save_dict
        )
        if save_flag:
            save_iteration_history(self.power_system, it, save_dir)
        return save_dict

    def run_monte_carlo(
        self,
        iterations: int,
        start_time: TimeStamp,
        stop_time: TimeStamp,
        time_step: Time,
        time_unit: TimeUnit,
        load_dict: dict,
        prod_dict: dict,
        save_iterations: list = [],
        save_dir: str = "results",
        n_procs: int = 1,
        debug: bool = False,
    ):
        """
        Runs Monte Carlo simulation of the power system

        Parameters
        ----------
        iterations : int 
            Number of iterations
        start_time : TimeStamp
            The start time of the simulation/iteration
        stop_time : TimeStamp
            The stop time of the simulation/iteration
        time_step : Time
            A time step (1 hour, 2 hours, ect.)
        time_unit : TimeUnit
            A time unit (hour, seconds, ect.)
        load_dict : dict
            Dictionary containing the loads in the system
        prod_dict : dict
            Dictionary containing the generation in the system
        save_iterations : list
        save_dir : str
            The saving path
        n_procs : int
            Number of processors
        debug : bool
            Indicates if debug mode is on or off

        Returns
        ----------
        None

        """
        ss = SeedSequence(self.random_seed)
        child_seeds = ss.spawn(iterations)
        self.power_system.create_sections()
        increments = int((stop_time - start_time)/time_step)
        time_increments = np.arange(
            stop=increments * time_step.get_unit_quantity(time_unit),
            step=time_step.get_unit_quantity(time_unit),
        )
        time_increment_indices = np.arange(increments)
        self.power_system.add_load_dict(load_dict, time_increment_indices)
        self.power_system.add_prod_dict(prod_dict, time_increment_indices)
        initialize_history(self.power_system)
        if debug:
            it_dicts = []
            for it in range(1, iterations + 1):
                it_dicts.append(
                    self.run_iteration(
                        it,
                        start_time,
                        time_increments,
                        time_unit,
                        save_dir,
                        save_iterations,
                        child_seeds[it - 1],
                    )
                )
        else:
            with Pool(processes=n_procs) as pool:
                it_dicts = pool.starmap(
                    self.run_iteration,
                    [
                        [
                            it,
                            start_time,
                            time_increments,
                            time_unit,
                            save_dir,
                            save_iterations,
                            child_seeds[it - 1],
                        ]
                        for it in range(1, iterations + 1)
                    ],
                )
        save_dict = merge_monte_carlo_history(
            self.power_system,
            time_unit,
            it_dicts,
        )
        save_network_monte_carlo_history(
            self.power_system,
            os.path.join(save_dir, "monte_carlo"),
            save_dict,
        )
