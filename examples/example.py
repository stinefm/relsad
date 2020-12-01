from stinetwork.network.systems import PowerSystem, Distribution, Microgrid
from stinetwork.network.components import Bus, Line, Battery, Disconnector, Production, CircuitBreaker
from stinetwork.visualization.plotting import plot_topology

#Example network

b1 = Bus("B1", coordinate=[0,0])
b2 = Bus("B2", coordinate=[0,1])
b3 = Bus("B3", coordinate=[1,0])
b4 = Bus("B4", coordinate=[1,-1])
m1 = Bus("M1", coordinate=[0,-1])

l1 = Line("L1",b1,b2,0.001,0.001,1,1,1,1)
l2 = Line("L2",b1,b3,0.001,0.001,1,1,1,1)
l3 = Line("L3",b3,b4,0.001,0.001,1,1,1,1)
l4 = Line("L4",b1,m1,0.001,0.001,1,1,1,1)

ps = PowerSystem()

dist = Distribution(ps)

dist.add_buses([b1,b2,b3,b4])

dist.add_lines([l1,l2,l3])

microgrid = Microgrid(ps,l4)
microgrid.add_buses([m1])

plot_topology(ps.active_buses, ps.active_lines)