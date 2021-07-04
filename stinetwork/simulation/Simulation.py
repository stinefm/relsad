import os
import numpy as np
from stinetwork.network.systems import (
    Network,
    PowerSystem,
)
from stinetwork.loadflow.ac import run_bfs_load_flow
from stinetwork.simulation.system_config import (
    find_sub_systems,
    update_sub_system_slack,
    reset_system,
)
from stinetwork.load_shed.run_load_shed import shed_loads
from stinetwork.simulation.sequence.history import update_history
from stinetwork.simulation.monte_carlo.history import (
    initialize_history,
    initialize_monte_carlo_history,
    update_monte_carlo_history,
    save_network_monte_carlo_history,
    save_iteration_history,
)


class Simulation:
    def __init__(self, power_system: PowerSystem, random_seed: int):
        self.power_system = power_system
        self.random_instance = np.random.default_rng(random_seed)
        self.distribute_random_instance()
        self.fail_duration = 0

    def distribute_random_instance(self):
        """
        Adds a global numpy random instance
        """
        self.power_system.random_instance = self.random_instance
        for comp in self.power_system.comp_list:
            comp.add_random_seed(self.random_instance)

    def run_load_flow(self, network: Network):
        """
        Runs load flow in power system
        """
        ## Run load flow
        run_bfs_load_flow(network)

    def run_increment(self, curr_time, save_flag: bool):
        """
        Runs power system at current state for one time increment
        """
        ## Set loads
        self.power_system.set_load(curr_time)
        ## Set productions
        self.power_system.set_prod(curr_time)
        ## Set fail status
        self.power_system.update_fail_status(curr_time)
        if (
            self.power_system.failed_comp()
            or not self.power_system.full_batteries()
        ):
            self.fail_duration += 1
            ## Find sub systems
            find_sub_systems(self.power_system, curr_time)
            update_sub_system_slack(self.power_system)
            ## Load flow
            for sub_system in self.power_system.sub_systems:
                ## Update batteries and history
                sub_system.update_batteries(self.fail_duration)
                ## Run load flow
                sub_system.reset_load_flow_data()
                if sub_system.slack is not None:
                    self.run_load_flow(sub_system)
                ## Shed load
                shed_loads(sub_system)
            ## Log results
            update_history(self.power_system, curr_time, save_flag)
        else:
            if self.fail_duration > 0:
                self.fail_duration = 0

    def run_sequence(self, increments: int, save_flag: bool):
        """
        Runs power system for a sequence of increments
        """
        for curr_time in range(1, increments + 1):
            self.run_increment(curr_time, save_flag)

    def run_monte_carlo(
        self,
        iterations: int,
        increments: int,
        save_iterations: list = [],
        save_dir: str = "results",
    ):
        initialize_history(self.power_system)
        initialize_monte_carlo_history(self.power_system)
        for it in range(1, iterations + 1):
            save_flag = it in save_iterations
            reset_system(self.power_system, save_flag)
            print("it: {}".format(it), flush=True)
            self.run_sequence(increments, save_flag)
            update_monte_carlo_history(self.power_system, it)
            save_network_monte_carlo_history(
                self.power_system,
                os.path.join(save_dir, "monte_carlo"),
            )
            if save_flag:
                save_iteration_history(self.power_system, it, save_dir)
