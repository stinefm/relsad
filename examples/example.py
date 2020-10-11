from network.systems import Distribution, Microgrid
from network.components import Bus, Line, Battery, LoadBreaker, Production, SlackBus, CircuitBreaker
from plotting.plot_network import plot

#Example network

b1 = Bus(1, [0,0])
b2 = Bus(2, [0,1])
b3 = Bus(3, [1,0])
b4 = Bus(4, [1,-1])
microgrid = Microgrid(1, [0,-1])

l1 = Line(b1,b2,0.001,0.001,1,1,1,1)
l2 = Line(b1,b3,0.001,0.001,1,1,1,1)
l3 = Line(b3,b4,0.001,0.001,1,1,1,1)
l4 = Line(b1,microgrid,0.001,0.001,1,1,1,1)

dist = Distribution()

dist.add_buses([b1,b2,b3,b4])
dist.add_microgrids([microgrid])
dist.add_lines([l1,l2,l3,l4])

plot(dist.buses, dist.lines)