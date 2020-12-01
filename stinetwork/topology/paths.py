from stinetwork.network.components import Line, Bus

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

def configure(BusList, LineList):
    """Function that sets up the nested topology array and configures the radial tree according to the slack bus
    """

    def line_between_buses(bus1, bus2, LineList):
        for line in LineList:
            if (line.tbus == bus1 and line.fbus==bus2) or \
                (line.tbus == bus2 and line.fbus==bus1):
                return line

    def change_dir(target_bus, BusList, checked_buses, LineList):
        if target_bus not in checked_buses:
            for bus in BusList:
                if bus not in checked_buses:
                    if target_bus in bus.nextbus:
                        #print(target_bus.name, bus.name)
                        line = line_between_buses(target_bus, bus, LineList)
                        #print(line.name)
                        line.change_direction()
                        checked_buses.append(target_bus)
                        return bus

    def get_paths(parent_bus):
        """Function that finds all downstream paths in a radial tree

        Input: 
        parent_bus(Bus): Parent bus of radial tree

        Output:
        paths(list): List of all downstream paths from parent_bus

        """
        if len(parent_bus.nextbus)==0:
            return [[[parent_bus]]]
        paths = []
        for nbus in parent_bus.nextbus:
            for path in get_paths(nbus):
                paths.append([[parent_bus]]+path)
        return paths

    def get_topology(paths):
        """Function that constructs a nested topology array

        Input:
        paths(list): List of all downstream paths from parent_bus in radial tree

        Output:
        topology(list): Nested topology list
        """
        used_buses = list()
        main_path = paths[0]
        used_buses += main_path
        topology = [main_path]
        for path in paths[1:]:
            sub_path = list()
            for bus in path:
                if bus not in used_buses:
                    sub_path.append(bus)
            used_buses+=sub_path
            topology.append(sub_path)

        while len(topology) > 1:
            last_path = topology[-1]
            top_bus = last_path[0][0]
            for n, path in enumerate(topology[:-1]):
                for k, bus in enumerate(path):
                    if top_bus in bus[0].nextbus:
                        topology[n][k].append(last_path)
                        topology.remove(last_path)
                        break

        topology = topology[0]

        return topology

    ## Find slack bus
    for i, bus in enumerate(BusList):
        if bus.is_slack:
            slack_bus = bus
            old = BusList[0]
            BusList[0] = slack_bus
            BusList[i] = old
            break

    ## Update directions based on slack bus (making slack bus parent of the radial tree)
    checked_buses = list()
    target_bus = change_dir(slack_bus, BusList, checked_buses, LineList)
    while target_bus != None:
        target_bus = change_dir(target_bus, BusList, checked_buses, LineList)

    paths = get_paths(slack_bus)

    topology = get_topology(paths)

    return topology, BusList, LineList

def flatten(toflatten):    
    for element in toflatten:
        try:
            yield from flatten(element)
        except TypeError:
            yield element

