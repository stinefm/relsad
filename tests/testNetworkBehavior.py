import pytest
from stinetwork.test_networks.smallNetwork import initialize_test_network
from stinetwork.network.systems import find_sub_systems

class MyError(Exception):
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return self.m


def test_B1_trafo_fail():
    ps = initialize_test_network()


    ps.get_comp("B1").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_B2_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B2").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_B3_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B3").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_B4_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B4").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_B5_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("B5").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_M1_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("M1").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_M2_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("M2").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_M3_trafo_fail():
    ps = initialize_test_network()
    
    ps.get_comp("M3").trafo_fail()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False


def test_L1_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L1").fail()     
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == True
    assert ps.get_comp("L1a").is_open == True
    assert ps.get_comp("L1b").is_open == True
    assert ps.get_comp("L1c").is_open == True
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L2_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L2").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == True
    assert ps.get_comp("L2b").is_open == True
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L6b").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L3_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L3").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == True
    assert ps.get_comp("L3b").is_open == True
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L6b").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L4_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L4").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == False
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == True
    assert ps.get_comp("L4b").is_open == True
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L5_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L5").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L5b").is_open == True
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L6b").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L6_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L6").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L7_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L7").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == False
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == True
    assert ps.get_comp("L7b").is_open == True
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_ML1_fail():
    ps = initialize_test_network()
    
    ps.get_comp("ML1").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == False
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == True
    assert ps.get_comp("ML1b").is_open == True
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_ML2_fail():
    ps = initialize_test_network()
    
    ps.get_comp("ML2").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == False
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == True
    assert ps.get_comp("ML2b").is_open == True

def test_E1_fail():
    ps = initialize_test_network()
    
    ps.get_comp("E1").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == False
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == True
    assert ps.get_comp("L1a").is_open == True
    assert ps.get_comp("L1b").is_open == True
    assert ps.get_comp("L1c").is_open == True
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == False
    assert ps.get_comp("L3b").is_open == False
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == True
    assert ps.get_comp("L6b").is_open == True
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False


def test_L2_and_L3_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L2").fail()
    ps.get_comp("L3").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == True
    assert ps.get_comp("L2b").is_open == True
    assert ps.get_comp("L3a").is_open == True
    assert ps.get_comp("L3b").is_open == True
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == False
    assert ps.get_comp("L5b").is_open == False
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L6b").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False

def test_L3_and_L5_fail():
    ps = initialize_test_network()
    
    ps.get_comp("L3").fail()
    ps.get_comp("L5").fail()
          
    find_sub_systems(ps)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("L6").connected == True
    assert ps.get_comp("L7").connected == True
    assert ps.get_comp("ML1").connected == True
    assert ps.get_comp("ML2").connected == True
    assert ps.get_comp("E1").is_open == False
    assert ps.get_comp("L1a").is_open == False
    assert ps.get_comp("L1b").is_open == False
    assert ps.get_comp("L1c").is_open == False
    assert ps.get_comp("L2a").is_open == False
    assert ps.get_comp("L2b").is_open == False
    assert ps.get_comp("L3a").is_open == True
    assert ps.get_comp("L3b").is_open == True
    assert ps.get_comp("L4a").is_open == False
    assert ps.get_comp("L4b").is_open == False
    assert ps.get_comp("L5a").is_open == True
    assert ps.get_comp("L5b").is_open == True
    assert ps.get_comp("L6a").is_open == False
    assert ps.get_comp("L6b").is_open == False
    assert ps.get_comp("L7a").is_open == False
    assert ps.get_comp("L7b").is_open == False
    assert ps.get_comp("ML1a").is_open == False
    assert ps.get_comp("ML1b").is_open == False
    assert ps.get_comp("ML2a").is_open == False
    assert ps.get_comp("ML2b").is_open == False