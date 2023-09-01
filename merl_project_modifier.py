# Copyright (C) 2020, 2023 Mitsubishi Electric Research Laboratories (MERL)
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os

import merl_code_generator

os.system("mv test_embd.py ../.")

os.system("mv template_embedding.py ../scripts/.")
os.system("mv MIP_embedding.py ../scripts/.")
os.system("mv experiment.py ../scripts/.")
os.system("mv program_generator.py ../scripts/.")
os.system("mv utilities2.py ../scripts/.")

os.system("mkdir ../data")
os.system("mkdir ../data/config")
