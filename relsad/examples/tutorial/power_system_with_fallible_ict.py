from relsad.examples.tutorial.system_components import *

from relsad.network.systems import ICTNetwork
from relsad.network.components import (
    ICTNode,
    ICTLine,
)

from relsad.network.systems import PowerSystem

ps = PowerSystem(controller=C1)

# ICT nodes
ICTNC1 = ICTNode(
    name="ICTNC1",
)
ICTNISW1 = ICTNode(
    name="ICTNISW1",
)
ICTNS1 = ICTNode(
    name="ICTNS1",
)

# ICT lines
ICTL1 = ICTLine(
    name="ICTL1",
    fnode=ICTNC1,
    tnode=ICTNISW1,
)
ICTL2 = ICTLine(
    name="ICTL2",
    fnode=ICTNC1,
    tnode=ICTNS1,
)
ICTL3 = ICTLine(
    name="ICTL3",
    fnode=ICTNS1,
    tnode=ICTNISW1,
)

# ICT network
ict_network = ICTNetwork(ps)
ict_network.add_nodes(
    [
        ICTNC1,
        ICTNISW1,
        ICTNS1,
    ]
)
ict_network.add_lines(
    [
        ICTL1,
        ICTL2,
        ICTL3,
    ]
)
