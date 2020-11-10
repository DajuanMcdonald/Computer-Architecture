#!/usr/bin/env python3

"""Main."""

import sys
from sys import argv
from cpu import *

cpu = CPU()

"""
so you can look in `sys.argv[1]` for the name of the file to load.
"""
file_to_load = sys.argv[1]

program = open(file_to_load, 'r').read().split('\n')

cpu.load(program)

cpu.run()
