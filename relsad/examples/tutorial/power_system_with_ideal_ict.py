from relsad.examples.tutorial.system_components import *

from relsad.network.components import (
    MainController,
    Sensor,
    IntelligentSwitch,
)

C1 = MainController(name="C1")

Isw1 = IntelligentSwitch(
    name="Isw1",
    disconnector=DL2a,
)

S1 = Sensor(
    name="S1",
    line=L2,
)
