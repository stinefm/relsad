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
from relsad.utils import (
    TimeUnit,
    Time,
)


class Simulation:
    def __init__(self, power_system: PowerSystem, random_seed: int = None):
        self.power_system = power_system
        self.random_seed = random_seed
        self.fail_duration = Time(0)

    def distribute_random_instance(self, random_instance):
        """
        Adds a global numpy random instance
        """
        self.power_system.random_instance = random_instance
        for comp in self.power_system.comp_list:
            comp.add_random_instance(random_instance)
        self.power_system.controller.add_random_instance(random_instance)

    def run_load_flow(self, network: Network):
        """
        Runs load flow in power system
        """
        ## Run load flow
        run_bfs_load_flow(network)

    def run_increment(
        self, inc_idx: int, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        """
        Runs power system at current state for one time increment
        """
        ## Set loads
        self.power_system.set_load(inc_idx)
        ## Set productions
        self.power_system.set_prod(inc_idx)
        ## Set fail status
        dt = curr_time - prev_time if prev_time is not None else curr_time
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
        self, time_increments: np.ndarray, time_unit: TimeUnit, save_flag: bool
    ):
        """
        Runs power system for a sequence of increments
        """
        prev_time = Time(0, unit=time_unit)
        curr_time = Time(0, unit=time_unit)
        for inc_idx, time_quantity in enumerate(time_increments):
            curr_time = Time(time_quantity, unit=time_unit)
            self.run_increment(inc_idx, prev_time, curr_time, save_flag)
            prev_time = copy.deepcopy(curr_time)

    def run_iteration(
        self,
        it: int,
        time_increments: np.ndarray,
        time_unit: TimeUnit,
        save_dir: str,
        save_iterations: list,
        random_seed: int,
    ):
        if random_seed is None:
            random_instance = np.random.default_rng()
        else:
            random_instance = np.random.default_rng(random_seed)
        self.distribute_random_instance(random_instance)
        save_dict = initialize_monte_carlo_history(self.power_system)
        print("it: {}".format(it), flush=True)
        save_flag = it in save_iterations
        reset_system(self.power_system, save_flag)
        self.run_sequence(time_increments, time_unit, save_flag)
        save_dict = update_monte_carlo_power_system_history(
            self.power_system, it, time_unit, save_dict
        )
        if save_flag:
            save_iteration_history(self.power_system, it, save_dir)
        return save_dict

    def run_monte_carlo(
        self,
        iterations: int,
        increments: int,
        time_step: Time,
        time_unit: TimeUnit,
        load_dict: dict,
        prod_dict: dict,
        save_iterations: list = [],
        save_dir: str = "results",
        n_procs: int = 1,
        debug: bool = False,
    ):
        ss = SeedSequence(self.random_seed)
        child_seeds = ss.spawn(iterations)
        self.power_system.create_sections()
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
