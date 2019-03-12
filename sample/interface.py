import time
from tkinter import *

from sample import Tree, parameters


def run_interface():
    my_tree = Tree.Tree(parameters.retrieve())
    if my_tree.arg_dict['interface']:
        root = Tk()
        GUI(root)
        root.mainloop()
    else:
        app = CLI(my_tree)
        app.print_indefinitely()


class CLI:
    def __init__(self, my_tree):
        self.tree = my_tree

    def print_indefinitely(self):
        # print the first 6 upon execution to immediately fill the screen with snowy trees
        for curr_tree in range(6):
            print(self.tree.list[curr_tree])

        # continuous loop that iterates through the list of trees
        while True:
            for curr_tree in range(self.tree.length):
                print(self.tree.list[curr_tree])
                # pause execution for the time specified in the --speed argument provided.
                time.sleep(self.tree.sleep_time)


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent
        self.root.configure(bd=0)

        self.textbox = Text()
        self.set_text_box()

        # TODO: refactor window_manager_frame into a separate class
        self.window_manager_frame = None
        self.window_close = None
        self.window_minimize = None
        self.window_maximize = None
        self.maximized_bool = False
        self.set_win_man_frame()

        # TODO: refactor opt_frame into a separate class
        self.opt_frame = None
        self.opt_bool = None
        self.opt_button = None
        self.set_options()

        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = Tree.Tree(parameters.retrieve())

        # Assigns values to the options Frame sliders
        self.opt_speed_label = None
        self.opt_speed = None
        self.curr_speed = None
        self.int_speed = None

        self.opt_density_label = None
        self.opt_density = None
        self.curr_density = None
        self.int_density = None

        self.opt_tiers_label = None
        self.opt_tiers = None
        self.int_tiers = None

        self.opt_ornaments_label = None
        self.ornaments_bool = None
        self.opt_ornaments_frame = None
        self.opt_ornaments_on = None
        self.opt_ornaments_off = None

        self.init_options()

        # self.update()
        self.update_idletasks()
        self.w_dim = self.tree.screen_width * 6 + 12  # self.winfo_width() - 6
        self.h_dim = 117 * self.tree.tree_tiers + 163  # self.winfo_height() * 2
        self.x_dim = self.winfo_x()
        self.y_dim = self.winfo_y()

        self.set_root()

        # print the first 6 upon execution to immediately fill the screen with snowy trees
        self.print_init()

        # continue execution
        self.busy = False
        self.run_gui(self.textbox, 6)
        # self.set_screen_width()

    def init_options(self):
        speeds = ['slow', 'average', 'fast', 'ultra']
        self.int_speed = speeds.index(self.tree.arg_dict['speed']) + 1
        self.curr_speed = speeds[self.int_speed - 1]

        densities = ['thin', 'average', 'heavy', 'ultra']
        self.int_density = densities.index(self.tree.arg_dict['density']) + 1
        self.curr_density = densities[self.int_density - 1]

        self.int_tiers = self.tree.tree_tiers

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        self.root.resizable(width=True, height=True)
        # self.root.configure(bd=0)
        self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))

    def set_text_box(self):
        self.textbox = Text(self, fg='green', background='#000000', height=200, width=150,
                            wrap='none', font='fixed', highlightthickness=0)
        self.textbox.pack(fill=BOTH)

    def click_options(self):
        if self.opt_bool:
            self.set_options()
        else:
            self.opt_bool = True
            self.set_sub_options()

    def set_win_man_frame(self):
        self.window_manager_frame = Frame(self, highlightthickness=0)
        self.window_manager_frame.place(relx=0, rely=0, anchor="nw")
        self.window_close = Button(self.window_manager_frame, text='×', highlightthickness=0,
                                   font=('times new roman', 18, 'bold'), command=self._close)
        self.window_close.grid(row=0, column=0)
        self.window_maximize = Button(self.window_manager_frame, text='+', highlightthickness=0,
                                      font=('times new roman', 18, 'bold'), command=self._maximize)
        self.window_maximize.grid(row=0, column=1)
        self.window_minimize = Button(self.window_manager_frame, text='−', highlightthickness=0,
                                      font=('times new roman', 18, 'bold'), command=self._minimize)
        self.window_minimize.grid(row=0, column=2)

    def _close(self):
        self.root.destroy()

    def _maximize(self):
        if not self.maximized_bool:
            self.root.overrideredirect(1)
            self.root.call("wm", "attributes", ".", "-fullscreen", "true")
        else:
            self.root.overrideredirect(0)
            self.root.call("wm", "attributes", ".", "-fullscreen", "false")
        self.maximized_bool = not self.maximized_bool

    def _minimize(self):
        if self.maximized_bool:
            self._maximize()
        self.root.state('iconic')

    def set_opt_button(self):
        self.opt_button = Button(self.opt_frame, text='options', font=('courier', 25),
                                 highlightthickness=0, command=self.click_options)
        self.opt_button['activebackground'] = '#444444'
        self.opt_button['activeforeground'] = '#cccccc'
        self.opt_button['bg'] = '#000000'
        self.opt_button['fg'] = '#ffffff'
        self.opt_button.grid(row=0, column=0, sticky=N + E + S)

    def set_sub_options(self):
        # Create the rest of the frame
        self.set_opt_speed()
        self.set_opt_density()
        self.set_opt_tiers()
        self.set_opt_ornaments()

    def set_opt_speed(self):
        self.opt_speed_label = Label(self.opt_frame, text='Refresh Speed', bg='#aaaaaa', fg='#3d008e',
                                     highlightthickness=0, font=('courier', 25), relief=FLAT, width=16)
        self.opt_speed_label.grid(row=1, column=0, sticky=W + E)

        self.opt_speed = Scale(self.opt_frame, label=None, font=('courier', 25), bg='#aaaaaa', fg='#3d008e',
                               from_=1, to=4, bd=0, showvalue=0, orient=HORIZONTAL, relief=FLAT, highlightthickness=0,
                               activebackground='#00ff80', troughcolor='#aaaaaa', command=self.set_speed)
        self.opt_speed.set(self.int_speed)
        self.opt_speed.grid(row=2, column=0, sticky=W + E)

    def set_opt_density(self):
        self.opt_density_label = Label(self.opt_frame, text='Snow Density', bg='#333333', fg='#00d165',
                                       highlightthickness=0, font=('courier', 25), relief=FLAT)
        self.opt_density_label.grid(row=3, column=0, sticky=W + E)

        self.opt_density = Scale(self.opt_frame, label=None, font=('courier', 25), bg='#333333', fg='#00d165',
                                 from_=1, to=4, bd=0, showvalue=0, orient=HORIZONTAL, relief=FLAT, highlightthickness=0,
                                 activebackground='#3d008e', troughcolor='#333333', command=self.set_density)
        self.opt_density.set(self.int_density)
        self.opt_density.grid(row=4, column=0, sticky=W + E)

    def set_opt_tiers(self):
        self.opt_tiers_label = Label(self.opt_frame, text='Tree Tiers', bg='#aaaaaa', fg='#3d008e',
                                     highlightthickness=0, font=('courier', 25), relief=FLAT)
        self.opt_tiers_label.grid(row=5, column=0, sticky=W + E)

        self.opt_tiers = Scale(self.opt_frame, label=None, font=('courier', 25), bg='#aaaaaa', fg='#3d008e',
                               from_=1, to=13, bd=0, showvalue=0, orient=HORIZONTAL, relief=FLAT, highlightthickness=0,
                               activebackground='#00ff80', troughcolor='#aaaaaa', command=self.set_tiers)
        self.opt_tiers.set(self.int_tiers)
        self.opt_tiers.grid(row=6, column=0, sticky=W + E)

    def set_opt_ornaments(self):
        self.opt_ornaments_label = Label(self.opt_frame, text='Ornaments', bg='#333333', fg='#00d165',
                                         highlightthickness=0, font=('courier', 25), relief=FLAT)
        self.opt_ornaments_label.grid(row=7, column=0, sticky=W + E)

        self.ornaments_bool = (False, True)[self.tree.arg_dict['ornaments']]

        self.set_opt_ornaments_frame()

    def set_opt_ornaments_frame(self):
        self.opt_ornaments_frame = Frame(self.opt_frame, bg='#ffffff')
        self.opt_ornaments_frame.grid(row=8, column=0, sticky=W + E)

        button_on = (FLAT, RIDGE)[self.ornaments_bool]
        button_off = (RIDGE, FLAT)[self.ornaments_bool]

        self.opt_ornaments_on = Button(self.opt_ornaments_frame, text='On', highlightthickness=0, width=6,
                                       font=('courier', 25), relief=button_on, bg='#333333', fg='#00d165',
                                       activebackground='#333333', activeforeground='#00d165',
                                       command=lambda: self.set_ornaments(True))
        self.opt_ornaments_on.grid(row=0, column=0, sticky=N + E + W + S, ipadx=1)
        self.opt_ornaments_off = Button(self.opt_ornaments_frame, text='Off', highlightthickness=0, width=6,
                                        font=('courier', 25), relief=button_off, bg='#333333', fg='#00d165',
                                        activebackground='#333333', activeforeground='#00d165',
                                        command=lambda: self.set_ornaments(False))
        self.opt_ornaments_off.grid(row=0, column=1, sticky=N + E + W + S, ipadx=1)

    def set_options(self):
        if self.opt_frame:
            self.opt_frame.destroy()
        self.opt_frame = Frame(self, width=65, height=26, highlightthickness=0)
        self.opt_frame['bg'] = '#000000'
        self.opt_frame.place(relx=1, rely=0, x=-2, y=2, anchor=NE)
        self.set_opt_button()
        self.opt_bool = False

    def set_speed(self, value):
        if not self.busy:
            self.busy = True
            before = self.curr_speed
            value = int(value)
            args = self.tree.arg_dict
            speeds = ['slow', 'average', 'fast', 'ultra']
            self.int_speed = value
            self.curr_speed = speeds[self.int_speed - 1]
            args['speed'] = self.curr_speed
            self.reset_tree(args)
            print_change('Speed', before, self.curr_speed)

    def set_density(self, value):
        value = int(value)
        if self.int_density is not value and not self.busy:
            self.busy = True
            before = self.curr_density
            args = self.tree.arg_dict
            densities = ['thin', 'average', 'heavy', 'ultra']
            self.int_density = value
            self.curr_density = densities[self.int_density - 1]
            args['density'] = self.curr_density
            self.reset_tree(args)
            print_change('Density', before, self.curr_density)

    def set_tiers(self, value):
        if not self.busy:
            self.busy = True
            before = self.int_tiers
            value = int(value)
            args = self.tree.arg_dict
            self.int_tiers = value
            args['tiers'] = self.int_tiers
            self.reset_tree(args)
            print_change('Tiers', before, self.int_tiers)

    def set_ornaments(self, arg_bool):
        if not self.busy and arg_bool is not self.ornaments_bool:

            self.busy = True
            before = self.ornaments_bool
            args = self.tree.arg_dict
            args['ornaments'] = arg_bool
            self.reset_tree(args)
            self.ornaments_bool = arg_bool
            # self.opt_ornaments_on.pack_forget()
            # self.opt_ornaments_off.pack_forget()
            # self.opt_ornaments_frame.grid_forget()
            self.opt_ornaments_frame.destroy()
            self.set_opt_ornaments_frame()
            print_change('Ornaments', before, self.ornaments_bool)

    def set_screen_width(self):
        if not self.busy:
            self.busy = True
            before = self.tree.screen_width
            args = self.tree.arg_dict
            args['width'] = max(self.w_dim // 6 - 2, self.tree.tree_width + 1)
            self.reset_tree(args)
            print_change('Window Width', before, self.tree.screen_width)

    def reset_tree(self, args):
        # print('reset')
        self.textbox.place_forget()
        self.set_text_box()

        self.tree.arg_dict = args
        self.tree.set_parameters()
        self.print_init()
        self.busy = False

    def window_change(self, event):
        # before = f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}'
        self.w_dim = self.winfo_width()
        if self.tree.screen_width is not self.w_dim // 6 - 2 and self.w_dim // 6 - 2 > self.tree.tree_width + 1:
            self.set_screen_width()
        self.h_dim = self.winfo_height()
        self.x_dim = self.winfo_rootx()
        self.y_dim = self.winfo_rooty()
        self.root.geometry('{}x{}'.format(self.w_dim, self.h_dim))
        # print_change('Dimensions', before, f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}')

    def print_init(self):
        """Print the initial 6 Trees to the GUI"""
        initial_tree_str = ''
        for curr_tree in range(6):
            initial_tree_str += self.tree.list[curr_tree] + '\n'
        self.textbox.insert('0.0', initial_tree_str + '\n')

    def run_gui(self, textbox, index):
        """Recursive loop that prints the tree at the top of the GUI"""
        textbox.insert('0.0', self.tree.list[index] + '\n')
        # pause execution for the time specified in the speed argument provided.
        textbox.after(int(self.tree.sleep_time * 1000),
                      self.run_gui, textbox, (index + 1) % self.tree.length)


def print_change(type_of, before, after):
    if str(before) != str(after):
        indent = (' * ', '')[type_of != 'Dimensions']
        print(f'{indent}{type_of}: {before} => {after}')
