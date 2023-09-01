# Copyright (C) 2020, 2023 Mitsubishi Electric Research Laboratories (MERL)
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
test embedding template
This is the file I used for the experiment in the IJOC embedding paper.
"""


import argparse
from subprocess import call


def write_C16():
    """
    write C16.config
    :return:
    """
    with open("data/config/C16.config", "w") as outfile:
        outfile.write("#hardware\n")
        outfile.write("4, 16, 16\n")
        outfile.write("#programs\n")
        outfile.write("nb 65:128:1 low\n")
        outfile.write("nb 65:128:1 medium\n")
        outfile.write("nb 65:128:1 high\n")
        outfile.write("gnp 65:128:1 low\n")
        outfile.write("gnp 65:128:1 medium\n")
        outfile.write("gnp 65:128:1 high\n")
        outfile.write("reg 65:128:1 low\n")
        outfile.write("reg 65:128:1 medium\n")
        outfile.write("reg 65:128:1 high\n")
        outfile.write("powerlaw 65:128:1 low\n")
        outfile.write("powerlaw 65:128:1 medium\n")
        outfile.write("powerlaw 65:128:1 high\n")
        outfile.write("perc 65:128:1 low\n")
        outfile.write("perc 65:128:1 medium\n")
        outfile.write("perc 65:128:1 high\n")
        outfile.write("#program_seeds\n")  # five graphs per setting
        outfile.write("0:4\n")
        outfile.write("#algorithms\n")
        outfile.write("fast-oct-reduce\n")  # FOR in Goodrich et al 2018
        outfile.write("M-BTE\n")  # BTE
        outfile.write("BTE-MOD-0\n")  # QTE
        outfile.write("#algorithm_seeds\n")
        outfile.write("0:0\n")


def write_C20():
    """
    write C20.config
    :return:
    """
    with open("data/config/C20.config", "w") as outfile:
        outfile.write("#hardware\n")
        outfile.write("4, 20, 20\n")
        outfile.write("#programs\n")
        outfile.write("nb 81:160:1 low\n")
        outfile.write("nb 81:160:1 medium\n")
        outfile.write("nb 81:160:1 high\n")
        outfile.write("gnp 81:160:1 low\n")
        outfile.write("gnp 81:160:1 medium\n")
        outfile.write("gnp 81:160:1 high\n")
        outfile.write("reg 81:160:1 low\n")
        outfile.write("reg 81:160:1 medium\n")
        outfile.write("reg 81:160:1 high\n")
        outfile.write("powerlaw 81:160:1 low\n")
        outfile.write("powerlaw 81:160:1 medium\n")
        outfile.write("powerlaw 81:160:1 high\n")
        outfile.write("perc 81:160:1 low\n")
        outfile.write("perc 81:160:1 medium\n")
        outfile.write("perc 81:160:1 high\n")
        outfile.write("#program_seeds\n")  # five graphs per setting
        outfile.write("0:4\n")
        outfile.write("#algorithms\n")
        outfile.write("fast-oct-reduce\n")  # FOR in Goodrich et al 2018
        outfile.write("M-BTE\n")  # BTE
        outfile.write("BTE-MOD-0\n")  # QTE
        outfile.write("#algorithm_seeds\n")
        outfile.write("0:0\n")


if __name__ == "__main__":
    """Main method for CLI interaction.

    Parameters
    ----------
    num_threads : int
        The number of CPU threads to use
    experiment : string
        An experiment from [embed_one, ...]

    Returns
    -------
    Nothing
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_threads", help="The number of compute threads used.", type=int)
    parser.add_argument(
        "--experiment",
        help="Run experiment from [small, medium, large, cmr,\
                            hybrid]. Runs medium if not specified",
        type=str,
    )
    args = parser.parse_args()

    config = ""
    if args.experiment:
        if args.experiment == "c16":
            write_C16()
            config = "C16.config"
        elif args.experiment == "c20":
            write_C20()
            config = "C20.config"

    # Set up the script commands
    experiment_command = [
        "python3",
        "scripts/experiment.py",
        config,
        str(args.num_threads),
    ]

    # Call the scripts
    call(experiment_command)
