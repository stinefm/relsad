from stinetwork.network.components import (
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
)
from stinetwork.network.systems import Distribution, PowerSystem, Transmission
from stinetwork.visualization.plotting import plot_topology


def initialize_network():
    ps = PowerSystem()
    fail_rate_trafo = 0.007  # 0.008
    fail_rate_line = 0.07  # 0.08

    B0 = Bus("B0", coordinate=[0, 0], failure_rate_per_year=0)

    B1 = Bus("B1", coordinate=[-1, -1], fail_rate_per_year=fail_rate_trafo)
    B2 = Bus("B2", coordinate=[0, -1], fail_rate_per_year=fail_rate_trafo)
    B3 = Bus("B3", coordinate=[1, -1], fail_rate_per_year=fail_rate_trafo)

    B4 = Bus("B4", coordinate=[-1, -2], fail_rate_per_year=fail_rate_trafo)
    B5 = Bus("B5", coordinate=[-0.5, -3], fail_rate_per_year=fail_rate_trafo)
    B6 = Bus("B6", coordinate=[-1, -3], fail_rate_per_year=fail_rate_trafo)
    B7 = Bus("B7", coordinate=[-1, -4], fail_rate_per_year=fail_rate_trafo)

    B8 = Bus("B8", coordinate=[0, -2], fail_rate_per_year=fail_rate_trafo)
    B9 = Bus("B9", coordinate=[0, -3], fail_rate_per_year=fail_rate_trafo)
    B10 = Bus("B10", coordinate=[0.5, -4], fail_rate_per_year=fail_rate_trafo)
    B11 = Bus("B11", coordinate=[-0.5, -3], fail_rate_per_year=fail_rate_trafo)
    B12 = Bus("B12", coordinate=[0, -4], fail_rate_per_year=fail_rate_trafo)

    B13 = Bus("B13", coordinate=[1, -2], fail_rate_per_year=fail_rate_trafo)
    B14 = Bus("B14", coordinate=[0.5, -3], fail_rate_per_year=fail_rate_trafo)
    B15 = Bus("B15", coordinate=[1, -3], fail_rate_per_year=fail_rate_trafo)
    B16 = Bus("B16", coordinate=[1, -4], fail_rate_per_year=fail_rate_trafo)

    # L01 = Line(
    #     "L01",
    #     B0,
    #     B1,
    #     r=0.057526629463617,
    #     x=0.029324854498807,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    # L02 = Line(
    #     "L02",
    #     B0,
    #     B2,
    #     r=0.057526629463617,
    #     x=0.029324854498807,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    # L03 = Line(
    #     "L03",
    #     B0,
    #     B3,
    #     r=0.057526629463617,
    #     x=0.029324854498807,
    #     fail_rate_density_per_year=fail_rate_line,
    # )
    L1 = Line(
        "L2",
        B1,
        B4,
        r=0.307599005700253,
        x=0.156669594992563,
        fail_rate_density_per_year=fail_rate_line,
    )
    L2 = Line(
        "L2",
        B2,
        B8,
        r=0.307599005700253,
        x=0.156669594992563,
        fail_rate_density_per_year=fail_rate_line,
    )
    L3 = Line(
        "L3",
        B3,
        B13,
        r=0.228359505246029,
        x=0.11630112507612,
        fail_rate_density_per_year=fail_rate_line,
    )
    L4 = Line(
        "L4",
        B4,
        B5,
        r=0.237780894670114,
        x=0.121105409749329,
        fail_rate_density_per_year=fail_rate_line,
    )
    L5 = Line(
        "L5",
        B4,
        B6,
        r=0.511001187968574,
        x=0.441120683630991,
        fail_rate_density_per_year=fail_rate_line,
    )
    L6 = Line(
        "L6",
        B6,
        B7,
        r=0.116800271535674,
        x=0.386089786465145,
        fail_rate_density_per_year=fail_rate_line,
    )
    L7 = Line(
        "L7",
        B8,
        B9,
        r=1.06779906360124,
        x=0.770619740244183,
        fail_rate_density_per_year=fail_rate_line,
    )
    L8 = Line(
        "L8",
        B9,
        B11,
        r=0.642651066675984,
        x=0.4617104750876,
        fail_rate_density_per_year=fail_rate_line,
    )
    L9 = Line(
        "L9",
        B9,
        B12,
        r=0.651386129718182,
        x=0.4617104750876,
        fail_rate_density_per_year=fail_rate_line,
    )
    L10 = Line(
        "L10",
        B13,
        B14,
        r=0.122665242435435,
        x=0.040555649838776,
        fail_rate_density_per_year=fail_rate_line,
    )
    L11 = Line(
        "L11",
        B13,
        B15,
        r=0.233600543071348,
        x=0.077242914616007,
        fail_rate_density_per_year=fail_rate_line,
    )
    L12 = Line(
        "L12",
        B15,
        B16,
        r=0.915933753281888,
        x=0.720642700981322,
        fail_rate_density_per_year=fail_rate_line,
    )

    L13 = Line(
        "L13",
        B5,
        B11,
        r=0.337922153118168,
        x=0.444801888770203,
        fail_rate_density_per_year=fail_rate_line,
    )
    L14 = Line(
        "L14",
        B7,
        B16,
        r=0.368744446995637,
        x=0.328188797156862,
        fail_rate_density_per_year=fail_rate_line,
    )
    L15 = Line(
        "L15",
        B10,
        B14,
        r=0.465641253456589,
        x=0.340043525571273,
        fail_rate_density_per_year=fail_rate_line,
    )

    E1 = CircuitBreaker("E1", L1)

    Disconnector("L1a", L1, B1, E1)
    Disconnector("L1b", L1, B2, E1)
    Disconnector("L1c", L1, B2)
    Disconnector("L2a", L2, B2)
    Disconnector("L2b", L2, B3)
    Disconnector("L3a", L3, B3)
    Disconnector("L3b", L3, B4)
    Disconnector("L4a", L4, B4)
    Disconnector("L4b", L4, B5)
    Disconnector("L5a", L5, B5)
    Disconnector("L5b", L5, B6)
    Disconnector("L6a", L6, B6)
    Disconnector("L6b", L6, B7)
    Disconnector("L7a", L7, B7)
    Disconnector("L7b", L7, B8)
    Disconnector("L8a", L8, B8)
    Disconnector("L8b", L8, B9)
    Disconnector("L9a", L9, B9)
    Disconnector("L9b", L9, B10)
    Disconnector("L10a", L10, B10)
    Disconnector("L10b", L10, B11)
    Disconnector("L11a", L11, B11)
    Disconnector("L11b", L11, B12)
    Disconnector("L12a", L12, B12)
    Disconnector("L12b", L12, B13)
    Disconnector("L13a", L13, B13)
    Disconnector("L13b", L13, B14)
    Disconnector("L14a", L14, B14)
    Disconnector("L14b", L14, B15)
    Disconnector("L15a", L15, B15)
    Disconnector("L15b", L15, B16)

    tn = Transmission(ps, B0)

    dn = Distribution(tn, L1)

    dn.add_buses(
        [
            B1,
            B2,
            B3,
            B4,
            B5,
            B6,
            B7,
            B8,
            B9,
            B10,
            B11,
            B12,
            B13,
            B14,
            B15,
            B16,
        ]
    )

    dn.add_lines(
        [
            L1,
            L2,
            L3,
            L4,
            L5,
            L6,
            L7,
            L8,
            L9,
            L10,
            L11,
            L12,
            L13,
            L14,
            L15,
        ]
    )

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines, figsize=(40, 40))

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "IEEE33_testnetwork.pdf",
        )
    )
