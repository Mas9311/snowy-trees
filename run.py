#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from sample import parameters, Tree

if __name__ == '__main__':
    # parser = parameters.retrieve()
    my_tree = Tree.Tree(parameters.retrieve())
    # print(f'width    = {str(parser.parse_args().width)}\n'
    #       f'speed    = {str(parser.parse_args().speed)}\n'
    #       f'density  = {str(parser.parse_args().density)}\n'
    #       f'tiers    = {str(parser.parse_args().tiers)}\n'
    #       f'ornaments= {str(parser.parse_args().yes)}')
    count = 0
    while True:
        print(my_tree)
        if count > 6:
            time.sleep(my_tree.sleep_time)
        count += 1
