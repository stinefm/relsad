def connectivity(nodelist, linelist):
    ## Initializing dictionaries
    undirectPathDict = dict()
    directPathDict = dict()
    for node in nodelist:
        undirectPathDict[node.name] = dict()
        directPathDict[node.name] = dict()
        for connectedNode in nodelist:
            undirectPathDict[node.name][connectedNode.name] = []
            directPathDict[node.name][connectedNode.name] = []

    for line in linelist:
        for toBusNode in [line.to_element]:
            for fromBusNode in [line.from_element]:
                if not toBusNode == fromBusNode:
                    directPathDict[fromBusNode.name][toBusNode.name] = [[line]]
                    undirectPathDict[fromBusNode.name][toBusNode.name] = [[line]]
                    undirectPathDict[toBusNode.name][fromBusNode.name] = [[line]]

    ## Creating directPathDict
    for _ in range(len(nodelist)):
        for nodeObject in nodelist:
            node = nodeObject.name
            for connectedNodeObject in nodelist:
                connectedNode = connectedNodeObject.name
                if not node == connectedNode:
                    lines_nTcn = directPathDict[node][connectedNode] #paths between node and connectedNode
                    if not lines_nTcn == []: # If line between node and connectedNode exists
                        linesConnectedToConnectedNode = [line for line in linelist if \
                        connectedNodeObject in [line.from_element]]
                        for line in linesConnectedToConnectedNode:
                            for newNode in [line.to_element.name]:
                                if not node == newNode and not connectedNode == newNode:
                                    lines_nTnn = directPathDict[node][newNode] #paths between node and newNode                                      
                                    for i in range(len(lines_nTcn)):
                                            accept = True
                                            if lines_nTcn[i]+[line] in lines_nTnn or lines_nTnn in lines_nTcn[i]+[line] \
                                                or line in lines_nTcn[i]:
                                                accept = False
                                            toAndFromBuses = list()
                                            for l in lines_nTcn[i]+[line]:
                                                for toBusNode in [l.to_element.name]:
                                                    toAndFromBuses.append(toBusNode)
                                                for fromBusNode in [l.from_element.name]:
                                                    toAndFromBuses.append(fromBusNode)
                                            for e in toAndFromBuses:
                                                if toAndFromBuses.count(e) > 2:
                                                    accept = False
                                            if accept:
                                                newlines_nTnn = \
                                                [lines_nTcn[i]+ \
                                                [line]]
                                                lines_nTnn += newlines_nTnn
                                    directPathDict[node][newNode] = lines_nTnn #Updating pathDict

    ## Creating undirectPathDict
    for _ in range(len(nodelist)):
        for nodeObject in nodelist:
            node = nodeObject.name
            for connectedNodeObject in nodelist:
                connectedNode = connectedNodeObject.name
                if not node == connectedNode:
                    lines_nTcn = undirectPathDict[node][connectedNode] #paths between node and connectedNode
                    if not lines_nTcn == []: # If line between node and connectedNode exists
                        linesConnectedToConnectedNode = [line for line in linelist if \
                        connectedNodeObject in [line.to_element] or connectedNodeObject in [line.from_element]]
                        for line in linesConnectedToConnectedNode:
                            if connectedNode in line.to_element.name:
                                newNodes = [line.from_element.name]
                            elif connectedNode in line.from_element.name:
                                newNodes = [line.to_element.name]
                            else:
                                break
                            for newNode in newNodes:
                                if not node == newNode and not connectedNode == newNode:
                                    lines_nTnn = undirectPathDict[node][newNode] #paths between node and newNode                                      
                                    for i in range(len(lines_nTcn)):
                                            accept = True
                                            if lines_nTcn[i]+[line] in lines_nTnn or lines_nTnn in lines_nTcn[i]+[line] \
                                                or line in lines_nTcn[i]:
                                                accept = False
                                            toAndFromBuses = list()
                                            for l in lines_nTcn[i]+[line]:
                                                for toBusNode in [l.to_element.name]:
                                                    toAndFromBuses.append(toBusNode)
                                                for fromBusNode in [l.from_element.name]:
                                                    toAndFromBuses.append(fromBusNode)
                                            for e in toAndFromBuses:
                                                if toAndFromBuses.count(e) > 2:
                                                    accept = False
                                            if accept:
                                                newlines_nTnn = \
                                                [lines_nTcn[i]+ \
                                                [line]]
                                                lines_nTnn += newlines_nTnn
                                    undirectPathDict[node][newNode] = lines_nTnn #Updating pathDict
                                    if not lines_nTnn == []:
                                        for path in lines_nTnn:
                                            if not path[::-1] in undirectPathDict[newNode][node] and not path == []:
                                                undirectPathDict[newNode][node].append(path[::-1])

    return undirectPathDict, directPathDict

def config(BusList, LineList):
    """Function for making the topology - it sets up the connection between two buses by assigned the line to the to bus
    and by preparing a list of from bus connections (branching)

    """
    for lobj in LineList:
        if lobj.ibstat:
            itr = lobj.tbus.num - 1
            ifr = lobj.fbus.num - 1
            BusList[itr].tolinelist.append(lobj)
            BusList[itr].toline = lobj  # Add information to each bus of a line abouth which line that connects
            BusList[ifr].fromline = lobj

    for lobj in LineList:
        if lobj.ibstat:
            if lobj.fbus.num > 1 and BusList[lobj.fbus.num - 1].toline == 0:  # Identify broken chains in the grid
                itb = lobj.tbus.num
                lobj.tbus.num = lobj.fbus.num  # Change direction and identify next line in the chain.
                lobj.fbus.num = itb
                BusList[lobj.tbus.num - 1].toline = lobj
                lobj1 = BusList[lobj.fbus.num - 1].fromline  # Keep the next line

                OneMore = True
                while OneMore:
                    if lobj1.tbus.num > lobj1.fbus.num:  # Changes currently too many
    #                     print('lobj:', lobj1.fbus, lobj1.tbus)
                        itb = lobj1.tbus.num
                        lobj1.tbus.num = lobj1.fbus.num
                        lobj1.fbus.num = itb
                        BusList[lobj1.tbus.num - 1].toline = lobj1
                        lobj1 = BusList[lobj1.fbus.num - 1].fromline
                        if len(BusList[lobj1.tbus.num - 1].tolinelist) == 2:
                            OneMore = False
        #         print('lobj:', lobj1.fbus, lobj1.tbus)
                itb = lobj1.tbus.num
                lobj1.tbus.num = lobj1.fbus.num
                lobj1.fbus.num = itb
                BusList[lobj1.tbus.num - 1].toline = lobj1

    # Add the topology information needed to define the tree structure
    for lobj in LineList:
        if lobj.ibstat:
            itr = lobj.tbus.num - 1
            ifr = lobj.fbus.num - 1
            BusList[ifr].nextbus.append(BusList[itr])  # Add the next bus to the list of branches of the bus
        #     print('Line: ',lobj.fbus, lobj.tbus, self.BusList[itr].toline.fbus )

    return BusList, LineList

def mainstruct(BusList):
    """ The algorithm builds up a tree structure based on topology information provided in instances of a node class
    There can be any number of branching on a bus in the main path.
    Multiple branching in sublists are possible.

    The principle is to insert a sublist til the element where the branching appears
    """
    mainlist = []
    mainlist.append([BusList[0]])
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