import tkinter as tk
import time


def run_gui(my_tree, tree_list, max_len):
    root = tk.Tk()
    root.title('')
    # root.overrideredirect(1)
    root.configure(borderwidth='0')
    # root.geometry('2552x1381')
    root.geometry('400x100+200+200')
    close_button = tk.Button(root, text='X', command=root.destroy)
    close_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    textbox = tk.Text(root, fg='green', background='#000000', font=12)
    textbox.pack()
    quote = """**********************"""
    textbox.insert(tk.END, quote)

    # print the first 6 upon execution to immediately fill the screen with snowy trees
    for curr_tree in range(6):
        # print(tree_list[curr_tree])
        textbox.insert(tk.END, quote)

    # continuous loop that iterates through the list of trees
    while True:
        for curr_tree in range(max_len):
            print(tree_list[curr_tree])
            # pause execution for the time specified in the --speed argument provided.
            time.sleep(my_tree.sleep_time)

    root.mainloop()