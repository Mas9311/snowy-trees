from tkinter import *

from sample.file_helper import export_file_as, list_config_files, import_from_file


class FileFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.parent, bg='black', highlightthickness=0)
        self.pack(side=LEFT, fill=X, expand=True)  # .grid(row=1, column=0, sticky=NW + SE, fill=X, expand=True)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.gui.toolbar_frame.get_font()
        self.color = self.parent.parent.get_color

        self._defined = ['save', 'open']
        self.buttons = {}
        self.configurations = {}
        self.opened_frame = None

        self.create()

    def create(self):
        """Creates the buttons in FileFrame._defined"""
        self.set_configurations()

        for i, curr in enumerate(self._defined):
            _text = self.configurations[curr]['text_string']
            _command = self.configurations[curr]['command']
            self.buttons[curr] = Button(self, font=self._font, text=_text, command=_command,
                                        bg=self.color('bg', i), fg=self.color('fg', i),
                                        activeforeground=self.color('fg', -1),
                                        activebackground=self.color('bg', -1),
                                        width=20, highlightthickness=0)
            self.buttons[curr].pack(anchor=NW)  # .grid(row=index, column=0, sticky=NW + SE)

    def set_configurations(self):
        self.configurations['save'] = {'text_string': 'Save As...', 'command': self.click_save}
        self.configurations['open'] = {'text_string': 'Open File', 'command': self.click_open}

    def click_save(self):
        is_closed = False if type(self.opened_frame) is SaveFrame else True
        self.close_frame()
        if is_closed:
            # opens the SaveFrame
            self.opened_frame = SaveFrame(self)

    def click_open(self):
        is_closed = False if type(self.opened_frame) is OpenFrame else True
        self.close_frame()
        if is_closed:
            # opens the OpenFrame
            self.opened_frame = OpenFrame(self)

    def close_frame(self):
        if self.opened_frame is not None:
            if self.gui.tree.arg_dict['verbose']:
                *_, f_type = str(self.opened_frame).split('.!')
                try:
                    int(f_type[-1])
                    f_type = f_type[:-1]
                except:
                    pass
                f_type = f'{f_type[0].upper()}{f_type[1:-5]} button\'s {f_type[-5].upper()}{f_type[-4:]}'
                print(f'Closing the {f_type}')

            self.opened_frame.pack_forget()
            self.opened_frame = None

    def get_defined_len(self):
        return len(self._defined)


class SaveFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black', highlightthickness=0)
        self.pack(fill=X, expand=True)  # .grid(row=1, column=0, sticky=NW + SE, fill=X, expand=True)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.gui.toolbar_frame.get_font()
        self.color = self.parent.color

        self._defined = ['save', 'open']
        self.save_label_1 = None
        self.save_label_2 = None
        self.save_entry = None

        self.create()

    def create(self):
        i = self.parent.get_defined_len()
        self.create_save_label(i)
        self.create_save_label_2(i + 1)
        self.create_save_text(i + 2)

    def create_save_label(self, i):
        self.save_label_1 = Label(self, text='Save your configurations as:',
                                  bg=self.color('bg', i), fg=self.color('fg', i), highlightthickness=0, font=self._font)
        self.save_label_1.pack(fill=X, expand=True)  # .grid(row=_row, column=0, sticky=NW + SE)

    def create_save_label_2(self, i):
        self.save_label_2 = Label(self, text='(omit filename extension)',
                                  bg=self.color('bg', i), fg=self.color('fg', i), highlightthickness=0, font=self._font)
        self.save_label_2.pack(fill=X, expand=True)  # .grid(row=_row, column=0, sticky=NW + SE)

    def create_save_text(self, i):
        self.save_entry = Entry(self, bg=self.color('bg', i), fg=self.color('fg', i), width=28,
                                highlightthickness=0, font=self._font)
        for _enter_button in ['<Return>', '<KP_Enter>']:
            self.save_entry.bind(_enter_button,
                                 (lambda event:
                                  export_file_as(self.save_entry.get(), self.gui.tree.arg_dict)))
        self.save_entry.pack(fill=X, expand=True)  # .grid(row=_row, column=0, sticky=NW)


class OpenFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black', highlightthickness=0)
        self.pack(side=RIGHT, fill=X, expand=True)  # .grid(row=1, column=0, sticky=NW + SE, fill=X, expand=True)

        self.parent = parent
        self.gui = self.parent.gui

        self._font = self.gui.toolbar_frame.get_font()
        self.color = self.parent.color

        self._defined = ['save', 'open']
        self._files = None

        self.create_buttons(len(self._defined) + 1)

    def create_open_label(self, _row):
        temp = Label(self, text='Click any buttons below\nto import the configs', bg='#aaaaaa', fg='#3d008e',
                                highlightthickness=0, font=self._font)
        temp.grid(row=_row, column=0, sticky=NW + SE)

    def create_buttons(self, _row):
        self._files = list_config_files()  # alphabetically sorted list of configuration files
        if self._files:
            self.create_open_label(_row)
            for i, file in enumerate(self._files, start=_row + 1):
                temp = Button(self, font=self._font, text=file, anchor=W, width=10, highlightthickness=0,
                              bg=self.color('bg', i+1), fg=self.color('fg', i+1),
                              activeforeground=self.color('fg', -1), activebackground=self.color('bg', -1),
                              command=lambda file=file: self.open_file(file))
                temp.grid(row=i, column=0, sticky=NW + SE)
        else:
            i = len(self._defined)
            temp = Label(self, text='No configuration files', highlightthickness=0, font=self._font,
                         bg=self.color('bg', i), fg=self.color('fg', i))
            temp.grid(row=_row, column=0, sticky=NW + SE)

    def open_file(self, filename):
        new_dict = import_from_file(filename)
        if self.gui.tree.arg_dict != new_dict:  # If they aren't the same
            if self.gui.tree.arg_dict['maximized']:  # If GUI is not maximized
                new_dict['width'] = self.gui.tree.arg_dict['width']  # update the width
            if not new_dict['maximized'] and self.gui.tree.arg_dict['maximized']:
                # self.gui.tree.arg_dict['maximized'] = False
                self.gui.window_manager_frame._maximize()
            if self.gui.tree.arg_dict != new_dict:  # if they still aren't the same after updating
                self.gui.tree.arg_dict = new_dict  # update the Tree's dict
                self.gui.reset_tree(key='new file')  # manually set the dimensions and print the new Tree.
        else:
            print('  ...But it has the same configurations as the current GUI\n')
