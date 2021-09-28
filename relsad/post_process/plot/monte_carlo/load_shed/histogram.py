import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_histogram(path: str, file_type: str):
    save_path = os.path.join(path, "acc_p_load_shed.csv")
    df = pd.read_csv(save_path, index_col=0)
    df.plot.hist()
    plt.show()
