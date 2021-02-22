import numpy as np
from stinetwork.topology.paths import configure, flatten
from stinetwork.network.components import Bus

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
            p1,q1, p2, q2 = accload(topology)
            # print('Iter: ',iloop+1, 'Pload:', '{:7.4f}'.format(p1), 'Qload:', '{:7.4f}'.format(q1),
            #         'Ploss:', '{:7.4f}'.format(p2), 'Qloss:', '{:7.4f}'.format(q2))
            UpdateVolt(topology)
            iloop += 1
        # print('\n',"****** Load flow completed ******",'\n')

        return BusList

    #
    # Calculate the accumulated load and losses starting on the last node
    #

    def accload(topologyList):
        """Calculates the accumulated downstream active and reactive load at all buses
        and calculates the active and reactive losses of lines and make an accumulated equivalent load at the buses
        """
        pl1 = 0.0
        ql1 = 0.0
        ploss1 = 0.0
        qloss1 = 0.0

        for branch in reversed(topologyList):        # Start on last node
            if len(branch) > 1:
                iloop = 1
                while iloop < len(branch):       # Do for all branches at a bus
                    pl2, ql2, ploss2, qloss2 = accload(branch[iloop])
                    pl1 += pl2      # Add accumulated powers and losses in a branch to the node where the brancing accurs.
                    ql1 += ql2
                    ploss1 += ploss2
                    qloss1 += qloss2
                    iloop += 1
                pla, qla, dPdV1, dQdV1 = getload(branch[0])       # Add local loads
                pl1 += pla   # Add local loads
                ql1 += qla
                branch[0].ploadds = pl1      # Add accumulated descriptions to the branching node
                branch[0].qloadds = ql1
                branch[0].pblossds = ploss1
                branch[0].qblossds = qloss1
                if pl1 != 0:
                    branch[0].dPdV = (branch[0].dPdV*(pl1-pla) + dPdV1*pla)/pl1
                if ql1 != 0:
                    branch[0].dQdV = (branch[0].dQdV*(ql1-qla) + dQdV1*qla)/ql1
                if branch[0].toline:         # Follow the next node in the main path
                    lobj = branch[0].toline
                    if lobj.connected:
                        pto = branch[0].ploadds + branch[0].pblossds      # Find the flow to the downstream bus
                        qto = branch[0].qloadds + branch[0].qblossds
                        lobj.ploss = lobj.r * (pto ** 2 + qto ** 2) / branch[0].vomag ** 2   # Estimate the losses of the branch
                        lobj.qloss = lobj.x* (pto ** 2 + qto ** 2) / branch[0].vomag ** 2
                        ploss1 += lobj.ploss
                        qloss1 += lobj.qloss
                        branch[0].pblossds = ploss1      # Add the losses to the downstream bus
                        branch[0].qblossds = qloss1

            else:                               # No branching at the bus
                pla, qla, dPdV1, dQdV1 = getload(branch[0])
                pl1 += pla   # Add local loads
                ql1 += qla
                branch[0].ploadds = pl1
                branch[0].qloadds = ql1
                if pl1 != 0:
                    branch[0].dPdV = (branch[0].dPdV*(pl1-pla) + dPdV1*pla)/pl1 # Weighting accumulated and bus DPDV
                if ql1 != 0:
                    branch[0].dQdV = (branch[0].dQdV*(ql1-qla) + dQdV1*qla)/ql1
                if branch[0].toline:
                    lobj = branch[0].toline
                    if lobj.connected:
                        pto = branch[0].ploadds + ploss1
                        qto = branch[0].qloadds + qloss1
                        lobj.ploss = lobj.r * (pto ** 2 + qto ** 2) / branch[0].vomag ** 2
                        lobj.qloss = lobj.x * (pto ** 2 + qto ** 2) / branch[0].vomag ** 2
                        ploss1 += lobj.ploss
                        qloss1 += lobj.qloss
                        branch[0].pblossds = ploss1
                        branch[0].qblossds = qloss1

        return pl1, ql1, ploss1,  qloss1            # Return the accumulated loads and losses from the current branch

    #
    # Update the voltage profile starting on the top node
    #
    def UpdateVolt(topologyList):
        """Update the voltage profile based on the accumulated load on each bus
        """

        #
        # Function for calculating the voltages and sensitivities in the single phase case
        #
        def nodeVoltSensSP(fbus, tbus, tline, busobj):
            """
            Calculate the node voltages and sensitivities in the single phase case
            :param fbus:
            :param tbus:
            :param tline:
            :param busobj:
            :return:
            """

            vk2 = fbus.vomag ** 2
            tpload = busobj[0].ploadds + busobj[0].pblossds  # Find the accumulated loads and losses flowing on the branch
            tqload = busobj[0].qloadds + busobj[0].qblossds
            # Voltage calculation
            term2 = 2 * (tpload * tline.r + tqload * tline.x)
            term3 = (tpload ** 2 + tqload ** 2) * (tline.r ** 2 + tline.x ** 2) / fbus.vomag ** 2
            tbus.vomag = np.sqrt(vk2 - term2 + term3)  # Update the bus voltage magnitude on the down-stream bus
            # Calculate the sensitivities for changing the load
            dvdp = (-tline.r + tpload * (tline.r ** 2 + tline.x ** 2) / fbus.vomag ** 2) / tbus.vomag
            dpdq = (2 * tline.r * tqload / tbus.vomag ** 2) * (
                        1 + 2 * tline.r * tpload / tbus.vomag ** 2)
            dvdq = (-tline.x + tqload * (tline.r ** 2 + tline.x ** 2) / fbus.vomag ** 2) / tbus.vomag
            dqdp = (2 * tline.x * tpload / tbus.vomag ** 2) * (
                        1 + 2 * tline.x * tqload / tbus.vomag ** 2)
            dpldp = (2 * tline.r * tpload / tbus.vomag ** 2) * (
                        1 + 2 * tline.x * tqload / tbus.vomag ** 2)

            tbus.dVdP = fbus.dVdP + dvdp + dvdq * dqdp
            tbus.dVdQ = fbus.dVdQ + dvdq + dvdp * dpdq
            # Calculate sensitivities for change in losses
            tbus.dPlossdP = fbus.dPlossdP + dpldp
            tbus.dPlossdQ = fbus.dPlossdQ + dpdq
            tbus.dQlossdP = fbus.dQlossdP + dqdp
            tbus.dQlossdQ = fbus.dQlossdQ + 2 * tline.x * tqload / tbus.vomag ** 2 + 2 * tline.x * tpload * tbus.dPlossdQ / tbus.vomag ** 2
            # Calculate the second-order derivatives
            if tqload != 0:
                tbus.dP2lossdQ2 = fbus.dP2lossdQ2 + dpdq / tqload + (
                                2 * tline.r * tqload / tbus.vomag ** 2) * 2 * tline.r * dpdq / tbus.vomag ** 2
            else:
                tbus.dP2lossdQ2 = fbus.dP2lossdQ2 + dpdq / 1E-9 + (
                                2 * tline.r * tqload / tbus.vomag ** 2) * 2 * tline.r * dpdq / tbus.vomag ** 2
            if tpload != 0:
                tbus.dP2lossdP2 = fbus.dP2lossdQ2 + dpldp / tpload + (
                                2 * tline.r * tpload / tbus.vomag ** 2) * 2 * tline.x * dqdp / tbus.vomag ** 2
            else:
                tbus.dP2lossdP2 = fbus.dP2lossdQ2 + dpldp / 1E-9 + (
                                2 * tline.r * tpload / tbus.vomag ** 2) * 2 * tline.x * dqdp / tbus.vomag ** 2

            tbus.lossRatioQ = tbus.dPlossdQ / tbus.dP2lossdQ2
            tbus.lossRatioP = tbus.dPlossdP / tbus.dP2lossdP2

            # Update the voltage for the purpose of loss minimization - adjust the sensitivity acording to the chosen step.
            if tbus.iloss:
                if np.abs(tbus.dPlossdQ) >= 1.0 / tbus.pqcostRatio:  # Equivalent to that the dP cost more than pqcostRatio times dQ
                    qcomp = tbus.dPlossdQ / tbus.dP2lossdQ2
                    tbus.qload -= qcomp
                    tbus.dPlossdQ = 0.0

            # Voltage angle calculation
            busvoltreal = fbus.vomag - (tpload * tline.r + tqload * tline.x) / fbus.vomag
            busvoltimag = (tqload * tline.r - tpload * tline.x) / fbus.vomag
            tbus.voang = fbus.voang + np.arctan2(busvoltimag, busvoltreal)  # Update voltage angles
            #  End

        for branch in topologyList:
            if len(branch) > 1:

                if branch[0].toline:
                    tline = branch[0].toline
                    fbus = tline.fbus
                    tbus = tline.tbus

                    # Update voltages and sensitivities Single Phase
                    nodeVoltSensSP(fbus, tbus, tline, branch)

                iloop = 1
                while iloop < len(branch):         # Update voltages along the branches
                    UpdateVolt(branch[iloop])
                    iloop += 1
            else:                   # Continue along the current path
                if branch[0].toline:
                    tline = branch[0].toline
                    fbus = tline.fbus
                    tbus = tline.tbus

                    # Update voltages and sensitivities Single Phase
                    nodeVoltSensSP(fbus, tbus, tline, branch)

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

    topology, BusList, LineList = configure(BusList, LineList)

    BusList = DistLF(topology, BusList, maxit=5)

    return BusList


#
# Calculates the load for the actual volage at the bus
#
def getload(busobj):
    """ Calculates the net voltage corrected load at the bus - currently a simple ZIP model is applied.
    Input: The busobject
    Returns: pLoadAct, qLoadAct
    """
    relative_pload = busobj.pload-busobj.pprod # load - production
    relative_qload = busobj.qload-busobj.qprod # load - production

    pLoadAct = relative_pload*(busobj.ZIP[0]*busobj.vomag**2 + busobj.ZIP[1]*busobj.vomag + busobj.ZIP[2])
    qLoadAct = relative_qload*(busobj.ZIP[0]*busobj.vomag**2 + busobj.ZIP[1]*busobj.vomag + busobj.ZIP[2])
    dPdV = relative_pload*(busobj.ZIP[0]*2*busobj.vomag + busobj.ZIP[1])
    dQdV = relative_qload*(busobj.ZIP[0]*2*busobj.vomag + busobj.ZIP[1])
    return pLoadAct, qLoadAct, dPdV, dQdV

