import tkinter as tk
import tkinter.font as tkf
import time


def run_gui(textbox, my_tree, tree_list, index, max_len):
    # continuous loop that iterates through the list of trees
    # while True:
    #     for curr_tree in range(max_len):
    textbox.insert('0.0', tree_list[index] + '\n')
    # pause execution for the time specified in the --speed argument provided.
    textbox.after(int(my_tree.sleep_time * 1000), run_gui, textbox, my_tree, tree_list, (index + 1) % max_len, max_len)


def gui(my_tree, tree_list, max_len):
    root = tk.Tk()
    root.title('')
    # root.overrideredirect(1)
    root.configure(borderwidth='0')
    root.geometry('820x820+0+0')
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    close_button = tk.Button(root, text='X', command=root.destroy)
    close_button.pack(side=tk.RIGHT, fill=tk.Y)

    text_font = tkf.Font(family='DejaVu Sans fixed', slant='roman', size=-12)
    textbox = tk.Text(root, fg='green', background='#000000', height=1000, width=50, wrap='none', font=text_font)
    textbox.pack(fill=tk.BOTH)
    textbox.config(yscrollcommand=scrollbar.set)
    print(tkf.families())
    # print the first 6 upon execution to immediately fill the screen with snowy trees
    initial_tree_str = ''
    for curr_tree in range(6):
        initial_tree_str += tree_list[curr_tree] + '\n'
    textbox.insert(tk.END, initial_tree_str)

    run_gui(textbox, my_tree, tree_list, 6, max_len)
    root.mainloop()
