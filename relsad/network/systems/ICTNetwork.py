from relsad.network.components import ICTLine, ICTNode
from relsad.utils import unique

from .PowerSystem import PowerSystem


class ICTNetwork:

    """
    Class defining a ICT network type

    ...

    Attributes
    ----------
    name : str
        Name of the ICT network
    nodes : list
        List containing the nodes connected to the ICT network
    lines : list
        List containing the lines connected to the ICT network
    comp_list : list
        List containing the components in the ICT network
    comp_dict : dict
        Dictionary containing the components in the ICT network
    power_system : Network
        Connects the ICT network to the power system
    failed_line : Bool
        Flag stating if the ICT network contains a failed line
    history : dict
        Dictionary containing the history variables of the network
    monte_carlo_history : dict
        Dictionary containing the history variables from the monte carlo simulation



    Methods
    ----------
    add_node(node)
        Adding a node to the ICT network
    add_nodes(nodes)
        Adding nodes to the ICT network
    add_line(line)
        Adding a line to the ICT network
    add_lines(lines)
        Adding lines to the ICT network
    get_lines()
        Returns the lines in the ICT network
    get_monte_carlo_history(attribute)
        Returns the specified history variable from the Monte Carlo simulation
    get_history(attribute)
        Returns the specified history variable
    """

    ## Visual attributes
    color = "steelblue"

    ## Counter
    counter = 0

    def __init__(self, power_system: PowerSystem):
        ICTNetwork.counter += 1
        self.name = "ict_network{:d}".format(ICTNetwork.counter)

        # Components
        self.nodes = list()
        self.lines = list()
        self.comp_list = list()
        self.comp_dict = dict()

        # Network connections
        self.power_system = power_system

        self.failed_line = False

        ## History
        self.history: dict = {}
        self.monte_carlo_history: dict = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ICTNetwork(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_node(self, node: ICTNode):
        """
        Adding a node to the ICT network

        Parameters
        ----------
        node : ICTNode
            A ICT node element

        Returns
        ----------
        None

        """
        # Add bus to distribution network
        self.comp_dict[node.name] = node
        node.handle.color = self.color
        node.color = self.color
        node.parent_network = self
        self.nodes.append(node)
        self.nodes = unique(self.nodes)

        # Add bus to the power system
        self.power_system.add_ict_node(node)

    def add_nodes(self, nodes: list):
        """
        Adding buses to the ICT network node list

        Parameters
        ----------
        nodes : list
            A list of ICT node elements in the ICT network

        Returns
        ----------
        None

        """
        for node in nodes:
            self.add_node(node)

    def add_line(self, line: ICTLine):
        """
        Adding a line to the ICT network

        Parameters
        ----------
        line : ICTLine
            A ICTLine element

        Returns
        ----------
        None

        """

        # Add line to the ICT network
        line.handle.color = self.color
        line.color = self.color
        line.parent_network = self
        self.comp_dict[line.name] = line
        self.lines.append(line)
        self.lines = unique(self.lines)

        # Add line to power system
        self.power_system.add_ict_line(line)

    def add_lines(self, lines: list):
        """
        Adding lines to ICT network line list

        Parameters
        ----------
        lines : list
            A list of ICTLine elements in the ICT network

        Returns
        ----------
        None

        """
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the ICT network

        Parameters
        ----------
        None

        Returns
        ----------
        lines : list
            List of ICTLine elements

        """
        return self.lines

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable from the Monte Carlo simulation

        Parameters
        ----------
        attribute : str
            ICT network attribute

        Returns
        ----------
        monte_carlo_history[attribute] : dict
            Returns the history variables of an attribute from the Monte Carlo simulation

        """
        return self.monte_carlo_history[attribute]

    def get_history(self, attribute):
        """
        Returns the specified history variable

        Parameters
        ----------
        attribute : str
            ICT network attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]
