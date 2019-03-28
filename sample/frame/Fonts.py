from tkinter import *

from sample import parameters, format


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
            format.print_change('Textbox Font Size', before, self.curr_textbox)

    def set_toolbar(self, value):
        value = int(value)
        if self.int_toolbar != value:
            before = self.curr_toolbar
            self.int_toolbar = value
            self.curr_toolbar = parameters.toolbar_font_choices()[self.int_toolbar - 1]
            self.gui.toolbar_frame.set_font(self.curr_toolbar)
            format.print_change('Toolbar Font Size', before, self.curr_toolbar)

    def set_windows(self, value):
        value = int(value)
        if self.int_windows != value:
            before = self.curr_windows
            self.int_windows = value
            self.curr_windows = parameters.windows_font_choices()[self.int_windows - 1]
            self.gui.window_manager_frame.set_font(self.curr_windows)
            format.print_change('Windows Font Size', before, self.curr_windows)
