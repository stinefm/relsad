import sys
import runpy

def test_tutorial_system_components():
    if "relsad.examples.tutorial.system_components" in sys.modules:
        del sys.modules["relsad.examples.tutorial.system_components"]
    runpy.run_module(
        "relsad.examples.tutorial.system_components"
    )
