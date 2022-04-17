import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from relsad.utils import (
    random_choice,
    convert_yearly_fail_rate,
)

from relsad.Time import (
    Time,
    TimeUnit,
)

"""
### What it should include: ###
    This class will look similar to the bus class.

    Attributes:
        1. Name of the ICT node
        2. coordinate for placing the node
        3. Can be connected ontop of a power bus such that the ICT components could be connected to a ICT node as well for sending signals. But the ICT node should also be able to not be connected to a bys
        4. Counter that tells how many signals that are at the ICT node - the intesity of the signlas
        5. Number of customer that can send signals
        6. Possibility of connecting traffic from other sources. Do not need to specifiy which, only that it will add to the total customers and the arrival intensity.

    Methods:
        1. A function that connects the ICT node and the power bus


    Assumptions:
        During a failure no new cars can come to the park and now cars will leave the park during the outage period.
        Do not consider which time of the day the failure occurs
        Assume equal size of all cars



"""


class ICTNode(Component):

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        coordinate: list = [0, 0],
        fail_rate_per_year: float = 0,
        outage_time: Time = Time(0, TimeUnit.HOUR),
        queue: float = 10,
    ):

        self.name = name
        self.coordinate = coordinate
        self.queue = queue

        ## Topological attributes
        self.toICTline = None
        self.fromICTline = None
        self.toICTline_list = list()
        self.fromICTline_list = list()
        self.nextICTnode = list()
        self.connected_ICTlines = list()

        ## Reliability attributes
        self.fail_rate_per_year = fail_rate_per_year
        self.outage_time = outage_time
        self.acc_outage_time = Time(0)
        self.avg_fail_rate = 0
        self.avg_outage_time = Time(0)
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0

        ## History
        self.history = {}
        self.monte_carlo_history = {}

        self.reset_status(True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ICT_Node(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, ICTNode)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def node_fail(self, dt: Time):
        """
        Failure on a ICT node
        """
        self.ICTnode_failed = True
        self.remaining_outage_time = self.outage_time

    def node_not_fail(self):
        self.ICTnode_failed = False

    def update_fail_status(self, dt: Time):
        if self.ICTnode_failed:
            self.remaining_outage_time -= dt
            if self.remaining_outage_time <= Time(0):
                self.node_not_fail()
        else:
            p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
            if random_choice(self.ps_random, p_fail):
                self.node_fail(dt)
            else:
                self.node_not_fail()

    def print_status(self):
        print(
            "name: {:3s}, ICTnode_failed={}".format(
                self.name, self.ICTnode_failed
            )
        )

    def add_random_instance(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

    # Usikker på denne:
    def get_avg_fail_rate(self):
        """
        Returns the average failure rate of the ICT node
        """

        avg_fail_rate = self.fail_rate_per_year
        if self.parent_network is not None:
            for line in self.parent_network.get_lines():
                avg_fail_rate += line.fail_rate_per_year
        return avg_fail_rate

    def reset_status(self, save_flag: bool):
        self.ICTnode_failed = False
        self.remaining_outage_time = Time(0)
        self.acc_outage_time = Time(0)
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0
        if save_flag:
            self.initialize_history()
