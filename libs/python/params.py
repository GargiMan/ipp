# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: params.py
# Description: Script parameter parsing
# Date: 2023-04-07

import argparse
import sys
from . import error 

source=""
input=""

def parse():
    parser = argparse.ArgumentParser(description='Interpret script for IPPcode23 in XML format', add_help=False,)
    parser.add_argument('--help', action='store_true', help='show this help message and exit')
    parser.add_argument('--source', metavar='filename', type=str, help='the source file with the source code IPPcode23 in XML format')
    parser.add_argument('--input', metavar='filename', type=str, help='the input file with input data')

    args = parser.parse_args()
    if args.help:
        if len(sys.argv) == 2:
            parser.print_help()
            exit(0)
        else:
            error.exit(error.code.ERR_PARAMS, 'Parameter \'--help\' must be used alone\n')

    if not args.source and not args.input:
        error.exit(error.code.ERR_PARAMS, 'Parameter \'--source\' or \'--input\' have to be specified\n')

    global source
    if args.source:
        source = args.source
    else:
        source = sys.stdin

    global input
    if args.input:
        input = args.input
    else:
        input = sys.stdin
