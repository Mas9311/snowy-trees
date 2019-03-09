from tkinter import *

from sample import Tree, parameters

# TODO: refactor 'options' into separate class! It will act as a Modal in js


class TreeGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent

        self.textbox = Text(self, fg='green', background='#000000', height=200, width=150, wrap='none', font='fixed')
        self.textbox.pack(fill=BOTH)

        self.close_button = None
        self.set_close_button()

        self.opt_frame = None
        self.opt_bool = False
        self.opt_button = None
        self.set_options()

        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = Tree.Tree(parameters.retrieve())
        self.w_dim = self.tree.screen_width * 6
        self.h_dim = 17 * (self.tree.tree_tiers * 4 + 3) * 4
        self.x_dim = 0
        self.y_dim = 0

        self.set_root()

        # max length of list to compute. This will save you energy from each snowflake's numpy.random call.
        self.max_len = 25

        # creates a list of 25 unique snow/ornament arrangements
        self.tree_list = self.tree.build_list(self.max_len)

        # print the first 6 upon execution to immediately fill the screen with snowy trees
        self.print_init()

        # continue execution
        self.run_gui(6)
        self.root.update()

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        # self.root.overrideredirect(1)
        self.root.resizable(width=True, height=True)
        self.root.configure(borderwidth='0')
        self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))
        # self.root.call("wm", "attributes", ".", "-fullscreen", "true")

    def click_options(self):
        if self.opt_bool:
            self.opt_frame['width'] = 60
            self.opt_frame['height'] = 25
            self.opt_bool = False
        else:
            self.opt_frame['width'] = 200
            self.opt_frame['height'] = 200
            self.opt_bool = True

    def set_close_button(self):
        r = '#ff0000'
        g = '#00ff00'
        self.close_button = Button(self.textbox, text='×', font=('times new roman', 18), command=self.root.destroy,
                                   background=r, foreground=g, activebackground=r, activeforeground=g)
        self.close_button.place(relx=0, rely=0, anchor="nw")

    def set_opt_button(self):
        self.opt_button = Button(self.opt_frame, text='options', font=('courier', 25), command=self.click_options)
        self.opt_button['activebackground'] = '#444444'
        self.opt_button['activeforeground'] = '#cccccc'
        self.opt_button['bg'] = '#000000'
        self.opt_button['fg'] = '#ffffff'
        # self.opt_button.pack(fill=BOTH)
        self.opt_button.place(relx=1, rely=0, anchor="ne")

    def set_options(self):
        self.opt_frame = Frame(self, width=60, height=25)
        self.opt_frame.place(relx=1, rely=0, x=-2, y=2, anchor="ne")
        self.set_opt_button()

    def window_change(self, event):
        self.w_dim = self.winfo_width()
        self.h_dim = self.winfo_height()
        self.x_dim = event.x  # - 3
        self.y_dim = event.y  # - 29
        # print(self.winfo_geometry(), f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}')
        # self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))

    def print_init(self):
        """Print the initial 6 Trees to the GUI"""
        initial_tree_str = ''
        for curr_tree in range(6):
            initial_tree_str += self.tree_list[curr_tree] + '\n'
        self.textbox.insert(END, initial_tree_str)

    def run_gui(self, index):
        """Recursive loop that prints the tree at the top of the GUI"""
        self.textbox.insert('0.0', self.tree_list[index] + '\n')

        # pause execution for the time specified in the --speed argument provided.
        self.textbox.after(int(self.tree.sleep_time * 1000),
                           self.run_gui, (index + 1) % self.max_len)
