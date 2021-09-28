from relsad.post_process.plot.monte_carlo import monte_carlo_menu
from relsad.post_process.plot.iteration import iteration_menu


def plot_menu(path: str, file_type: str):
    # Making menu
    menu = """Menu:
0: Exit
1: Monte Carlo
2: Iteration
Enter choice:\n"""
    choice = int(input(menu))
    while choice != 0:
        if choice == 1:
            monte_carlo_menu(path, file_type)
        if choice == 2:
            iteration_menu(path, file_type)
        choice = int(input(menu))
