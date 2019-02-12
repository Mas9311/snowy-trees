#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from sample import parameters, Tree

if __name__ == '__main__':
    my_tree = Tree.Tree(parameters.retrieve())
    count = 0
    while True:
        print(my_tree)
        if count > 6:
            time.sleep(my_tree.sleep_time)
        count += 1
