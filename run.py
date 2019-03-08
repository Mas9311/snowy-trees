#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *

from sample import interface

if __name__ == '__main__':
    """The controller of the execution. Retrieves the parsed arguments, and if they're valid, create a list of
    25 Trees (each with their own unique snow/ornament arrangements), then loop the same 25 forever."""
    root = Tk()
    tree_gui = interface.TreeGUI(root)
    root.mainloop()
