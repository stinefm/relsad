from relsad.topology.ICT.dfs import is_connected
from relsad.network.components import (
    ICTNode,
    ICTLine,
    MainController,
)
from relsad.network.systems import (
    PowerSystem,
    ICTNetwork,
)


def test_is_connected_1():
    n1 = ICTNode(name="n1")
    n2 = ICTNode(name="n2")
    n3 = ICTNode(name="n3")
    n4 = ICTNode(name="n4")
    n5 = ICTNode(name="n5")
    n6 = ICTNode(name="n6")

    l1 = ICTLine(
        name="l1",
        fnode=n1,
        tnode=n2,
    )
    l2 = ICTLine(
        name="l2",
        fnode=n1,
        tnode=n3,
    )
    l3 = ICTLine(
        name="l3",
        fnode=n2,
        tnode=n4,
    )
    l4 = ICTLine(
        name="l4",
        fnode=n3,
        tnode=n5,
    )
    l5 = ICTLine(
        name="l5",
        fnode=n5,
        tnode=n6,
    )
    controller = MainController(name="C")
    power_system = PowerSystem(controller=controller)
    network = ICTNetwork(power_system=power_system)

    network.add_nodes([n1, n2, n3, n4, n5, n6])
    network.add_lines([l1, l2, l3, l4, l5])

    assert is_connected(n1, n2, network) is True
    assert is_connected(n1, n3, network) is True
    assert is_connected(n1, n4, network) is True
    assert is_connected(n1, n5, network) is True
    assert is_connected(n1, n6, network) is True
    assert is_connected(n2, n3, network) is True
    assert is_connected(n2, n4, network) is True
    assert is_connected(n2, n5, network) is True
    assert is_connected(n2, n6, network) is True
    assert is_connected(n3, n4, network) is True
    assert is_connected(n3, n5, network) is True
    assert is_connected(n3, n6, network) is True
    assert is_connected(n4, n5, network) is True
    assert is_connected(n4, n6, network) is True
    assert is_connected(n5, n6, network) is True


def test_is_connected_2():
    n1 = ICTNode(name="n1")
    n2 = ICTNode(name="n2")
    n3 = ICTNode(name="n3")
    n4 = ICTNode(name="n4")
    n5 = ICTNode(name="n5")
    n6 = ICTNode(name="n6")

    l1 = ICTLine(
        name="l1",
        fnode=n1,
        tnode=n2,
    )
    l2 = ICTLine(
        name="l2",
        fnode=n1,
        tnode=n3,
    )
    l3 = ICTLine(
        name="l3",
        fnode=n2,
        tnode=n4,
    )
    l4 = ICTLine(
        name="l4",
        fnode=n3,
        tnode=n5,
    )
    l5 = ICTLine(
        name="l5",
        fnode=n5,
        tnode=n6,
    )
    controller = MainController(name="C")
    power_system = PowerSystem(controller=controller)
    network = ICTNetwork(power_system=power_system)

    network.add_nodes([n1, n2, n3, n4, n5, n6])
    network.add_lines([l1, l2, l3, l4, l5])

    l2.disconnect()

    assert is_connected(n1, n2, network) is True
    assert is_connected(n1, n3, network) is False
    assert is_connected(n1, n4, network) is True
    assert is_connected(n1, n5, network) is False
    assert is_connected(n1, n6, network) is False
    assert is_connected(n2, n3, network) is False
    assert is_connected(n2, n4, network) is True
    assert is_connected(n2, n5, network) is False
    assert is_connected(n2, n6, network) is False
    assert is_connected(n3, n4, network) is False
    assert is_connected(n3, n5, network) is True
    assert is_connected(n3, n6, network) is True
    assert is_connected(n4, n5, network) is False
    assert is_connected(n4, n6, network) is False
    assert is_connected(n5, n6, network) is True
