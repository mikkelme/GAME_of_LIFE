import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches



class GAME_of_LIFE:
    def __init__(self, dim):
        self.dim = dim
        self.cells = np.zeros((dim), dtype = int)
        self.cells_new = np.zeros((dim), dtype = int)
        self.b_wrap_x = [-1, 0, 1, 2, 3, 4, 0]
        self.b_wrap_y = [-1, 0, 1, 2, 3, 4, 0]


        # plot cells
        self.fig, self.ax = plt.subplots()
        self.plot()

        # Remove ticks
        self.ax.xaxis.set_ticklabels([])
        self.ax.yaxis.set_ticklabels([])
        self.ax.tick_params(left=False, bottom=False)

        # List for flipping cells
        self.flip = [1, 0]



    def coordinate_to_index(self, x, y,  extent):
        # Cell info
        x_cell_length = (extent[1]-extent[0])/dim[0]
        x_centers = extent[0] + np.arange(dim[0]) * x_cell_length + x_cell_length/2
        y_cell_length = (extent[2]-extent[3])/dim[1]
        y_centers = extent[3] + np.arange(dim[1]) * y_cell_length + y_cell_length/2

        # Cell indexes
        ix = np.argmin(abs(x_centers - x))
        iy = np.argmin(abs(y_centers - y))

        return iy, ix # switched around to match imshow


    def pick_cell(self, event):
        if event.inaxes == self.ax:
            # Retrieve extent
            extent = self.ax.get_xlim() +  self.ax.get_ylim()  #floats (left, right, bottom, top)

            # Get cordinate and index
            x, y = event.xdata, event.ydata

            x = float(x); y = float(y)
            ix, iy = self.coordinate_to_index(x, y, extent)

            # Flip cell
            self.cells[ix,iy] = self.flip[self.cells[ix,iy]]

            # Redraw
            self.plot()
            self.fig.canvas.draw()


    def plot(self):
        self.ax.imshow(self.cells, origin = "upper", extent = (0,1,0,1), cmap='Greys', vmin = 0, vmax = 1)


    def set_init(self):
        self.ax.grid(color='red', linestyle='-', linewidth=1)

        # Enable button_press_event
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.pick_cell)

        # Add start button
        button_ax = plt.axes([0.85, 0.02, 0.1, 0.075])
        start_button = Button(button_ax, 'Start',color='lightgrey', hovercolor='lightgreen')
        start_button.on_clicked(self.start)

        plt.show()


    def start(self, botton_axes):
        self.fig.canvas.mpl_disconnect(self.cid)
        # print("start", botton_axes)
        self.advance()


    def get_neighbour_sum(i,j):
            self.b_wrap_x = [0, 1, 2, 3, 4, 0]
            self.b_wrap_y = [0, 1, 2, 3, 4, 0]
            neighbour_sum = self.cells[b_wrap_x[i-1],b_wrap_y[j-1]] + \

            neighbour_sum = self.cells[self.b_wrap_x[i-1],self.b_wrap_y[j-1]] + \
                            self.cells[self.b_wrap_x[i-1],self.b_wrap_y[j]  ] + \
                            self.cells[self.b_wrap_x[i-1],self.b_wrap_y[j+1]] + \
                            self.cells[self.b_wrap_x[i],  self.b_wrap_y[j-1]] + \
                            self.cells[self.b_wrap_x[i],  self.b_wrap_y[j+1]] + \
                            self.cells[self.b_wrap_x[i+1],self.b_wrap_y[j-1]] + \
                            self.cells[self.b_wrap_x[i+1],self.b_wrap_y[j]  ] + \
                            self.cells[self.b_wrap_x[i+1],self.b_wrap_y[j+1]]

    def advance(self):

        for i in range(dim[0]):
            for j in range(dim[1]):

                pass


        # flip1 = np.argwhere(self.cells == 1)
        # print(flip1)
        # Rule 1
        # flip1 = np.argwhere(self.cells[i,j] == 1 and    self.cells[i-1,j-1] +
        #                                                 self.cells[i-1,j]   +
        #                                                 self.cells[i-1,j+1] +
        #                                                 self.cells[i,j-1]   +
        #                                                 self.cells[i,j]     +
        #                                                 self.cells[i,j+1]   +
        #                                                 self.cells[i+1,j-1] +
        #                                                 self.cells[i+1,j]   +
        #                                                 self.cells[i+1,j+1] < 2)









if __name__ == "__main__":
    dim = (5,5)

    game = GAME_of_LIFE(dim)
    game.set_init()

    exit()
