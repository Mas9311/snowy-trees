#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from sample import parameters, Tree

if __name__ == '__main__':
    """The controller of the execution. Retrieves the parsed arguments, and if they're valid, create a list of
    25 Trees (each with their own unique snow/ornament arrangements), then loop the same 25 forever."""
    known_args_dict = parameters.retrieve()

    # creates the template of the Tree to print; snow & ornaments are unique upon printing.
    my_tree = Tree.Tree(known_args_dict)

    # max length of list to compute. This will save you energy from each snowflake's numpy.random call.
    max_len = 25

    # creates a list of 25 unique snow/ornament arrangements
    tree_list = my_tree.build_list(max_len)

    # print the first 6 upon execution to immediately fill the screen with snowy trees
    for curr_tree in range(6):
        print(tree_list[curr_tree])

    # continuous loop that iterates through the list of trees
    while True:
        for curr_tree in range(max_len):
            print(tree_list[curr_tree])
            # pause execution for the time specified in the --speed argument provided.
            time.sleep(my_tree.sleep_time)
