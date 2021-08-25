import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))


def calc_convergence(array):
    return [np.mean(array[:i]) for i in range(len(array))]


data_P_shed = pd.read_csv(
    os.path.join("acc_p_load_shed.csv"), header=None, skiprows=1
)
data_SAIFI = pd.read_csv(os.path.join("SAIFI.csv"), header=None, skiprows=1)
data_SAIDI = pd.read_csv(os.path.join("SAIDI.csv"), header=None, skiprows=1)
data_CAIDI = pd.read_csv(os.path.join("CAIDI.csv"), header=None, skiprows=1)


P_shed = data_P_shed[1].values
SAIFI_value = data_SAIFI[1].values
SAIDI_value = data_SAIDI[1].values
CAIDI_value = data_CAIDI[1].values


# Calculate mean variable:

mean_P_shed = np.mean(P_shed)
print("P_shed", mean_P_shed)
mean_SAIFI = np.mean(SAIFI_value)
print("SAIFI", mean_SAIFI)
mean_SAIDI = np.mean(SAIDI_value)
print("SAIDI", mean_SAIDI)
mean_CAIDI = np.mean(CAIDI_value)
print("CAIDI", mean_CAIDI)


fig1, ax1 = plt.subplots()
ax1.plot(calc_convergence(P_shed), label="Shedded load")
ax1.legend()

fig2, ax2 = plt.subplots()
ax2.plot(calc_convergence(SAIFI_value), label="SAIFI")
ax2.legend()

fig3, ax3 = plt.subplots()
ax3.plot(calc_convergence(SAIDI_value), label="SAIDI")
ax3.legend()

fig4, ax4 = plt.subplots()
ax4.plot(calc_convergence(CAIDI_value), label="CAIDI")
ax4.legend()


plt.show()
