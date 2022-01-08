import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
import time



class GAME_of_LIFE:
    def __init__(self, dim):
        self.dim = dim
        self.cells = np.zeros((dim), dtype = int)
        self.cells_new = np.zeros((dim), dtype = int)
        self.b_wrap_x = [dim[0]-1] + [k for k in range(dim[0])] + [0]
        self.b_wrap_y = [dim[1]-1] + [k for k in range(dim[1])] + [0]


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

    def plot_new(self):
        self.ax.imshow(self.cells_new, origin = "upper", extent = (0,1,0,1), cmap='Greys', vmin = 0, vmax = 1)



    def set_init(self):
        self.ax.grid(color='red', linestyle='-', linewidth=1)

        # Enable button_press_event
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.pick_cell)


        # Add start/stop button
        self.start_stop_ax = plt.axes([0.85, 0.02, 0.1, 0.075])
        self.start_stop = Button(self.start_stop_ax, 'Start',color='lightgrey', hovercolor='lightgreen')
        self.start_stop.on_clicked(self.start)

        self.start_stop.stop_label = self.start_stop_ax.text(
            0.5, 0.5, 'Stop',
            verticalalignment='center',
            horizontalalignment='center',
            transform=self.start_stop_ax.transAxes)
        self.start_stop.stop_label.set_visible(False)


        # Add advance button
        advance_ax = plt.axes([0.85, 0.1, 0.1, 0.075])
        advance_button = Button(advance_ax, 'Advance',color='lightgrey', hovercolor='lightgreen')
        advance_button.on_clicked(self.advance)

        # Add reset button
        reset_ax = plt.axes([0.85, 0.18, 0.1, 0.075])
        reset_button = Button(reset_ax, 'Reset',color='lightgrey', hovercolor='lightgreen')
        reset_button.on_clicked(self.reset)




        plt.show()

    def reset(self, botton_axes):
        self.cells = np.zeros((dim), dtype = int)
        self.plot()
        self.fig.canvas.draw()



    def stop(self, botton_axes):
        exit()

    def start(self, botton_axes):
        self.round = 0
        runtime = 10
        print("start button hit")
        self.fig.canvas.mpl_disconnect(self.cid)




        self.start_stop.label.set_visible(False)
        self.start_stop.stop_label.set_visible(True)

        # self.start_button.disconnect(self.start_id)
        #
        # start_button = Button(self.start_ax, 'Stop',color='lightgrey', hovercolor='lightgreen')
        # start_button.on_clicked(self.stop)

        # # Add stop button
        # stop_ax = plt.axes([0.65, 0.02, 0.1, 0.075])
        # stop_button = Button(stop_ax, 'Stop',color='lightgrey', hovercolor='lightgreen')
        # stop_button.on_clicked(self.stop)


        while self.round <= runtime:
            self.advance()
            print(self.round)
            plt.pause(0.05)
            self.round += 1


    def get_neighbour_sum(self, i,j):
        i += 1
        j += 1

        neighbour_sum = self.cells[self.b_wrap_x[i-1],self.b_wrap_y[j-1]] + \
                        self.cells[self.b_wrap_x[i-1],self.b_wrap_y[j]  ] + \
                        self.cells[self.b_wrap_x[i-1],self.b_wrap_y[j+1]] + \
                        self.cells[self.b_wrap_x[i],  self.b_wrap_y[j-1]] + \
                        self.cells[self.b_wrap_x[i],  self.b_wrap_y[j+1]] + \
                        self.cells[self.b_wrap_x[i+1],self.b_wrap_y[j-1]] + \
                        self.cells[self.b_wrap_x[i+1],self.b_wrap_y[j]  ] + \
                        self.cells[self.b_wrap_x[i+1],self.b_wrap_y[j+1]]
        return neighbour_sum

    def advance(self, *args):
        # Copy old configuration
        self.cells_new[:,:] = self.cells[:,:]

        for i in range(dim[0]):
            for j in range(dim[1]):
                sum = self.get_neighbour_sum(i,j)


                if self.cells[i,j] == 1:
                    # Rule 1 (Underpopulation)
                    if sum < 2:
                        self.cells_new[i,j] = 0

                    # Rule 3 (Overpopulation)
                    if sum > 3:
                        self.cells_new[i,j] = 0

                # Rule 4 (resurrection)
                if self.cells[i,j] == 0 and sum == 3:
                    self.cells_new[i,j] = 1

        # Redraw
        self.cells[:,:] = self.cells_new[:,:]
        self.plot()
        self.fig.canvas.draw()











if __name__ == "__main__":
    dim = (5,5)

    game = GAME_of_LIFE(dim)
    game.set_init()

    exit()
