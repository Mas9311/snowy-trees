from tkinter import *

from sample.file_helper import export_file_as


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
                                  export_file_as(self.save_entry.get(), self.gui.tree.arg_dict)))
        self.save_entry.grid(row=_row, column=0, sticky=NW)
