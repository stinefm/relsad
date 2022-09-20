import runpy

def test_tutorial_power_system_with_fallible_ict():
    runpy.run_module(
        "relsad.examples.tutorial.power_system_with_fallible_ict"
    )
