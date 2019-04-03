from tkinter import *

from sample.parameters import font_dict


class WindowManagerFrame(Frame):
    """Creates a Frame for the [Minimize, Maximize, Close] buttons in the top-right corner of the GUI"""
    def __init__(self, parent):
        Frame.__init__(self, parent, highlightthickness=0)
        self.place(relx=1, rely=0, anchor=NE)

        self.gui = parent
        self.root = self.gui.root

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
        self.configurations['maximize'] = {'text_char': '+', 'command': self.maximize}
        self.configurations['minimize'] = {'text_char': '−', 'command': self._minimize}

    def set_font(self, value=None):
        new_font_key = (value, self.gui.tree.arg_dict['windows'])[value is None]
        self._font = font_dict()['windows'][new_font_key]
        # print('WindowManager metrics:\t', self._font.metrics())                  # TODO: test on [windows 10, mac OSX]
        if value is not None:
            self.gui.tree.arg_dict['windows'] = new_font_key
            for key in self.buttons.keys():
                self.buttons[key].config(font=self._font)
                # print('WindowManager: Changed font on', key, 'button')

    def _close(self):
        self.root.destroy()

    def maximize(self):
        if self.gui.tree.arg_dict['verbose']:
            print('maximize:', self.gui.tree.arg_dict['maximized'], '=>', not self.gui.tree.arg_dict['maximized'])

        self.gui.tree.arg_dict['maximized'] = not self.gui.tree.arg_dict['maximized']
        self.root.wm_attributes('-zoomed', self.gui.tree.arg_dict['maximized'])  # Should work on all OS
        # self.root.overrideredirect(self.gui.tree.arg_dict['maximized'])  # No borders or title bar
        # self.root.call('wm', 'attributes', '.', '-fullscreen', f'{self.gui.tree.arg_dict["maximized"]}')

    def _minimize(self):
        if self.gui.tree.arg_dict['maximized']:
            self.maximize()
            print('WMF._minimize:\n\tMaximized => not Maximized, then Minimized')
        self.root.state('iconic')
