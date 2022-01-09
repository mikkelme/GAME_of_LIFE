import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import time



class GAME_of_LIFE:
    def __init__(self, dim):
        self.dim = dim
        self.length = np.array([0.0,0.0])
        self.length[np.argmax(dim)] = 1
        self.length[np.argmin(self.length)] = dim[np.argmin(dim)]/dim[np.argmax(dim)]


        self.cells = np.zeros((dim), dtype = int)
        self.cells_new = np.zeros((dim), dtype = int)
        self.b_wrap_x = [dim[0]-1] + [k for k in range(dim[0])] + [0]
        self.b_wrap_y = [dim[1]-1] + [k for k in range(dim[1])] + [0]

        # plot cells
        self.fig, self.ax = plt.subplots()
        self.plot()


        self.ax.set_xticks(np.linspace(0,self.length[1],dim[1]+1), minor=False)
        self.ax.set_xticks(np.linspace(0,self.length[1],dim[1]+1), minor=True)
        self.ax.xaxis.grid(True, which='major')
        self.ax.xaxis.grid(True, which='minor')

        self.ax.set_yticks(np.linspace(0,self.length[0],dim[0]+1), minor=False)
        self.ax.set_yticks(np.linspace(0,self.length[0],dim[0]+1), minor=True)
        self.ax.yaxis.grid(True, which='major')
        self.ax.yaxis.grid(True, which='minor')


        # Remove ticks
        self.ax.xaxis.set_ticklabels([])
        self.ax.yaxis.set_ticklabels([])
        self.ax.tick_params(left=False, bottom=False)

        # List for flipping cells
        self.flip = [1, 0]


        # Extra things
        self.generation = 0
        self.running = False
        self.pause = 0.05


    def coordinate_to_index(self, x, y,  extent):
        # Cell info
        x_cell_length = self.length[1]/dim[1]
        y_cell_length = self.length[0]/dim[0]
        x_centers = 0 + np.arange(dim[1]) * x_cell_length + x_cell_length/2
        y_centers = np.arange(dim[0])[::-1] * y_cell_length + y_cell_length/2

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
            # print(self.cells)

            # Redraw
            self.plot()
            self.fig.canvas.draw()




    def plot(self):
        self.ax.imshow(self.cells, origin = "upper", extent = (0,self.length[1],0,self.length[0]), cmap='Greys', vmin = 0, vmax = 1)


    def set_init(self):
        # Enable button_press_event
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.pick_cell)


        # Add start/stop button
        self.start_stop_ax = plt.axes([0.85, 0.02, 0.1, 0.075])
        self.start_stop = Button(self.start_stop_ax, 'Start',color='lightgrey', hovercolor='lightgreen')
        self.start_stop.on_clicked(self.run)

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

        # Add random button
        random_ax = plt.axes([0.225, 0.02, 0.1, 0.075])
        random_button = Button(random_ax, 'Random',color='lightgrey', hovercolor='lightgreen')
        random_button.on_clicked(self.random)
        self.random_pct = 20

        random_input_ax = plt.axes([0.35, 0.02, 0.05, 0.075])
        text_box = TextBox(random_input_ax, '', initial=str(self.random_pct))
        text_box.on_submit(self.random_input)

        text_box.label = random_input_ax.text(
            1.5, 0.5, '%',
            verticalalignment='center',
            horizontalalignment='center',
            transform=random_input_ax.transAxes)


        plt.show()


    def random_input(self, text):
        try:
            self.random_pct = eval(text)
        except:
            print("Please insert number between 0-100")
        if self.random_pct < 0:
            self.random_pct = 0
        elif self.random_pct > 100:
            self.random_pct = 100

        print(f"Random generator set to {self.random_pct} %")


    def random(self, botton_axes):
        RN = np.random.rand(dim[0],dim[1])
        self.cells = np.where(RN < self.random_pct/100, 1, 0)
        self.plot()
        self.fig.canvas.draw()



    def reset(self, botton_axes):
        self.cells = np.zeros((dim), dtype = int)
        self.plot()
        self.generation = 0
        self.ax.set_title("")
        self.fig.canvas.draw()



    def stop(self, botton_axes):
        exit()

    def run(self, botton_axes):

        if not self.running: # Start
            self.start_stop.label.set_visible(False)
            self.start_stop.stop_label.set_visible(True)
            self.fig.canvas.mpl_disconnect(self.cid)
            self.running = True

            while self.running:
                self.advance()
                plt.pause(self.pause)



        elif self.running: # Stop
            self.start_stop.stop_label.set_visible(False)
            self.start_stop.label.set_visible(True)
            self.cid = self.fig.canvas.mpl_connect('button_press_event', self.pick_cell)
            self.running = False



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
        self.generation += 1
        self.ax.set_title(f"Generation: {self.generation}")
        self.fig.canvas.draw()








if __name__ == "__main__":
    dim = (15,15)

    game = GAME_of_LIFE(dim)
    game.set_init()
