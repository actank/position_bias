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
import numpy
import numpy.matlib as mat

# ------ Sub Functions ------ #
def matrix_decomposition(R, P, Q, K, steps=100000, alpha=0.0002, beta=0.02):
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :],Q[:, j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P, Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i, :],Q[:, j]), 2)
                    for k in xrange(K):
                        e = e + (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        if e < 0.001:
            break
    return P, Q.T


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
        query_item = terms[0]
        position = terms[1]
        click = float(terms[2])
        if 1 == query_item_list.count(query_item) and 1 == position_list.count(position):
            position_index = position_list.index(position)
            query_item_index = query_item_list.index(query_item)
            show_mat[position_index, query_item_index] += 1.0
            click_mat[position_index, query_item_index] += click
    ptr.close()
    #print show_mat
    #print click_mat
    for i in xrange(N):
        for j in xrange(M):
            ctr_mat[i, j] = click_mat[i, j]
            if 0.0 != show_mat[i, j]:
                ctr_mat[i, j] /= show_mat[i, j]
    return ctr_mat, query_item_list, position_list


def normalize(inP, inQ):
    if 0 == len(inP) or 0 == len(inQ):
        return -1
    outP = inP
    outQ = inQ
    nor_factor = 1.0 / inP[0]
    for i in xrange(len(inP)):
        outP[i] *= nor_factor
    for i in xrange(len(inQ)):
        outQ[i] /= nor_factor
    return outP, outQ


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: " + sys.argv[0] + " position_list_file query_item_list_file train.dat \n")
        return -1
    ctr_mat, query_item_list, position_list = read_matrix(sys.argv[1], sys.argv[2], sys.argv[3])

    R = numpy.array(ctr_mat)

    N = len(R)
    M = len(R[0])
    K = 1

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(K, M)

    nP, nQ = matrix_decomposition(R, P, Q, K)
    outP, outQ = normalize(nP, nQ)
    print "### position bias ###"
    for i in xrange(len(outP)):
        print "%s\t%f" % (position_list[i], outP[i])
    print "### query_item ctr ###"
    for i in xrange(len((outQ))):
        print "%s\t%f" % (query_item_list[i], outQ[i])


# ------ Main Process ------ #
if __name__ == "__main__":
    main()
