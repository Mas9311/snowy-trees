from tkinter import *

from sample.parameters import font_dict


class Textbox(Text):
    def __init__(self, parent):
        Text.__init__(self, parent, fg='green', background='black', wrap='none', highlightthickness=0)
        self.pack(fill=BOTH, expand=True)

        self.gui = parent

        self._font = None
        self.set_font()

    def set_font(self, value=None):  # TODO {24, 19, 18, 17  |  0  |  -15 -11 -4 -3 -2})
        new_font_key = (value, self.gui.tree.arg_dict['textbox'])[value is None]
        self._font = font_dict()['textbox'][new_font_key]
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
