#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
# Description:
# Author: hao.003.hao@gmail.com
# Last Modified Time: 2015-06-19, 11:30:11
"""

# ------ Import & Param ------ #

import os
import sys
import time
import numpy
import numpy.matlib as mat

# ------ Sub Functions ------ #
def read_matrix(position_list_file, query_item_list_file, train_dat_file):
    position_list = []
    query_item_list = []
    ptr = open(position_list_file)
    for line in ptr:
        terms = line.strip().split("\t")
        position_key = terms[0]
        if 0 == position_list.count(position_key):
            position_list.append(position_key)
    ptr.close()
    ptr = open(query_item_list_file)
    for line in ptr:
        terms = line.strip().split("\t")
        query_item_key = terms[0]
        if 0 == query_item_list.count(query_item_key):
            query_item_list.append(query_item_key)
    ptr.close()

    N = len(position_list)
    M = len(query_item_list)
    show_mat = mat.zeros((N, M), dtype=float)
    click_mat = mat.zeros((N, M), dtype=float)
    ctr_mat = mat.zeros((N, M), dtype=float)

    ptr = open(train_dat_file)
    for line in ptr:
        terms = line.strip().split("\t")
        if 4 > len(terms):
            continue
        query_item = terms[0]
        position = terms[1]
        show = float(terms[3])
        click = float(terms[2])
        if 1 == query_item_list.count(query_item) and 1 == position_list.count(position):
            position_index = position_list.index(position)
            query_item_index = query_item_list.index(query_item)
            show_mat[position_index, query_item_index] += show
            click_mat[position_index, query_item_index] += click
    ptr.close()
    return click_mat, show_mat, query_item_list, position_list


def normalize(inP, inQ):
    if 0 == len(inP) or 0 == len(inQ):
        return -1
    outP = inP
    outQ = inQ
    nor_factor = 1.0 / inP[0]
    for i in xrange(len(inP)):
        outP[i] *= nor_factor
    for i in xrange(len(inQ[0])):
        outQ[0][i] /= nor_factor
    return outP, outQ

def em_optimiz(show_mat, click_mat, steps=10000, epsilon=1e-6):
    N = len(show_mat)
    M = len(show_mat[0])

    mat_x = numpy.random.rand(N, 1)
    mat_r = numpy.random.rand(1, M)
    mat_x1 = mat_x.copy()

    sum_click_col = []
    sum_click_row = []
    for i in xrange(N):
        sum_click_row.append(0.0)
        for j in xrange(M):
            sum_click_row[i] += click_mat[i][j]
    for j in xrange(M):
        sum_click_col.append(0.0)
        for i in xrange(N):
            sum_click_col[j] += click_mat[i][j]

    for k in xrange(steps):
        # E-step, update mat_r
        for j in xrange(M):
            temp_denominator = 0.0
            for i in xrange(N):
                if 0.0 != 1.0 - mat_x[i][0] * mat_r[0][j]:
                    temp_denominator += (show_mat[i][j] - click_mat[i][j]) * mat_x[i][0] / (1.0 - mat_x[i][0] * mat_r[0][j])
            if 0.0 != temp_denominator:
                mat_r[0][j] = sum_click_col[j] / temp_denominator
        #print temp_denominator

        # M-step, update mat_x
        for i in xrange(N):
            temp_denominator = 0.0
            for j in xrange(M):
                if 0.0 != 1.0 - mat_x[i][0] * mat_r[0][j]:
                    temp_denominator += (show_mat[i][j] - click_mat[i][j]) * mat_r[0][j] / (1.0 - mat_x[i][0] * mat_r[0][j])
            if 0.0 != temp_denominator:
                mat_x[i][0] = sum_click_row[i] / temp_denominator
        #time.sleep(10)

        if 0 == k%100:
            mat_x, mat_r = normalize(mat_x, mat_r)
            delta = 0
            for i in xrange(N):
                delta = max(delta, mat_x1[i] - mat_x[i], mat_x[i] - mat_x1[i])
            print "interation:{} delta:{}".format(k, delta)
            if delta < epsilon:
                break
            mat_x1 = mat_x.copy()

    return normalize(mat_x, mat_r)


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: " + sys.argv[0] + " position_list_file query_item_list_file train.dat \n")
        return -1
    click_mat, show_mat, query_item_list, position_list = read_matrix(sys.argv[1], sys.argv[2], sys.argv[3])

    click_mat_np = numpy.array(click_mat)
    show_mat_np = numpy.array(show_mat)


    #print mat_x, mat_r

    outP, outQ = em_optimiz(show_mat_np, click_mat_np)
    print "### position bias ###"
    for i in xrange(len(outP)):
        print "%s\t%f" % (position_list[i], outP[i])
    print "### query_item ctr ###"
    for i in xrange(len((outQ[0]))):
        print "%s\t%f" % (query_item_list[i], outQ[0][i])


# ------ Main Process ------ #
if __name__ == "__main__":
    main()
