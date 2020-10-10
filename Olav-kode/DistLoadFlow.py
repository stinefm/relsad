# Copyright (c) 2020, Olav B. Fosso, NTNU
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.

import numpy as np
import matplotlib.pyplot as plt

# Locale definitions
from DistribObjects import *

#
# Import the case description
#
from IEEE69BusDist import *
#from IEEE33BusDist import *


class DistLoadFlow:
    """
    Common base class Radial System's (Distribution)  Load Flow
    Input:
        BusList      - List off all Bus objects
        LineList    - List of all transmission lines objects
    Returns: None

    """

    def __init__(self,BusList,LineList):
        self.BusList = BusList
        self.LineList = LineList
        self.voang = np.zeros(len(self.BusList))
        self.vomag = np.ones(len(self.BusList))
        self.topology = []

    #
    # Set up additional configuration information
    #
    def config2(self):
        """Function for making the topology - it sets up the connection between two buses by assigned the line to the to bus
        and by preparing a list of from bus connections (branching)
        Problem: Currently turn the direction of too many lines when the connection point splits the chain
        """
        for lobj in self.LineList:
            if lobj.ibstat:
                itr = lobj.tbus - 1
                ifr = lobj.fbus - 1
                self.BusList[itr].tolinelist.append(lobj)
                self.BusList[itr].toline = lobj         # Add information to each bus of a line abouth which line that connects the meighbour bus.
                self.BusList[ifr].fromline = lobj
        for lobj in self.LineList:
            if lobj.ibstat:
                if lobj.fbus > 1 and BusList[lobj.fbus-1].toline == 0:          # Identify broken chains in the grid
                    itb = lobj.tbus
                    lobj.tbus = lobj.fbus   # Change direction and identify next line in the chain.
                    lobj.fbus = itb
                    BusList[lobj.tbus-1].toline = lobj
                    lobj1 = BusList[lobj.fbus - 1].fromline  # Keep the next line
#                    print('lobj:',lobj1.fbus, lobj1.tbus)
                    while lobj1 != 0:               # Stop when the chain connects to the main chain
                        if lobj1.tbus > lobj1.fbus:         # Changes currently too many
                            print('lobj:', lobj1.fbus, lobj1.tbus)
                            itb = lobj1.tbus
                            lobj1.tbus = lobj1.fbus
                            lobj1.fbus = itb
                            BusList[lobj1.tbus-1].toline = lobj1
                            lobj1 = BusList[lobj1.fbus-1].fromline


        # Add the topology information needed to define the tree structure
        for lobj in self.LineList:
            if lobj.ibstat:
                itr = lobj.tbus - 1
                ifr = lobj.fbus - 1
                self.BusList[ifr].nextbus.append(self.BusList[itr])     # Add the next bus to the list of branches of the bus

    def config(self):
        """Function for making the topology - it sets up the connection between two buses by assigned the line to the to bus
        and by preparing a list of from bus connections (branching)

        """
        for lobj in self.LineList:
            if lobj.ibstat:
                itr = lobj.tbus - 1
                ifr = lobj.fbus - 1
                self.BusList[itr].tolinelist.append(lobj)
                self.BusList[itr].toline = lobj  # Add information to each bus of a line abouth which line that connects
                self.BusList[ifr].fromline = lobj


        for lobj in self.LineList:
            if lobj.ibstat:
                if lobj.fbus > 1 and BusList[lobj.fbus - 1].toline == 0:  # Identify broken chains in the grid
                    itb = lobj.tbus
                    lobj.tbus = lobj.fbus  # Change direction and identify next line in the chain.
                    lobj.fbus = itb
                    BusList[lobj.tbus - 1].toline = lobj
                    lobj1 = BusList[lobj.fbus - 1].fromline  # Keep the next line

                    OneMore = True
                    while OneMore:
                        if lobj1.tbus > lobj1.fbus:  # Changes currently too many
       #                     print('lobj:', lobj1.fbus, lobj1.tbus)
                            itb = lobj1.tbus
                            lobj1.tbus = lobj1.fbus
                            lobj1.fbus = itb
                            BusList[lobj1.tbus - 1].toline = lobj1
                            lobj1 = self.BusList[lobj1.fbus - 1].fromline
                            if len(self.BusList[lobj1.tbus - 1].tolinelist) == 2:
                                OneMore = False
           #         print('lobj:', lobj1.fbus, lobj1.tbus)
                    itb = lobj1.tbus
                    lobj1.tbus = lobj1.fbus
                    lobj1.fbus = itb
                    self.BusList[lobj1.tbus - 1].toline = lobj1

        # Add the topology information needed to define the tree structure
        for lobj in self.LineList:
            if lobj.ibstat:
                itr = lobj.tbus - 1
                ifr = lobj.fbus - 1
                self.BusList[ifr].nextbus.append(self.BusList[itr])  # Add the next bus to the list of branches of the bus
           #     print('Line: ',lobj.fbus, lobj.tbus, self.BusList[itr].toline.fbus )

    #
    # Set up the list suitable for a recursive algorithm
    #
    def mainstruct2(self):
        """ The algorithm builds up a tree structure based on topology information provided in instances of a node class
        There can be any number of branching on a bus in the main path.
        There can currently be no branching from a bus in the sub-branches

        The principle is to insert a sublist til the element where the branching appears
        """
        mainlist = []
        mainlist.append([self.BusList[0]])
        nextobj = mainlist[-1][0].nextbus
        while len(nextobj) > 0:
            if len(nextobj) == 1:
                mainlist.append(nextobj)            # Add the next element when no branching occurs
                nextobj = nextobj[0].nextbus
            if len(nextobj) > 1:
                branch = nextobj
                mainlist.append([nextobj[0]])       # Add the next element in the main branch
                iloop = 1
                while iloop < len(branch):
                    newpath = [[branch[iloop]]]     # Follow each sub-branch
                    nextobj = newpath[-1][0].nextbus        # The second last element of the main path
                    while len(nextobj) > 0:
                        newpath.append(nextobj)             # Add the next element in the new path
                        nextobj = nextobj[0].nextbus
                    mainlist[-2].append(newpath)            # When the newpath is completed add it as a sublist of the branching bus
                    iloop += 1
            nextobj = mainlist[-1][0].nextbus
        return mainlist

    #
    # Set up the list suitable for a recursive algorithm (generalized with branching in sub-trees
    #
    def mainstruct(self):
        """ The algorithm builds up a tree structure based on topology information provided in instances of a node class
        There can be any number of branching on a bus in the main path.
        Multiple branching in sublists are possible.

        The principle is to insert a sublist til the element where the branching appears
        """
        mainlist = []
        mainlist.append([self.BusList[0]])
        nextobj = mainlist[-1][0].nextbus
        while len(nextobj) > 0:
            if len(nextobj) == 1:
                mainlist.append(nextobj)            # Add the next element when no branching occurs
                nextobj = nextobj[0].nextbus
            if len(nextobj) > 1:
                branch = nextobj
                mainlist.append([nextobj[0]])       # Add the next element in the main branch
                iloop = 1
                while iloop < len(branch):
                    newpath = [[branch[iloop]]]     # Follow each sub-branch
                    nextobj = newpath[-1][0].nextbus        # The second last element of the main path
                    while len(nextobj) > 0:
                        if len(nextobj) == 1:
                            newpath.append(nextobj)             # Add the next element in the new path
                            nextobj = nextobj[0].nextbus
                        if len(nextobj) > 1:
                            sbranch = nextobj
                            newpath.append([nextobj[0]])        # Add the next object of the subpaths before branching
                            iloop1 = 1
                            while iloop1 < len(sbranch):            # Do for all branhces in paths of a node in the subtree
                                spath = [[sbranch[iloop1]]]
                                nextobj = spath[-1][0].nextbus
                                while len(nextobj) > 0:
                                    spath.append(nextobj)   # Add the next element in the new path
                                    nextobj = nextobj[0].nextbus
                                newpath[-2].append(spath)
                                iloop1 += 1
                        nextobj = newpath[-1][0].nextbus
                    mainlist[-2].append(newpath)            # When the newpath is completed add it as a sublist of the branching bus
                    iloop += 1
            nextobj = mainlist[-1][0].nextbus
        return mainlist


    #
    # Display transmission line flows
    #
    def dispFlow(self,fromLine=0,toLine=0, tpres=False):
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
            toLine = len(self.LineList)
        if tpres:
            toLine = np.minimum(fromLine + 13, toLine)
        inum = fromLine
        for line in self.LineList[fromLine:toLine]:
            ifr = line.fbus - 1
            itr = line.tbus - 1
            bsh = 0.0           # No shunts included so far
            teta1 = self.BusList[ifr].voang
            teta2 = self.BusList[itr].voang
            v1 = self.BusList[ifr].vomag
            v2 = self.BusList[itr].vomag
            b = bij(line.r,line.x)
            g = gij(line.r,line.x)

            Pfrom = g * v1 * v1 - v1 * v2 * tij(g, b, teta1, teta2)
            Pto = g * v2 * v2 - v1 * v2 * tij(g, b, teta2, teta1)
            Qfrom = -(b + bsh) * v1 * v1 - v1 * v2 * uij(g, b, teta1, teta2)
            Qto = -(b + bsh) * v2 * v2 - v1 * v2 * uij(g, b, teta2, teta1)

            if tpres == False:
                print(' FromBus :', '{:4.0f}'.format(ifr+1), ' ToBus :', '{:4.0f}'.format(itr+1),
                      ' Pfrom :', '{:7.4f}'.format(Pfrom), ' Qfrom : ', '{:7.4f}'.format(Qfrom),
                      ' Pto :', '{:7.4f}'.format(Pto), ' Qto :', '{:7.4f}'.format(Qto))

            sublist = [ifr+1, itr+1, '{:7.4f}'.format(Pfrom), '{:7.4f}'.format(Qfrom),
                       '{:7.4f}'.format(Pto), '{:7.4f}'.format(Qfrom)]
            mainlist.append(sublist)
            rowno.append('Line ' + str(inum))
            inum += 1

        if tpres:
            title = 'Transmission line flow'
            colind = ['FromBus :', ' ToBus :', 'Pfrom :', ' Qfrom : ', ' Pto :', ' Qto :']
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

    #
    # Conduct a distribution system load flow based on FBS
    #
    def DistLF(self, maxit = 3):
        """ Solves the distribution load flow with a specified number of iterations
        The two first septs are to set up additions topology information and to build the main structure
        Next, it is switched between forward sweeps (Voltage updates) and backward sweeps(load update and loss calcuation)
        """

#        self.config()
#        self.topology = self.mainstruct()
        iloop = 0
        while iloop < maxit:
            p1,q1, p2, q2 = self.accload(self.topology, self.BusList)
            print('Iter: ',iloop+1, 'Pload:', '{:7.4f}'.format(p1), 'Qload:', '{:7.4f}'.format(q1),
                  'Ploss:', '{:7.4f}'.format(p2), 'Qloss:', '{:7.4f}'.format(q2))
            self.UpdateVolt(self.topology, self.BusList)
            iloop += 1
        print('\n',"****** Load flow completed ******",'\n')


    #
    # Visit all nodes in the reverse list.
    #
    def BackwardSearch(self,topologyList):
        """ Visit all the nodes in a backward approach and prints the Bus name
        """
        for x in reversed(topologyList):
            if len(x) > 1:
                print('Bus' + str(x[0].busnum))
                iloop = 1
                while iloop < len(x):           # Do for all branches of a bus
                    self.BackwardSearch(x[iloop])
                    iloop += 1
            else:
                print('Bus' + str(x[0].busnum))

    #
    # Visit all nodes in the forward list.
    #
    def ForwardSearch(self,topologyList):
        """Visit all nodes in a forward approach and prints the us name
        """
        for x in topologyList:
            if len(x) > 1:
                print('Bus' + str(x[0].busnum))
                iloop = 1
                while iloop < len(x):   # Do for all branches of a bus
                    self.ForwardSearch(x[iloop])
                    iloop += 1
            else:
                print('Bus' + str(x[0].busnum))


    #
    # Calculations the load for the actual volage at the bus
    #
    def getload(self,busobj):
        """ Calculates the net voltage corrected load at the bus - currently a simple ZIP model is applied.
        Input: The busobject
        Returns: pLoadAct, qLoadAct
        """
#        if busobj.vset > 0:
#            self.voltCrtl(busobj)
        qcomp = 0.0
        if busobj.comp:
            qcomp = self.SVCCrtl(busobj)
        pLoadAct = busobj.pload*(busobj.ZIP[0]*busobj.vomag**2 + busobj.ZIP[1]*busobj.vomag + busobj.ZIP[2])
        qLoadAct = busobj.qload*(busobj.ZIP[0]*busobj.vomag**2 + busobj.ZIP[1]*busobj.vomag + busobj.ZIP[2]) - qcomp
        dPdV = busobj.pload*(busobj.ZIP[0]*2*busobj.vomag + busobj.ZIP[1])
        dQdV = busobj.qload*(busobj.ZIP[0]*2*busobj.vomag + busobj.ZIP[1])
        return pLoadAct, qLoadAct, dPdV, dQdV

    def voltCrtl(self, busobj, mode='Reactive'):
        """ Changes the net injection at voltage controlled buses
                Input: The busobject
                mode - Control mode ('Active', 'Reactive', 'Both' - default = 'Reactive')
                Returns: pLoadAct, qLoadAct
                """
        if busobj.vset > 0 and busobj.vomag < 1.0:
            if np.abs(busobj.vomag - busobj.vset) > 0.0002:
                if mode == 'Active':
                    deltap = (busobj.vset - busobj.vomag)/(busobj.dVdP*(1+ busobj.dPlossdP))
                    busobj.pload += deltap
                    print('Load corr (Active): ', busobj.busnum, deltap, busobj.pload)
                elif mode == 'Reactive':
                    deltaq = (busobj.vset - busobj.vomag)/(busobj.dVdQ*(1+ busobj.dQlossdQ))
                    busobj.qload += deltaq
                    print('Load corr (Reactive): ', busobj.busnum, deltaq, busobj.qload)

    def SVCCrtl(self, busobj):
        """Calculates the SVC contribution to voltage control"""
        svcobj = busobj.comp
        if svcobj.stat:
            qsens = busobj.dVdQ*(1.0 + busobj.dQlossdQ)
            if qsens:
                a = 1.0
                b = -(svcobj.vprev + svcobj.slopeQ / qsens)
                c = svcobj.slopeQ/qsens*busobj.vomag
                v = (-b + np.sqrt(b**2 -4*a*c))/2.0
                v2 = (-b - np.sqrt(b ** 2 - 4 * a * c))/2.0
                print('v1 :', v, '   v2 : ', v2)
            else:
                v = svcobj.vprev
    #        v = (busobj.vomag - qsens*svcobj.vprev/svcobj.slopeQ)/(1.0 - qsens/svcobj.slopeQ)
            Qc = -1.0/svcobj.slopeQ *v*(v - svcobj.vref)
            svcobj.vprev = v
            print('Volt: ', v,'   Qinj = ', Qc)
            svcobj.Qinj = Qc
            return Qc

    def SVCCrtl2(self, busobj):
        """Calculates the SVC contribution to voltage control"""
        svcobj = busobj.comp
        if svcobj.stat:
            qsens = busobj.dVdQ*(1.0 + busobj.dQlossdQ)
            v = (busobj.vomag - qsens*svcobj.vprev/svcobj.slopeQ)/(1.0 - qsens/svcobj.slopeQ)
            Qc = -1.0/svcobj.slopeQ *(v - svcobj.vref)
            svcobj.vprev = v
            print('Volt: ', v,'   Qinj = ', Qc)
            svcobj.Qinj = Qc
            return Qc


    #
    # Calculate the accumulated load and losses starting on the last node
    #

    def accload(self, topologyList, BusList):
        """Calculates the accumulated downstream active and reactive load at all buses
        and calculates the active and reactive losses of lines and make an accumulated equivalent load at the buses
        """
        pl1 = 0.0
        ql1 = 0.0
        ploss1 = 0.0
        qloss1 = 0.0

        for x in reversed(topologyList):        # Start on last node
            if len(x) > 1:
                iloop = 1
                while iloop < len(x):       # Do for all branches at a bus
                    pl2, ql2, ploss2, qloss2 = self.accload(x[iloop],BusList)
                    pl1 += pl2      # Add accumulated powers and losses in a branch to the node where the brancing accurs.
                    ql1 += ql2
                    ploss1 += ploss2
                    qloss1 += qloss2
                    iloop += 1
                pla, qla, dPdV1, dQdV1 = self.getload(x[0])       # Add local loads
                pl1 += pla   # Add local loads
                ql1 += qla
                x[0].ploadds = pl1      # Add accumulated descriptions to the branching node
                x[0].qloadds = ql1
                x[0].pblossds = ploss1
                x[0].qblossds = qloss1
                if pl1 != 0:
                    x[0].dPdV = (x[0].dPdV*(pl1-pla) + dPdV1*pla)/pl1
                if ql1 != 0:
                    x[0].dQdV = (x[0].dQdV*(ql1-qla) + dQdV1*qla)/ql1
                if x[0].toline:         # Follow the next node in the main path
                    lobj = x[0].toline
                    if lobj.ibstat:
                        ifr = lobj.fbus
                        itr = lobj.tbus
                        pto = x[0].ploadds + x[0].pblossds      # Find the flow to the downstream bus
                        qto = x[0].qloadds + x[0].qblossds
                        lobj.ploss = lobj.r * (pto ** 2 + qto ** 2) / x[0].vomag ** 2   # Estimate the losses of the branch
                        lobj.qloss = lobj.x * (pto ** 2 + qto ** 2) / x[0].vomag ** 2
                        ploss1 += lobj.ploss
                        qloss1 += lobj.qloss
                        x[0].pblossds = ploss1      # Add the losses to the downstream bus
                        x[0].qblossds = qloss1

            else:                               # No branching at the bus
#                pl1 += x[0].pload
#                ql1 += x[0].qload
                pla, qla, dPdV1, dQdV1 = self.getload(x[0])
                pl1 += pla   # Add local loads
                ql1 += qla
                x[0].ploadds = pl1
                x[0].qloadds = ql1
                if pl1 != 0:
                    x[0].dPdV = (x[0].dPdV*(pl1-pla) + dPdV1*pla)/pl1
                if ql1 != 0:
                    x[0].dQdV = (x[0].dQdV*(ql1-qla) + dQdV1*qla)/ql1
                if x[0].toline:
                    lobj = x[0].toline
                    if lobj.ibstat:
                        ifr = lobj.fbus
                        itr = lobj.tbus
                        pto = x[0].ploadds + ploss1
                        qto = x[0].qloadds + qloss1
                        lobj.ploss = lobj.r * (pto ** 2 + qto ** 2) / x[0].vomag ** 2
                        lobj.qloss = lobj.x * (pto ** 2 + qto ** 2) / x[0].vomag ** 2
                        ploss1 += lobj.ploss
                        qloss1 += lobj.qloss
                        x[0].pblossds = ploss1
                        x[0].qblossds = qloss1

        return pl1, ql1, ploss1,  qloss1            # Return the accumulated loads and losses from the current branch

    #
    # Update the voltage profile starting on the top node
    #
    def UpdateVolt(self,topologyList, BusList):
        """Update the voltage profile based on the accumulated load on each bus
        """

        #
        # Function for calculating the voltages and sensitivities in the single phase case
        #
        def nodeVoltSensSP(BusList, ifr, itr, tline, obj):
            """
            Calculate the node voltages and sensitivities in the single phase case
            :param BusList:
            :param ifr:
            :param itf:
            :param tline:
            :param obj:
            :return:
            """

            vk2 = BusList[ifr].vomag ** 2
            tpload = obj[0].ploadds + obj[0].pblossds  # Find the accumulated loads and losses flowing on the branch
            tqload = obj[0].qloadds + obj[0].qblossds
            # Voltage calculation
            term2 = 2 * (tpload * tline.r + tqload * tline.x)
            term3 = (tpload ** 2 + tqload ** 2) * (tline.r ** 2 + tline.x ** 2) / BusList[ifr].vomag ** 2
            BusList[itr].vomag = np.sqrt(vk2 - term2 + term3)  # Update the bus voltage magnitude on the down-stream bus
            # Calculate the sensitivities for changing the load
            dvdp = (-tline.r + tpload * (tline.r ** 2 + tline.x ** 2) / BusList[ifr].vomag ** 2) / BusList[itr].vomag
            dpdq = (2 * tline.r * tqload / BusList[itr].vomag ** 2) * (
                        1 + 2 * tline.r * tpload / BusList[itr].vomag ** 2)
            dvdq = (-tline.x + tqload * (tline.r ** 2 + tline.x ** 2) / BusList[ifr].vomag ** 2) / BusList[itr].vomag
            dqdp = (2 * tline.x * tpload / BusList[itr].vomag ** 2) * (
                        1 + 2 * tline.x * tqload / BusList[itr].vomag ** 2)
            dpldp = (2 * tline.r * tpload / BusList[itr].vomag ** 2) * (
                        1 + 2 * tline.x * tqload / BusList[itr].vomag ** 2)

            BusList[itr].dVdP = BusList[ifr].dVdP + dvdp + dvdq * dqdp
            BusList[itr].dVdQ = BusList[ifr].dVdQ + dvdq + dvdp * dpdq
            # Calculate sensitivities for change in losses
            BusList[itr].dPlossdP = BusList[ifr].dPlossdP + dpldp
            BusList[itr].dPlossdQ = BusList[ifr].dPlossdQ + dpdq
            BusList[itr].dQlossdP = BusList[ifr].dQlossdP + dqdp
            #                    BusList[itr].dQlossdQ = BusList[ifr].dQlossdQ + (2 * tline.x * tqload/BusList[itr].vomag**2) * (1 + 2 * tline.r * tpload/BusList[itr].vomag**2)
            BusList[itr].dQlossdQ = BusList[ifr].dQlossdQ + 2 * tline.x * tqload / BusList[
                itr].vomag ** 2 + 2 * tline.x * tpload * BusList[itr].dPlossdQ / BusList[itr].vomag ** 2
            # Calculate the second-order derivatives
            BusList[itr].dP2lossdQ2 = BusList[ifr].dP2lossdQ2 + dpdq / tqload + (
                        2 * tline.r * tqload / BusList[itr].vomag ** 2) * 2 * tline.r * dpdq / BusList[itr].vomag ** 2
            BusList[itr].dP2lossdP2 = BusList[ifr].dP2lossdQ2 + dpldp / tpload + (
                    2 * tline.r * tpload / BusList[itr].vomag ** 2) * 2 * tline.x * dqdp / BusList[itr].vomag ** 2
            BusList[itr].lossRatioQ = BusList[itr].dPlossdQ / BusList[itr].dP2lossdQ2
            BusList[itr].lossRatioP = BusList[itr].dPlossdP / BusList[itr].dP2lossdP2

            # Update the voltage for the purpose of loss minimization - adjust the sensitivity acording to the chosen step.
            if BusList[itr].iloss:
                if np.abs(BusList[itr].dPlossdQ) >= 1.0 / BusList[
                    itr].pqcostRatio:  # Equivalent to that the dP cost more than pqcostRatio times dQ
                    qcomp = BusList[itr].dPlossdQ / BusList[itr].dP2lossdQ2
                    BusList[itr].qload -= qcomp
                    BusList[itr].dPlossdQ = 0.0

            # Voltage angle calculation
            busvoltreal = BusList[ifr].vomag - (tpload * tline.r + tqload * tline.x) / BusList[ifr].vomag
            busvoltimag = (tqload * tline.r - tpload * tline.x) / BusList[ifr].vomag
            BusList[itr].voang = BusList[ifr].voang + np.arctan2(busvoltimag, busvoltreal)  # Update voltage angles
            return
#  End

        for obj in topologyList:
            if len(obj) > 1:

                if obj[0].toline:
                    tline = obj[0].toline
                    ifr = tline.fbus - 1
                    itr = tline.tbus -1

                    # Update voltages and sensitivities Single Phase
                    nodeVoltSensSP(BusList, ifr, itr, tline, obj)


                iloop = 1
                while iloop < len(obj):         # Update voltages along the branches
                    self.UpdateVolt(obj[iloop], BusList)
                    iloop += 1
            else:                   # Continue along the current path
                if obj[0].toline:
                    tline = obj[0].toline
                    ifr = tline.fbus - 1
                    itr = tline.tbus - 1

                    # Update voltages and sensitivities Single Phase
                    nodeVoltSensSP(BusList, ifr, itr, tline, obj)
                    

    #
    # Estimate the losses of each line based on voltage level and acculated flow
    #

    def lossEstimate(busobjects, lineobjects):
        """Estimates the losses of each line based on volatage level and acculated flow
        """
        for lobj in reversed(lineobjects):
            ifr = lobj.fbus - 1
            itr = lobj.tbus - 1
            pto = busobjects[itr].ploadds
            qto = busobjects[itr].qloadds
            lobj.ploss = lobj.r*(pto**2 + qto**2)/busobjects[itr].vomag**2
            lobj.qloss = lobj.x*(pto**2 + qto**2)/busobjects[itr].vomag**2
            busobjects[ifr].ploadds += lobj.ploss
            busobjects[ifr].qloadds += lobj.qloss
    #
    # Display the voltages.
    #
    def dispVolt(self, fromBus=0, toBus = 0, tpres=False):
        """
        Desc:    Display voltages at all buses
        Input:   tpres= False (Display in tableformat if True)
                 fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
        Returns: None
        """
        mainlist = []
        rowno = []
        if toBus == 0:
            toBus = len(self.BusList)
        if tpres:
            toBus = np.minimum(fromBus + 13, toBus)

        iloop = fromBus
        print(' ')
        while iloop < toBus:
            oref = self.BusList[iloop]
            if tpres == False:
                print(' Bus no :', '{:4.0f}'.format(oref.busnum),
                      ' Vmag :', '{:7.5f}'.format(oref.vomag),
                      ' Theta :', '{:7.5f}'.format(oref.voang * 180 / np.pi))
            # Prepare for graphics presentation
            sublist = ['{:4.0f}'.format(oref.busnum),
                       '{:7.5f}'.format(oref.vomag),
                       '{:7.5f}'.format(oref.voang * 180 / np.pi)]

            mainlist.append(sublist)
            rowno.append('Bus ' + str(iloop+1))
            iloop += 1
        # Present table
        if tpres:
            title = 'Bus Voltages'
            colind = [' Bus no ', ' Vmag ', ' Theta ']
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

    #
    # Display voltage estimate for a chaninge in active or reactive load on a bus
    #
    def dispVoltEst(self, bus=0, deltap=0.0, deltaq=0.0, tpres=False ):
        """ The method estimates the voltages for a change in active or reactive load at a bus
        deltap and deltaq must reflect the change (negative by load reduction)
        """
        itr = bus -1
        mainlist = []
        rowno = []
        iloop = 0
        while self.BusList[itr].toline:
            busobj = self.BusList[itr]
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
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

            #
    # Display the voltages.
    #
    def dispVoltSens(self, fromBus=0, toBus = 0, tpres=False):
        """
        Desc:    Display Load sensitivities for change in voltage at all buses
        Input:   tpres= False (Display in tableformat if True)
                 fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
        Returns: None
        """
        mainlist = []
        rowno = []
        if toBus == 0:
            toBus = len(self.BusList)
        if tpres:
            toBus = np.minimum(fromBus + 13, toBus)

        iloop = fromBus
        print(' ')
        while iloop < toBus:
            oref = self.BusList[iloop]
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
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

    #
    def dispLossSens(self, fromBus=0, toBus = 0, tpres=False):
        """
        Desc:    Display Loss sensitivities for change in active or reactive injection at all buses
        Input:   tpres= False (Display in tableformat if True)
                 fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
        Returns: None
        """
        mainlist = []
        rowno = []
        if toBus == 0:
            toBus = len(self.BusList)
        if tpres:
            toBus = np.minimum(fromBus + 13, toBus)

        iloop = fromBus
        print(' ')
        while iloop < toBus:
            oref = self.BusList[iloop]
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
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

    #

    #
    def dispLossSensP(self, fromBus=0, toBus=0, tpres=False):
        """
        Desc:    Display Loss sensitivities for change in active or reactive injection at all buses
        Input:   tpres= False (Display in tableformat if True)
                 fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
        Returns: None
        """
        mainlist = []
        rowno = []
        if toBus == 0:
            toBus = len(self.BusList)
        if tpres:
            toBus = np.minimum(fromBus + 13, toBus)

        iloop = fromBus
        print(' ')
        while iloop < toBus:
            oref = self.BusList[iloop]
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
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

    #
    #
    def dispLossSensQ(self, fromBus=0, toBus=0, tpres=False):
        """
        Desc:    Display Loss sensitivities for change in active or reactive injection at all buses
        Input:   tpres= False (Display in tableformat if True)
                 fromBus and toBus defines the block, If tpres=True, it will display 13 lines from fromBus
        Returns: None
        """
        mainlist = []
        rowno = []
        if toBus == 0:
            toBus = len(self.BusList)
        if tpres:
            toBus = np.minimum(fromBus + 13, toBus)

        iloop = fromBus
        print(' ')
        while iloop < toBus:
            oref = self.BusList[iloop]
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
            self.tableplot(mainlist, title, colind, rowno, columncol=[], rowcol=[])

    #

    # General table controlled by the application
    #
    def tableplot(self, table_data, title, columns, rows, columncol=[], rowcol=[]):
        """
        Desc:   Make a table of the provided data. There must be a row and a column
                data correpsonding to the table
        Input:  table_data  - np.array
                title - string
                columns - string vector
                rows    - string vector
                columncol - colors of each column label (default [])
                rowcol - colors of each row lable
        """

        fig = plt.figure(dpi=150)
        ax = fig.add_subplot(1, 1, 1)

        tdim = np.shape(table_data)
        iloop = 0
        if rowcol == []:
            while iloop < tdim[0]:
                rowcol.append('cyan')
                iloop += 1
        iloop = 0
        if columncol == []:
            while iloop < tdim[1]:
                columncol.append('cyan')
                iloop += 1

        table = ax.table(cellText=table_data, rowLabels=rows, colColours=columncol, rowColours=rowcol,
                         colLabels=columns, loc='center')
        table.set_fontsize(11)
        table.scale(1, 1.5)
        ax.set_title(title, fontsize=14)
        ax.axis('off')
        plt.show()

    #
    # Display total losses
    #
    def dispLosses(self):
        pline = 0.0
        qline = 0.0
        for x in self.LineList:
            pline += x.ploss
            qline += x.qloss
        print('\n', 'Ploss:', pline, '   Qloss:', qline)
    #
    # Display total load (no voltage correction)
    #
    def dispLoad(self):
        aload = 0.0
        rload = 0.0
        for x in self.BusList:
            pla, qla = self.getload(x)
            aload += pla  # Add local loads
            rload += qla
        print('\n','Total load  P: ', aload, '   Q: ', rload, '  Losses: P',
              BusList[1].pblossds, '   Q: ', BusList[1].qblossds)

    def zeroxq(self):
        for a in self.LineList:
            a.x = 0.0
        for a in self.BusList:
            a.qload = 0.0

# Demo case (Illustration of how to build up a script)

dlf = DistLoadFlow(BusList, LineList)           # Create object
dlf.config()                                    # Set up additional configuration
dlf.topology = dlf.mainstruct()                 # Set up the configuration for recursive
dlf.DistLF(maxit=5)                             # Solve load flow

dlf.dispVolt(fromBus=1,tpres=True)              # Display voltages for the firste 13 buses
dlf.dispVolt(fromBus=15,tpres=True)
dlf.dispVolt(fromBus=59,toBus=63, tpres=True)
dlf.dispVoltSens(fromBus=59,toBus=63,tpres=True)         # Voltage sensitivities for reduced load at the same bus and the sensitivity in reduced losses
dlf.dispLossSens(fromBus=57,toBus=65,tpres=True)         # Loss sensitivities for reduced load at the same bus and the rate of change of loss sensitivities
#dlf.dispFlow(tpres=True)                        # Display flow on transmission lines (in graphic pres only 13 is deplayed (spes start point)
#dlf.dispFlow(fromLine=56,tpres=True)
