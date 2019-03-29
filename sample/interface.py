import time
from tkinter import *

from sample.format import print_change
from sample.frame.Textbox import Textbox
from sample.frame.Toolbar import ToolbarFrame
from sample.frame.WindowManager import WindowManagerFrame
from sample.image import Tree
from sample.parameters import retrieve_parameters


def run_interface():
    my_tree = Tree(retrieve_parameters())
    if my_tree.arg_dict['interface']:
        root = Tk()
        GUI(root, my_tree)
        root.mainloop()
    else:
        app = CLI(my_tree)
        app.print_indefinitely()


class CLI:
    def __init__(self, my_tree):
        self.tree = my_tree

    def print_indefinitely(self):
        # immediately prints all trees too fill the CLI window with snowy trees
        for _ in range(min(self.tree.length, 50)):
            print(self.tree.list[self.tree.increment_index()])

        # continuous loop that iterates through the list of trees
        while True:
            print(self.tree.list[self.tree.increment_index()])
            # pause execution for the time specified in the --speed argument provided.
            time.sleep(self.tree.sleep_time)


class GUI(Frame):
    def __init__(self, parent, my_tree):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent
        self.root.configure(bd=0)
        # self.root.image = PhotoImage(file='./assets/icons/transparent.png')  # ToolbarFrame bg will be transparent
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='./assets/icons/tree_icon.png'))

        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = my_tree

        self.textbox = None
        self.window_manager_frame = None
        self.toolbar_frame = None
        self._create()

        self.update_idletasks()
        self.w_dim = 0
        self.h_dim = 0
        self.x_dim = 0
        self.y_dim = 0
        self.set_dimensions()

        self.set_root()

        self.textbox.print_trees_now()  # immediately fills the current GUI window with trees
        self.textbox.run_gui()  # continue execution

    def _create(self):
        self.textbox = Textbox(self)
        self.window_manager_frame = WindowManagerFrame(self)
        self.toolbar_frame = ToolbarFrame(self)

    def set_dimensions(self):
        self.assign_width_to_pixels()
        self.set_height_dim()
        self.x_dim = self.winfo_x()
        self.y_dim = self.winfo_y()

    def assign_width_to_pixels(self):
        self.w_dim = (self.tree.screen_width + self.tree.make_even) * 6

    def set_height_dim(self):
        num_trees = 2
        if self.tree.arg_dict['textbox'] == 'small':
            self.h_dim = ((48 * self.tree.tree_tiers) + 53) * num_trees
        elif self.tree.arg_dict['textbox'] == 'medium':
            self.h_dim = int(self.tree.screen_height * 13 * num_trees)

    def _convert_pixels_to_width(self):
        return self.w_dim // 6

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        self.root.resizable(width=True, height=True)
        self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))

    def set_screen_width(self):
        before = self.tree.screen_width
        self.reset_tree('width', self._convert_pixels_to_width())
        print_change('Window Width', before, self.tree.screen_width)

    def reset_tree(self, key=None, value=None):
        if key and value:
            self.tree.arg_dict[key] = value
        self.tree.update_parameters()
        if key == 'new file':
            self.manually_set_dimensions()
        self.textbox.print_trees_now()

    def manually_set_dimensions(self):
        if not self.window_manager_frame.maximized_bool:
            before = self.w_dim
            self.assign_width_to_pixels()
            if before != self.w_dim:
                if self.tree.arg_dict['verbose']:
                    print('File\'s new width:', before, '=>', self.w_dim)
                self.window_change()
        else:
            print('Currently maximized')

    def _dim(self):
        return {
            'w': self.w_dim,
            'h': self.h_dim,
            'x': self.x_dim,
            'y': self.y_dim
        }

    def window_change(self, event=None):
        if self.tree.arg_dict['verbose']:
            # print(_) # prints the <event> parameter
            before_w = self.w_dim
            before_h = self.h_dim
            before_x = self.x_dim
            before_y = self.y_dim
        if isinstance(event, Event):
            self.w_dim = self.winfo_width()
            if self.tree.screen_width != self._convert_pixels_to_width():
                # Only resets the tree if the width changes (~6 pixels), not every GUI pixel change
                self.set_screen_width()
            self.h_dim = self.winfo_height()
            self.x_dim = self.winfo_rootx()
            self.y_dim = self.winfo_rooty()
        else:
            print('  Manually changing the GUI dimensions\n'
                  '  - Ignore the first printed width')
        self.root.geometry('{}x{}'.format(self.w_dim, self.h_dim))

        if self.tree.arg_dict['verbose']:
            print_change('\t   gui width', before_w, self.w_dim)
            print_change('\t  gui height', before_h, self.h_dim)
            print_change('\tgui x offset', before_x, self.x_dim)
            print_change('\tgui y offset', before_y, self.y_dim)
