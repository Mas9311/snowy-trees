import time
# from tkinter.font import Font
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
        # immediately prints all trees too fill the CLI window with snowy trees
        for _ in range(min(self.tree.length, 50)):
            print(self.tree.list[self.tree.increment_index()])

        # continuous loop that iterates through the list of trees
        while True:
            print(self.tree.list[self.tree.increment_index()])
            # pause execution for the time specified in the --speed argument provided.
            time.sleep(self.tree.sleep_time)


class WindowManagerFrame(Frame):
    """Creates a Frame for the [Minimize, Maximize, Close] buttons in the top-right corner of the GUI"""
    def __init__(self, parent):
        Frame.__init__(self, parent, highlightthickness=0)
        self.place(relx=1, rely=0, anchor=NE)

        self.gui = parent
        self.root = self.gui.root

        self.maximized_bool = False
        self._font = None
        self._defined = ['minimize', 'maximize', 'close']
        self.buttons = {}         # Contains: close, maximize, minimize           # ?maybe: border
        self.configurations = {}  # Contains: close, maximize, minimize
        self._create()

    def _create(self):
        self.set_configurations()

        for (curr, _col) in zip(self._defined, range(len(self._defined))):
            _text = self.configurations[curr]['text_char']
            _command = self.configurations[curr]['command']
            self.buttons[curr] = Button(self, font=self._font, highlightthickness=0, text=_text, command=_command)
            self.buttons[curr].grid(row=0, column=_col)
            # print(f'WMF: Created the \'{curr}\' button.')

    def set_configurations(self):
        self.set_font()
        self.configurations['close'] = {'text_char': '×', 'command': self._close}
        self.configurations['maximize'] = {'text_char': '+', 'command': self._maximize}
        self.configurations['minimize'] = {'text_char': '−', 'command': self._minimize}

    def set_font(self, value=None):
        new_font_key = (value, self.gui.tree.arg_dict['windows'])[value is None]
        self._font = parameters.font_dict()['windows'][new_font_key]
        # print('WindowManager metrics:\t', self._font.metrics())                  # TODO: test on [windows 10, mac OSX]
        if value is not None:
            self.gui.tree.arg_dict['windows'] = new_font_key
            for key in self.buttons.keys():
                self.buttons[key].config(font=self._font)
                # print('WindowManager: Changed font on', key, 'button')

    def _close(self):
        self.root.destroy()

    def _maximize(self):
        self.maximized_bool = not self.maximized_bool
        self.root.overrideredirect(self.maximized_bool)  # No borders or title bar
        self.root.call('wm', 'attributes', '.', '-fullscreen', f'{self.maximized_bool}')

    def _minimize(self):
        if self.maximized_bool:
            self._maximize()
            # print('WMF._minimize:\n\tMaximized => not Maximized, then Minimized')
        self.root.state('iconic')


class ToolbarFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black', highlightthickness=0)
        self.place(relx=0, rely=0, anchor=NW)

        self.gui = parent

        self._font = None
        self._defined = ['options', 'view']
        self.buttons = {}
        self.configurations = {}
        self.frames = {}
        self.bools = {}

        self._create()

    def _create(self):
        self.set_configurations()

        for curr in zip(range(len(self._defined)), self._defined):
            self.bools[curr[1]] = False
            _text = self.configurations[curr[1]]['text_string']
            _command = self.configurations[curr[1]]['command']
            self.buttons[curr[0]] = Button(self, font=self._font, bg='#000000', fg='#ffffff',
                                           activebackground='#444444', activeforeground='#cccccc',
                                           highlightthickness=0, text=_text, command=_command)
            self.buttons[curr[0]].grid(row=0, column=curr[0], sticky=N + W + S)

    def set_configurations(self):
        self.set_font()
        self.configurations['options'] = {'text_string': 'options', 'command': self.click_options}
        self.configurations['view'] = {'text_string': 'view', 'command': self.click_view}

    def close_frames(self):
        for key in self._defined:
            if self.bools[key]:
                self.frames[key].grid_forget()
            self.bools[key] = False

    def set_font(self, value=None):
        new_font_key = (value, self.gui.tree.arg_dict['toolbar'])[value is None]
        self._font = parameters.font_dict()['toolbar'][new_font_key]
        # print('Toolbar metrics:\t', self._font.metrics())                        # TODO: test on [windows 10, mac OSX]
        if value is not None:
            self.gui.tree.arg_dict['toolbar'] = new_font_key
            for key in self.buttons.keys():
                self.buttons[key].config(font=self._font)
            self.frames['view'].update_font(new_font_key)

    def get_font(self):
        return self._font

    def click_options(self):
        _curr = 'options'
        is_open = not self.bools[_curr]
        self.close_frames()
        if is_open:
            # opens the OptionsFrame and sets the 'options' boolean to True
            self.frames[_curr] = OptionsFrame(self)
            self.bools[_curr] = True

    def click_view(self):
        _curr = 'view'
        is_open = not self.bools[_curr]
        self.close_frames()
        if is_open:
            # opens the ViewFrame and sets the 'view' boolean to True
            self.frames[_curr] = ViewFrame(self)
            self.bools[_curr] = True


class ViewFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black', highlightthickness=0)
        self.grid(row=1, column=0)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.parent.get_font()

        self.curr_textbox = None
        self.int_textbox = None
        self.textbox_label = None
        self.textbox_scale = None

        self.int_toolbar = None
        self.curr_toolbar = None
        self.toolbar_label = None
        self.toolbar_scale = None

        self.int_windows = None
        self.curr_windows = None
        self.windows_label = None
        self.windows_scale = None

        self._create()

    def _create(self):
        fonts = parameters.textbox_font_choices()
        self.int_textbox = fonts.index(self.gui.tree.arg_dict['textbox']) + 1
        self.curr_textbox = fonts[self.int_textbox - 1]

        fonts = parameters.toolbar_font_choices()
        self.int_toolbar = fonts.index(self.gui.tree.arg_dict['toolbar']) + 1
        self.curr_toolbar = fonts[self.int_toolbar - 1]

        fonts = parameters.windows_font_choices()
        self.int_windows = fonts.index(self.gui.tree.arg_dict['windows']) + 1
        self.curr_windows = fonts[self.int_windows - 1]

        self.set_view_textbox(1)
        self.set_view_toolbar(3)
        self.set_view_windows(5)

    def update_font(self, new_font_key):
        self._font = parameters.font_dict()['toolbar'][new_font_key]
        self.textbox_label.config(font=self._font)
        self.textbox_scale.config(font=self._font)
        self.toolbar_label.config(font=self._font)
        self.toolbar_scale.config(font=self._font)
        self.windows_label.config(font=self._font)
        self.windows_scale.config(font=self._font)
        # print('ViewFrame: Changed font on all buttons in sight')

    def set_view_textbox(self, _row):
        self.textbox_label = Label(self, text='Textbox Font Size', bg='#aaaaaa', fg='#3d008e',
                                   highlightthickness=0, font=self._font, relief=FLAT)
        self.textbox_label.grid(row=_row, column=0, sticky=W + E)

        self.textbox_scale = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                   bg='#aaaaaa', fg='#3d008e', activebackground='#00ff80', troughcolor='#aaaaaa',
                                   showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                   to=len(parameters.textbox_font_choices()), command=self.set_textbox)
        self.textbox_scale.set(self.int_textbox)
        self.textbox_scale.grid(row=_row + 1, column=0, sticky=W + E)

    def set_view_toolbar(self, _row):
        self.toolbar_label = Label(self, text='Toolbar Font Size', bg='#333333', fg='#00d165',
                                   highlightthickness=0, font=self._font, relief=FLAT)
        self.toolbar_label.grid(row=_row, column=0, sticky=W + E)

        self.toolbar_scale = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                   bg='#333333', fg='#00d165', activebackground='#3d008e', troughcolor='#333333',
                                   showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                   to=len(parameters.toolbar_font_choices()), command=self.set_toolbar)
        self.toolbar_scale.set(self.int_toolbar)
        self.toolbar_scale.grid(row=_row + 1, column=0, sticky=W + E)

    def set_view_windows(self, _row):
        self.windows_label = Label(self, text='Windows Font Size', bg='#aaaaaa', fg='#3d008e',
                                   highlightthickness=0, font=self._font, relief=FLAT)
        self.windows_label.grid(row=_row, column=0, sticky=W + E)

        self.windows_scale = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                   bg='#aaaaaa', fg='#3d008e', activebackground='#00ff80', troughcolor='#aaaaaa',
                                   showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                   to=len(parameters.windows_font_choices()), command=self.set_windows)
        self.windows_scale.set(self.int_windows)
        self.windows_scale.grid(row=_row + 1, column=0, sticky=W + E)

    def set_textbox(self, value):
        value = int(value)
        if self.int_textbox != value:
            before = self.curr_textbox
            self.int_textbox = value
            self.curr_textbox = parameters.textbox_font_choices()[self.int_textbox - 1]
            self.gui.textbox.set_font(self.curr_textbox)
            print_change('Textbox Font Size', before, self.curr_textbox)

    def set_toolbar(self, value):
        value = int(value)
        if self.int_toolbar != value:
            before = self.curr_toolbar
            self.int_toolbar = value
            self.curr_toolbar = parameters.toolbar_font_choices()[self.int_toolbar - 1]
            self.gui.toolbar_frame.set_font(self.curr_toolbar)
            print_change('Toolbar Font Size', before, self.curr_toolbar)

    def set_windows(self, value):
        value = int(value)
        if self.int_windows != value:
            before = self.curr_windows
            self.int_windows = value
            self.curr_windows = parameters.windows_font_choices()[self.int_windows - 1]
            self.gui.window_manager_frame.set_font(self.curr_windows)
            print_change('Windows Font Size', before, self.curr_windows)


class OptionsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black', highlightthickness=0)
        self.grid(row=1, column=0)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.parent.get_font()

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

        self._create()

    def _create(self):
        speeds = parameters.speed_choices()
        self.int_speed = speeds.index(self.gui.tree.arg_dict['speed']) + 1
        self.curr_speed = speeds[self.int_speed - 1]

        densities = parameters.density_choices()
        self.int_density = densities.index(self.gui.tree.arg_dict['density']) + 1
        self.curr_density = densities[self.int_density - 1]

        self.int_tiers = self.gui.tree.tree_tiers

        self.ornaments_bool = self.gui.tree.arg_dict['ornaments']

        # Create the rest of the options frame
        self.set_opt_speed(1)
        self.set_opt_density(3)
        self.set_opt_tiers(5)
        self.set_opt_ornaments(7)

    def set_opt_speed(self, _row):
        self.opt_speed_label = Label(self, text='Refresh Speed', bg='#aaaaaa', fg='#3d008e',
                                     highlightthickness=0, font=self._font, relief=FLAT, width=16)
        self.opt_speed_label.grid(row=_row, column=0, sticky=W + E)

        self.opt_speed = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                               bg='#aaaaaa', fg='#3d008e', activebackground='#00ff80', troughcolor='#aaaaaa',
                               showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                               to=len(parameters.speed_choices()), command=self.set_speed)
        self.opt_speed.set(self.int_speed)
        self.opt_speed.grid(row=_row + 1, column=0, sticky=W + E)

    def set_opt_density(self, _row):
        self.opt_density_label = Label(self, text='Snow Density', bg='#333333', fg='#00d165',
                                       highlightthickness=0, font=self._font, relief=FLAT)
        self.opt_density_label.grid(row=_row, column=0, sticky=W + E)

        self.opt_density = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                 bg='#333333', fg='#00d165', activebackground='#3d008e', troughcolor='#333333',
                                 showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                 to=len(parameters.speed_choices()), command=self.set_density)
        self.opt_density.set(self.int_density)
        self.opt_density.grid(row=_row + 1, column=0, sticky=W + E)

    def set_opt_tiers(self, _row):
        self.opt_tiers_label = Label(self, text='Tree Tiers', bg='#aaaaaa', fg='#3d008e',
                                     highlightthickness=0, font=self._font, relief=FLAT)
        self.opt_tiers_label.grid(row=_row, column=0, sticky=W + E)

        self.opt_tiers = Scale(self, label=None, font=self._font, bg='#aaaaaa', fg='#3d008e',
                               from_=1, to=13, bd=0, showvalue=0, orient=HORIZONTAL, relief=FLAT, highlightthickness=0,
                               activebackground='#00ff80', troughcolor='#aaaaaa', command=self.set_tiers)
        self.opt_tiers.set(self.int_tiers)
        self.opt_tiers.grid(row=_row + 1, column=0, sticky=W + E)

    def set_opt_ornaments(self, _row):
        self.opt_ornaments_label = Label(self, text='Ornaments', bg='#333333', fg='#00d165',
                                         highlightthickness=0, font=self._font, relief=FLAT)
        self.opt_ornaments_label.grid(row=_row, column=0, sticky=W + E)

        self.set_opt_ornaments_frame(_row + 1)

    def set_opt_ornaments_frame(self, _row):
        self.opt_ornaments_frame = Frame(self, bg='#ffffff')
        self.opt_ornaments_frame.grid(row=_row, column=0, sticky=W + E)

        button_on = (FLAT, RIDGE)[self.ornaments_bool]
        self.opt_ornaments_on = Button(self.opt_ornaments_frame, text='On', highlightthickness=0, width=6,
                                       font=self._font, relief=button_on, bg='#333333', fg='#00d165',
                                       activebackground='#333333', activeforeground='#00d165',
                                       command=lambda: self.set_ornaments(True))
        self.opt_ornaments_on.grid(row=0, column=0, sticky=N + E + W + S, ipadx=1)

        button_off = (RIDGE, FLAT)[self.ornaments_bool]
        self.opt_ornaments_off = Button(self.opt_ornaments_frame, text='Off', highlightthickness=0, width=6,
                                        font=self._font, relief=button_off, bg='#333333', fg='#00d165',
                                        activebackground='#333333', activeforeground='#00d165',
                                        command=lambda: self.set_ornaments(False))
        self.opt_ornaments_off.grid(row=0, column=1, sticky=N + E + W + S, ipadx=1)

    def set_speed(self, value):
        value = int(value)
        if self.int_speed != value:
            before = self.curr_speed
            self.int_speed = value
            self.curr_speed = parameters.speed_choices()[self.int_speed - 1]
            self.gui.reset_tree('speed', self.curr_speed)
            print_change('Speed', before, self.curr_speed)

    def set_density(self, value):
        value = int(value)
        if self.int_density != value:
            before = self.curr_density
            self.int_density = value
            self.curr_density = parameters.density_choices()[self.int_density - 1]
            self.gui.reset_tree('density', self.curr_density)
            print_change('Density', before, self.curr_density)

    def set_tiers(self, value):
        value = int(value)
        if self.int_tiers != value:
            before = self.int_tiers
            self.int_tiers = value
            self.gui.reset_tree('tiers',  self.int_tiers)
            print_change('Tiers', before, self.int_tiers)

    def set_ornaments(self, arg_bool):
        """Does not update if the currently-activated button is clicked again"""
        if arg_bool is not self.ornaments_bool:
            before = self.ornaments_bool
            self.ornaments_bool = arg_bool

            button_on = (FLAT, RIDGE)[self.ornaments_bool]
            self.opt_ornaments_on.configure(relief=button_on)
            button_off = (RIDGE, FLAT)[self.ornaments_bool]
            self.opt_ornaments_off.configure(relief=button_off)

            self.gui.reset_tree('ornaments', arg_bool)
            print_change('Ornaments', before, self.ornaments_bool)


class Textbox(Text):
    def __init__(self, parent):
        Text.__init__(self, parent, fg='green', background='black', wrap='none', highlightthickness=0,
                      font=parameters.font_dict()['textbox'][parent.tree.arg_dict['textbox']])
        self.pack(fill=BOTH, expand=True)

        self.gui = parent

    def set_font(self, value=None):  # TODO {24, 19, 18, 17  |  0  |  -15 -11 -4 -3 -2})
        new_font_key = (value, self.gui.tree.arg_dict['textbox'])[value is None]
        self.gui.textbox.configure(font=parameters.font_dict()['textbox'][new_font_key])
        self.gui.tree.arg_dict['textbox'] = new_font_key

    def print_trees_now(self):
        """Prints the (minimum + 1) number of trees in order to fill the height of the GUI window"""
        initial_tree_str = ''
        num_trees = (self.gui.h_dim // 13 // self.gui.tree.screen_height) + 2
        for _ in range(num_trees):
            initial_tree_str = self.gui.tree.list[self.gui.tree.increment_index()] + '\n' + initial_tree_str
        self.insert('0.0', initial_tree_str)

    def run_gui(self):
        """Recursive loop that prints the tree at the top of the GUI"""
        self.insert('0.0', self.gui.tree.list[self.gui.tree.increment_index()] + '\n')
        # pause execution for the time specified in the speed argument provided.
        self.after(int(self.gui.tree.sleep_time * 1000), self.run_gui)


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent
        self.root.configure(bd=0)

        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = Tree.Tree(parameters.retrieve())

        self.textbox = None
        self.window_manager_frame = None
        self.toolbar_frame = None
        self._create()

        self.update_idletasks()
        self.w_dim = (self.tree.screen_width + self.tree.make_even + 2) * 6
        if self.tree.arg_dict['textbox'] == 'small':
            self.h_dim = ((48 * self.tree.tree_tiers) + 53) * 2
        elif self.tree.arg_dict['textbox'] == 'medium':
            self.h_dim = int(self.tree.screen_height * 13 * 2)  # prints 2 trees
        self.x_dim = self.winfo_x()
        self.y_dim = self.winfo_y()

        self.set_root()

        self.textbox.print_trees_now()  # immediately fills the current GUI window with trees
        self.textbox.run_gui()  # continue execution

    def _create(self):
        self.textbox = Textbox(self)
        self.window_manager_frame = WindowManagerFrame(self)
        self.toolbar_frame = ToolbarFrame(self)

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        self.root.resizable(width=True, height=True)
        self.root.geometry('{}x{}+{}+{}'.format(self.w_dim, self.h_dim, self.x_dim, self.y_dim))

    def set_screen_width(self):
        before = self.tree.screen_width
        self.reset_tree('width', max(self.w_dim // 6 - 2, self.tree.tree_width + 1))
        print_change('Window Width', before, self.tree.screen_width)

    def reset_tree(self, key, value):
        self.tree.arg_dict[key] = value
        self.tree.update_parameters()
        self.textbox.print_trees_now()

    def window_change(self, event):
        # TODO -v --verbose => prints the dimensions upon adjusting
        # before = f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}'
        self.w_dim = self.winfo_width()
        if self.tree.screen_width is not self.w_dim // 6 - 2 and self.w_dim // 6 - 2 > self.tree.tree_width + 1:  # TODO
            self.set_screen_width()
        self.h_dim = self.winfo_height()
        self.x_dim = self.winfo_rootx()
        self.y_dim = self.winfo_rooty()
        self.root.geometry('{}x{}'.format(self.w_dim, self.h_dim))
        # print_change('\tDimensions', before, f'{self.w_dim}x{self.h_dim}+{self.x_dim}+{self.y_dim}')


def print_change(type_of, before, after):
    """Prints the changed option to the console with before and after values"""
    if str(before) != str(after):
        print(f'{type_of}: {before} => {after}')
