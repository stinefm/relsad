import numpy as np
from topology.paths import config, mainstruct

def DistLoadFlow(BusList,LineList):
    """
    Common base class Radial System's (Distribution)  Load Flow
    Input:
        BusList     - List off all Bus objects
        LineList    - List of all transmission lines objects
    Returns: None

    """

    #
    # Conduct a distribution system load flow based on FBS
    #
    def DistLF(topology, BusList, maxit = 3):
        """ Solves the distribution load flow with a specified number of iterations
        The two first septs are to set up additions topology information and to build the main structure
        Next, it is switched between forward sweeps (Voltage updates) and backward sweeps(load update and loss calcuation)
        """

        iloop = 0
        while iloop < maxit:
            p1,q1, p2, q2 = accload(topology, BusList)
            print('Iter: ',iloop+1, 'Pload:', '{:7.4f}'.format(p1), 'Qload:', '{:7.4f}'.format(q1),
                    'Ploss:', '{:7.4f}'.format(p2), 'Qloss:', '{:7.4f}'.format(q2))
            BusList = UpdateVolt(topology, BusList)
            iloop += 1
        print('\n',"****** Load flow completed ******",'\n')

        return BusList


    #
    # Calculate the accumulated load and losses starting on the last node
    #

    def accload(topologyList, BusList):
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
                    pl2, ql2, ploss2, qloss2 = accload(x[iloop],BusList)
                    pl1 += pl2      # Add accumulated powers and losses in a branch to the node where the brancing accurs.
                    ql1 += ql2
                    ploss1 += ploss2
                    qloss1 += qloss2
                    iloop += 1
                pla, qla, dPdV1, dQdV1 = getload(x[0])       # Add local loads
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
                        # ifr = lobj.fbus
                        # itr = lobj.tbus
                        pto = x[0].ploadds + x[0].pblossds      # Find the flow to the downstream bus
                        qto = x[0].qloadds + x[0].qblossds
                        lobj.ploss = lobj.r * (pto ** 2 + qto ** 2) / x[0].vomag ** 2   # Estimate the losses of the branch
                        lobj.qloss = lobj.x * (pto ** 2 + qto ** 2) / x[0].vomag ** 2
                        ploss1 += lobj.ploss
                        qloss1 += lobj.qloss
                        x[0].pblossds = ploss1      # Add the losses to the downstream bus
                        x[0].qblossds = qloss1

            else:                               # No branching at the bus
                # pl1 += x[0].pload
                # ql1 += x[0].qload
                pla, qla, dPdV1, dQdV1 = getload(x[0])
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
                        # ifr = lobj.fbus
                        # itr = lobj.tbus
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
    def UpdateVolt(topologyList, BusList):
        """Update the voltage profile based on the accumulated load on each bus
        """

        #
        # Function for calculating the voltages and sensitivities in the single phase case
        #
        def nodeVoltSensSP(BusList, ifr, itr, tline, busobj):
            """
            Calculate the node voltages and sensitivities in the single phase case
            :param BusList:
            :param ifr:
            :param itf:
            :param tline:
            :param busobj:
            :return:
            """

            vk2 = BusList[ifr].vomag ** 2
            tpload = busobj[0].ploadds + busobj[0].pblossds  # Find the accumulated loads and losses flowing on the branch
            tqload = busobj[0].qloadds + busobj[0].qblossds
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
            return BusList
            #  End

        for busobj in topologyList:
            if len(busobj) > 1:

                if busobj[0].toline:
                    tline = busobj[0].toline
                    ifr = tline.fbus.num - 1
                    itr = tline.tbus.num -1

                    # Update voltages and sensitivities Single Phase
                    BusList = nodeVoltSensSP(BusList, ifr, itr, tline, busobj)


                iloop = 1
                while iloop < len(busobj):         # Update voltages along the branches
                    UpdateVolt(busobj[iloop], BusList)
                    iloop += 1
            else:                   # Continue along the current path
                if busobj[0].toline:
                    tline = busobj[0].toline
                    ifr = tline.fbus.num - 1
                    itr = tline.tbus.num - 1

                    # Update voltages and sensitivities Single Phase
                    BusList = nodeVoltSensSP(BusList, ifr, itr, tline, busobj)
                    
        return BusList

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
    

    def zeroxq(BusList, LineList):
        for a in range(len(LineList)):
            LineList[a].x = 0.0
        for a in range(len(BusList)):
            BusList[a].qload = 0.0
        return BusList, LineList


    BusList, LineList = config(BusList, LineList)
    mainList = mainstruct(BusList)

    BusList = DistLF(mainList, BusList, maxit=5)

    return BusList


#
# Calculates the load for the actual volage at the bus
#
def getload(busobj):
    """ Calculates the net voltage corrected load at the bus - currently a simple ZIP model is applied.
    Input: The busobject
    Returns: pLoadAct, qLoadAct
    """
    pLoadAct = busobj.pload*(busobj.ZIP[0]*busobj.vomag**2 + busobj.ZIP[1]*busobj.vomag + busobj.ZIP[2])
    qLoadAct = busobj.qload*(busobj.ZIP[0]*busobj.vomag**2 + busobj.ZIP[1]*busobj.vomag + busobj.ZIP[2])
    dPdV = busobj.pload*(busobj.ZIP[0]*2*busobj.vomag + busobj.ZIP[1])
    dQdV = busobj.qload*(busobj.ZIP[0]*2*busobj.vomag + busobj.ZIP[1])
    return pLoadAct, qLoadAct, dPdV, dQdV

