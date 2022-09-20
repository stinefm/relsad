from relsad.examples.tutorial.system import *

from relsad.simulation import Simulation

sim = Simulation(power_system=ps, random_seed=0)
sim.run_monte_carlo(
    iterations=10,
    start_time=TimeStamp(
        year=2019,
        month=0,
        day=0,
        hour=0,
        minute=0,
        second=0,
    ),
    stop_time=TimeStamp(
        year=2020,
        month=0,
        day=0,
        hour=0,
        minute=0,
        second=0,
    ),
    time_step=Time(1, TimeUnit.HOUR),
    time_unit=TimeUnit.HOUR,
    callback=None,
    save_iterations=[1, 2],
    save_dir="results",
    n_procs=1,
)

path = os.path.join(
    "results",
    "monte_carlo",
    "ps1",
    "ENS.csv",
)

df = pd.read_csv(path, index_col=0)
fig, ax = plt.subplots()
df.hist(ax=ax)

fig.savefig(
    "ENS.png",
    dpi=600,
)

print(df.describe())

import shutil

shutil.rmtree("results")
os.remove("ENS.png")
