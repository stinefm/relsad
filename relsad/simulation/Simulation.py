import copy
from enum import Enum
import os
from multiprocessing import Pool

import numpy as np
from numpy.random import SeedSequence

from relsad.energy.shedding import shed_energy
from relsad.loadflow.ac.bfs import run_bfs_load_flow
from relsad.network.systems import PowerNetwork, PowerSystem
from .monte_carlo.history import (
    merge_monte_carlo_history,
    save_network_monte_carlo_history,
)
from .sequence.history import save_sequence_history
from .system_config import (
    find_sub_systems,
    prepare_system,
    reset_system,
    update_sub_system_slack,
)
from relsad.Time import Time, TimeStamp, TimeUnit


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
    run_sequence(start_time, time_array, time_unit, save_flag)
        Runs power system for a sequence of increments
    run_sequential(start_time, stop_time, time_step, time_unit, save_dir, save_flag)
        Runs a sequential simulation with the power system
    run_iteration(it, start_time, time_array, time_unit, save_dir, save_iterations, random_seed)
        Runs a sequential iteration with the power system
    run_monte_carlo(iterations, start_time, stop_time, time_step, time_unit, save_iterations, save_dir, n_procs, debug)
        Runs Monte Carlo simulation of the power system
    """

    def __init__(self, power_system: PowerSystem, random_seed: int = None):
        self.power_system = power_system
        self.power_system.verify_component_setup()
        self.random_seed = random_seed
        self.fail_duration = Time(0)

    def distribute_random_instance(self, random_instance):
        """
        Adds a global numpy random instance

        Parameters
        ----------
        random_instance : np.random.Generator
            A random generator

        Returns
        ----------
        None

        """
        self.power_system.random_instance = random_instance
        for comp in self.power_system.comp_list:
            comp.add_random_instance(random_instance)
        self.power_system.controller.add_random_instance(random_instance)

    def run_load_flow(self, network: PowerNetwork):
        """
        Runs load flow of a network

        Parameters
        ----------
        network : PowerNetwork
            A PowerNetwork element

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
        save_flag: bool = True,
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
        self.power_system.set_load_and_cost(inc_idx=inc_idx)
        ## Set productions
        self.power_system.set_prod(inc_idx=inc_idx)
        ## Set fail status
        self.power_system.update_fail_status(dt=dt)
        ## Run control loop
        self.power_system.controller.run_control_loop(
            curr_time=curr_time,
            dt=dt,
        )
        if (
            self.power_system.failed_comp()
            or not self.power_system.full_batteries()
        ):
            self.fail_duration += dt
            ## Find sub systems
            find_sub_systems(
                p_s=self.power_system,
                curr_time=curr_time,
            )
            update_sub_system_slack(p_s=self.power_system)
            ## Load flow
            for sub_system in self.power_system.sub_systems:
                ## Update batteries and history
                sub_system.update_batteries(
                    fail_duration=self.fail_duration,
                    dt=dt,
                )
                ## Update EV parks
                sub_system.update_ev_parks(
                    fail_duration=self.fail_duration,
                    dt=dt,
                    start_time=start_time,
                    curr_time=curr_time,
                )
                ## Run load flow
                sub_system.reset_load_flow_data()
                if sub_system.slack is not None:
                    self.run_load_flow(network=sub_system)
                ## Shed load
                shed_energy(
                    power_system=sub_system,
                    dt=dt,
                )
            ## Log results
            self.power_system.update_sequence_history(
                prev_time=prev_time,
                curr_time=curr_time,
                save_flag=save_flag,
            )
            self.power_system.reset_load_flow_data()
        else:
            if self.fail_duration > Time(0):
                ## Log results
                self.power_system.update_sequence_history(
                    prev_time=prev_time,
                    curr_time=curr_time,
                    save_flag=save_flag,
                )
                ## Reset fail duration
                self.fail_duration = Time(0)

    def run_sequence(
        self,
        start_time: TimeStamp,
        time_array: np.ndarray,
        time_unit: TimeUnit,
        callback: callable = None,
        save_flag: bool = True,
    ):
        """
        Runs power system for a sequence of increments

        Parameters
        ----------
        start_time : TimeStamp
            The start time of the simulation/iteration
        time_array : np.ndarray
            Time array
        time_unit : TimeUnit
            Time unit
        callback : callable, optional
            A callback function that allows for user-defined
            behavior. The callback function is called at the start
            of every increment. The callback function must contain
            the following arguments: ps, prev_time, curr_time
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        prev_time = Time(0, unit=time_unit)
        curr_time = Time(0, unit=time_unit)
        for inc_idx, time_quantity in enumerate(time_array):
            curr_time = Time(time_quantity, unit=time_unit)
            if callback is not None:
                callback(
                    ps=self.power_system,
                    prev_time=prev_time,
                    curr_time=curr_time,
                )
            self.run_increment(
                inc_idx,
                start_time,
                prev_time,
                curr_time,
                save_flag,
            )
            prev_time = copy.deepcopy(curr_time)

    def run_sequential(
        self,
        start_time: TimeStamp,
        stop_time: TimeStamp,
        time_step: Time,
        time_unit: TimeUnit,
        callback: callable = None,
        save_dir: str = "results",
        save_flag: bool = True,
    ):
        """
        Runs sequential simulation of the power system

        Parameters
        ----------
        start_time : TimeStamp
            The start time of the simulation/iteration
        stop_time : TimeStamp
            The stop time of the simulation/iteration
        time_step : Time
            A time step (1 hour, 2 hours, ect.)
        time_unit : TimeUnit
            A time unit (hour, seconds, ect.)
        callback : callable, optional
            A callback function that allows for user-defined
            behavior. The callback function is called at the start
            of every increment. The callback function must contain
            the following arguments: ps, prev_time, curr_time
        save_dir : str
            The saving directory
        save_flag : bool
            Flag for saving the simulation results

        Returns
        ----------
        None

        """
        if callback is not None and not callable(callback):
            raise Exception("The callback argument must be callable")

        # Initialize random seed
        ss = SeedSequence(self.random_seed)
        random_seed = ss.spawn(1)[0]

        # Initiate random instance
        random_instance = np.random.default_rng(random_seed)

        # Distribute random instance to power system components
        self.distribute_random_instance(random_instance)

        # Prepare power system for simulation
        time_array = prepare_system(
            power_system=self.power_system,
            start_time=start_time,
            stop_time=stop_time,
            time_step=time_step,
            time_unit=time_unit,
        )

        # Initialize sequence history variables
        self.power_system.initialize_sequence_history()

        # Run sequence
        self.run_sequence(
            start_time=start_time,
            time_array=time_array,
            time_unit=time_unit,
            callback=callback,
            save_flag=save_flag,
        )

        if save_flag is True:
            # Save sequence history
            save_sequence_history(
                power_system=self.power_system,
                time_unit=time_unit,
                save_dir=os.path.join(
                    save_dir,
                    "sequence",
                ),
            )

    def run_iteration(
        self,
        it: int,
        start_time: TimeStamp,
        time_array: np.array,
        time_unit: TimeUnit,
        save_dir: str,
        save_flag: bool,
        random_seed: int,
        callback: callable = None,
    ):
        """
        Runs power system for an iteration

        Parameters
        ----------
        it : int
            Iteration number
        start_time : TimeStamp
            The start time of the simulation/iteration
        stop_time : TimeStamp
            The stop time of the simulation/iteration
        time_array : np.array
            A time step (1 hour, 2 hours, ect.)
        time_unit : TimeUnit
            A time unit (hour, seconds, ect.)
        save_dir: str
            The saving directory
        save_flag : bool
            Flag for saving the iteration results
        random_seed : int
            Random seed number
        callback : callable, optional
            A callback function that allows for user-defined
            behavior. The callback function is called at the start
            of every increment. The callback function must contain
            the following arguments: prev_time, curr_time

        Returns
        ----------
        save_dict : dict
            Dictionary with simulation results

        """
        # Initiate random instance
        if random_seed is None:
            random_instance = np.random.default_rng()
        else:
            random_instance = np.random.default_rng(random_seed)

        # Distribute random instance to power system components
        self.distribute_random_instance(random_instance)

        # Initialize monte carlo history variables
        save_dict = self.power_system.initialize_monte_carlo_history()

        # Print current iteration
        print(f"it: {it}", flush=True)

        # Reset power system
        reset_system(self.power_system, save_flag)

        # Initialize sequence history variables
        self.power_system.initialize_sequence_history()

        # Run iteration sequence
        self.run_sequence(
            start_time=start_time,
            time_array=time_array,
            time_unit=time_unit,
            callback=callback,
            save_flag=save_flag,
        )

        if save_flag is True:
            # Save sequence history
            save_sequence_history(
                power_system=self.power_system,
                time_unit=time_unit,
                save_dir=os.path.join(
                    save_dir,
                    "sequence",
                    str(it),
                ),
            )

        # Update monte carlo history variables
        sim_duration = Time(time_array[-1], time_unit)
        save_dict = self.power_system.update_monte_carlo_history(
            it=it,
            current_time=sim_duration,
            save_dict=save_dict,
        )
        return save_dict

    def run_monte_carlo(
        self,
        iterations: int,
        start_time: TimeStamp,
        stop_time: TimeStamp,
        time_step: Time,
        time_unit: TimeUnit,
        callback: callable = None,
        save_iterations: list = [],
        save_dir: str = "results",
        n_procs: int = 1,
        debug: bool = False,
        save_flag: bool = True,
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
        callback : callable, optional
            A callback function that allows for user-defined
            behavior. The callback function is called at the start
            of every increment. The callback function must contain
            the following arguments: prev_time, curr_time
        save_iterations : list
            List of iterations where the sequence results will be saved
        save_dir : str
            The saving directory
        n_procs : int
            Number of processors
        debug : bool
            Indicates if debug mode is on or off
        save_flag : bool
            Flag for saving the simulation results

        Returns
        ----------
        None

        """
        if callback is not None and not callable(callback):
            raise Exception("The callback argument must be callable")

        # Initialize random seeds
        ss = SeedSequence(self.random_seed)
        child_seeds = ss.spawn(iterations)

        # Prepare power system for simulation
        time_array = prepare_system(
            power_system=self.power_system,
            start_time=start_time,
            stop_time=stop_time,
            time_step=time_step,
            time_unit=time_unit,
        )

        # Run iterations
        if debug:
            it_dicts = []
            for it in range(1, iterations + 1):
                it_dicts.append(
                    self.run_iteration(
                        it=it,
                        start_time=start_time,
                        time_array=time_array,
                        time_unit=time_unit,
                        save_dir=save_dir,
                        save_flag=(
                            it in save_iterations and save_flag is True
                        ),
                        random_seed=child_seeds[it - 1],
                        callback=callback,
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
                            time_array,
                            time_unit,
                            save_dir,
                            (it in save_iterations and save_flag is True),
                            child_seeds[it - 1],
                            callback,
                        ]
                        for it in range(1, iterations + 1)
                    ],
                )

        if save_flag is True:
            # Merge monte carlo history variables from iterations
            save_dict = merge_monte_carlo_history(
                power_system=self.power_system,
                iteration_dicts=it_dicts,
            )
            # Save monte carlo history variables
            save_network_monte_carlo_history(
                power_system=self.power_system,
                save_dir=os.path.join(save_dir, "monte_carlo"),
                save_dict=save_dict,
            )
