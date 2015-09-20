#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
# Description:
# Author: chenhao21@baidu.com
# Last Modified Time: 2015-06-23, 11:00:02
"""

# ------ Import & Param ------ #

import os
import sys

# ------ Sub Functions ------ #
def cal_position_bias(position_list_file, train_dat_file):
    position_list = []
    ptr = open(position_list_file)
    for line in ptr:
        terms = line.strip().split("\t")
        position_key = terms[0]
        if 0 == position_list.count(position_key):
            position_list.append(position_key)
    ptr.close()

    position_click = {}
    position_show = {}
    position_bias = {}
    for i in range(len(position_list)):
        position_click[position_list[i]] = 0.0
        position_show[position_list[i]] = 0.0

    ptr = open(train_dat_file)
    for line in ptr:
        terms=line.strip().split('\t')
        position = terms[1]
        if 0 == position_list.count(position):
            continue
        position_click[position] += float(terms[2])
        position_show[position] += 1.0
    if 0 != position_show[position_list[0]]:
        base_ctr = position_click[position_list[0]] / position_show[position_list[0]]
    else:
        return -1
    if 0.0 == base_ctr:
        return -1
    for i in range(len(position_list)):
        if 0 != position_show[position_list[i]]:
            ctr = position_click[position_list[i]] / position_show[position_list[i]]
            position_bias[position_list[i]] =  ctr / base_ctr
    ptr.close()
    #print position_bias
    return position_bias, position_list


def cal_query_item_ctr(query_item_list_file, train_dat_file, position_bias, position_list):
    query_item_list = []
    ptr = open(query_item_list_file)
    for line in ptr:
        terms = line.strip().split("\t")
        query_item_key = terms[0]
        if 0 == query_item_list.count(query_item_key):
            query_item_list.append(query_item_key)
    ptr.close()

    show_dict = {}
    click_dict = {}
    ctr_dict = {}
    ptr = open(train_dat_file)
    for line in ptr:
        terms=line.strip().split('\t')
        position = terms[1]
        if 1 == position_list.count(position):
            qi = terms[0]
            if 0 == query_item_list.count(qi):
                continue
            if qi not in show_dict:
                show_dict[qi] = 0.0
                click_dict[qi] = 0.0
            show_dict[qi] += 1.0 * position_bias[position]
            click_dict[qi] += float(terms[2])
    for i in show_dict:
        ctr_dict[i] = click_dict[i]
        if 0.0 != show_dict[i]:
            ctr_dict[i] /= show_dict[i]
    ptr.close()
    return ctr_dict, query_item_list


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: " + sys.argv[0] + " position_list_file query_item_list_file train.dat \n")
        return -1
    position_bias, position_list = cal_position_bias(sys.argv[1], sys.argv[3])
    print "### position bias ###"
    for i in xrange(len(position_list)):
        print "%s\t%f" % (position_list[i], position_bias[position_list[i]])

    ctr_dict, query_item_list = cal_query_item_ctr(sys.argv[2], sys.argv[3], position_bias, position_list)
    print "### query_item ctr ###"
    for i in xrange(len(query_item_list)):
        print "%s\t%f" % (query_item_list[i], ctr_dict[query_item_list[i]])

    return 0


# ------ Main Process ------ #
if __name__ == "__main__":
    main()
