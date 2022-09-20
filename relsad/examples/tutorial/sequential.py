from relsad.examples.tutorial.system import *

from relsad.simulation import Simulation


def callback(ps, prev_time, curr_time):
    dt = curr_time - prev_time
    if curr_time <= dt:
        ps.get_comp("L2").fail(dt=dt)
        ps.get_comp("L6").fail(dt=dt)
    elif Time(1.95, unit=dt.unit) < curr_time < Time(2.05, unit=dt.unit):
        ps.get_comp("L3").fail(dt=dt)


sim = Simulation(power_system=ps, random_seed=0)
sim.run_sequential(
    start_time=TimeStamp(
        year=2019,
        month=0,
        day=0,
        hour=0,
        minute=0,
        second=0,
    ),
    stop_time=TimeStamp(
        year=2019,
        month=0,
        day=0,
        hour=10,
        minute=0,
        second=0,
    ),
    time_step=Time(0.1, TimeUnit.HOUR),
    time_unit=TimeUnit.HOUR,
    callback=callback,
    save_dir="results",
)

path = os.path.join(
    "results",
    "sequence",
    "ps1",
    "ENS.csv",
)

df = pd.read_csv(path)
fig, ax = plt.subplots()
df.plot(
    x="HOUR",
    y="ps1",
    ax=ax,
)

fig.savefig(
    "ENS.png",
    dpi=600,
)

print(df.describe())

import shutil

shutil.rmtree("results")
os.remove("ENS.png")
