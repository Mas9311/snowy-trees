#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from sample import parameters, Tree

if __name__ == '__main__':
    args_to_parse = parameters.retrieve()
    unknown_args = args_to_parse.parse_known_args()[1]
    if unknown_args:
        args_to_parse.print_help()
        print('\nThe argument(s)', unknown_args, 'are not valid.')
        input('\nPress [Enter] to quit\n>')
        args_to_parse.parse_args()
        raise Exception('Unknown arguments')  # Redundant Exception to ensure failure
    my_tree = Tree.Tree(args_to_parse.parse_args())
    count = 0
    while True:
        print(my_tree)
        if count <= 5:
            count += 1
            continue
        time.sleep(my_tree.sleep_time)
