<!--
Copyright (C) 2023 Mitsubishi Electric Research Laboratories (MERL)

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# TEAQC - Template-Based Embedding for Adiabatic Quantum Computation

## Features

TEAQC is collection of Python files necessary to replicate the results in our manuscript ["Template-based Minor Embedding for Adiabatic Quantum Optimization"](https://pubsonline.informs.org/doi/10.1287/ijoc.2021.1065) by Serra, Huang, Raghunathan, and Bergman. The paper is also available on [arXiv](https://arxiv.org/abs/1910.02179).

Quantum Annealing (QA) can be used to quickly obtain near-optimal solutions for Quadratic Unconstrained Binary Optimization (QUBO) problems. In QA hardware, each decision variable of a QUBO should be mapped to one or more adjacent qubits in such a way that pairs of variables defining a quadratic term in the objective function are mapped to some pair of adjacent qubits. However, qubits have limited connectivity in existing QA hardware. This has spurred work on preprocessing algorithms for embedding the graph representing problem variables with quadratic terms into the hardware graph representing qubits adjacencies

TEAQC computes a minor embedding of a problem graph into the hardware graph of q Quantum Annealer. The hardware graph that we consider is the [Chimera graph](https://docs.dwavesys.com/docs/latest/c_gs_4.html#topology-intro-chimera). [D-Wave Systems](https://www.dwavesys.com/) is a leading manufacturer of Quantum Processing Units (QPUs) for quantum annealing. The connectivity between the qubits of the [D-Wave 2000Q]([https://docs.dwavesys.com/docs/latest/c_gs_1.html#), a QPU, follows the Chimera graph.


## Installation

As a starting point, we used the code by [Goodrich et al., 2018](https://github.com/TheoryInPractice/aqc-virtual-embedding) (License: `BSD-3-Clause`)


1. Please download the [repo](https://github.com/TheoryInPractice/aqc-virtual-embedding) using the following command

```
git clone -b master https://github.com/TheoryInPractice/aqc-virtual-embedding.git
```

2. Copy TEAQC folder into the project aqc-virtual-embedding.

3. Change the working directory to TEAQC. From that folder, all you need to do is run the following command:
   ```
   python merl_project_modifier.py
   ```

4. Alternatively, you can follow the following steps to replicate all the modifications:
    1. We need to perform modifications to two files of the original source: `scripts/experiment.py` and `scripts/program_generator.py`. This can be achieved with the following command from that TEAQC folder:
       ```
       python merl_code_generator.py
       ```

    2. Put `test_embd.py` in the same folder as `recreate_paper.py`, i.e., the root folder of the project aqc-virtual-embedding.

    3. Put `template_embedding.py`, `MIP_embedding.py`, `experiment.py`, `program_generator.py`, and `utilities2.py` in `/scripts`.
        1. `template_embedding.py` contains our templates.
        2. `MIP_embedding.py` contains the embedding algorithms we used in the paper.
        3. `experiment.py` and `program_generator.py` are modifications of the original source code by Goodrich et al.
        4. `utilities2.py` is a small extension of `utilities.py` to control the time limit of the tests.


    4. Make sure you have a `/data` folder and a `/data/config` folder.


## Usage

To reproduce the results in the paper, do the following.

    1. Change the working directory to aqc-virtual-embedding.

    2. Run `make`. This is for creating subfolders and compile the C++ code. A successful output will look like this:
        ```
        Compiling C++ code
        g++ -std=c++11 -O2 embedding/*/src/*.cpp embedding/driver.cpp -o embedding/driver.exe
        Build completed!
        ```

    3. To ensure Python dependencies are installed run
        ```
        pip install -r requirements.txt
        ```

## Testing

The experiments in the paper can be reproduced using the following commands.

    * Change the working folder to aqc-virtual-embedding.

    * To replicate the experiments for C$_{4,16,16}$ graphs, run the following command.
        ```python3 test_embd.py --num_threads 1 --experiment c16```

    * To replicate the experiments for C$_{4,20,20}$ graphs, run the following command.
        ```python3 test_embd.py --num_threads 1 --experiment c20```

        Note:
        1. `--num_threads 1` indicates we allow for only one thread.
        2. `--experiment c16` means running Goodrich's `fast-oct-reduced` and 2 template embedding algorithms, namely `BTE` and `QTE` using the C16 Chimera architecture.
        3. The final argument specifies the hardware graph to be considered.


## Citation

If you use the software, please cite the following [paper](https://pubsonline.informs.org/doi/10.1287/ijoc.2021.1065):

```BibTeX
@journal{TEAQC,
author = {Thiago Serra and Teng Huang and Arvind~U.~Raghunathan and David Bergman },
title = {Template-Based Minor Embedding for Adiabatic Quantum Optimization},
journal = {INFORMS Journal on Computing},
year = {2022},
pages = {427-439},
volume={34},
issue={1},
doi = {https://doi.org/10.1287/ijoc.2021.1065},
url = {https://pubsonline.informs.org/doi/10.1287/ijoc.2021.1065}
}
```

## Contact

For questions and comments, please write to: Arvind Raghunathan(raghunathan@merl.com), Thiago Serra (Thiago.Serra@bucknell.edu), and David Bergman (david.bergman@business.uconn.edu).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for our policy on contributions.

## License

Released under `AGPL-3.0-or-later` license, as found in the [LICENSE.md](LICENSE.md) file.

All files:

```
Copyright (C) 2020, 2023 Mitsubishi Electric Research Laboratories (MERL).

SPDX-License-Identifier: AGPL-3.0-or-later
```
