import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, Slider
import time

class GAME_of_LIFE:
    def __init__(self, dim, random_pct = 20, valinit = 3):
        # Class input
        self.random_pct = random_pct
        self.valinit = valinit
        self.dim = dim

        # Cell matrices
        self.cells = np.zeros((dim), dtype = int)
        self.cells_new = np.zeros((dim), dtype = int)

        #--- Plot cells ---#
        # Find axis length
        self.length = np.array([0.0,0.0])
        self.length[np.argmax(dim)] = 1
        self.length[np.argmin(self.length)] = dim[np.argmin(dim)]/dim[np.argmax(dim)]

        # Initialize figure, axis and plotting image
        self.fig, self.ax = plt.subplots(figsize = (7,6))
        self.image = self.ax.imshow(self.cells, origin = "upper", extent = (0, self.length[1], 0, self.length[0]), cmap='Greys', vmin = 0, vmax = 1)
        self.title_y = 1.03
        self.ax.set_title("GAME OF LIFE", y = self.title_y)

        # Create grid
        self.ax.set_xticks(np.linspace(0,self.length[1],dim[1]+1), minor=False)
        self.ax.set_xticks(np.linspace(0,self.length[1],dim[1]+1), minor=True)
        self.ax.xaxis.grid(True, which='major')
        self.ax.xaxis.grid(True, which='minor')

        self.ax.set_yticks(np.linspace(0,self.length[0],dim[0]+1), minor=False)
        self.ax.set_yticks(np.linspace(0,self.length[0],dim[0]+1), minor=True)
        self.ax.yaxis.grid(True, which='major')
        self.ax.yaxis.grid(True, which='minor')

        # Remove axis ticks
        self.ax.xaxis.set_ticklabels([])
        self.ax.yaxis.set_ticklabels([])
        self.ax.tick_params(left=False, bottom=False)


        #--- Additional class content ---#
        # List for flipping cells
        self.flip = [1, 0]

        # Simulation settings
        self.generation = 0
        self.running = False
        self.pause_array = np.array([1, 0.5, 0.1, 0.05, 0.01])

        # Button layout
        self.std_button_length = 0.1
        self.std_button_height = 0.075
        self.axis_padding = 0.015
        self.spacer = 0.01

        # Boundary handling lists
        self.b_wrap_x = [dim[0]-1] + [k for k in range(dim[0])] + [0]
        self.b_wrap_y = [dim[1]-1] + [k for k in range(dim[1])] + [0]

        #--- Launch: create buttons and show figure ---#
        self.launch()


    def launch(self):

        #--- Adjust left-right-margins ---#

        # Get axis positions
        ax_pos = self.ax.get_position()._points

        # Adjust for right margin fit
        right_goal = 1 - 2*self.axis_padding - 1.5*self.std_button_length
        plt.subplots_adjust(left = 0, right = right_goal)

        # Correct missmatch with left margin
        ax_pos = self.ax.get_position()._points
        plt.subplots_adjust(left = max(self.axis_padding, 2*(right_goal-ax_pos[1,0])), right = right_goal)
        ax_pos = self.ax.get_position()._points

        # Update for final axis positions
        ax_pos = self.ax.get_position()._points


        #--- Add buttons ---#
        # Add random button
        random_ax = plt.axes([
            0.25*self.std_button_length + self.axis_padding,
            self.axis_padding,
            self.std_button_length,
            self.std_button_height ])
        self.random_button = Button(
            random_ax,
            'Random',
            color='lightgrey',
            hovercolor='lightgreen')

        # Add random symmetric button
        random_sumbit_length = 0.05
        sym_ax = plt.axes([
            random_ax.get_position()._points[1,0] + self.spacer,
            random_ax.get_position()._points[0,1],
            random_sumbit_length,
            self.std_button_height])
        self.sym_button = Button(
            sym_ax,
            'SYM',
            color='lightgrey',
            hovercolor='lightgreen')

        # Add sumbit textbox for random button
        random_input_ax = plt.axes([
            sym_ax.get_position()._points[1,0] + self.spacer,
            sym_ax.get_position()._points[0,1],
            random_sumbit_length,
            self.std_button_height])
        self.submit = TextBox(
            random_input_ax,
            '',
            initial=str(self.random_pct))
        self.submit.label = random_input_ax.text(
            1.3, 0.5, '%',
            verticalalignment='center',
            horizontalalignment='center',
            transform=random_input_ax.transAxes)

        # Create slider
        slider_ax = plt.axes([
            random_input_ax.get_position()._points[1,0] + random_sumbit_length,
            random_ax.get_position()._points[0,1],
            1 - random_input_ax.get_position()._points[1,0] - random_sumbit_length - 2*self.axis_padding - 1.5*self.std_button_length,
            0.03])

        self.slider = Slider(slider_ax, '', 1, 5, valinit=self.valinit, valstep=1, color="green" )
        self.slider.valtext.set_visible(False)
        self.cid_slider = self.slider.on_changed(self.update_speed)
        self.pause = self.pause_array[self.slider.val-1]
        self.slider.text = slider_ax.text(1, 1.5 , f"Speed: {self.slider.val}/5    (Pause: {self.pause:.2f}s)")


        # Add start/stop button
        start_stop_ax = plt.axes([
            1 - 1.25*self.std_button_length - self.axis_padding,
            self.axis_padding,
            self.std_button_length,
            self.std_button_height])
        self.start_stop = Button(
            start_stop_ax,
            'Start',
            color='lightgrey',
            hovercolor='lightgreen')
        self.cid_start_stop = self.start_stop.on_clicked(self.run)
        self.start_stop.stop_label = start_stop_ax.text(
            0.5, 0.5, 'Stop',
            verticalalignment='center',
            horizontalalignment='center',
            transform=start_stop_ax.transAxes)
        self.start_stop.stop_label.set_visible(False)

        # Add advance button
        advance_ax = plt.axes([
            start_stop_ax.get_position()._points[0,0],
            start_stop_ax.get_position()._points[1,1] + self.spacer + self.axis_padding,
            self.std_button_length,
            self.std_button_height])
        self.advance_button = Button(
            advance_ax,
            'Advance',
            color='lightgrey',
            hovercolor='lightgreen')

        # Add reset button
        reset_ax = plt.axes([
            start_stop_ax.get_position()._points[0,0],
            advance_ax.get_position()._points[1,1] + self.spacer,
            self.std_button_length,
            self.std_button_height])
        self.reset_button = Button(
            reset_ax,
            'Reset',
            color='lightgrey',
            hovercolor='lightgreen')

        # Add dimension buttons
        dim_refresh_ax = plt.axes([
            start_stop_ax.get_position()._points[0,0] - 0.25*self.std_button_length ,
            reset_ax.get_position()._points[1,1] + self.spacer + self.axis_padding,
            1.5*self.std_button_length,
            self.std_button_height])
        dim_refresh_ax.text(0.49,1.6, r"$\times$", size = 12, ha='center', va='center')
        TextBox_length = 0.06
        self.xdim_ax = plt.axes([
            dim_refresh_ax.get_position()._points[0,0],
            dim_refresh_ax.get_position()._points[1,1] + self.spacer,
            TextBox_length,
            self.std_button_height])
        self.ydim_ax = plt.axes([
            dim_refresh_ax.get_position()._points[1,0] -  TextBox_length,
            dim_refresh_ax.get_position()._points[1,1] + self.spacer,
            TextBox_length,
            self.std_button_height])
        self.refresh_button = Button(dim_refresh_ax, 'Refresh dim', color='lightgrey', hovercolor='lightgreen')
        self.xdim_submit = TextBox(self.xdim_ax, '', initial=str(self.dim[0]))
        self.ydim_submit = TextBox(self.ydim_ax, '', initial=str(self.dim[1]))

        # Activate buttons
        self.activate_buttons()

        # Enable button_press_event
        self.cid_stop = self.fig.canvas.mpl_connect('close_event', self.window_closed)

        # Show
        plt.show()



    def activate_buttons(self):
        self.start_stop.stop_label.set_visible(False)
        self.start_stop.label.set_visible(True)
        self.cid_pick = self.fig.canvas.mpl_connect('button_press_event', self.pick_cell)

        self.cid_reset = self.reset_button.on_clicked(self.reset)
        self.cid_advance = self.advance_button.on_clicked(self.advance)
        self.cid_random = self.random_button.on_clicked(self.random)
        self.cid_submit = self.submit.on_submit(self.random_input)
        self.cid_refresh = self.refresh_button.on_clicked(self.refresh)
        self.cid_xdim_submit = self.xdim_submit.on_submit(self.update_xdim)
        self.cid_ydim_submit = self.ydim_submit.on_submit(self.update_ydim)
        self.cid_sym = self.sym_button.on_clicked(self.RN_sym)


    def deactivate_buttons(self):
        self.start_stop.label.set_visible(False)
        self.start_stop.stop_label.set_visible(True)
        self.fig.canvas.mpl_disconnect(self.cid_pick)

        self.reset_button.disconnect(self.cid_reset)
        self.advance_button.disconnect(self.cid_advance)
        self.random_button.disconnect(self.cid_random)
        self.submit.disconnect(self.cid_submit)
        self.sym_button.disconnect(self.cid_sym)



    def RN_sym(self, event):
        xint_half = self.dim[1]//2
        left_over = self.dim[1]%2

        RN = np.random.rand(dim[0], xint_half)
        RN_binary = np.where(RN < self.random_pct/100, 1, 0)
        RN_binary_flip = np.flip(RN_binary, axis = 1)

        self.cells[:, :xint_half] = RN_binary
        self.cells[:, xint_half+left_over:self.dim[1]] = RN_binary_flip

        self.generation = 0
        self.update_plot()
        self.fig.canvas.draw_idle()


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
            self.update_plot()
            self.fig.canvas.draw_idle()


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



    def window_closed(self, event):
        exit()


    def update_plot(self):
        self.image.set_data(self.cells)
        self.ax.set_title(f"Generation: {self.generation}", y = self.title_y)


    def random_input(self, text):
        try:
            self.random_pct = eval(text)
        except:
            print("Please insert number between 0-100")
        if self.random_pct < 0:
            self.random_pct = 0
            self.submit.set_val(self.random_pct)

        elif self.random_pct > 100:
            self.random_pct = 100
            self.submit.set_val(self.random_pct)

        print(f"Random generator set to {self.random_pct} %")


    def random(self, botton_axes):
        RN = np.random.rand(dim[0],dim[1])
        self.cells = np.where(RN < self.random_pct/100, 1, 0)
        self.generation = 0
        self.update_plot()
        self.fig.canvas.draw_idle()


    def reset(self, botton_axes):
        self.cells = np.zeros((dim), dtype = int)
        self.generation = 0
        self.update_plot()
        self.fig.canvas.draw_idle()


    def update_speed(self, event    ):
        index = self.slider.val - 1
        self.pause = self.pause_array[index]
        self.slider.text.set_text(f"Speed: {self.slider.val}/5    (Pause: {self.pause:.2f}s)")


    def update_xdim(self, text):
        try:
            self.dim[0] = int(eval(text))
        except:
            print("Please insert valid integer number")

        self.xdim_submit.set_val(self.dim[0])


    def update_ydim(self, text):
        try:
            self.dim[1] = int(eval(text))
        except:
            print("Please insert valid integer number")

        self.ydim_submit.set_val(self.dim[1])


    def refresh(self, event):
        self.fig.canvas.mpl_disconnect(self.cid_stop)
        plt.close(self.fig)
        self.__init__(self.dim, self.random_pct, self.slider.val)


    def run(self, botton_axes):
        if not self.running: # Start
            self.deactivate_buttons()
            self.running = True

            while self.running:
                start_ad = time.time()
                self.advance()
                end_ad = time.time()

                plt.pause(self.pause)
                end_pause = time.time()

                print(f"\r Timing (gen. {self.generation}): Advance: {end_ad-start_ad:.5f}, Pause: {end_pause-end_ad:.5f}", end="")

        elif self.running: # Stop
            self.activate_buttons()
            self.running = False



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
        self.generation += 1
        self.update_plot()
        self.fig.canvas.draw_idle()


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





if __name__ == "__main__":
    dim = np.array([10,10])
    game = GAME_of_LIFE(dim)
