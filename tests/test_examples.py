import os
from relsad.examples.CINELDI.simulation import run_simulation as run_cineldi
from relsad.examples.IEEE33.simulation import run_simulation as run_ieee33
from relsad.examples.IEEE16_modified.simulation import run_simulation as run_ieee16_modified
from relsad.examples.RBTS2.simulation import run_simulation as run_rbts2
from relsad.examples.TEST10.simulation import run_simulation as run_test10


def test_run_cineldi():
    run_cineldi(
        data_dir=os.path.join(
            "relsad",
            "examples",
            "load",
            "data",
        ),
        save_flag=False,
    )


def test_run_ieee16_modified():
    run_ieee16_modified(
        data_dir=os.path.join(
            "relsad",
            "examples",
            "load",
            "data",
        ),
        save_flag=False,
    )


def test_run_ieee33():
    run_ieee33(
        data_dir=os.path.join(
            "relsad",
            "examples",
            "load",
            "data",
        ),
        save_flag=False,
    )


def test_run_rbts2():
    run_rbts2(
        save_flag=False,
    )


def test_run_test10():
    run_test10(
        data_dir=os.path.join(
            "relsad",
            "examples",
            "load",
            "data",
        ),
        save_flag=False,
    )
