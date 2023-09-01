# Copyright (C) 2020, 2023 Mitsubishi Electric Research Laboratories (MERL)
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import operator
import os

import networkx as nx
import numpy as np
from gurobipy import *
from utilities import Directory

from template_embedding import *
from utilities2 import Constants


def MIP_BTE_MOD(offset, algorithm, program_file, G, H, L, M, N, warm=False):
    """
    I think this is later called QTE.
    add constraints: each vertex assign to at least one group
    :param algorithm:
    :param program_file:
    :param G:
    :param H:
    :param L:
    :param M:
    :param N:
    :param warm:
    :return:
    """

    L = int(L)
    M = int(M)
    offset = int(offset)

    size_of_A = int(M / 2 + offset) * L
    size_of_B = L * M - size_of_A
    size_of_C = L * M
    size_of_D = L * M
    group_sizes = [size_of_A, size_of_B, size_of_C, size_of_D]

    n_partitions = 4

    now = datetime.datetime.now()
    time_format = "{:%Y-%m-%d-%H:%M:%S.%f}".format(now)
    fh_stats = open(algorithm + ".stats", "a")

    if G.order() > (size_of_A + size_of_B + size_of_C + size_of_D) * L:
        # the 23 is determined by this template
        fh_stats.write(
            "{0}\t{1}\t{2}\tUNEMBEDDABLE: not enough groups on the template\n".format(program_file, time_format, warm)
        )
        fh_stats.close()
        return
    if G.order() <= L * M:
        fh_stats.write("{0}\t{1}\t{2}\tEMBEDDABLE: less than L * M variables\n".format(program_file, time_format, warm))
        fh_stats.close()
        return

    # construct x_i1,i2 based on G
    num_vertices = G.order()
    x = np.zeros([num_vertices, num_vertices], dtype=int)
    for line in nx.generate_edgelist(G, data=False):
        i1 = line.split()[0]
        i2 = line.split()[1]
        x[int(i1), int(i2)] = 1
        x[int(i2), int(i1)] = 1  # Teng added on March 12, 2020

    # construct z_j1,j2 based on H
    num_vertices = H.order()
    z = np.zeros([num_vertices, num_vertices], dtype=int)
    for line in nx.generate_edgelist(H, data=False):
        j1 = line.split()[0]
        j2 = line.split()[1]
        z[int(j1), int(j2)] = 1

    g_n = G.order()
    h_n = H.order()

    try:

        # Create a new model
        m = Model("mip_bte_mod")

        # Create variables
        y_prime = []
        for i in range(g_n):
            y_prime.append(m.addVar(vtype=GRB.BINARY, name="y_prime[%d]" % i))

        y = []
        for i in range(g_n):
            new = []
            for k in range(n_partitions):
                new.append(m.addVar(vtype=GRB.BINARY, name="y[%d,%d]" % (i, k)))
            y.append(new)

        z = []
        for i in range(g_n):
            new1 = []
            for j in range(g_n):
                new2 = []
                for w in range(n_partitions):
                    new2.append(m.addVar(vtype=GRB.BINARY, name="z[%d,%d,%d]" % (i, j, w)))
                new1.append(new2)
            z.append(new1)

        # Set objective
        objFnc = LinExpr()
        for i in range(0, g_n):
            objFnc += y_prime[i]
        m.setObjective(objFnc, GRB.MAXIMIZE)

        # add constraints
        for i in range(g_n):
            var_constr = LinExpr()
            for k in range(n_partitions):
                var_constr += y[i][k]
            m.addConstr(var_constr >= y_prime[i], "var_constr[%d]" % (i))

            # This is the constraint added in this version.
            m.addConstr(var_constr >= 1, "vertex_constr[%d]" % (i))

        for k in range(n_partitions):
            group_constr = LinExpr()
            for i in range(g_n):
                group_constr += y[i][k]
            m.addConstr(group_constr <= group_sizes[k], "group_constr[%d]" % (k))

        for i in range(g_n):
            m.addConstr(y[i][0] + y[i][3] - y[i][2] <= 1, "rule_2[%d]" % (i))
            m.addConstr(y[i][1] + y[i][2] - y[i][3] <= 1, "rule_3[%d]" % (i))
            m.addConstr(y[i][0] + y[i][1] - y[i][2] <= 1, "rule_4_1[%d]" % (i))
            m.addConstr(y[i][0] + y[i][1] - y[i][3] <= 1, "rule_4_2[%d]" % (i))

        for i in range(g_n):
            for j in range(i + 1, g_n):
                if x[i, j] == 1:
                    z_constr = LinExpr()
                    for w in range(n_partitions):
                        z_constr += z[i][j][w]
                    m.addConstr(z_constr >= 1, "z_constr[%d][%d]" % (i, j))

                    # m.addConstr(y[i][0] + y[j][2] >= 2 * z[i][j][0], "AC[%d][%d]" % (i, j))
                    # m.addConstr(y[i][1] + y[j][3] >= 2 * z[i][j][1], "BD[%d][%d]" % (i, j))
                    # m.addConstr(y[i][2] + y[j][0] >= 2 * z[i][j][2], "CA[%d][%d]" % (i, j))
                    # m.addConstr(y[i][3] + y[j][1] >= 2 * z[i][j][3], "DB[%d][%d]" % (i, j))
                    m.addConstr(y[i][0] >= z[i][j][0], "AC_1[%d][%d]" % (i, j))
                    m.addConstr(y[j][2] >= z[i][j][0], "AC_2[%d][%d]" % (i, j))
                    m.addConstr(y[i][1] >= z[i][j][1], "BD_1[%d][%d]" % (i, j))
                    m.addConstr(y[j][3] >= z[i][j][1], "BD_2[%d][%d]" % (i, j))
                    m.addConstr(y[i][2] >= z[i][j][2], "CA_1[%d][%d]" % (i, j))
                    m.addConstr(y[j][0] >= z[i][j][2], "CA_2[%d][%d]" % (i, j))
                    m.addConstr(y[i][3] >= z[i][j][3], "DB_1[%d][%d]" % (i, j))
                    m.addConstr(y[j][1] >= z[i][j][3], "DB_2[%d][%d]" % (i, j))

        m.setParam(GRB.Param.TimeLimit, Constants.TIME_LIMIT)
        # m.write(algorithm + '_' + str(M) + '_' + program_file.replace('/', '-') + '.lp')  # Teng added on March 12, 2020
        m.optimize()

        now = datetime.datetime.now()
        time_format = "{:%Y-%m-%d-%H:%M:%S.%f}".format(now)
        # fh = open(algorithm + '.result', 'a')
        fh_stats = open(algorithm + ".stats", "a")

        # in .stats file:
        # graph_filename \t time_format \t lower_bound (objVal) \t upper_bound \t runtime \t time_limit
        if m.status != GRB.Status.INF_OR_UNBD and m.status != GRB.Status.INFEASIBLE:
            fh_stats.write(
                program_file
                + "\t"
                + time_format
                + "\t"
                + str(warm)
                + "\t"
                + str(m.objVal)
                + "\t"
                + str(m.objBound)
                + "\t"
                + str(m.Runtime)
                + "\t"
                + str(m.Params.TIME_LIMIT)
                + "\n"
            )
        else:
            fh_stats.write(
                program_file
                + "\t"
                + time_format
                + "\t"
                + str(warm)
                + "\t"
                + "DIDNT SOLVE"
                + "\t"
                + "str(m.objBound)"
                + "\t"
                + str(m.Runtime)
                + "\t"
                + str(m.Params.TIME_LIMIT)
                + "\n"
            )
        fh_stats.close()
        # if m.status == GRB.Status.OPTIMAL:
        #     fh.write("########## FOUND SOLUTION: ##########\n")
        #     for j in range(2):
        #         solution = "Group %d:\t" % j
        #         for i in range(0, g_n):
        #             if y[i][j].x > 0.9:
        #                 solution += str(i) + "\t"
        #         fh.write(solution + "\n")
        #     fh.write("** Obj: " + str(m.objVal) + "** Runtime: " + str(m.Runtime) + "\n")
        # else:
        #     fh.write("########## NO SOLUTION ##########\n")
        # fh.close()

    except GurobiError as e:
        print(e)


def MIP_BTE(algorithm, program_file, G, H, L, M, N, warm=False):
    """
    for BTE, allow to be assigned to multiple groups.
    didn't use the code for generating the template; the implementation is incorporated in the MIP formulation.

    Upon the SoCS version, we add constraints such that one vertex is assigned to at least one group.
    :return:
    """
    L = int(L)
    M = int(M)

    now = datetime.datetime.now()
    time_format = "{:%Y-%m-%d-%H:%M:%S.%f}".format(now)
    fh_stats = open(algorithm + ".stats", "a")

    if G.order() > H.order() * L:
        fh_stats.write(
            "{0}\t{1}\t{2}\tUNEMBEDDABLE: not enough groups on the template\n".format(program_file, time_format, warm)
        )
        fh_stats.close()
        return
    if G.order() <= L * M:
        fh_stats.write("{0}\t{1}\t{2}\tEMBEDDABLE: less than L * M variables\n".format(program_file, time_format, warm))
        fh_stats.close()
        return

    # construct x_i1,i2 based on G
    num_vertices = G.order()

    x = np.zeros([num_vertices, num_vertices], dtype=int)
    for line in nx.generate_edgelist(G, data=False):
        i1 = line.split()[0]
        i2 = line.split()[1]
        x[int(i1), int(i2)] = 1
        x[int(i2), int(i1)] = 1  # Teng added on March 12, 2020

    # construct z_j1,j2 based on H
    num_vertices = H.order()
    z = np.zeros([num_vertices, num_vertices], dtype=int)
    for line in nx.generate_edgelist(H, data=False):
        j1 = line.split()[0]
        j2 = line.split()[1]
        z[int(j1), int(j2)] = 1

    g_n = G.order()
    h_n = H.order()

    try:

        # Create a new model
        m = Model("mip_bte")

        # Create variables
        y_prime = []
        for i in range(g_n):
            y_prime.append(m.addVar(vtype=GRB.BINARY, name="y_prime[%d]" % i))

        y = []
        for i in range(g_n):
            new = []
            for k in range(2):
                # bipartite, two groups
                new.append(m.addVar(vtype=GRB.BINARY, name="y[%d,%d]" % (i, k)))
            y.append(new)

        # Set objective
        objFnc = LinExpr()
        for i in range(0, g_n):
            objFnc += y_prime[i]
        m.setObjective(objFnc, GRB.MAXIMIZE)

        # add constraints
        for k in range(2):
            bipartite_constr = LinExpr()
            for i in range(g_n):
                bipartite_constr += y[i][k]
            m.addConstr(bipartite_constr <= M * L, "bipartite_constr[%d]" % (k))

        for i in range(g_n):
            m.addConstr(y_prime[i] <= y[i][0] + y[i][1], "bipartite_constr[%d]" % (i))

        for i in range(g_n):
            for j in range(i + 1, g_n):
                if x[i, j] == 1:
                    m.addConstr(y[i][0] + y[j][0] - y[i][1] - y[j][1] <= 1, "connect_constr_1[%d][%d]" % (i, j))
                    m.addConstr(y[i][1] + y[j][1] - y[i][0] - y[j][0] <= 1, "connect_constr_2[%d][%d]" % (i, j))

        # This is the new constraint added in this version.
        for i in range(g_n):
            m.addConstr(y[i][0] + y[i][1] >= 1)

        m.setParam(GRB.Param.TimeLimit, Constants.TIME_LIMIT)
        # m.write(algorithm + '_' + str(M) + '_' + program_file.replace('/', '-') + '.mps')  # Teng added on March 12, 2020
        # m.write(algorithm + '_' + str(M) + '_' + program_file.replace('/', '-') + '.lp')  # Teng added on March 12, 2020
        m.optimize()
        # m.write(algorithm + '_' + str(M) + '_' + program_file.replace('/', '-') + '.sol')  # Teng added on March 12, 2020

        now = datetime.datetime.now()
        time_format = "{:%Y-%m-%d-%H:%M:%S.%f}".format(now)
        # fh = open(algorithm + '.result', 'a')
        fh_stats = open(algorithm + ".stats", "a")

        # in .stats file:
        # graph_filename \t time_format \t lower_bound (objVal) \t upper_bound \t runtime \t time_limit
        if m.status != GRB.Status.INF_OR_UNBD and m.status != GRB.Status.INFEASIBLE:
            fh_stats.write(
                program_file
                + "\t"
                + time_format
                + "\t"
                + str(warm)
                + "\t"
                + str(m.objVal)
                + "\t"
                + str(m.objBound)
                + "\t"
                + str(m.Runtime)
                + "\t"
                + str(m.Params.TIME_LIMIT)
                + "\n"
            )
        else:
            fh_stats.write(
                program_file
                + "\t"
                + time_format
                + "\t"
                + str(warm)
                + "\t"
                + "DIDNT SOLVE"
                + "\t"
                + "str(m.objBound)"
                + "\t"
                + str(m.Runtime)
                + "\t"
                + str(m.Params.TIME_LIMIT)
                + "\n"
            )
        fh_stats.close()
        # if m.status == GRB.Status.OPTIMAL:
        #     fh.write("########## FOUND SOLUTION: ##########\n")
        #     for j in range(2):
        #         solution = "Group %d:\t" % j
        #         for i in range(0, g_n):
        #             if y[i][j].x > 0.9:
        #                 solution += str(i) + "\t"
        #         fh.write(solution + "\n")
        #     fh.write("** Obj: " + str(m.objVal) + "** Runtime: " + str(m.Runtime) + "\n")
        # else:
        #     fh.write("########## NO SOLUTION ##########\n")
        # fh.close()

    except GurobiError as e:
        print(e)
