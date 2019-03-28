from tkinter import *

from sample import parameters, format


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
            format.print_change('Speed', before, self.curr_speed)

    def set_density(self, value):
        value = int(value)
        if self.int_density != value:
            before = self.curr_density
            self.int_density = value
            self.curr_density = parameters.density_choices()[self.int_density - 1]
            self.gui.reset_tree('density', self.curr_density)
            format.print_change('Density', before, self.curr_density)

    def set_tiers(self, value):
        value = int(value)
        if self.int_tiers != value:
            before = self.int_tiers
            self.int_tiers = value
            self.gui.reset_tree('tiers',  self.int_tiers)
            format.print_change('Tiers', before, self.int_tiers)

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
            format.print_change('Ornaments', before, self.ornaments_bool)
