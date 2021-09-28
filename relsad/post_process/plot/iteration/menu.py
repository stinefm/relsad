from relsad.post_process.plot.iteration import (
    load_shed_menu,
    outage_time_menu,
    energy_not_supplied_menu,
)


def iteration_menu(path: str, file_type: str):
    # Making menu
    menu = """Menu:
0: Exit
1: Load shed
2: Outage time
3: Energy not supplied
Enter choice:\n"""
    choice = int(input(menu))
    while choice != 0:
        if choice == 1:
            load_shed_menu(path, file_type)
        if choice == 2:
            outage_time_menu(path, file_type)
        if choice == 3:
            energy_not_supplied_menu(path, file_type)
        choice = int(input(menu))
