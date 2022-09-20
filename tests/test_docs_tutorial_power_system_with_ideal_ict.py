import importlib
import runpy
import relsad.examples.tutorial.system_components

def test_tutorial_power_system_with_ideal_ict():
    importlib.reload(relsad.examples.tutorial.system_components)
    runpy.run_module(
        "relsad.examples.tutorial.power_system_with_ideal_ict"
    )
