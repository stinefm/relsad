import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from relsad.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    IntelligentSwitch,
    Sensor,
)
import os


def plot_topology(
    buses: list,
    lines: list,
    bus_text: bool=True,
    line_text: bool=False,
    circuitbreaker_text: bool=False,
    disconnector_text: bool=False,
    intelligent_switch_text: bool=False,
    sensor_text: bool=False,
    **kwargs):

    """
    Plots the system topology 

    Parameters
    ----------
    buses : list 
        List with Bus elements in the system
    lines : list 
        List with Line elements in the system
    bus_text : bool
        Flag determining if bus name will be plotted
    line_text : bool
        Flag determining if line name will be plotted
    circuitbreaker_text : bool
        Flag determining if circuitbreaker name will be plotted
    disconnector_text : bool
        Flag determining if disconnector name will be plotted
    intelligent_switch_text : bool
        Flag determining if intelligent switch name will be plotted
    sensor_text : bool
        Flag determining if sensor name will be plotted
    **kwargs : dict
        Plotting keyword arguments.

    Returns
    ----------
    fig : figure
        Figure of the system topology 
    None

    """

    fig, ax = plt.subplots(**kwargs)
    left = 0.02
    right = 0.98
    bottom = 0.1
    top = 0.75

    text_size = 6

    fig.subplots_adjust(
        left=left, bottom=bottom, right=right, top=top, wspace=None, hspace=None
    )
    legends = {}
    for bus in buses:
        _plot_bus(ax, bus, text=bus_text, text_size=text_size)
        legends["Bus"] = Bus.handle
    for line in lines:
        _plot_line(ax, line, text=line_text, text_size=text_size)
        legends["Line"] = Line.handle
        if line.circuitbreaker is not None:
            _plot_circuitbreaker(ax, line, text=circuitbreaker_text, text_size=text_size)
            legends["Circuit breaker"] = CircuitBreaker.handle
            for discon in line.circuitbreaker.disconnectors:
                _plot_disconnector(ax, discon, text=disconnector_text, text_size=text_size)
                legends["Disconnector"] = Disconnector.handle
                if discon.intelligent_switch:
                    _plot_intelligent_switch(ax, discon, text=intelligent_switch_text, text_size=text_size)
                legends["Intelligent switch"] = IntelligentSwitch.handle
        for discon in line.disconnectors:
            _plot_disconnector(ax, discon, text=disconnector_text, text_size=text_size)
            legends["Disconnector"] = Disconnector.handle
            if discon.intelligent_switch:
                _plot_intelligent_switch(ax, discon, text=intelligent_switch_text, text_size=text_size)
                legends["Intelligent switch"] = IntelligentSwitch.handle
        if line.sensor:
            _plot_sensor(ax, line, text=sensor_text, text_size=text_size)
            legends["Sensor"] = Sensor.handle

    plt.figlegend(
        legends.values(),
        legends.keys(),
        ncol=len(legends),
        loc="upper center",
        bbox_to_anchor=(left + (right - left) / 2, 0.978),
        frameon=False,
        prop={'size': 8},
    )

    plt.axis("off")

    return fig

def _plot_line(ax: plt.axis, line: Line, text: bool=False, text_size: int=8):
    """
    Plot lines 

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    line : Line
        A Line element
    text : bool
        Flag determining if line name will be plotted
    text_size : int 
        The size of the text in the plot 

    Returns
    ----------
    None

    """
    ax.plot(
        [line.fbus.coordinate[0], line.tbus.coordinate[0]],
        [line.fbus.coordinate[1], line.tbus.coordinate[1]],
        color=line.color,
        linestyle=line.linestyle,
        zorder=2,
    )
    if text:
        ax.text(
            (line.fbus.coordinate[0] + line.tbus.coordinate[0]) / 2,
            (line.fbus.coordinate[1] + line.tbus.coordinate[1]) / 2,
            line.name,
            ha="center",
            va="center",
            size=text_size,
        )

def _plot_circuitbreaker(ax: plt.axis, line: Line, text: bool=False, text_size: int=8):
    """
    Plot circuitbreakers

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    line : Line
        A Line element
    text : bool
        Flag determining if circuitbreaker name will be plotted
    text_size : int 
        The size of the text in the plot 

    Returns
    ----------
    None

    """
    cb = line.circuitbreaker
    ax.plot(
        cb.coordinate[0],
        cb.coordinate[1],
        marker=cb.marker,
        markeredgewidth=cb.handle.get_markeredgewidth(),
        markersize=cb.size,
        linestyle="None",
        color=cb.color,
        markeredgecolor=cb.edgecolor,
        zorder=3,
    )
    if text:
        ax.text(
            cb.coordinate[0],
            cb.coordinate[1] - 0.2,
            cb.name,
            ha="center",
            va="center",
            size=text_size,
        )

def _plot_disconnector(ax: plt.axis, discon: Disconnector, text: bool=False, text_size: int=8):
    """
    Plot disconnectors

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    discon : Disconnecotr
        A Disconnector elements
    text : bool
        Flag determining if disconnector name will be plotted
    text_size : int 
        The size of the text in the plot 

    Returns
    ----------
    None

    """
    ax.plot(
        discon.coordinate[0],
        discon.coordinate[1],
        marker=discon.marker,
        markeredgewidth=discon.handle.get_markeredgewidth(),
        markersize=discon.size,
        linestyle="None",
        color=discon.color,
        markeredgecolor=discon.edgecolor,
        zorder=3,
    )
    if text:
        ax.text(
            discon.coordinate[0],
            discon.coordinate[1] - 0.2,
            discon.name,
            ha="center",
            va="center",
            size=text_size,
        )

def _plot_intelligent_switch(ax: plt.axis, discon: Disconnector, text: bool=False, text_size: int=8):
    """
    Plot intelligent switches 

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    discon : Disconnector
        A Disconnector elements
    text : bool
        Flag determining if intelligent switch name will be plotted
    text_size : int 
        The size of the text on the plot 

    Returns
    ----------
    None

    """
    ax.plot(
        discon.coordinate[0],
        discon.coordinate[1],
        marker=discon.intelligent_switch.marker,
        markeredgewidth=discon.intelligent_switch.handle.get_markeredgewidth(),
        markersize=discon.intelligent_switch.size,
        linestyle="None",
        color=discon.intelligent_switch.color,
        zorder=3,
    )
    if text:
        ax.text(
            discon.coordinate[0],
            discon.coordinate[1] - 0.2,
            discon.intelligent_switch.name,
            ha="center",
            va="center",
            size=text_size,
        )

def _plot_sensor(ax: plt.axis, line: Line, text: bool=False, text_size: int=8):
    """
    Plot sensors

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    line : Line
        A Line element
    text : bool
        Flag determining if sensor name will be plotted
    text_size : int 
        The size of the text in the plot 

    Returns
    ----------
    None

    """
    ax.plot(
        (line.fbus.coordinate[0] + line.tbus.coordinate[0]) / 2,
        (line.fbus.coordinate[1] + line.tbus.coordinate[1]) / 2,
        marker=line.sensor.marker,
        markeredgewidth=line.sensor.handle.get_markeredgewidth(),
        markersize=line.sensor.size,
        linestyle="None",
        color=line.sensor.color,
        zorder=3,
    )
    if text:
        ax.text(
            (line.fbus.coordinate[0] + line.tbus.coordinate[0]) / 2,
            (line.fbus.coordinate[1] + line.tbus.coordinate[1]) / 2 - 0.2,
            line.sensor.name,
            ha="center",
            va="center",
            size=text_size,
        )

def _plot_bus(ax: plt.axis, bus: list, text: bool=False, text_size: int=8):
    """
    Plot circuitbreakers

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot axis
    bus : list
        List of Bus elements
    text : bool
        Flag determining if bus name will be plotted
    text_size : int 
        The size of the text in the plot 

    Returns
    ----------
    None

    """
    ax.plot(
        bus.coordinate[0],
        bus.coordinate[1],
        marker=bus.marker,
        markeredgewidth=bus.handle.get_markeredgewidth(),
        markersize=bus.size,
        linestyle="None",
        color=bus.color,
        clip_on=False,
        zorder=3,
    )
    if text:
        ax.text(
            bus.coordinate[0],
            bus.coordinate[1] - 0.3,
            bus.name,
            ha="center",
            va="center",
            size=text_size,
        )


def plot_history(comp_list: list, attribute: str, save_dir: str):
    """
    Plots the history 

    Parameters
    ----------
    comp_list : list 
        List of components
    attribute : str
        An attribute 
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    for comp in comp_list:
        data = comp.get_history(attribute)
        ax.plot(list(data.values()), label=comp.name)
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


def plot_monte_carlo_history(comp_list: list, attribute: str, save_dir: str):
    """
    Plots the history from the Monte Carlo simulation

    Parameters
    ----------
    comp_list : list 
        List of components
    attribute : str
        An attribute 
    save_dir : str
        The saving directory

    Returns
    ----------
    None


    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    for comp in comp_list:
        data = comp.get_monte_carlo_history(attribute)
        ax.plot(list(data.values()), label=comp.name)
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


def plot_history_last_state(comp_list: list, attribute: str, save_dir: str):
    """
    Plots the last state from the history 

    Parameters
    ----------
    comp_list : list 
        List of components
    attribute : str
        An attribute 
    save_dir : str
        The saving directory

    Returns
    ----------
    None


    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    df = pd.DataFrame()
    for comp in comp_list:
        data = comp.get_history(attribute)
        df[comp] = data.values()
    df.iloc[-1].plot.bar()
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


if __name__ == "__main__":
    pass
