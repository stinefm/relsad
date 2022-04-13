import numpy as np
from relsad.visualization.plotting import tableplot


#
# Display transmission line flows
#
def dispFlow(line_list, fromLine=0, toLine=0, tpres=False):
    """
    Display the flow on the requested distribution lines
    
    Parameters
    ----------
    line_list : list
        List containing Line elements
    fromLine : 
    toLine : 
    tpres : bool

    Returns
    ----------
    None
    """

    mainlist = []
    rowno = []

    def uij(gij, bij, tetai, tetaj):
        return gij * np.sin(tetai - tetaj) - bij * np.cos(tetai - tetaj)

    def tij(gij, bij, tetai, tetaj):
        return gij * np.cos(tetai - tetaj) + bij * np.sin(tetai - tetaj)

    def bij(R, X):
        return (1.0 / complex(R, X)).imag

    def gij(R, X):
        return (1.0 / complex(R, X)).real

    if toLine == 0:
        toLine = len(line_list)
    if tpres:
        toLine = np.minimum(fromLine + 13, toLine)
    inum = fromLine
    for line in line_list[fromLine:toLine]:
        if line.connected:
            fbus = line.fbus
            tbus = line.tbus
            bsh = 0.0  # No shunts included so far
            teta1 = fbus.voang
            teta2 = tbus.voang
            v1 = fbus.vomag
            v2 = tbus.vomag
            b = bij(line.r, line.x)
            g = gij(line.r, line.x)

            Pfrom = g * v1 * v1 - v1 * v2 * tij(g, b, teta1, teta2)
            Pto = g * v2 * v2 - v1 * v2 * tij(g, b, teta2, teta1)
            Qfrom = -(b + bsh) * v1 * v1 - v1 * v2 * uij(g, b, teta1, teta2)
            Qto = -(b + bsh) * v2 * v2 - v1 * v2 * uij(g, b, teta2, teta1)

            if tpres is False:
                print(
                    "Line:{:5s} FromBus :{:5s} ToBus :{:5s}".format(
                        line.name, line.fbus.name, line.tbus.name
                    ),
                    " Pfrom :",
                    "{:7.4f}".format(Pfrom),
                    " Qfrom : ",
                    "{:7.4f}".format(Qfrom),
                    " Pto :",
                    "{:7.4f}".format(Pto),
                    " Qto :",
                    "{:7.4f}".format(Qto),
                )

            sublist = [
                line.fbus,
                line.fbus,
                "{:7.4f}".format(Pfrom),
                "{:7.4f}".format(Qfrom),
                "{:7.4f}".format(Pto),
                "{:7.4f}".format(Qfrom),
            ]
            mainlist.append(sublist)
            rowno.append("Line " + str(inum))
            inum += 1

    if tpres:
        title = "Transmission line flow"
        colind = [
            "FromBus :",
            " ToBus :",
            "Pfrom :",
            " Qfrom : ",
            " Pto :",
            " Qto :",
        ]
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])


#
# Display the voltages.
#
def dispVolt(bus_list, fromBus=0, toBus=0, tpres=False):
    """
    Display voltages at all buses

    Parameters
    ----------
    bus_list : list
        List containing Bus elements
    fromBus : 
    toBus : 
    tpres : Bool

    Returns
    ----------
    None
    """
    mainlist = []
    rowno = []
    if toBus == 0:
        toBus = len(bus_list)
    if tpres:
        toBus = np.minimum(fromBus + 13, toBus)

    iloop = fromBus
    print(" ")
    while iloop < toBus:
        oref = bus_list[iloop]
        if tpres is False:
            print(
                " Bus name :",
                "{:5s}".format(oref.name),
                " Vmag :",
                "{:7.5f}".format(oref.vomag),
                " Theta [deg]:",
                "{:7.5f}".format(oref.voang * 180 / np.pi),
            )
        # Prepare for graphics presentation
        sublist = [
            "{}".format(oref.name),
            "{:7.5f}".format(oref.vomag),
            "{:7.5f}".format(oref.voang * 180 / np.pi),
        ]

        mainlist.append(sublist)
        rowno.append("Bus " + str(iloop + 1))
        iloop += 1
    # Present table
    if tpres:
        title = "Bus Voltages"
        colind = [" Bus no ", " Vmag ", " Theta "]
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

#
# Display total load (no voltage correction)
#
def dispTotalLoad(bus_list):
    """
    Displays the total load and power losess in the system 

    Parameters
    ----------
    bus_list : list
        List containing Bus elements

    Returns
    ----------
    None
    """
    aload = 0.0
    rload = 0.0
    for bus in bus_list:
        # load - production [PU]
        relative_pload = bus.pload_pu - bus.pprod_pu
        relative_qload = bus.qload_pu - bus.qprod_pu

        p_load_act = relative_pload * (
            bus.ZIP[0] * bus.vomag ** 2 + bus.ZIP[1] * bus.vomag + bus.ZIP[2]
        )
        q_load_act = relative_qload * (
            bus.ZIP[0] * bus.vomag ** 2 + bus.ZIP[1] * bus.vomag + bus.ZIP[2]
        )
        aload += p_load_act  # Add local loads
        rload += q_load_act
    print(
        "Total load  P: {:.4f}   Q: {:.4f}  Losses: P {:.4f}\
          Q: {:.4f} ".format(
            aload,
            rload,
            bus_list[1].p_loss_downstream,
            bus_list[1].q_loss_downstream,
        )
    )


#
# Display bus loads for subsystem
#
def dispLoads(bus_list):
    """
    Displays the load at the bus 

    Parameters
    ----------
    bus_list : list
        List containing Bus elements

    Returns
    ----------
    None
    """
    for bus in bus_list:
        print(
            "Name: {}, P: {:.4f}, Q: {:.4f}".format(
                bus.name, bus.pload, bus.qload
            )
        )


#
# Visit all nodes in the reverse list.
#
def BackwardSearch(topology_list):
    """
    Visit all the nodes in a backward approach and prints the Bus name
    
    Parameters
    ----------
    topology_list : list
        List containing the system topology

    Returns
    ----------
    None
    """
    for x in reversed(topology_list):
        if len(x) > 1:
            print(x[0].name)
            iloop = 1
            while iloop < len(x):  # Do for all branches of a bus
                BackwardSearch(x[iloop])
                iloop += 1
        else:
            print(x[0].name)


#
# Visit all nodes in the forward list.
#
def ForwardSearch(topology_list):
    """Visit all nodes in a forward approach and prints the us name
   
    Parameters
    ----------
    topology_list : list
        List containing the system topology

    Returns
    ----------
    None
    """
    for x in topology_list:
        if len(x) > 1:
            print(x[0].name)
            iloop = 1
            while iloop < len(x):  # Do for all branches of a bus
                ForwardSearch(x[iloop])
                iloop += 1
        else:
            print(x[0].name)


if __name__ == "__main__":
    pass
