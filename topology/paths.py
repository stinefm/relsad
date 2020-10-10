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