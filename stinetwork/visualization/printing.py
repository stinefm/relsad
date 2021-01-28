import numpy as np
from stinetwork.loadflow.ac import getload
from stinetwork.visualization.plotting import tableplot

#
# Display transmission line flows
#
def dispFlow(BusList, LineList, fromLine=0, toLine=0, tpres=False):
        """ Display the flow on the requested distribution lines
        """

        mainlist = []
        rowno = []

        def uij(gij,bij,tetai,tetaj):
            return (gij*np.sin(tetai-tetaj)-bij*np.cos(tetai-tetaj))

        def tij(gij,bij,tetai,tetaj):
            return (gij*np.cos(tetai-tetaj)+bij*np.sin(tetai-tetaj))

        def bij(R, X):
            return (1.0 / complex(R, X)).imag

        def gij(R, X):
            return (1.0 / complex(R, X)).real

        if toLine == 0:
            toLine = len(LineList)
        if tpres:
            toLine = np.minimum(fromLine + 13, toLine)
        inum = fromLine
        for line in LineList[fromLine:toLine]:
            if line.connected:
                fbus = line.fbus
                tbus = line.tbus
                bsh = 0.0           # No shunts included so far
                teta1 = fbus.voang
                teta2 = tbus.voang
                v1 = fbus.vomag
                v2 = tbus.vomag
                b = bij(line.r,line.x)
                g = gij(line.r,line.x)

                Pfrom = g * v1 * v1 - v1 * v2 * tij(g, b, teta1, teta2)
                Pto = g * v2 * v2 - v1 * v2 * tij(g, b, teta2, teta1)
                Qfrom = -(b + bsh) * v1 * v1 - v1 * v2 * uij(g, b, teta1, teta2)
                Qto = -(b + bsh) * v2 * v2 - v1 * v2 * uij(g, b, teta2, teta1)

                if tpres == False:
                    print('Line:{:5s} FromBus :{:5s} ToBus :{:5s}'.format(line.name,line.fbus.name,line.tbus.name),
                            ' Pfrom :', '{:7.4f}'.format(Pfrom), ' Qfrom : ', '{:7.4f}'.format(Qfrom),
                            ' Pto :', '{:7.4f}'.format(Pto), ' Qto :', '{:7.4f}'.format(Qto))

                sublist = [line.fbus.num, line.fbus.num, '{:7.4f}'.format(Pfrom), '{:7.4f}'.format(Qfrom),
                            '{:7.4f}'.format(Pto), '{:7.4f}'.format(Qfrom)]
                mainlist.append(sublist)
                rowno.append('Line ' + str(inum))
                inum += 1

        if tpres:
            title = 'Transmission line flow'
            colind = ['FromBus :', ' ToBus :', 'Pfrom :', ' Qfrom : ', ' Pto :', ' Qto :']
            tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

#
# Display the voltages.
#
def dispVolt(BusList, fromBus=0, toBus = 0, tpres=False):
    """
    Desc:    Display voltages at all buses
    Input:   tpres= False (Display in tableformat if True)
                fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
    Returns: None
    """
    mainlist = []
    rowno = []
    if toBus == 0:
        toBus = len(BusList)
    if tpres:
        toBus = np.minimum(fromBus + 13, toBus)

    iloop = fromBus
    print(' ')
    while iloop < toBus:
        oref = BusList[iloop]
        if tpres == False:
            print(' Bus name :', '{:5s}'.format(oref.name),
                    ' Vmag :', '{:7.5f}'.format(oref.vomag),
                    ' Theta [deg]:', '{:7.5f}'.format(oref.voang * 180 / np.pi))
        # Prepare for graphics presentation
        sublist = ['{}'.format(oref.name),
                    '{:7.5f}'.format(oref.vomag),
                    '{:7.5f}'.format(oref.voang * 180 / np.pi)]

        mainlist.append(sublist)
        rowno.append('Bus ' + str(iloop+1))
        iloop += 1
    # Present table
    if tpres:
        title = 'Bus Voltages'
        colind = [' Bus no ', ' Vmag ', ' Theta ']
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

#
# Display voltage estimate for a chaninge in active or reactive load on a bus
#
def dispVoltEst(BusList, bus=0, deltap=0.0, deltaq=0.0, tpres=False ):
    """ The method estimates the voltages for a change in active or reactive load at a bus
    deltap and deltaq must reflect the change (negative by load reduction)
    """
    itr = bus -1
    mainlist = []
    rowno = []
    iloop = 0
    while BusList[itr].toline:
        busobj = BusList[itr]
        voltest = busobj.vomag + deltap*(1+busobj.dPlossdP)*busobj.dVdP + deltaq*(1+busobj.dQlossdQ)*busobj.dVdQ
        if tpres == False:
            print(' Bus no :', '{:4.0f}'.format(busobj.busnum),
                    ' Vmag :', '{:7.4f}'.format(busobj.vomag),
                    ' Vest :', '{:7.4f}'.format(voltest))
        # Prepare for graphics presentation
        if iloop < 14:
            sublist = ['{:4.0f}'.format(busobj.busnum),
                        '{:7.4f}'.format(busobj.vomag),
                        '{:7.4f}'.format(voltest)]
            mainlist.append(sublist)
            rowno.append('Bus ' + str(iloop + 1))
        iloop += 1
        itr = busobj.toline.fbus - 1

    # Present table
    if tpres:
        title = 'Voltage estimat for changed injection of P and Q'
        colind = [' Bus no ', ' Bus volt', 'Volt est']
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

        #
# Display the voltages.
#
def dispVoltSens(BusList, fromBus=0, toBus = 0, tpres=False):
    """
    Desc:    Display Load sensitivities for change in voltage at all buses
    Input:   tpres= False (Display in tableformat if True)
                fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
    Returns: None
    """
    mainlist = []
    rowno = []
    if toBus == 0:
        toBus = len(BusList)
    if tpres:
        toBus = np.minimum(fromBus + 13, toBus)

    iloop = fromBus
    print(' ')
    while iloop < toBus:
        oref = BusList[iloop]
        if tpres == False:
            print(' Bus no :', '{:4.0f}'.format(oref.busnum),
                    ' dV/dP :', '{:7.5}'.format(oref.dVdP *( 1.0 + oref.dPlossdP)),
                    ' dPloss/dP :,{:7.5}'.format(oref.dPlossdP),
                    ' dPloss/dQ :,{:7.5}'.format(oref.dPlossdQ),
                    ' dV/dQ :', '{:7.5}'.format(oref.dVdQ * (1.0 + oref.dPlossdQ)),
                    ' dQloss/dQ :,{:7.5}'.format(oref.dQlossdQ),
                    ' dQloss/dP :,{:7.5}'.format(oref.dQlossdP))

        # Prepare for graphics presentation
        sublist = ['{:4.0f}'.format(oref.busnum),
                    '{:7.5}'.format(oref.dVdP * ( 1.0 + oref.dPlossdP)),
                    '{:7.5}'.format(oref.dPlossdP),
                    '{:7.5}'.format(oref.dPlossdQ),
                    '{:7.5}'.format(oref.dVdQ * np.sqrt((1.0 + oref.dPlossdQ)**2 + oref.dQlossdQ**2)),
                    '{:7.5}'.format(oref.dQlossdQ),
                    '{:7.5}'.format(oref.dQlossdP)
                    ]

        mainlist.append(sublist)
        rowno.append('Bus ' + str(iloop+1))
        iloop += 1
    # Present table
    if tpres:
        title = 'Bus Voltage sensitivites to changes in load and loss'
        colind = [' Bus no ', ' dV/dP ', ' dPloss/dP', ' dPloss/dQ', ' dV/dQ :', ' dQloss/dQ', ' dQloss/dP']
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

#
def dispLossSens(BusList, fromBus=0, toBus = 0, tpres=False):
    """
    Desc:    Display Loss sensitivities for change in active or reactive injection at all buses
    Input:   tpres= False (Display in tableformat if True)
                fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
    Returns: None
    """
    mainlist = []
    rowno = []
    if toBus == 0:
        toBus = len(BusList)
    if tpres:
        toBus = np.minimum(fromBus + 13, toBus)

    iloop = fromBus
    print(' ')
    while iloop < toBus:
        oref = BusList[iloop]
        if tpres == False:
            print(' Bus no :', '{:4.0f}'.format(oref.busnum),
                    ' dV/dP :', '{:7.5}'.format(oref.dVdP * (1.0 + oref.dPlossdP)),
                    ' dPloss/dP :,{:7.5}'.format(oref.dPlossdP),
                    ' dPloss/dQ :,{:7.5}'.format(oref.dPlossdQ),
                    ' dV/dQ :', '{:7.5}'.format(oref.dVdQ * (1.0 + oref.dPlossdQ)),
                    ' dP2loss/dP2 :,{:7.5}'.format(oref.dP2lossdP2-1.0),
                    ' dP2loss/dQ2 :,{:7.5}'.format(oref.dP2lossdQ2-1.0))


        # Prepare for graphics presentation
        sublist = ['{:4.0f}'.format(oref.busnum),
                    '{:7.5}'.format(oref.dVdP * (1.0 + oref.dPlossdP)),
                    '{:7.5}'.format(oref.dPlossdP),
                    '{:7.5}'.format(oref.dPlossdQ),
                    '{:7.5}'.format(oref.dVdQ * (1.0 + oref.dPlossdQ)),
                    '{:7.5}'.format(oref.dP2lossdP2-1.0),
                    '{:7.5}'.format(oref.dP2lossdQ2-1.0)
                    ]

        mainlist.append(sublist)
        rowno.append('Bus ' + str(iloop+1))
        iloop += 1
    # Present table
    if tpres:
        title = 'Bus Voltage sensitivites to changes in load and loss'
        colind = [' Bus no ', ' dV/dP ', ' dPloss/dP', ' dPloss/dQ', ' dV/dQ ', ' d2Ploss/dP2', ' d2Ploss/dQ2']
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

def dispLossSensP(BusList, fromBus=0, toBus=0, tpres=False):
    """
    Desc:    Display Loss sensitivities for change in active or reactive injection at all buses
    Input:   tpres= False (Display in tableformat if True)
                fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
    Returns: None
    """
    mainlist = []
    rowno = []
    if toBus == 0:
        toBus = len(BusList)
    if tpres:
        toBus = np.minimum(fromBus + 13, toBus)

    iloop = fromBus
    print(' ')
    while iloop < toBus:
        oref = BusList[iloop]
        if tpres == False:
            print(' Bus no :', '{:4.0f}'.format(oref.busnum),
                    ' dV/dP :', '{:7.5}'.format(oref.dVdP * (1.0 + oref.dPlossdP)),
                    ' dPloss/dP :,{:7.5}'.format(oref.dPlossdP),
                    ' dP2loss/dP2 :,{:7.5}'.format(oref.dP2lossdP2-1.0),
                    ' Loss Ratio P :,{:7.5}'.format(oref.lossRatioP))

        # Prepare for graphics presentation
        sublist = ['{:4.0f}'.format(oref.busnum),
                    '{:7.5}'.format(oref.dVdP * (1.0 + oref.dPlossdP)),
                    '{:7.5}'.format(oref.dPlossdP),
                    '{:7.5}'.format(oref.dP2lossdP2-1.0),
                    '{:7.5}'.format(oref.lossRatioP)
                    ]

        mainlist.append(sublist)
        rowno.append('Bus ' + str(iloop + 1))
        iloop += 1
    # Present table
    if tpres:
        title = 'Bus Voltage sensitivites to changes in load and loss'
        colind = [' Bus no ', ' dV/dP ', ' dPloss/dP', ' d2Ploss/dP2',
                    ' Loss Ratio P']
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

def dispLossSensQ(BusList, fromBus=0, toBus=0, tpres=False):
    """
    Desc:    Display Loss sensitivities for change in active or reactive injection at all buses
    Input:   tpres= False (Display in tableformat if True)
                fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
    Returns: None
    """
    mainlist = []
    rowno = []
    if toBus == 0:
        toBus = len(BusList)
    if tpres:
        toBus = np.minimum(fromBus + 13, toBus)

    iloop = fromBus
    print(' ')
    while iloop < toBus:
        oref = BusList[iloop]
        if tpres == False:
            print(' Bus no :', '{:4.0f}'.format(oref.busnum),
                    ' dV/dQ :', '{:7.5}'.format(oref.dVdQ * (1.0 + oref.dPlossdQ)),
                    ' dPloss/dQ :,{:7.5}'.format(oref.dPlossdQ),
                    ' dP2loss/dQ2 :,{:7.5}'.format(oref.dP2lossdQ2-1.0),  # 1.0 ref value
                    ' Loss Ratio Q :,{:7.5}'.format(oref.lossRatioQ))

        # Prepare for graphics presentation
        sublist = ['{:4.0f}'.format(oref.busnum),
                    '{:7.5}'.format(oref.dVdQ * (1.0 + oref.dPlossdQ)),
                    '{:7.5}'.format(oref.dPlossdQ),
                    '{:7.5}'.format(oref.dP2lossdQ2-1.0),
                    '{:7.5}'.format(oref.lossRatioQ)
                    ]

        mainlist.append(sublist)
        rowno.append('Bus ' + str(iloop + 1))
        iloop += 1
    # Present table
    if tpres:
        title = 'Bus Voltage sensitivites to changes in load and loss'
        colind = [' Bus no ', ' dV/dQ ',' dPloss/dQ', ' d2Ploss/dQ2',
                    ' Loss Ratio Q']
        tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

#
# Display total losses
#
def dispTotalLosses(LineList):
    pline = 0.0
    qline = 0.0
    for x in LineList:
        pline += x.ploss
        qline += x.qloss
    print('\n', 'Ploss:', pline, '   Qloss:', qline)
#
# Display total load (no voltage correction)
#
def dispTotalLoad(BusList):
    aload = 0.0
    rload = 0.0
    for x in BusList:
        pla, qla, _dPdV, _dPdV = getload(x)
        aload += pla  # Add local loads
        rload += qla
    print('Total load  P: {:.4f}   Q: {:.4f}  Losses: P {:.4f}\
          Q: {:.4f} '.format(aload, rload, BusList[1].pblossds, BusList[1].qblossds))

#
# Display bus loads for subsystem
#
def dispLoads(BusList):
    for bus in BusList:
        print('Name: {}, P: {:.4f}, Q: {:.4f}'.format(bus.name, bus.pload, bus.qload))


#
# Visit all nodes in the reverse list.
#
def BackwardSearch(topologyList):
    """ Visit all the nodes in a backward approach and prints the Bus name
    """
    for x in reversed(topologyList):
        if len(x) > 1:
            print(x[0].name)
            iloop = 1
            while iloop < len(x):           # Do for all branches of a bus
                BackwardSearch(x[iloop])
                iloop += 1
        else:
            print(x[0].name)

#
# Visit all nodes in the forward list.
#
def ForwardSearch(topologyList):
    """Visit all nodes in a forward approach and prints the us name
    """
    for x in topologyList:
        if len(x) > 1:
            print(x[0].name)
            iloop = 1
            while iloop < len(x):   # Do for all branches of a bus
                ForwardSearch(x[iloop])
                iloop += 1
        else:
            print(x[0].name)

if __name__=="__main__":
    pass