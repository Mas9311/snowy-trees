#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from sample import parameters, Tree

if __name__ == '__main__':
    my_tree = Tree.Tree(parameters.retrieve())
    max_len = 10
    tree_list = my_tree.build_list(max_len)

    for curr_tree in range(6):
        print(tree_list[curr_tree])

    while True:
        for curr_tree in range(max_len):
            print(tree_list[curr_tree])
            print(curr_tree)
            time.sleep(my_tree.sleep_time)
