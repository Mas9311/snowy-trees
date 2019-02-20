#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from sample import parameters, Tree

if __name__ == '__main__':
    # create a template for the Tree
    my_tree = Tree.Tree(parameters.retrieve())

    # max length of list to compute
    max_len = 10

    # creates a list of 10 unique snow/ornament arrangements
    tree_list = my_tree.build_list(max_len)

    # print the first 6 upon execution (to fill the screen)
    for curr_tree in range(6):
        print(tree_list[curr_tree])

    # continuous loop that iterates through the list of trees
    while True:
        for curr_tree in range(max_len):
            print(tree_list[curr_tree])
            # pause execution for the time specified in the --speed argument
            time.sleep(my_tree.sleep_time)
