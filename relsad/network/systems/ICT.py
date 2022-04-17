from relsad.network.components import Bus, Line, DistributionController
from .Network import Network
from .Transmission import Transmission
from relsad.utils import unique


"""
Need to include:

* ICT nodes
* ICT lines
* ICT components
* Informasjon on tilkobled kraftststem?



Function:
* Need to collect all the ICT parameters togheter to a system

"""


class ICT:
    def __init__(self):
        self.ICT_buses = list()
        self.ICT_lines = list()
