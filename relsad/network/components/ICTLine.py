import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Bus import Bus
from relsad.utils import (
    random_choice,
    convert_yearly_fail_rate,
)
from relsad.Time import (
    Time,
    TimeUnit,
)
from relsad.StatDist import StatDist

"""
### What it should include: ### 
    This class will look similar to the Line class. 

    Attributes: 
        1. Name of the ICT line
        2. From ICT node and to ICT node list
        3. A failure rate 
        4. An outage time 
        5. A capacity of the line, max number of signals/packages the line are able to transfer 
        6. Possibility to calaculate how many packages that are transffered over the line
        7. A probability of this ICT line being used - the probability of all lines going out of an ICT node needs to be 1. The easiest is to either divided it based on the capacity of the lines or just divided it equally on all the line out of a node. 
        9. Counter that can count how many signlas there is on a line

    Methods: 
        1. A function that distributes the signals packages out on the lines. 
        2. Need a function for reerouting signlas if 
        3. The average time it takes for one signal is the average number of cutomers in the system divided by the average arrival intensity: W_avg = N_avg/lambda_avg
    
    Assumptions: 
        During a failure no new cars can come to the park and now cars will leave the park during the outage period. 
        Do not consider which time of the day the failure occurs
        Assume equal size of all cars
        


"""


class ICTLine(Component):


    ICTlineCount = 0

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self, 
        name: str,
        fnode: ICTNode,
        tnode: ICTNode, 
        outage_time_dist: StatDist, 
        fail_rate_density_per_year: float = 0, 
        capacity: float = 100, 
    ):

        self.name = name

        ## Topological attributes
        self.fnode = fnode
        self.tnode = tnode
        fnode.connected_lines.append(self)
        tnode.connected_lines.append(self)
        tnode.tonode = self
        tnode.toline_list.append(self)
        fnode.fromline = self
        fnode.fromline_list.append(self)
        fnode.nextnode.append(self.tnode)
        self.parent_network = None
        ICTLine.ICTlineCount += 1

        self.capacity = capacity

        ## Reliabilility attributes
        self.fail_rate_per_year = (
            fail_rate_density_per_year * self.length
        )  # failures per year
        self.outage_time_dist = outage_time_dist

        ## Status attribute
        self.failed_line = False
        self.remaining_outage_time = Time(0)

        ## History
        self.history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ICT_Line(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, ICTLine)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def draw_outage_time(self, dt: Time):
        return Time(
            self.outage_time_dist.draw(self.ps_random), 
            dt.unit,
        )

    def fail(self, dt: Time):
        self.failed_line = True
        self.remaining_outage_time = self.draw_outage_time(dt)

    def not_fail(self):
        pass

    def get_line_load(self):
        pass























