from tkinter import *

from sample import Tree, parameters

# TODO: refactor 'options' into separate class! It will act as a Modal in js


class TreeGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent

        self.textbox = Text()
        self.set_text_box()

        self.window_manager_frame = None
        self.window_close = None
        self.window_minimize = None
        self.window_maximize = None
        self.maximized = False
        self.set_win_man_frame()

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
        self.curr_tiers = None
        self.init_options()

        # self.update()
        self.update_idletasks()
        self.w_dim = self.tree.screen_width * 6 + 12  # self.winfo_width() - 6
        self.h_dim = 117 * self.tree.tree_tiers + 163  # self.winfo_height() * 2
        self.x_dim = self.winfo_x()
        self.y_dim = self.winfo_y()
        print(self.w_dim, self.h_dim, self.x_dim, self.y_dim)

        self.set_root()

        # print the first 6 upon execution to immediately fill the screen with snowy trees
        self.print_init()

        # continue execution
        self.run_gui(self.textbox, 6)

    def init_options(self):
        speeds = ['slow', 'average', 'fast', 'ultra']
        self.int_speed = speeds.index(self.tree.arg_dict['speed']) + 1
        self.curr_speed = speeds[self.int_speed - 1]

        densities = ['thin', 'average', 'heavy', 'ultra']
        self.int_density = densities.index(self.tree.arg_dict['density']) + 1
        self.curr_density = densities[self.int_density - 1]

        self.curr_tiers = self.tree.tree_tiers

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        self.root.resizable(width=True, height=True)
        self.root.configure(borderwidth='0')
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
        # self.root.state('withdrawn')

    def _maximize(self):
        if not self.maximized:
            self.maximized = True
            self.root.overrideredirect(1)
            self.root.call("wm", "attributes", ".", "-fullscreen", "true")
        else:
            self.maximized = False
            self.root.overrideredirect(0)
            self.root.call("wm", "attributes", ".", "-fullscreen", "false")

    def _minimize(self):
        self.root.state('iconic')

    def set_opt_button(self):
        self.opt_button = Button(self.opt_frame, text='options', font=('courier', 25),
                                 highlightthickness=0, command=self.click_options)
        self.opt_button['activebackground'] = '#444444'
        self.opt_button['activeforeground'] = '#cccccc'
        self.opt_button['bg'] = '#000000'
        self.opt_button['fg'] = '#ffffff'
        self.opt_button.grid(row=0, column=0, sticky=E)

    def set_sub_options(self):
        # Create the rest of the frame
        self.set_opt_speed()
        self.set_opt_density()
        c = Button(self.opt_frame, text='3rd', font=('courier', 25), bg='khaki', highlightthickness=0, command=self._c)
        c.grid(row=5, column=0, sticky=W + E)
        d = Button(self.opt_frame, text='4th', font=('courier', 25), bg='gold', highlightthickness=0, command=self._c)
        d.grid(row=6, column=0, sticky=W + E)

    def _c(self):
        print('*' * 35)

    def set_opt_speed(self):
        self.opt_speed_label = Label(self.opt_frame, text='Refresh Speed', bg='#aaaaaa', fg='#3d008e',
                                     highlightthickness=0, font=('courier', 25), relief=FLAT)
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

    def set_options(self):
        if self.opt_frame:
            self.opt_frame.destroy()
        self.opt_frame = Frame(self, width=65, height=26, highlightthickness=0)
        self.opt_frame['bg'] = '#000000'
        self.opt_frame.place(relx=1, rely=0, x=-2, y=2, anchor=NE)
        self.set_opt_button()
        self.opt_bool = False

    def set_speed(self, value):
        value = int(value)
        args = self.tree.arg_dict
        speeds = ['slow', 'average', 'fast', 'ultra']
        self.int_speed = value
        self.curr_speed = speeds[self.int_speed - 1]
        args['speed'] = self.curr_speed
        self.reset_tree(args)
        print('speed', self.curr_speed)

    def set_density(self, value):
        value = int(value)
        if self.int_density is not value:
            args = self.tree.arg_dict
            densities = ['thin', 'average', 'heavy', 'ultra']
            self.int_density = value
            self.curr_density = densities[self.int_density - 1]
            args['density'] = self.curr_density
            self.reset_tree(args)
            print('density', self.curr_density)

    def set_screen_width(self):
        args = self.tree.arg_dict
        args['width'] = max(self.w_dim // 6, self.tree.tree_width)
        self.reset_tree(args)
        print('screen_width', self.tree.screen_width)

    def reset_tree(self, args):
        print('reset')
        self.textbox.place_forget()
        self.set_text_box()

        self.tree.arg_dict = args
        self.tree.set_parameters()
        self.print_init()

    def window_change(self, event):
        self.w_dim = self.winfo_width()
        if self.tree.screen_width is not self.w_dim // 6 and self.w_dim // 6 > self.tree.tree_width + 1:
            self.set_screen_width()
        self.h_dim = self.winfo_height()
        self.x_dim = self.winfo_rootx()
        self.y_dim = self.winfo_rooty()
        self.root.geometry('{}x{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))

    def print_init(self):
        """Print the initial 6 Trees to the GUI"""
        initial_tree_str = ''
        for curr_tree in range(6):
            initial_tree_str += self.tree.list[curr_tree] + '\n'
        self.textbox.insert('0.0', initial_tree_str)

    def run_gui(self, textbox, index):
        """Recursive loop that prints the tree at the top of the GUI"""
        print(f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}')

        textbox.insert('0.0', self.tree.list[index] + '\n')
        # pause execution for the time specified in the speed argument provided.
        textbox.after(int(self.tree.sleep_time * 1000),
                      self.run_gui, textbox, (index + 1) % self.tree.list_len)
