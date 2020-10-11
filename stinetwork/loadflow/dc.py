import numpy as np

def runDCPowerFlow(self):

    self.PowerElements = [x for x in self.systemComponents if (x.comp_type == 'P' and type(x)==Element)]      
    self.PowerIndices = [i for i, x in enumerate(self.systemComponents) if (x.comp_type == 'P' and type(x)==Element)]
    self.PowerLines = [x for x in self.systemComponents if (x.comp_type == 'P' and type(x)==Connection)]
    self.PowerLinePaths, _ = self.connectivity(self.PowerElements, self.PowerLines)

    self.PowerStates = list()
    for i in range(len(self.systemStates)):
        tempList = list()
        for j in range(len(self.systemStates[i])):
            if j in self.PowerIndices:
                tempList.append(self.systemStates[i][j])
        self.PowerStates.append(tempList)
        
    self.Pline = list()  
    self.Pload = list()
    self.Pgen = list()    

    # DC Power Flow: 

    for i in range(len(self.PowerStates)):
        self.Pload.append(np.zeros(len(self.PowerElements)))
        self.Pgen.append(np.zeros(len(self.PowerElements)))
        self.Pline.append(np.zeros(len(self.PowerLines)))

        busSortDict = dict()
        n = 0
        for k in range(len(self.PowerStates[i])):
            elem = self.PowerElements[k]
            sum_con = 0
            sum_con_failed = 0
            if self.PowerStates[i][k] == 0:
                for conLine in elem.from_lines+elem.to_lines:
                    for conElem in [conLine.from_element,conLine.to_element]:
                        if conElem.comp_type == elem.comp_type and conElem != elem:
                            sum_con += 1
                            index = self.PowerElements.index(conElem)
                            if self.PowerStates[i][index] == 1:
                                sum_con_failed += 1
                                    
                if sum_con_failed < sum_con:
                    busSortDict[elem] = n
                    n += 1
                    slackBus = elem

        n_dim = len(busSortDict.values())

        for j in range(len(self.PowerStates[i])):
            self.Pload[i][j] = self.PowerElements[j].load
            if self.PowerStates[i][j] == 1:
                self.Pgen[i][j] = 0
            else:
                self.Pgen[i][j] = self.PowerElements[j].gen
                
        if n_dim > 0:

            # Creating Bbus

            Bbus = np.zeros((n_dim,n_dim))

            for k in range(len(self.PowerStates[i])):
                elem1 = self.PowerElements[k]
                if self.PowerStates[i][k] == 0:
                    for conLine in elem1.from_lines+elem1.to_lines:
                        for conElem in [conLine.from_element,conLine.to_element]:
                            if conElem.comp_type == elem1.comp_type and conElem != elem1:
                                l = self.PowerElements.index(conElem)
                                if self.PowerStates[i][l] == 0:
                                    Bbus[busSortDict[self.PowerElements[k]],busSortDict[self.PowerElements[k]]] += 1/conLine.x
                                    Bbus[busSortDict[self.PowerElements[k]],busSortDict[self.PowerElements[l]]] -= 1/conLine.x
            P = np.zeros(n_dim)
            for j in range(len(self.PowerStates[i])):
                try:P[busSortDict[self.PowerElements[j]]] = self.Pgen[i][j] - self.Pload[i][j]
                except:pass

            # if i == self.testindex:
            #     print(P)
            #     print(self.PowerLinePaths[slackBus.name])


            slackBusPowerBalance = slackBus.gen - slackBus.load

            k = 1
            while k < len(P):
                for elemName in self.PowerLinePaths[slackBus.name]:
                    elem = [x for x in self.PowerElements if x.name == elemName][0]
                    if elem in list(busSortDict.keys()) and \
                        len(self.PowerLinePaths[slackBus.name][elemName]) == k:
                        index = busSortDict[elem]
                        if sum(P) <= 0:
                            if slackBusPowerBalance >= 0:
                                if P[index] < 0:
                                    if slackBusPowerBalance + P[index] < 0:
                                        P[index] = -slackBusPowerBalance
                                        slackBusPowerBalance = 0
                                    else:
                                        slackBusPowerBalance += P[index]
                                        P[index] = 0
                        else:
                            if slackBusPowerBalance <= 0:
                                if P[index] > 0:
                                    if slackBusPowerBalance + P[index] < 0:
                                        P[index] = 0
                                        slackBusPowerBalance += P[index]
                                    else:
                                        slackBusPowerBalance = 0
                                        P[index] += slackBusPowerBalance
                            else:
                                if P[index] > 0:
                                    P[index] = 0

                k += 1



            # if i == self.testindex:
            #     print('Trimmed:', P)
            #     print(slackBusPowerBalance)
                


            #Reducing Bbus

            B = np.zeros((n_dim-1,n_dim-1))
            for elem1 in busSortDict:
                k = busSortDict[elem1]
                if elem1 == slackBus:
                    for n in busSortDict.values():
                        if n != k:
                            B[n] = np.delete(Bbus[n],k)
                    P = np.delete(P,k)


            theta = np.zeros(n_dim)

            theta_solved = np.linalg.solve(B, P)
            for t in range(len(theta_solved)):
                theta[t] = theta_solved[t]

            for line in self.PowerLines:
                if all([x in busSortDict.keys() for x in [line.from_element, line.to_element]]):
                    j = self.PowerLines.index(line)
                    m = busSortDict[line.to_element]
                    n = busSortDict[line.from_element]
                    self.Pline[i][j] = (theta[m]-theta[n])/line.x

            # if i == self.testindex:
            #     print(Bbus)
            #     print(B)
            #     print(P)
            #     print(theta)
            #     print(self.Pline[i])
        else:
            theta = 0
            self.Pline[i] = [0]*(len(self.PowerStates[i])-1)
