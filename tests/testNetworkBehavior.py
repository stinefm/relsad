import pytest
from smallNetwork import initialize_test_network

class MyError(Exception):
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return self.m


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