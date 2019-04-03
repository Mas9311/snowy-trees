import time
from tkinter import *
from screeninfo import get_monitors
import pyautogui

from sample.file_helper import make_sure_dir_exists, file_exists, export_file_as, get_filepath, import_from_file
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
        self.root.configure(background='black')
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
        self.offsets_are_set = False
        self._create()

        self.set_root()

        self.textbox.print_trees_now()  # immediately fills the current GUI window with trees
        self.textbox.run_gui()  # continue execution
        print(f"{self.tree.arg_dict['w_dim']}x{self.tree.arg_dict['h_dim']}+"
              f"{self.tree.arg_dict['x_dim']}+{self.tree.arg_dict['y_dim']}")

    def _create(self):
        self._create_monitors()
        self._create_configurations()
        self._create_dimensions()

        self.textbox = Textbox(self)
        self.window_manager_frame = WindowManagerFrame(self)
        self.toolbar_frame = ToolbarFrame(self)

    def _create_default_file(self):
        make_sure_dir_exists()
        if not file_exists(get_filepath('default')):
            mouse_x, mouse_y = pyautogui.position()
            pyautogui.moveTo(30, 30)

            old = self.tree
            re_maximize = retrieve_parameters()['maximized']
            if re_maximize:
                print('DEFAULT UNMAXIMIZE')
                self.tree.arg_dict['maximized'] = True
                self.window_manager_frame._maximize()

            self.tree = Tree(default_configurations())
            print('DEFAULT:', self.root.winfo_width(), self.root.winfo_height(), self.winfo_rootx(), self.winfo_rooty())
            self.tree.arg_dict['w_dim'] = 0
            self.tree.arg_dict['h_dim'] = 0
            self.tree.arg_dict['x_dim'] = self.winfo_rootx()  # 3 or 4
            self.tree.arg_dict['y_dim'] = self.winfo_rooty()  # 29 or 54

            export_file_as('default', self.tree.arg_dict, False)
            pyautogui.moveTo(mouse_x, mouse_y)
            self.tree = old
            if re_maximize:
                self.tree.arg_dict['maximized'] = False
                self.window_manager_frame._maximize()

        defaults = import_from_file('default', False)
        self.configurations['x_dim']['offset'] = defaults['x_dim']
        self.configurations['y_dim']['offset'] = defaults['y_dim']
        if self.tree.arg_dict['verbose']:
            print(f"Offsets set to: x={self.configurations['x_dim']['offset']} "
                  f"y={self.configurations['y_dim']['offset']}")

    def _create_monitors(self):
        screen_info = get_monitors()
        for m in screen_info[::-1]:  # for me, the monitors are right-to-left. May not always be the case, though
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
        self.configurations['x_dim'] = {'assign': self.assign_x_dim, 'offset': 0}  # 0 => 3 or 4
        self.configurations['y_dim'] = {'assign': self.assign_y_dim, 'offset': 0}  # 0 => 29 or 54

    def _create_dimensions(self):
        if not self.tree.arg_dict['maximized']:
            for curr_dim in self._defined:
                if self.tree.arg_dict[curr_dim] is default_configurations()[curr_dim]:  # 0
                    if self.tree.arg_dict['verbose']:
                        print(curr_dim, 'is assigned to', self.tree.arg_dict[curr_dim])
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
            self.manually_set_dimensions()

    def get_monitor(self, mouse_x=None, mouse_y=None):
        if mouse_x is None:
            mouse_x, _ = pyautogui.position()
        if mouse_y is None:
            _, mouse_y = pyautogui.position()
        for index, m in enumerate(self.monitors):
            if m['x_dim'] <= mouse_x <= m['w_dim'] + m['x_dim']:
                print('mouse inside monitor', index)
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
        self.correct_height()

    def correct_height(self):
        current_monitor = self.get_monitor()
        max_h = current_monitor['h_dim']

        if self.tree.arg_dict['h_dim'] + self.tree.arg_dict['y_dim'] > max_h:
            self.tree.arg_dict['h_dim'] -= (self.tree.arg_dict['h_dim'] + self.tree.arg_dict['y_dim']) - max_h
            print('correcting h_dim:', self.tree.arg_dict['h_dim'])
            self.root.geometry('{}x{}+{}+{}'.format(
                self.tree.arg_dict['w_dim'],
                self.tree.arg_dict['h_dim'],
                self.tree.arg_dict['x_dim'],
                self.tree.arg_dict['y_dim']
            ))

    def assign_x_dim(self):
        self.tree.arg_dict['x_dim'] = self.winfo_x()

    def assign_y_dim(self):
        self.tree.arg_dict['y_dim'] = self.winfo_y()

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        self.root.resizable(width=True, height=True)
        # self.root.configure(bd=0)

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
            self.tree.arg_dict[key] = value
        self.tree.update_parameters()
        if key == 'new file':
            if self.tree.arg_dict['verbose']:
                print('manually setting the dimensions')
            self.manually_set_dimensions()
        self.textbox.print_trees_now()

    def manually_set_dimensions(self):
        if not self.tree.arg_dict['maximized']:
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
        # print('manual maximized:', self.tree.arg_dict['w_dim'], self.tree.arg_dict['h_dim'],
        #       self.tree.arg_dict['x_dim'], self.tree.arg_dict['y_dim'])

    def have_root_dimensions_changed(self):
        w = self.winfo_width() == self.tree.arg_dict['w_dim']
        h = self.winfo_height() == self.tree.arg_dict['h_dim']
        x = self.winfo_rootx() == self.tree.arg_dict['x_dim']
        y = self.winfo_rooty() == self.tree.arg_dict['y_dim']

        # if self.tree.arg_dict['verbose']:
        #     if not w:
        #         print('\tdifferent w:', self.winfo_width(), self.tree.arg_dict['w_dim'])
        #     if not h:
        #         print('\tdifferent h:', self.winfo_height(), self.tree.arg_dict['h_dim'])
        #     if not x:
        #         print('\tdifferent x:', self.winfo_rootx(), self.tree.arg_dict['x_dim'])
        #     if not y:
        #         print('\tdifferent y:', self.winfo_rooty(), self.tree.arg_dict['y_dim'])

        return w or h or x or y

    def textbox_change(self):
        if self.tree.arg_dict['verbose']:
            print('textbox: ', end='')

        if not self.tree.arg_dict['maximized']:
            if self.tree.arg_dict['verbose']:
                print('not maximized.')
            before = (f"{self.winfo_width()}x{self.winfo_height()}+"
                      f"{self.winfo_rootx()}+{self.winfo_rooty()}")

            self.tree.arg_dict['w_dim'] = self.winfo_width()
            self.tree.arg_dict['width'] = self.convert_w_dim()

            self.tree.arg_dict['h_dim'] = self.winfo_height()

            if abs(self.tree.arg_dict['x_dim'] - self.winfo_rootx()) == self.configurations['x_dim']['offset']:
                print('  subtracting offset from x_dim')
                self.tree.arg_dict['x_dim'] -= self.configurations['x_dim']['offset']

            if abs(self.tree.arg_dict['y_dim'] - self.winfo_rooty()) == self.configurations['y_dim']['offset']:
                print('  subtracting offset from y_dim')
                self.tree.arg_dict['y_dim'] -= self.configurations['y_dim']['offset']

            # self.correct_height()

            after = (f"{self.tree.arg_dict['w_dim']}x{self.tree.arg_dict['h_dim']}+"
                     f"{self.tree.arg_dict['x_dim']}+{self.tree.arg_dict['y_dim']}")

            if before != after:
                if self.tree.arg_dict['verbose']:
                    print('textbox setting:', before, '=>', after)

            self.tree.update_parameters()
            self.textbox.print_trees_now()
            self.root.geometry('{}x{}+{}+{}'.format(
                self.tree.arg_dict['w_dim'],
                self.tree.arg_dict['h_dim'],
                self.tree.arg_dict['x_dim'],
                self.tree.arg_dict['y_dim'])
            )
        else:
            if self.tree.arg_dict['verbose']:
                print('maximized.')
            print('current  : ', end='')
            curr_monitor = self.get_monitor()
            print('requested: ', end='')
            requested_monitor = self.get_monitor(self.tree.arg_dict['x_dim'], self.tree.arg_dict['y_dim'])

            if curr_monitor != requested_monitor:
                mouse_x, mouse_y = pyautogui.position()
                delta_x = (self.tree.arg_dict['x_dim'] - mouse_x) + 1
                delta_y = (self.tree.arg_dict['y_dim'] - mouse_y) + 1
                pyautogui.move(delta_x, 0)
                pyautogui.move(0, delta_y)

            l_border = b_border = r_border = self.configurations['x_dim']['offset']  # { left, bottom, right } borders
            t_border = self.configurations['y_dim']['offset']  # { top } border

            self.tree.arg_dict['w_dim'] = requested_monitor['w_dim'] - (l_border + r_border)
            self.tree.arg_dict['h_dim'] = requested_monitor['h_dim'] - (t_border + b_border)
            self.tree.arg_dict['x_dim'] = requested_monitor['x_dim']
            self.tree.arg_dict['y_dim'] = requested_monitor['y_dim']

            self.tree.update_parameters()
            self.textbox.print_trees_now()

            self.tree.arg_dict['maximized'] = False
            self.window_manager_frame._maximize()

            self.root.geometry('{}x{}+{}+{}'.format(
                self.tree.arg_dict['w_dim'],
                self.tree.arg_dict['h_dim'],
                self.tree.arg_dict['x_dim'],
                self.tree.arg_dict['y_dim']
            ))
            if curr_monitor != requested_monitor:
                pyautogui.moveTo(mouse_x, mouse_y)

    def root_change(self):
        if self.have_root_dimensions_changed():
            before = (f"{self.winfo_width()}x{self.winfo_height()}+"
                      f"{self.winfo_rootx()}+{self.winfo_rooty()}")
            self.tree.arg_dict['w_dim'] = self.winfo_width()
            self.tree.arg_dict['width'] = self.convert_w_dim()

            self.tree.arg_dict['h_dim'] = self.winfo_height()

            self.tree.arg_dict['x_dim'] = self.winfo_rootx()
            # if abs(self.tree.arg_dict['x_dim'] - self.winfo_rootx()) == self.configurations['x_dim']['offset']:
            #     if self.tree.arg_dict['x_dim'] == self.configurations['x_dim']['offset']:
            #         print('  subtracting offset from x_dim')
            #         self.tree.arg_dict['x_dim'] -= self.configurations['x_dim']['offset']

            self.tree.arg_dict['y_dim'] = self.winfo_rooty()
            # if abs(self.tree.arg_dict['y_dim'] - self.winfo_rooty()) == self.configurations['y_dim']['offset']:
            #     if self.tree.arg_dict['y_dim'] == self.configurations['y_dim']['offset']:
            #         print('  subtracting offset from y_dim')
            #         self.tree.arg_dict['y_dim'] -= self.configurations['y_dim']['offset']
            # if abs(self.tree.arg_dict['y_dim'] - self.winfo_rooty()) == ((54 / 2) - 4):
            #     self.tree.arg_dict['y_dim'] -= 23

            # self.correct_height()

            after = (f"{self.tree.arg_dict['w_dim']}x{self.tree.arg_dict['h_dim']}+"
                     f"{self.tree.arg_dict['x_dim']}+{self.tree.arg_dict['y_dim']}")

            if before != after:
                if self.tree.arg_dict['verbose'] and before != after:
                    print('root: setting', before, '=>', after)

            # self._create_dimensions()
            # self.root.geometry('{}x{}+{}+{}'.format(
            #     self.tree.arg_dict['w_dim'],
            #     self.tree.arg_dict['h_dim'],
            #     self.tree.arg_dict['x_dim'],
            #     self.tree.arg_dict['y_dim']
            # ))

    def window_change(self, event=None):
        if self.winfo_width() is not 1:
            if self.tree.arg_dict['verbose']:
                # print(_) # prints the <event> parameter
                before_w = self.tree.arg_dict['w_dim']
                before_h = self.tree.arg_dict['h_dim']
                before_x = self.tree.arg_dict['x_dim']
                before_y = self.tree.arg_dict['y_dim']
            if not self.offsets_are_set:
                self.offsets_are_set = True
                self._create_default_file()

            if event.widget.winfo_id() == self.textbox.winfo_id():
                self.textbox_change()
            elif event.widget.winfo_id() == self.root.winfo_id():
                self.root_change()

            if self.tree.arg_dict['verbose']:
                print_change('\t   gui width', before_w, self.tree.arg_dict['w_dim'])
                print_change('\t  gui height', before_h, self.tree.arg_dict['h_dim'])
                print_change('\tgui x offset', before_x, self.tree.arg_dict['x_dim'])
                print_change('\tgui y offset', before_y, self.tree.arg_dict['y_dim'])
