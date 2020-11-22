from stinetwork.network.components import Bus, Line, Disconnector, CircuitBreaker
from stinetwork.network.systems import Distribution
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow
from stinetwork.visualization.plotting import plot_topology
import pytest

class MyError(Exception):
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return self.m

def initialize_test_network():
    B0 = Bus(0, 0, 0, coordinate=[0, 0]) #Slack bus
    B1 = Bus(1, 5, 0, coordinate=[0, -1])
    B2 = Bus(2, 4, 0, coordinate=[1, -2])
    B3 = Bus(3, 3, 0, coordinate=[0, -2])
    B4 = Bus(4, 2, 0, coordinate=[0, -3])
    B5 = Bus(5, 0, 0, coordinate=[1, -3]) # Microgrid
    B6 = Bus(6, -10, 0, coordinate=[-1, -2]) # Production

    L1 = Line(1, B0, B1, 0.057526629463617, 0.029324854498807)
    L2 = Line(2, B1, B2, 0.057526629463617, 0.029324854498807)
    L3 = Line(3, B1, B3, 0.057526629463617, 0.029324854498807)
    L4 = Line(4, B3, B4, 0.057526629463617, 0.029324854498807)
    L5 = Line(5, B2, B5, 0.057526629463617, 0.029324854498807)
    L6 = Line(6, B3, B5, 0.057526629463617, 0.029324854498807)
    L7 = Line(7, B1, B6, 0.057526629463617, 0.029324854498807)

    E1 = CircuitBreaker("E1", L1)

    Disconnector("L1a", L1, B0, E1)
    Disconnector("L1b", L1, B1, E1)
    Disconnector("L1c", L1, B1)
    Disconnector("L2a", L2, B1)
    Disconnector("L3a", L3, B1)
    Disconnector("L3b", L3, B3)
    Disconnector("L4a", L4, B3)
    Disconnector("L5a", L5, B2)
    Disconnector("L6a", L6, B3)
    Disconnector("L7a", L7, B1)
    Disconnector("L7b", L7, B6)

    dn = Distribution()

    dn.add_buses([B0,B1,B2,B3,B4,B5,B6])
    dn.add_lines([L1,L2,L3,L4,L5,L6,L7])

    return dn

def test_plot_topology():
    dn = initialize_test_network()
    try:
        pass#plot_topology(dn.buses,dn.lines)
    except MyError:
        pytest.fail("Unexpected MyError ..")

def test_B1_fail():
    dn = initialize_test_network()


    dn.get_comp("B1").fail()

    assert dn.get_comp("L1").connected == False
    assert dn.get_comp("L2").connected == False
    assert dn.get_comp("L3").connected == False
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == False
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == True
    assert dn.get_comp("L2a").is_open == True
    assert dn.get_comp("L3a").is_open == True
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == True
    assert dn.get_comp("L7b").is_open == False

def test_B2_fail():
    dn = initialize_test_network()
    
    dn.get_comp("B2").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == False
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == False
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == True
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == True
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_B3_fail():
    dn = initialize_test_network()
    
    dn.get_comp("B3").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == False
    assert dn.get_comp("L4").connected == False
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == False
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == True
    assert dn.get_comp("L4a").is_open == True
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == True
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_B4_fail():
    dn = initialize_test_network()
    
    dn.get_comp("B4").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == False
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == True
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_B5_fail():
    dn = initialize_test_network()
    
    dn.get_comp("B5").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == False
    assert dn.get_comp("L6").connected == False
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == True
    assert dn.get_comp("L6a").is_open == True
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_B6_fail():
    dn = initialize_test_network()
    
    dn.get_comp("B6").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == False
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == True

def test_L1a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L1a").fail()

    assert dn.get_comp("L1").connected == False
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == True
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L1b_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L1b").fail()

    assert dn.get_comp("L1").connected == False
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == True
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L1c_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L1c").fail()

    assert dn.get_comp("L1").connected == False
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == True
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_E1_fail():
    dn = initialize_test_network()
    
    dn.get_comp("E1").fail()

    assert dn.get_comp("L1").connected == False
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == True
    assert dn.get_comp("L1a").is_open == True
    assert dn.get_comp("L1b").is_open == True
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L2a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L2a").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == False
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == True
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L3a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L3a").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == False
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == True
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L3b_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L3b").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == False
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == True
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L4a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L4a").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == False
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == True
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L5a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L5a").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == False
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == True
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L6a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L6a").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == False
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == True
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L7a_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L7a").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == False
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == True
    assert dn.get_comp("L7b").is_open == False

def test_L7b_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L7b").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == False
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == True

def test_L1_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L1").fail()

    assert dn.get_comp("L1").connected == False
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == True
    assert dn.get_comp("L1a").is_open == True
    assert dn.get_comp("L1b").is_open == True
    assert dn.get_comp("L1c").is_open == True
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L2_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L2").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == False
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == False
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == True
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == True
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L3_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L3").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == False
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == True
    assert dn.get_comp("L3b").is_open == True
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L4_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L4").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == False
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == True
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L5_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L5").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == False
    assert dn.get_comp("L6").connected == False
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == True
    assert dn.get_comp("L6a").is_open == True
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L6_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L6").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == False
    assert dn.get_comp("L6").connected == False
    assert dn.get_comp("L7").connected == True
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == True
    assert dn.get_comp("L6a").is_open == True
    assert dn.get_comp("L7a").is_open == False
    assert dn.get_comp("L7b").is_open == False

def test_L7_fail():
    dn = initialize_test_network()
    
    dn.get_comp("L7").fail()

    assert dn.get_comp("L1").connected == True
    assert dn.get_comp("L2").connected == True
    assert dn.get_comp("L3").connected == True
    assert dn.get_comp("L4").connected == True
    assert dn.get_comp("L5").connected == True
    assert dn.get_comp("L6").connected == True
    assert dn.get_comp("L7").connected == False
    assert dn.get_comp("E1").is_open == False
    assert dn.get_comp("L1a").is_open == False
    assert dn.get_comp("L1b").is_open == False
    assert dn.get_comp("L1c").is_open == False
    assert dn.get_comp("L2a").is_open == False
    assert dn.get_comp("L3a").is_open == False
    assert dn.get_comp("L3b").is_open == False
    assert dn.get_comp("L4a").is_open == False
    assert dn.get_comp("L5a").is_open == False
    assert dn.get_comp("L6a").is_open == False
    assert dn.get_comp("L7a").is_open == True
    assert dn.get_comp("L7b").is_open == True