import matplotlib.pyplot as plt

def plot(buses:list,lines:list):
        fig, ax = plt.subplots(figsize=(3.5, 4.5))
        for line in lines:
            lineHandle, = ax.plot([line.fbus.coordinate[0], line.tbus.coordinate[0]], \
            [line.fbus.coordinate[1], line.tbus.coordinate[1]], \
            color = 'steelblue')

        for bus in buses:
            busHandle, = ax.plot(bus.coordinate[0], bus.coordinate[1], \
                marker = 'o', markeredgewidth=3, markersize=25, linestyle = 'None', \
                color = 'steelblue')
            ax.text(bus.coordinate[0], bus.coordinate[1], bus.name, \
                ha='center', va='center')
    
        right = 0.85
        left = 0.15

        fig.subplots_adjust(left=left, bottom=0, right=right, top=None, wspace=None, hspace=None)
        
        plt.figlegend([lineHandle, busHandle], \
                    ['Line', 'Bus'], \
                    ncol=3, loc='upper center',bbox_to_anchor=(left+(right-left)/2,0.978),\
                    frameon=False)
        
        #plt.grid(True)


        plt.axis('off')

        # fig.savefig('/home/jonas/Downloads/Network.svg', dpi = 1000, format = 'svg')

        plt.show()

if __name__=="__main__":
    pass