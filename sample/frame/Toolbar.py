from tkinter import Frame, NW, TOP, X, Button, SE

from sample import parameters
from sample.frame.File import FileFrame
from sample.frame.Fonts import FontsFrame
from sample.frame.Options import OptionsFrame


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