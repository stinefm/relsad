#!/usr/bin/python
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
# Definition of common classes

class Bus:
    'Common base class for all distribution buses'
    busCount = 0

    def __init__(self, busnum, pload=0.0, qload=0.0, ZIP=[0.0, 0.0 ,1.0], vset=0.0, iloss=0, pqcostRatio=100):
        self.busnum = busnum
        self.pload = pload
        self.qload = qload
        self.ZIP = ZIP
        self.vset = vset
        self.iloss = iloss
        self.pqcostRatio = pqcostRatio
        self.comp = 0
        self.ploadds = 0.0
        self.qloadds = 0.0
        self.pblossds = 0.0
        self.qblossds = 0.0
        self.dPdV = 0.0
        self.dQdV = 0.0
        self.dVdP = 0.0
        self.dVdQ = 0.0
        self.dPlossdP = 0.0
        self.dPlossdQ = 0.0
        self.dQlossdP = 0.0
        self.dQlossdQ = 0.0
        self.dP2lossdP2 = 1.0   # To be able to run the voltage optimization also in the first iteration
        self.dP2lossdQ2 = 1.0   # To be able to run the voltage optimization also in the first iteration
        self.lossRatioP = 0.0
        self.lossRatioQ = 0.0
        self.voang = 0.0
        self.vomag = 1.0
        self.busname = 'Bus' + str(busnum)
        self.toline = 0
        self.fromline = 0
        self.tolinelist = []
        self.nextbus = []
        Bus.busCount += 1

class Line:
    'Common base class for all distribution lines'
    lineCount = 0

    def __init__(self, fbus, tbus, r, x, ibstat=1):
        self.fbus = fbus
        self.tbus = tbus
        self.ibstat = ibstat
        self.r = r
        self.x = x
        self.ibstat = ibstat
        self.ploss = 0.0
        self.qloss = 0.0
        Line.lineCount += 1


class Statcom:
    'Common class for Statcom'
    statcomCount = 0
    def __init__(self, bus, scstat = 1, vref=0.0, injQmax = 0.0, injQmin = 0.0, slopeQ = 0.0 ):
        self.bus = bus
        self.scstat = scstat
        self.vref = vref
        self.injQmax = injQmax
        self.injQmin = injQmin
        self.Qinj = 0.0
        self.slopeQ = slopeQ
        Statcom.statcomCount += 1


class SVC:
    'Common class for Static Var Compensator'
    svcCount = 0
    def __init__(self, bus, svcstat = 1, vref=0.0, injQmax = 0.0, injQmin = 0.0, slopeQ = 0.0 ):
        self.bus = bus
        self.stat = svcstat
        self.vref = vref
        self.vprev = vref
        self.injQmax = injQmax
        self.injQmin = injQmin
        self.Qinj = 0.0
        self.slopeQ = slopeQ
        SVC.svcCount += 1

class Battery:
    'Common class for Batteries'
    batteryCount = 0
    def __init__(self, bus, svcstat = 1, vref=0.0, injPmax = 0.0, injPmin = 0.0, injQmax = 0.0, injQmin = 0.0, slopeP = 0.0, slopeQ = 0.0 ):
        self.bus = bus
        self.stat = svcstat
        self.vref = vref
        self.injPmax = injPmax
        self.injPmin = injPmin
        self.injQmax = injQmax
        self.injQmin = injQmin
        self.Pinj = 0.0
        self.Qinj = 0.0
        self.Estorage = 0.0
        self.slopeP = slopeP
        self.slopeQ = slopeQ
        Battery.batteryCount += 1

class Capacitor:
    'Common class for capacitors'
    capacitorCount = 0
    def __init__(self, bus, capstat = 1, vref=0.0, blockSize = 0.0, numBlocks = 1):
        self.bus = bus
        self.capstat = capstat
        self.vref = vref
        self.blockSize = blockSize
        self.numBlocks = numBlocks
        self.currentStep = 0
        Capacitor.capacitorCount += 1

