import os
from stinetwork.post_process.plot.monte_carlo.energy_not_supplied import (
    plot_histogram,
    plot_boxplot,
)


def energy_not_supplied_menu(path: str, file_type: str):
    # Making menu
    menu = """
0: Go to main menu
1: Histogram
2: Boxplot
Enter choice:\n"""
    choice = int(input(menu))
    while choice != 0:
        if choice == 1:
            plot_histogram(path, file_type)
        if choice == 2:
            plot_boxplot(path, file_type)
        choice = int(input(menu))
