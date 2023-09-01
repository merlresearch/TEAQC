# Copyright (C) 2020, 2023 Mitsubishi Electric Research Laboratories (MERL)
#
# SPDX-License-Identifier: AGPL-3.0-or-later

pg_code_injection = {
    132: """

def percolation_graph(n, p, k=1.0, seed=42):
    \"\"\"
    -----------------------
    author : Teng Huang
    created on Feb 14, 2019
    some rights reserved
    -----------------------
    for each node we have random_location_i \in (0, 1)
    the probability of an edge is :
        p/abs(random_location_i - random_location_j)**k

    Parameters
    ----------
    n : int
        Number of nodes
    p : double
        Probability of bipartite edge
    k : double
    seed : int
        Seed for pseudorandom number generator

    Returns
    -------
    NeworkX Graph
        The random noisy bipartite graph
    \"\"\"

    random.seed(seed)
    random_location = []
    G = nx.Graph()
    n = int(n)
    for i in range(0, n):
        G.add_node(i)
        random_location.extend([random.random()])

    for i in range(0, n-1):
        for j in range(i+1, n):
            temp1 = random.random()
            if temp1 < p/(abs(random_location[i]-random_location[j])**k):
                G.add_edge(i, j)
    return G

def write_perc_graph(n, density, seed=42):
    \"\"\"
    -----------------------
    author : Teng Huang
    created on Feb 14, 2019
    some rights reserved
    -----------------------
    Write a noisy bipartite graph on n vertices and the desired density.

        Parameters
        ----------
        n : int
            Number of nodes
        density : str
            An edge density from \"low\", \"medium\", \"high\"
        seed : int
            Seed for pseudorandom number generator

        Returns
        -------
        Nothing
        \"\"\"
    p = noisy_bipartite_density_conversion[density]
    k = 1.0
    G = percolation_graph(n=n, p=p, k=k, seed=seed)
    graph_dir = os.path.join(Directory.INPUT_DIR,
                             "perc_%d_%s" % (n, density))
    write_graph(G, str(graph_dir), seed)



""",
    178: """    if k * n % 2 == 1:
        k = k -1
""",
}

pg_code_replacement = {
    158: """    fh = open(os.path.join(graph_dir, "%d.graph") % (seed), 'ab')
    nx.write_edgelist(G, fh, data=False)
    fh.close()
""",
    180: """    write_graph(G, str(graph_dir), seed)
""",
    202: """    write_graph(G, str(graph_dir), seed)
""",
    225: """    write_graph(G, str(graph_dir), seed)
""",
    248: """    write_graph(G, str(graph_dir), seed)
""",
    311: """    fh = open(os.path.join(graph_dir, "chimera_%d_%d_%d.graph"
                           % (L, M, N)), 'ab')
    nx.write_edgelist(G, fh, data=False)
    fh.close()



def genFaultyQubits(L, M, N, n_experiment = 1, max_n_faulty_qubits = 20):
    \"\"\"
    added by Teng on April 16, 2019
    To generate faulty qubits
    :param L:
    :param M:
    :param N:
    :param n_experiment:
    :param max_n_faulty_qubits:
    :return:
    \"\"\"
    L = int(L)
    M = int(M)

    offset = 0
    seeds = []
    for i in range(n_experiment):
        # to make sure the experiments are reproducable
        seeds.append(list([max_n_faulty_qubits * i + offset + x for x in range(max_n_faulty_qubits)]))
        # seeds should look like this:
        # [[0, ..., 20],
        #  [21, ..., 40], ...
        # ]

    for i in range(n_experiment):
        qubits = []
        for seed in seeds[i]:
            random.seed(seed)
            qubits.append(int(random.random() * 8 * int(M/2) * L))

            # write to a file
            qubit_dir = os.path.join(Directory.INPUT_DIR, \"faulty_qubits/%d\" % (i))
            # dir = \'data/input/faulty_qubits/%d/%d.faultyqubits\' % (i, len(qubits))
            if not os.path.exists(qubit_dir):
                os.makedirs(qubit_dir)
            with open(os.path.join(qubit_dir, \"%d.faultyqubits\" % (len(qubits))), \'w\') as outfile:
                # outfile.write(\"%d\\n\" % (len(qubits)))
                for q in qubits:
                    outfile.write(\"%d\\n\" % (q))
""",
    312: "",
    318: """                    \"nb\": write_noisy_bipartite,
                    \"perc\": write_perc_graph}
""",
}

file_in = open("../scripts/program_generator.py", "r")
file_out = open("program_generator.py", "w")
line_number = 1
for line in file_in:
    if line_number in pg_code_replacement:
        file_out.write(pg_code_replacement[line_number])
    else:
        if line_number in pg_code_injection:
            file_out.write(pg_code_injection[line_number])
        # file_out.write(str(line_number)+"   "+line)
        file_out.write(line)
    line_number += 1
file_out.close()
file_in.close()


ex_code_injection = {
    11: """from template_embedding import *
from MIP_embedding import *
""",
    75: """
    # Teng added on April 16, 2019:
    n_experiment = 1
    max_n_faulty_qubits = 20
""",
    90: """    if (algorithm in [\"fast-oct\",
                     \"fast-oct-reduce\",
                     \"hybrid-oct\",
                     \"hybrid-oct-reduce\",
                     \"oct-fast\",
                     \"oct-fast-native\",
                    \"cmr"]):

    """,
    92: "    ",
    93: "    ",
    94: "    ",
    95: "    ",
    96: "    ",
    97: "    ",
    98: "    ",
    100: "    ",
    101: "    ",
    102: "    ",
    103: "    ",
    104: "    ",
    105: "    ",
    107: "    ",
    108: "    ",
    109: "    ",
    110: "    ",
    111: "    ",
    112: "    ",
    113: "    ",
    114: "    ",
    115: "    ",
    116: "    ",
    118: "    ",
    119: "    ",
    120: """    elif algorithm == \"M-BTE\":
        MIP_BTE(algorithm, program_file, read_problem_graph(algorithm, program_file), bipartite_template_embedding(c, m, n), c, m, n)
    elif algorithm == \"BTE-MOD-0\":
        MIP_BTE_MOD(\"0\", \"BTE-MOD-0\", program_file, read_problem_graph(algorithm, program_file),
                    quapartite_template_embedding(c, m, n), c, m, n)
""",
    139: """        # added by Teng on April 16, 2019
        # For generating faulty qubits
        pg.genFaultyQubits(*([int(x) for x in hardware] + [1, 20]))
        # 1 means we run it once;
        # 20 means we generate a list of 20 qubits

""",
}

ex_code_replacement = {
    4: """import random
""",
    117: """        print(command)
""",
    183: """    generate_input(experiment)  # Teng commented on March 12, 2020
    print(\"Finished generating input graphs\")
    # exit(1)""",
}

file_in = open("../scripts/experiment.py", "r")
file_out = open("experiment.py", "w")
line_number = 1
for line in file_in:
    if line_number in ex_code_replacement:
        file_out.write(ex_code_replacement[line_number])
    else:
        if line_number in ex_code_injection:
            file_out.write(ex_code_injection[line_number])
        # file_out.write(str(line_number)+"   "+line)
        file_out.write(line)
    line_number += 1
file_out.close()
file_in.close()
