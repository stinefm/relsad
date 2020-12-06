import pytest
from stinetwork.test_networks.smallNetwork import initialize_test_network

class MyError(Exception):
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return self.m


def test_B1_fail():
    ps = initialize_test_network()


    ps.get_comp("B1").fail()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == False
    assert ps.get_comp("L8").connected == True
    assert ps.get_comp("L9").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == True
    assert ps.get_comp("L2a").is_open == True
    assert ps.get_comp("L3a").is_open == True
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == True
    assert ps.get_comp("L7b").is_open == False

def test_B2_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B2").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("L8").connected == True
    assert ps.get_comp("L9").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == True
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_B3_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B3").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == False
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("L8").connected == True
    assert ps.get_comp("L9").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == True
    assert ps.get_comp("L4a").is_open == True
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_B4_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B4").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == False
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("L8").connected == True
    assert ps.get_comp("L9").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == True
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_B5_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B5").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("L8").connected == True
    assert ps.get_comp("L9").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_M1_fail():
    ps = initialize_test_network()
    
    ps.get_comp("M1").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == False
    assert ps.get_comp("L8").connected == False
    assert ps.get_comp("L9").connected == False
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == True

def test_M2_fail():
    ps = initialize_test_network()
    
    ps.get_comp("M2").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("L8").connected == False
    assert ps.get_comp("L9").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_M3_fail():
    ps = initialize_test_network()
    
    ps.get_comp("M3").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("L8").connected == True
    assert ps.get_comp("L9").connected == False
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L1a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L1a").fail()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == True
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L1b_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L1b").fail()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == True
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L1c_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L1c").fail()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == True
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_E1_fail():
    ps = initialize_test_network()
    
    ps.get_comp("E1").fail()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == True
    assert ps.get_comp("L1a").is_open == True
    assert ps.get_comp("L1b").is_open == True
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L2a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L2a").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == True
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L3a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L3a").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == True
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L3b_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L3b").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == True
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L4a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L4a").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == False
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == True
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L5a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L5a").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L6a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L6a").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L7a_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L7a").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == False
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == True
    assert ps.get_comp("L7b").is_open == False

def test_L7b_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L7b").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == False
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == True

def test_L1_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L1").fail()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == True
    assert ps.get_comp("L1a").is_open == True
    assert ps.get_comp("L1b").is_open == True
    assert ps.get_comp("L1c").is_open == True
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L2_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L2").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == True
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L3_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L3").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == True
    assert ps.get_comp("L3b").is_open == True
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L4_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L4").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == False
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == True
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L5_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L5").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L6_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L6").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False

def test_L7_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L7").fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == False
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L7a").is_open == True
    assert ps.get_comp("L7b").is_open == True