import matplotlib.pyplot as plt
import numpy as np
from stinetwork.network.components import Bus, Line, Disconnector, CircuitBreaker

def plot_topology(buses:list,lines:list,**kwargs):
    fig, ax = plt.subplots(**kwargs)#figsize=(3.5, 4.5))
    for line in lines:
        ax.plot([line.fbus.coordinate[0], line.tbus.coordinate[0]], \
        [line.fbus.coordinate[1], line.tbus.coordinate[1]], \
        color = line.color, linestyle=line.linestyle)

        if line.circuitbreaker != None:
            cb = line.circuitbreaker
            ax.plot(cb.coordinate[0], cb.coordinate[1], \
            marker = cb.marker, markeredgewidth=1, markersize=cb.size, linestyle = 'None', \
            color = cb.color, markeredgecolor=cb.edgecolor)
            ax.text(cb.coordinate[0]-0.2, cb.coordinate[1], cb.name, \
            ha='center', va='center')

            for discon in cb.disconnectors:
                ax.plot(discon.coordinate[0], discon.coordinate[1], \
                marker = discon.marker, markeredgewidth=1, markersize=discon.size, linestyle = 'None', \
                color = discon.color, markeredgecolor=discon.edgecolor)
                ax.text(discon.coordinate[0]-0.2, discon.coordinate[1], discon.name, \
                ha='center', va='center')

        for discon in line.disconnectors:
            ax.plot(discon.coordinate[0], discon.coordinate[1], \
            marker = discon.marker, markeredgewidth=1, markersize=discon.size, linestyle = 'None', \
            color = discon.color, markeredgecolor=discon.edgecolor)
            ax.text(discon.coordinate[0]-0.2, discon.coordinate[1], discon.name, \
            ha='center', va='center')

    for bus in buses:
        ax.plot(bus.coordinate[0], bus.coordinate[1], \
            marker = bus.marker, markeredgewidth=3, markersize=bus.size, linestyle = 'None', \
            color = bus.color, clip_on=False)
        ax.text(bus.coordinate[0], bus.coordinate[1], bus.name, \
            ha='center', va='center')

    right = 0.85
    left = 0.15

    fig.subplots_adjust(left=left, bottom=0, right=right, top=None, wspace=None, hspace=None)
    
    plt.figlegend([Line.handle, Bus.handle, CircuitBreaker.handle, Disconnector.handle], \
                ['Line', 'Bus', 'Circuitbreaker', 'Disconnector'], \
                ncol=3, loc='upper center',bbox_to_anchor=(left+(right-left)/2,0.978),\
                frameon=False)
    
    plt.axis('off')

    return fig

def tableplot(table_data, title, columns, rows, columncol=[], rowcol=[]):
    """
    Desc:   Make a table of the provided data. There must be a row and a column
            data correpsonding to the table
    Input:  table_data  - np.array
            title - string
            columns - string vector
            rows    - string vector
            columncol - colors of each column label (default [])
            rowcol - colors of each row lable
    """

    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)

    tdim = np.shape(table_data)
    iloop = 0
    if rowcol == []:
        while iloop < tdim[0]:
            rowcol.append('cyan')
            iloop += 1
    iloop = 0
    if columncol == []:
        while iloop < tdim[1]:
            columncol.append('cyan')
            iloop += 1

    table = ax.table(cellText=table_data, rowLabels=rows, colColours=columncol, rowColours=rowcol,
                        colLabels=columns, loc='center')
    table.set_fontsize(11)
    table.scale(1, 1.5)
    ax.set_title(title, fontsize=14)
    ax.axis('off')
    plt.show()

if __name__=="__main__":
    pass