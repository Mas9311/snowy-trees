from tkinter import *

from sample import Tree, parameters


class TreeGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True, ipadx=1)
        self.root = parent
        self.root.bind("<Configure>", self.window_change)

        self.textbox = Text(self, fg='green', background='#000000', height=200, width=150, wrap='none', font='fixed')
        self.textbox.pack(fill=BOTH)

        r = '#ff0000'
        g = '#00ff00'
        self.close_button = Button(self.textbox, text='×', font=('times new roman', 18), command=self.root.destroy,
                                   background=r, foreground=g, activebackground=r, activeforeground=g)
        self.close_button.place(relx=0, rely=0, anchor="nw")

        self.options = Button(self, text='options', font=('courier', 25), height=1, width=6)
        self.options['activebackground'] = '#444444'
        self.options['activeforeground'] = '#cccccc'
        self.options['bg'] = '#000000'
        self.options['fg'] = '#ffffff'
        self.options.place(relx=1.0, rely=0, anchor="ne")

        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = Tree.Tree(parameters.retrieve())
        self.w_dim = self.tree.screen_width * 5
        self.h_dim = 17 * (self.tree.tree_tiers * 4 + 3)
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
        # self.root.overrideredirect(1)
        self.root.resizable(width=True, height=True)
        self.root.configure(borderwidth='0')
        self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))
        # self.root.call("wm", "attributes", ".", "-fullscreen", "true")

    def window_change(self, e):
        self.w_dim = self.winfo_width()
        self.h_dim = self.winfo_height()
        self.x_dim = self.winfo_x()
        self.y_dim = self.winfo_y()
        print(self.winfo_geometry(), f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}')
        # self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))

    def print_init(self):
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
