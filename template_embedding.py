# Copyright (C) 2020, 2023 Mitsubishi Electric Research Laboratories (MERL)
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import operator
import os

import networkx as nx
import numpy as np
from utilities import Directory


def quapartite_template_embedding(L, M, N):
    """

    :param L:
    :param M:
    :param N:
    :return:
    """
    G = nx.Graph()
    return G


# construct the template embedding graph
# have z_j1,j2
def bipartite_template_embedding(L, M, N):
    """
    bipartite template embedding, should/might be exactly the same as Klymko 2014
    :param L:
    :param M:
    :param N:
    :return: graph H
    """
    G = nx.Graph()

    left_partite_size = int(M)
    right_partite_size = int(N)

    for i in range(0, left_partite_size + right_partite_size):
        G.add_node(i)

    for i in range(0, left_partite_size):
        for j in range(0, right_partite_size):
            G.add_edge(i, j + left_partite_size)

    graph_dir = os.path.join(Directory.INPUT_DIR, "template")
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    with open(os.path.join(graph_dir, "BTE_%d_%d_%d.graph" % (int(L), int(M), int(N))), "w") as outfile:
        outfile.write("%d %d \n" % (G.order(), nx.diameter(G)))
        for v in G.nodes():
            outfile.write("%d\n" % v)
    fh = open(os.path.join(graph_dir, "BTE_%d_%d_%d.graph" % (int(L), int(M), int(N))), "ab")
    nx.write_edgelist(G, fh, data=False)
    fh.close()
    return G  # H - the virtual hardware, also the template


# read in the problem graph
# have x_i1,i2
def read_problem_graph(algorithm, graph_file):

    # now = datetime.datetime.now()
    # date_format = '{:%Y-%m-%d}'.format(now)
    # fh = open(date_format + '-' + algorithm + '.result', 'a')
    # fh.write("##############################\n")
    # fh.write("########## PROCESSING " + graph_file + " ##########\n")
    # fh.close()
    G = nx.Graph()
    fh = open(graph_file, "r")
    counter = -1
    num_vertices = -1
    for x in fh:
        # print(x)
        counter = counter + 1
        if counter == 0:
            num_vertices = int(x.split()[0])
            continue  # go to the next loop
        elif counter <= num_vertices:
            G.add_node(int(x.split()[0]))
        elif (counter > num_vertices) and (len(x.split()) > 1):  # no need for the second condition
            # since I correct the mistake in Goodrich
            nodes = x.split()
            G.add_edge(int(nodes[0]), int(nodes[1]))
    fh.close()
    # exit(1)
    return G
