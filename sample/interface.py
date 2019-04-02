import time
from tkinter import *
from screeninfo import get_monitors
import pyautogui

from sample.format import print_change, Notification
from sample.frame.Textbox import Textbox
from sample.frame.Toolbar import ToolbarFrame
from sample.frame.WindowManager import WindowManagerFrame
from sample.image import Tree
from sample.parameters import retrieve_parameters, default_configurations


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

        print(self.tree.arg_dict)
        self.monitors = []

        self.textbox = None
        self.window_manager_frame = None
        self.toolbar_frame = None

        self.update_idletasks()
        self._defined = ['w_dim', 'h_dim', 'x_dim', 'y_dim']
        self.configurations = {}
        self._create()

        self.set_root()

        self.textbox.print_trees_now()  # immediately fills the current GUI window with trees
        self.textbox.run_gui()  # continue execution

    def _create(self):
        self._create_monitors()
        self._create_configurations()
        self._create_dimensions()

        self.textbox = Textbox(self)
        self.window_manager_frame = WindowManagerFrame(self)
        self.toolbar_frame = ToolbarFrame(self)

        # print('_create:', self.tree.arg_dict['w_dim'], self.tree.arg_dict['h_dim'],
        #       self.tree.arg_dict['x_dim'], self.tree.arg_dict['y_dim'])

    def _create_monitors(self):
        screen_info = get_monitors()
        for m in screen_info[::-1]:
            print(str(m))
            self.monitors.append({
                'w_dim': m.width,
                'h_dim': m.height,
                'x_dim': m.x,
                'y_dim': m.y
            })

    def _create_configurations(self):
        self.configurations['w_dim'] = {'assign': self.assign_width_dim, 'offset': 0}
        self.configurations['h_dim'] = {'assign': self.assign_height_dim, 'offset': 0}
        self.configurations['x_dim'] = {'assign': self.assign_x_dim, 'offset': 3}
        self.configurations['y_dim'] = {'assign': self.assign_y_dim, 'offset': 29}

    def _create_dimensions(self):
        if not self.tree.arg_dict['maximized']:
            for curr_dim in self._defined:
                if self.tree.arg_dict[curr_dim] is default_configurations()[curr_dim]:  # 0
                    self.configurations[curr_dim]['assign']()
                else:
                    if self.tree.arg_dict[curr_dim] is self.configurations[curr_dim]['offset']:
                        if self.tree.arg_dict['verbose']:
                            print(curr_dim, 'is default. Subtracting offset')
                        self.tree.arg_dict[curr_dim] -= self.configurations[curr_dim]['offset']
                    else:
                        if self.tree.arg_dict['verbose']:
                            print(curr_dim, 'is custom. Leaving it alone')
            # self.correct_height()
        else:
            self.manually_set_dimensions(True)

    def get_monitor(self, x=None, y=None):
        if x is None and y is None:
            mouse_x, mouse_y = pyautogui.position()
        else:
            mouse_x, mouse_y = x, y
        for index, m in enumerate(self.monitors):
            if m['x_dim'] <= mouse_x <= m['w_dim'] + m['x_dim']:
                print('clicked inside monitor', index)
                return m

    def assign_width_dim(self):
        """Converts width (in characters) to pixels"""
        self.tree.arg_dict['w_dim'] = (self.tree.screen_width + self.tree.make_even) * 6

        # if self.tree.arg_dict['maximized']:
        #     self.tree.arg_dict['w_dim'] -= 3

    def convert_w_dim(self):
        """Converts pixels to width (in characters)"""
        return self.tree.arg_dict['w_dim'] // 6 - self.tree.make_even

    def assign_height_dim(self):
        num_trees = 2
        if self.tree.arg_dict['textbox'] == 'small':
            self.tree.arg_dict['h_dim'] = ((48 * self.tree.tree_tiers) + 53) * num_trees
        elif self.tree.arg_dict['textbox'] == 'medium':
            self.tree.arg_dict['h_dim'] = int(self.tree.screen_height * 13 * num_trees)
        else:
            Notification(['Height unknown', 'Just going to assign 500 pixels?'])
            self.tree.arg_dict['h_dim'] = 500
        # self.correct_height()

    # def correct_height(self):
    #     if self.tree.arg_dict['h_dim'] + self.tree.arg_dict['y_dim'] > self.max_height:
    #         self.tree.arg_dict['h_dim'] -= (self.tree.arg_dict['h_dim'] + self.tree.arg_dict['y_dim'])-self.max_height
    #         print('new h_dim', self.tree.arg_dict['h_dim'])
    #         self.root.geometry('{}x{}+{}+{}'.format(
    #             self.tree.arg_dict['w_dim'],
    #             self.tree.arg_dict['h_dim'],
    #             self.tree.arg_dict['x_dim'],
    #             self.tree.arg_dict['y_dim']
    #         ))

    def assign_x_dim(self):
        print('assigning x to', self.winfo_x())
        self.tree.arg_dict['x_dim'] = self.winfo_x()

    def assign_y_dim(self):
        print('assigning y to', self.winfo_y())
        self.tree.arg_dict['y_dim'] = self.winfo_y()

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        self.root.resizable(width=True, height=True)

        self.root.geometry('{}x{}+{}+{}'.format(
            self.tree.arg_dict['w_dim'],
            self.tree.arg_dict['h_dim'],
            self.tree.arg_dict['x_dim'],
            self.tree.arg_dict['y_dim']
        ))

    def set_screen_width(self):
        before = self.tree.screen_width
        self.reset_tree('width', self.convert_w_dim())
        print_change('Window Width', before, self.tree.screen_width)

    def reset_tree(self, key=None, value=None):
        if key is not None and value is not None:
            if self.tree.arg_dict['verbose']:
                print('reset tree: updating', key, ' to ', value)
            self.tree.arg_dict[key] = value
        self.tree.update_parameters()
        if key == 'new file':
            if self.tree.arg_dict['verbose']:
                print('manually setting the dimensions')
            self.manually_set_dimensions()
        self.textbox.print_trees_now()

    def manually_set_dimensions(self, set_max=False):
        if not self.tree.arg_dict['maximized'] or set_max:
            if self.tree.arg_dict['verbose']:
                before = (f"{self.tree.arg_dict['w_dim']}, {self.tree.arg_dict['h_dim']},"
                          f"{self.tree.arg_dict['x_dim']}, {self.tree.arg_dict['y_dim']}")
            # self.correct_height()
            self.root.geometry('{}x{}+{}+{}'.format(
                self.tree.arg_dict['w_dim'],
                self.tree.arg_dict['h_dim'],
                self.tree.arg_dict['x_dim'],
                self.tree.arg_dict['y_dim'])
            )
            self.tree.update_parameters()
            if self.tree.arg_dict['verbose']:
                after = (f"{self.tree.arg_dict['w_dim']}, {self.tree.arg_dict['h_dim']},"
                         f"{self.tree.arg_dict['x_dim']}, {self.tree.arg_dict['y_dim']}")
                if before != after:
                    print('manually set:', before, after)
        else:
            if self.tree.arg_dict['verbose']:
                print('Currently maximized')
        if set_max:
            print('manual maximized:', self.tree.arg_dict['w_dim'], self.tree.arg_dict['h_dim'],
                  self.tree.arg_dict['x_dim'], self.tree.arg_dict['y_dim'])

    def have_root_dimensions_changed(self):
        w = self.winfo_width() == self.tree.arg_dict['w_dim']
        h = self.winfo_height() == self.tree.arg_dict['h_dim']
        x = self.winfo_rootx() == self.tree.arg_dict['x_dim']
        y = self.winfo_rooty() == self.tree.arg_dict['y_dim']

        if self.tree.arg_dict['verbose']:
            if not w:
                print('\tdifferent w:', self.winfo_width(), self.tree.arg_dict['w_dim'])
            if not h:
                print('\tdifferent h:', self.winfo_height(), self.tree.arg_dict['h_dim'])
            if not x:
                print('\tdifferent x:', self.winfo_rootx(), self.tree.arg_dict['x_dim'])
            if not y:
                print('\tdifferent y:', self.winfo_rooty(), self.tree.arg_dict['y_dim'])

        return w or h or x or y

    def textbox_change(self):
        if self.winfo_width() is not 1 and not self.tree.arg_dict['maximized']:
            print('textbox before:', self.winfo_width(), self.winfo_height(),
                  self.winfo_rootx(), self.winfo_rooty())

            self.tree.arg_dict['w_dim'] = self.winfo_width()
            self.tree.arg_dict['width'] = self.convert_w_dim()

            self.tree.arg_dict['h_dim'] = self.winfo_height()

            if self.tree.arg_dict['x_dim'] != self.winfo_rootx():
                print('  subtracting offset from x_dim')
                self.tree.arg_dict['x_dim'] = self.winfo_rootx() - self.configurations['x_dim']['offset']

            if self.tree.arg_dict['y_dim'] != self.winfo_rooty():
                print('  subtracting offset from y_dim')
                self.tree.arg_dict['y_dim'] = self.winfo_rooty() - self.configurations['y_dim']['offset']
            # self.correct_height()

            print('textbox after: ', self.tree.arg_dict['w_dim'], self.tree.arg_dict['h_dim'],
                  self.tree.arg_dict['x_dim'], self.tree.arg_dict['y_dim'])

            self.tree.update_parameters()
            self.textbox.print_trees_now()
            self.root.geometry('{}x{}+{}+{}'.format(
                self.tree.arg_dict['w_dim'],
                self.tree.arg_dict['h_dim'],
                self.tree.arg_dict['x_dim'],
                self.tree.arg_dict['y_dim']
            ))
        elif self.tree.arg_dict['maximized']:
            print('maximized: textbox')
            curr_monitor = self.get_monitor()
            self.tree.arg_dict['w_dim'] = curr_monitor['w_dim'] - (2 * self.configurations['x_dim']['offset'])
            self.tree.arg_dict['h_dim'] = curr_monitor['h_dim'] - (self.configurations['y_dim']['offset'] + 3)
            self.tree.arg_dict['x_dim'] = curr_monitor['x_dim']
            self.tree.arg_dict['y_dim'] = curr_monitor['y_dim']
            # self.correct_height()

            self.tree.update_parameters()
            self.textbox.print_trees_now()
            self.root.geometry('{}x{}+{}+{}'.format(
                self.tree.arg_dict['w_dim'],
                self.tree.arg_dict['h_dim'],
                self.tree.arg_dict['x_dim'],
                self.tree.arg_dict['y_dim']
            ))
            # self.tree.arg_dict['maximized'] = False
            self.window_manager_frame._maximize()

    def root_change(self):
        if self.winfo_width() is not 1 and self.have_root_dimensions_changed():
            print('root before:   ', self.winfo_width(), self.winfo_height(), self.winfo_rootx(), self.winfo_rooty())

            self.tree.arg_dict['w_dim'] = self.winfo_width()
            self.tree.arg_dict['width'] = self.convert_w_dim()

            self.tree.arg_dict['h_dim'] = self.winfo_height()
            # self.correct_height()

            if abs(self.tree.arg_dict['x_dim'] - self.winfo_rootx()) != 3:
                self.tree.arg_dict['x_dim'] = self.winfo_rootx()
                if self.tree.arg_dict['x_dim'] == self.configurations['x_dim']['offset']:
                    print('  subtracting offset from x_dim')
                    self.tree.arg_dict['x_dim'] -= self.configurations['x_dim']['offset']

            if abs(self.tree.arg_dict['y_dim'] - self.winfo_rooty()) != 29:
                self.tree.arg_dict['y_dim'] = self.winfo_rooty()
                if self.tree.arg_dict['y_dim'] == self.configurations['y_dim']['offset']:
                    print('  subtracting offset from y_dim')
                    self.tree.arg_dict['y_dim'] -= self.configurations['y_dim']['offset']

            print('root after:    ', self.tree.arg_dict['w_dim'], self.tree.arg_dict['h_dim'],
                  self.tree.arg_dict['x_dim'], self.tree.arg_dict['y_dim'])

            # self._create_dimensions()
            # self.root.geometry('{}x{}+{}+{}'.format(
            #     self.tree.arg_dict['w_dim'],
            #     self.tree.arg_dict['h_dim'],
            #     self.tree.arg_dict['x_dim'],
            #     self.tree.arg_dict['y_dim']
            # ))

    def window_change(self, event=None):
        if self.tree.arg_dict['verbose']:
            # print(_) # prints the <event> parameter
            before_w = self.tree.arg_dict['w_dim']
            before_h = self.tree.arg_dict['h_dim']
            before_x = self.tree.arg_dict['x_dim']
            before_y = self.tree.arg_dict['y_dim']

        if event.widget.winfo_id() == self.textbox.winfo_id():
            self.textbox_change()
        elif event.widget.winfo_id() == self.root.winfo_id():
            self.root_change()

        if self.tree.arg_dict['verbose']:
            print_change('\t   gui width', before_w, self.tree.arg_dict['w_dim'])
            print_change('\t  gui height', before_h, self.tree.arg_dict['h_dim'])
            print_change('\tgui x offset', before_x, self.tree.arg_dict['x_dim'])
            print_change('\tgui y offset', before_y, self.tree.arg_dict['y_dim'])
