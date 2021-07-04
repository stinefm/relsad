from stinetwork.post_process.plot.iteration.load_shed import (
    plot_histogram,
    plot_boxplot,
)


def load_shed_menu(path: str, file_type: str):
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
