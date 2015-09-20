#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
# Description:
# Author: hao.003.hao@gmail.com
# Last Modified Time: 2015-06-15, 16:08:18
"""

# ------ Import & Param ------ #

import os
import sys
import random

# ------ Sub Functions ------ #
def load_position_bias(filename):
    position_bias = {}
    ptr = open(filename)
    for line in ptr:
        terms = line.strip().split('\t')
        position_bias[int(terms[0])] = float(terms[1])
    return position_bias


def load_query_item_ctr(filename):
    query_item_ctr = {}
    ptr = open(filename)
    for line in ptr:
        terms = line.strip().split('\t')
        query_item_ctr[terms[0]] = float(terms[1])
    return query_item_ctr


def generate_data(filename, position_bias, query_item_ctr):
    show_dict = {}
    ptr = open(filename)
    for line in ptr:
        terms = line.strip().split('\t')
        query_item = terms[0]
        position = int(terms[1])
        show = int(terms[2])
        for i in range(show):
            rand_val = random.random()
            if rand_val < position_bias[position] * query_item_ctr[query_item]:
                print "%s\t%d\t1" % (query_item, position)
            else:
                print "%s\t%d\t0" % (query_item, position)
    return 0


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: " + sys.argv[0] + " position_bias query_item_ctr show_dict\n")
        return -1
    position_bias = load_position_bias(sys.argv[1])
    query_item_ctr = load_query_item_ctr(sys.argv[2])
    generate_data(sys.argv[3], position_bias, query_item_ctr)
    return 0


if __name__ == "__main__":
    main()
