import time
# from tkinter.font import Font
from tkinter import *

from sample import file_helper, parameters, Tree


def run_interface():
    my_tree = Tree.Tree(parameters.retrieve())
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
        self.toolbar_buttons = None
        self._defined = ['file', 'options', 'fonts']
        self.opened_frame = None

        self._create()

    def _create(self):
        self.set_font()
        self.toolbar_buttons = ToolbarButtonsFrame(self)

    def set_font(self, value=None):
        new_font_key = (value, self.gui.tree.arg_dict['toolbar'])[value is None]
        self._font = parameters.font_dict()['toolbar'][new_font_key]
        # print('Toolbar metrics:\t', self._font.metrics())                        # TODO: test on [windows 10, mac OSX]
        if value is not None:
            self.gui.tree.arg_dict['toolbar'] = new_font_key
            self.opened_frame.update_font(new_font_key)
            self.toolbar_buttons.set_font(new_font_key)

    def close_frame(self):
        if self.opened_frame is not None:
            # self.opened_frame.grid_forget()
            self.opened_frame.pack_forget()
            self.opened_frame = None

    def get_font(self):
        return self._font

    def get_defined(self):
        return self._defined


class ToolbarButtonsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black', highlightthickness=0)
        self.pack(side=TOP, fill=X, expand=True)  # .grid(row=0, column=0, sticky=NW + SE)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.parent.get_font()
        self.buttons = {}
        self.configurations = {}

        self.create()

    def create(self):
        self.set_font()
        self.set_configurations()

        for index, curr in enumerate(self.parent.get_defined()):
            _text = self.configurations[curr]['text_string']
            _command = self.configurations[curr]['command']
            self.buttons[curr] = Button(self, font=self._font, bg='#000000', fg='#ffffff',
                                        activebackground='#444444', activeforeground='#cccccc',
                                        highlightthickness=0, text=_text, command=_command)
            self.buttons[curr].grid(row=0, column=index, sticky=NW + SE)

    def set_font(self, value=None):
        new_font_key = (value, self.gui.tree.arg_dict['toolbar'])[value is None]
        self._font = parameters.font_dict()['toolbar'][new_font_key]
        for key in self.buttons.keys():
            self.buttons[key].config(font=self._font)

    def set_configurations(self):
        self.configurations['file'] = {'text_string': 'File', 'command': self.click_file}
        self.configurations['options'] = {'text_string': 'Options', 'command': self.click_options}
        self.configurations['fonts'] = {'text_string': 'Fonts', 'command': self.click_view}

    def click_file(self):
        is_closed = False if type(self.parent.opened_frame) is FileFrame else True
        self.parent.close_frame()
        if is_closed:
            # opens the FontsFrame and sets the 'view' boolean to True
            self.parent.opened_frame = FileFrame(self)

    def click_options(self):
        is_closed = False if type(self.parent.opened_frame) is OptionsFrame else True
        self.parent.close_frame()
        if is_closed:
            # opens the OptionsFrame and sets the 'options' boolean to True
            self.parent.opened_frame = OptionsFrame(self)

    def click_view(self):
        is_closed = False if type(self.parent.opened_frame) is FontsFrame else True
        self.parent.close_frame()
        if is_closed:
            # opens the FontsFrame and sets the 'view' boolean to True
            self.parent.opened_frame = FontsFrame(self)


class FileFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.parent, bg='black', highlightthickness=0)
        self.pack(side=BOTTOM, fill=X, expand=True)  # .grid(row=1, column=0, sticky=NW + SE, fill=X, expand=True)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.gui.toolbar_frame.get_font()
        self._defined = ['save', 'open']
        self.buttons = {}
        self.opened_frame = None
        self.save_description = None
        self.save_label = None
        self.save_entry = None

        self.create()

    def create(self):
        self.create_save_label(1)
        self.create_save_description(2)
        self.create_save_text(3)

    def create_save_label(self, _row):
        self.save_label = Label(self, text='Save your configurations as:', bg='#aaaaaa', fg='#3d008e',
                                highlightthickness=0, font=self._font)
        self.save_label.grid(row=_row, column=0, sticky=NW + SE)

    def create_save_description(self, _row):
        self.save_description = Label(self, text='(omit filename extension)', bg='#aaaaaa', fg='#3d008e',
                                      highlightthickness=0, font=self._font)
        self.save_description.grid(row=_row, column=0, sticky=NW + SE)

    def create_save_text(self, _row):
        self.save_entry = Entry(self, bg='#aaaaaa', fg='#3d008e', width=28,
                                highlightthickness=0, font=self._font)
        for _enter_button in ['<Return>', '<KP_Enter>']:
            self.save_entry.bind(_enter_button,
                                 (lambda event:
                                  file_helper.export_file_as(self.save_entry.get(), self.gui.tree.arg_dict)))
        self.save_entry.grid(row=_row, column=0, sticky=NW)


class FontsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.parent, bg='black', highlightthickness=0)
        self.pack(side=BOTTOM, fill=X, expand=True)  # .grid(row=1, column=0, sticky=NW + SE, fill=X, expand=True)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.gui.toolbar_frame.get_font()

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
        # print('FontsFrame: Changed font on all visible toolbar children')

    def set_view_textbox(self, _row):
        self.textbox_label = Label(self, text='Textbox', bg='#aaaaaa', fg='#3d008e',
                                   highlightthickness=0, font=self._font, relief=FLAT)
        self.textbox_label.grid(row=_row, column=0, sticky=NW + SE)  # .pack(side=TOP, fill=X, expand=True)

        self.textbox_scale = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                   bg='#aaaaaa', fg='#3d008e', activebackground='#00ff80', troughcolor='#aaaaaa',
                                   showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                   to=len(parameters.textbox_font_choices()), command=self.set_textbox)
        self.textbox_scale.set(self.int_textbox)
        self.textbox_scale.grid(row=_row + 1, column=0, sticky=NW + SE)

    def set_view_toolbar(self, _row):
        self.toolbar_label = Label(self, text='Toolbar', bg='#333333', fg='#00d165',
                                   highlightthickness=0, font=self._font, relief=FLAT)
        self.toolbar_label.grid(row=_row, column=0, sticky=NW + SE)

        self.toolbar_scale = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                   bg='#333333', fg='#00d165', activebackground='#3d008e', troughcolor='#333333',
                                   showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                   to=len(parameters.toolbar_font_choices()), command=self.set_toolbar)
        self.toolbar_scale.set(self.int_toolbar)
        self.toolbar_scale.grid(row=_row + 1, column=0, sticky=NW + SE)

    def set_view_windows(self, _row):
        self.windows_label = Label(self, text='Window Manager', bg='#aaaaaa', fg='#3d008e',
                                   highlightthickness=0, font=self._font, relief=FLAT)
        self.windows_label.grid(row=_row, column=0, sticky=NW + SE)

        self.windows_scale = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                   bg='#aaaaaa', fg='#3d008e', activebackground='#00ff80', troughcolor='#aaaaaa',
                                   showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                   to=len(parameters.windows_font_choices()), command=self.set_windows)
        self.windows_scale.set(self.int_windows)
        self.windows_scale.grid(row=_row + 1, column=0, sticky=NW + SE)

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
        Frame.__init__(self, parent.parent, bg='black', highlightthickness=0)
        self.pack(side=BOTTOM, fill=X, expand=True)  # .grid(row=1, column=0, sticky=NW + SE, fill=X, expand=True)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.gui.toolbar_frame.get_font()

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
        self.opt_speed_label.grid(row=_row, column=0, sticky=NW + SE)

        self.opt_speed = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                               bg='#aaaaaa', fg='#3d008e', activebackground='#00ff80', troughcolor='#aaaaaa',
                               showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                               to=len(parameters.speed_choices()), command=self.set_speed)
        self.opt_speed.set(self.int_speed)
        self.opt_speed.grid(row=_row + 1, column=0, sticky=NW + SE)

    def set_opt_density(self, _row):
        self.opt_density_label = Label(self, text='Snow Density', bg='#333333', fg='#00d165',
                                       highlightthickness=0, font=self._font, relief=FLAT)
        self.opt_density_label.grid(row=_row, column=0, sticky=NW + SE)

        self.opt_density = Scale(self, label=None, font=self._font, orient=HORIZONTAL, bd=0,
                                 bg='#333333', fg='#00d165', activebackground='#3d008e', troughcolor='#333333',
                                 showvalue=0, relief=FLAT, highlightthickness=0, from_=1,
                                 to=len(parameters.speed_choices()), command=self.set_density)
        self.opt_density.set(self.int_density)
        self.opt_density.grid(row=_row + 1, column=0, sticky=NW + SE)

    def set_opt_tiers(self, _row):
        self.opt_tiers_label = Label(self, text='Tree Tiers', bg='#aaaaaa', fg='#3d008e',
                                     highlightthickness=0, font=self._font, relief=FLAT)
        self.opt_tiers_label.grid(row=_row, column=0, sticky=NW + SE)

        self.opt_tiers = Scale(self, label=None, font=self._font, bg='#aaaaaa', fg='#3d008e',
                               from_=1, to=13, bd=0, showvalue=0, orient=HORIZONTAL, relief=FLAT, highlightthickness=0,
                               activebackground='#00ff80', troughcolor='#aaaaaa', command=self.set_tiers)
        self.opt_tiers.set(self.int_tiers)
        self.opt_tiers.grid(row=_row + 1, column=0, sticky=NW + SE)

    def set_opt_ornaments(self, _row):
        self.opt_ornaments_label = Label(self, text='Ornaments', bg='#333333', fg='#00d165',
                                         highlightthickness=0, font=self._font, relief=FLAT)
        self.opt_ornaments_label.grid(row=_row, column=0, sticky=NW + SE)

        self.set_opt_ornaments_frame(_row + 1)

    def set_opt_ornaments_frame(self, _row):
        self.opt_ornaments_frame = Frame(self, bg='#ffffff')
        self.opt_ornaments_frame.grid(row=_row, column=0, sticky=NW + SE)

        button_on = (FLAT, RIDGE)[self.ornaments_bool]
        self.opt_ornaments_on = Button(self.opt_ornaments_frame, text='On', highlightthickness=0, width=6,
                                       font=self._font, relief=button_on, bg='#333333', fg='#00d165',
                                       activebackground='#333333', activeforeground='#00d165',
                                       command=lambda: self.set_ornaments(True))
        self.opt_ornaments_on.pack(side=LEFT, fill=X, expand=True)

        button_off = (RIDGE, FLAT)[self.ornaments_bool]
        self.opt_ornaments_off = Button(self.opt_ornaments_frame, text='Off', highlightthickness=0, width=6,
                                        font=self._font, relief=button_off, bg='#333333', fg='#00d165',
                                        activebackground='#333333', activeforeground='#00d165',
                                        command=lambda: self.set_ornaments(False))
        self.opt_ornaments_off.pack(side=LEFT, fill=X, expand=True)

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
        Text.__init__(self, parent, fg='green', background='black', wrap='none', highlightthickness=0)
        self.pack(fill=BOTH, expand=True)

        self.gui = parent

        self._font = None
        self.set_font()

    def set_font(self, value=None):  # TODO {24, 19, 18, 17  |  0  |  -15 -11 -4 -3 -2})
        new_font_key = (value, self.gui.tree.arg_dict['textbox'])[value is None]
        self._font = parameters.font_dict()['textbox'][new_font_key]
        self.config(font=self._font)
        # print('Textbox metrics:\t', self._font.metrics())                        # TODO: test on [windows 10, mac OSX]
        if value is not None:
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
        self.w_dim = self._convert_width_to_pixels()
        if self.tree.arg_dict['textbox'] == 'small':
            self.h_dim = ((48 * self.tree.tree_tiers) + 53) * 2
        elif self.tree.arg_dict['textbox'] == 'medium':
            self.h_dim = int(self.tree.screen_height * 13 * 2)  # prints 2 trees
        self.x_dim = self.winfo_x()
        self.y_dim = self.winfo_y()

        self.set_root()

        self.textbox.print_trees_now()  # immediately fills the current GUI window with trees
        self.textbox.run_gui()  # continue execution

    def _convert_width_to_pixels(self):
        return (self.tree.screen_width + self.tree.make_even) * 6

    def _convert_pixels_to_width(self):
        return self.w_dim // 6

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
            self.reset_tree('width', self._convert_pixels_to_width())
            print_change('Window Width', before, self.tree.screen_width)

    def reset_tree(self, key, value):
        self.tree.arg_dict[key] = value
        self.tree.update_parameters()
        self.textbox.print_trees_now()

    def window_change(self, _):
        if self.tree.arg_dict['verbose']:
            # print(_)
            before_w = self.w_dim
            before_h = self.h_dim
            before_x = self.x_dim
            before_y = self.y_dim

        self.w_dim = self.winfo_width()
        if self.tree.screen_width != self._convert_pixels_to_width():
            # does not reset tree for every pixel change in width
            self.set_screen_width()

        self.h_dim = self.winfo_height()
        self.x_dim = self.winfo_rootx()
        self.y_dim = self.winfo_rooty()
        self.root.geometry('{}x{}'.format(self.w_dim, self.h_dim))

        if self.tree.arg_dict['verbose']:
            print_change('\t   gui width', before_w, self.w_dim)
            print_change('\t  gui height', before_h, self.h_dim)
            print_change('\tgui x offset', before_x, self.x_dim)
            print_change('\tgui y offset', before_y, self.y_dim)


def print_change(type_of, before, after):
    """Prints the changed option to the console with before and after values"""
    if str(before) != str(after):
        print(f'{type_of}: {before} => {after}')
