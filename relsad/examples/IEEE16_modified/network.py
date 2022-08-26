from relsad.network.components import (
    Battery,
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
    ManualMainController,
    MicrogridMode,
    Production,
)
from relsad.network.systems import (
    Distribution,
    Microgrid,
    PowerSystem,
    Transmission,
)
from relsad.StatDist import NormalParameters, StatDist, StatDistType
from relsad.Table import Table
from relsad.Time import Time, TimeUnit
from relsad.visualization.plotting import plot_topology


def initialize_network(
    fail_rate_trafo: float = 0.007,
    fail_rate_line: float = 0.7,
    microgrid_mode: MicrogridMode = MicrogridMode.SURVIVAL,
    line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
):

    C1 = ManualMainController(
        name="C1",
        sectioning_time=Time(1, TimeUnit.HOUR),
    )

    ps = PowerSystem(C1)

    B1 = Bus(
        name="B1",
        coordinate=[0, 0],
        fail_rate_per_year=0,
    )

    B2 = Bus(
        name="B2",
        coordinate=[1, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B3 = Bus(
        name="B3",
        coordinate=[2, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B4 = Bus(
        name="B4",
        coordinate=[3, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B5 = Bus(
        name="B5",
        coordinate=[4, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B6 = Bus(
        name="B6",
        coordinate=[5, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B7 = Bus(
        name="B7",
        coordinate=[6, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B8 = Bus(
        name="B8",
        coordinate=[7, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B9 = Bus(
        name="B9",
        coordinate=[8, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B10 = Bus(
        name="B10",
        coordinate=[9, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B11 = Bus(
        name="B11",
        coordinate=[10, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B12 = Bus(
        name="B12",
        coordinate=[11, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B13 = Bus(
        name="B13",
        coordinate=[12, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B14 = Bus(
        name="B14",
        coordinate=[13, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B15 = Bus(
        name="B15",
        coordinate=[14, 0],
        fail_rate_per_year=fail_rate_trafo,
    )
    B16 = Bus(
        name="B16",
        coordinate=[15, 0],
        fail_rate_per_year=fail_rate_trafo,
    )

    # Microgrid:
    BM1 = Bus(
        name="BM1",
        coordinate=[13, 1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    BM2 = Bus(
        name="BM2",
        coordinate=[14, 1.5],
        fail_rate_per_year=fail_rate_trafo,
    )
    BM3 = Bus(
        name="BM3",
        coordinate=[14, 2],
        fail_rate_per_year=fail_rate_trafo,
    )
    BM4 = Bus(
        name="BM4",
        coordinate=[14, 1],
        fail_rate_per_year=fail_rate_trafo,
    )

    Battery("Bat1", BM1)
    Production("P1", BM3)
    Production("P2", BM4)

    # Lines, connections and impedances
    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=0.0922,  # 0.3660,
        x=0.0470,  # 0.1864,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=0.0922,  # 0.3811,
        x=0.0470,  # 0.1941,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B3,
        tbus=B4,
        r=0.0922,
        x=0.0470,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=0.0493,
        x=0.0251,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B5,
        tbus=B6,
        r=0.1872,  # 0.8190,
        x=0.0619,  # 0.2707,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L6 = Line(
        name="L6",
        fbus=B6,
        tbus=B7,
        r=0.1872,
        x=0.0619,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L7 = Line(
        name="L7",
        fbus=B7,
        tbus=B8,
        r=0.1872,  # 0.7114,
        x=0.0619,  # 0.2351,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L8 = Line(
        name="L8",
        fbus=B8,
        tbus=B9,
        r=0.1872,  # 1.0300,
        x=0.0619,  # 0.3400,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L9 = Line(
        name="L9",
        fbus=B9,
        tbus=B10,
        r=0.1872,  # 1.0440,
        x=0.0619,  # 0.3450,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L10 = Line(
        name="L10",
        fbus=B10,
        tbus=B11,
        r=0.1872,  # 1.0580,
        x=0.0619,  # 0.3496,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L11 = Line(
        name="L11",
        fbus=B11,
        tbus=B12,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L12 = Line(
        name="L12",
        fbus=B12,
        tbus=B13,
        r=0.1872,  # 1.0300,
        x=0.0619,  # 0.3400,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L13 = Line(
        name="L13",
        fbus=B13,
        tbus=B14,
        r=0.1872,  # 1.0440,
        x=0.0619,  # 0.3450,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L14 = Line(
        name="L14",
        fbus=B14,
        tbus=B15,
        r=0.1872,  # 1.0580,
        x=0.0619,  # 0.3496,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L15 = Line(
        name="L15",
        fbus=B15,
        tbus=B16,
        r=0.1966,
        x=0.0650,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )

    # Microgrid

    ML1 = Line(
        name="ML1",
        fbus=B13,
        tbus=BM1,
        r=0.1872,  # 0.7394,
        x=0.0619,  # 0.2444,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )

    ML2 = Line(
        name="ML2",
        fbus=BM1,
        tbus=BM2,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    ML3 = Line(
        name="ML3",
        fbus=BM1,
        tbus=BM3,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    ML4 = Line(
        name="ML4",
        fbus=BM1,
        tbus=BM4,
        r=0.0047,
        x=0.0016,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )

    CircuitBreaker(name="E1", line=L1)
    CircuitBreaker(name="E2", line=ML1)

    Disconnector(name="L1a", line=L1, bus=B1)
    Disconnector(name="L1b", line=L1, bus=B2)
    Disconnector(name="L2a", line=L2, bus=B2)
    Disconnector(name="L2b", line=L2, bus=B3)
    Disconnector(name="L3a", line=L3, bus=B3)
    Disconnector(name="L3b", line=L3, bus=B4)
    Disconnector(name="L4a", line=L4, bus=B4)
    Disconnector(name="L4b", line=L4, bus=B5)
    Disconnector(name="L5a", line=L5, bus=B5)
    Disconnector(name="L5b", line=L5, bus=B6)
    Disconnector(name="L6a", line=L6, bus=B6)
    Disconnector(name="L6b", line=L6, bus=B7)
    Disconnector(name="L7a", line=L7, bus=B7)
    Disconnector(name="L7b", line=L7, bus=B8)
    Disconnector(name="L8a", line=L8, bus=B8)
    Disconnector(name="L8b", line=L8, bus=B9)
    Disconnector(name="L9a", line=L9, bus=B9)
    Disconnector(name="L9b", line=L9, bus=B10)
    Disconnector(name="L10a", line=L10, bus=B10)
    Disconnector(name="L10b", line=L10, bus=B11)
    Disconnector(name="L11a", line=L11, bus=B11)
    Disconnector(name="L11b", line=L11, bus=B12)
    Disconnector(name="L12a", line=L12, bus=B12)
    Disconnector(name="L12b", line=L12, bus=B13)
    Disconnector(name="L13a", line=L13, bus=B13)
    Disconnector(name="L13b", line=L13, bus=B14)
    Disconnector(name="L14a", line=L14, bus=B14)
    Disconnector(name="L14b", line=L14, bus=B15)
    Disconnector(name="L15a", line=L15, bus=B15)
    Disconnector(name="L15b", line=L15, bus=B16)

    # Microgrid:

    Disconnector(name="ML1a", line=ML1, bus=B13)
    Disconnector(name="ML1b", line=ML1, bus=BM1)
    Disconnector(name="ML2a", line=ML2, bus=BM1)
    Disconnector(name="ML2b", line=ML2, bus=BM2)
    Disconnector(name="ML3a", line=ML3, bus=BM1)
    Disconnector(name="ML3b", line=ML3, bus=BM3)
    Disconnector(name="ML4a", line=ML4, bus=BM1)
    Disconnector(name="ML4b", line=ML4, bus=BM4)

    tn = Transmission(ps, B1)

    dn = Distribution(tn, L1)

    dn.add_buses(
        [
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

    m = Microgrid(dn, ML1, mode=microgrid_mode)
    m.add_buses([BM1, BM2, BM3, BM4])
    m.add_lines([ML2, ML3, ML4])

    return ps


if __name__ == "__main__":
    import os

    ps = initialize_network()
    fig = plot_topology(ps.buses, ps.lines)

    fig.savefig(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "IEEE16_modified.pdf"
        )
    )
