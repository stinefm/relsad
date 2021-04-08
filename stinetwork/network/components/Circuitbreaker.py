from stinetwork.utils import unique
from .Component import Component
from .Line import Line
import matplotlib.lines as mlines


class CircuitBreaker(Component):

    """
    Common base class for circuit breakers

    ...

        Attributes
        ----------
        name : string
            Name of the circuit breaker
        coordinate : list
            Coordinate of the circuit breaker
        is_open : bool
            Tells if the switch is open (True) or closed (False)
        failed : bool
            True if the circuit breaker is in a failed state, False if not
        fail_rate : float
            The failure rate of the circuit breaker [no of fails per year]
        outage_time : float
            The outage time of the circuit breaker [time units]
        line : Line
            The line the circuit breaker is connected to
        disconnecter : list(Disconnectors)
            Which disconnectors that are connected to the circuit breaker
        line.circuitbreaker :

        Functions
        ----------
        close(curr_time) :

    """

    ## Visual attributes
    color = "black"
    edgecolor = "black"
    marker = "s"
    size = 3 ** 2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=3,
        markersize=size,
        linestyle="None",
        color=color,
        markeredgecolor=edgecolor,
    )

    ## Random instance
    ps_random = None

    def __init__(
        self,
        name: str,
        line: Line,
        is_open: bool = False,
        section_time: float = 1,
        fail_rate: float = 0.0,
        outage_time: float = 1,
    ):
        self.name = name

        dx = line.tbus.coordinate[0] - line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1] - line.fbus.coordinate[1]
        self.coordinate = [
            line.fbus.coordinate[0] + dx / 3,
            line.fbus.coordinate[1] + dy / 3,
        ]
        self.initial_state = is_open
        self.is_open = is_open
        self.failed = False
        self.section_time = section_time
        self.prev_section_time = 0
        self.remaining_section_time = 0
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.line = line
        self.disconnectors = list()
        self.line.circuitbreaker = self

        ## History
        self.history = {
            "is_open": dict(),
            "remaining_section_time": dict(),
            "prev_section_time": dict(),
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Circuitbreaker(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def close(self, curr_time):
        if curr_time > self.prev_section_time or curr_time == 0:
            self.is_open = False
            self.color = "black"
            for discon in self.disconnectors:
                if discon.is_open:
                    discon.close(curr_time)

    def open(self, curr_time):
        self.is_open = True
        self.prev_section_time = curr_time
        self.remaining_section_time = self.section_time
        self.color = "white"
        for discon in unique(self.line.disconnectors + self.disconnectors):
            if not discon.is_open:
                discon.open(curr_time)

    def update_fail_status(self, curr_time):
        if self.is_open and curr_time > self.prev_section_time:
            if self.remaining_section_time >= 1:
                self.remaining_section_time -= 1
                if self.remaining_section_time == 0 and not self.line.failed:
                    self.close(curr_time)
            elif not self.line.failed:
                self.close(curr_time)

    def update_history(self, curr_time):
        self.history["is_open"][curr_time] = self.is_open
        self.history["remaining_section_time"][
            curr_time
        ] = self.remaining_section_time
        self.history["prev_section_time"][curr_time] = self.prev_section_time

    def get_history(self, attribute: str):
        return self.history[attribute]

    def add_random_seed(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

    def print_status(self):
        pass

    def reset_status(self):
        self.prev_section_time = 0
        self.remaining_section_time = 0

        self.close(0)

        self.history = {
            "is_open": dict(),
            "remaining_section_time": dict(),
            "prev_section_time": dict(),
        }


if __name__ == "__main__":
    pass
