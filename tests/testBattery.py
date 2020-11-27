from stinetwork.network.components import Battery

def eq(x,y):
    return (abs(x-y)<1E-6)

def test_charge_from_min():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(1)

    assert rem==0
    assert b.E_battery==1.97

def test_discharge_from_min():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.discharge(0.97)

    assert rem==0.97
    assert b.E_battery==1

def test_charge_from_max():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge((1/0.97-1)*4)

    rem = b.charge(0.5)

    assert eq(rem,0.5)
    assert b.E_battery==5

def test_discharge_from_max():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge((1/0.97-1)*4)

    rem = b.discharge(0.5)

    assert rem==0
    assert b.E_battery==(5-0.5/0.97)

def test_discharge_overload():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge((1/0.97-1)*4)

    rem = b.discharge(1.5)

    assert rem==0.5
    assert b.E_battery==(5-1/0.97)

def test_discharge_below_min():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(0.5)

    rem = b.discharge(1)

    assert eq(rem,(1-0.5*0.97*0.97))
    assert b.E_battery==1

def test_charge_above_max():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)

    rem = b.charge(1)

    assert eq(rem,(1-0.12/0.97))
    assert b.E_battery == 5

def test_charge_overload():
    b = Battery(1,1,5,0.2,1,0.97)
    rem = b.charge(1)

    rem = b.charge(2)

    assert rem==1
    assert b.E_battery == 1+2*0.97