from tkinter import *

from sample import Tree, parameters


class TreeGUI:
    def __init__(self, root):
        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = Tree.Tree(parameters.retrieve())

        # max length of list to compute. This will save you energy from each snowflake's numpy.random call.
        self.max_len = 25

        # creates a list of 25 unique snow/ornament arrangements
        self.tree_list = self.tree.build_list(self.max_len)

        self.root = root
        self.set_root()

        self.frame = Frame(root)
        self.frame.pack(fill=BOTH)

        self.close_button = Button(self.frame, text='X', command=root.destroy)
        self.close_button.configure(width=1, height=1)
        # TODO: allow button placement "floating" or overlaying the frame
        self.close_button.place(x=150, y=150)
        self.close_button.pack(anchor=NE)

        self.textbox = Text(self.frame, fg='green', background='#000000', height=1000, width=50, wrap='none', font='fixed')
        self.textbox.pack(fill=BOTH)

        # print the first 6 upon execution to immediately fill the screen with snowy trees
        self.print_init()

        # continue execution
        self.run_gui(6)
        self.root.update()

    def set_root(self):
        self.root.overrideredirect(1)
        self.root.configure(borderwidth='0')
        self.root.geometry('1074x1100+0+0')

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
