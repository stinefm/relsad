from stinetwork.network.components import Bus, Line
from stinetwork.network.systems import Distribution
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow


B0 = Bus(0, 0, 0) #Slack bus
B1 = Bus(1, 5, 0)
B2 = Bus(2, 4, 0)
B3 = Bus(3, 3, 0)
B4 = Bus(4, 2, 0)
B5 = Bus(5, 0, 0) # Microgrid
B6 = Bus(6, -10, 0) # Production

L1 = Line(B0, B1, 0.057526629463617, 0.029324854498807)
L2 = Line(B1, B2, 0.057526629463617, 0.029324854498807)
L3 = Line(B1, B3, 0.057526629463617, 0.029324854498807)
L4 = Line(B3, B4, 0.057526629463617, 0.029324854498807)
L5 = Line(B2, B6, 0.057526629463617, 0.029324854498807)
L6 = Line(B3, B6, 0.057526629463617, 0.029324854498807)
L7 = Line(B1, B5, 0.057526629463617, 0.029324854498807)
