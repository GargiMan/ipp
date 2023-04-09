# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: error.py
# Description: Script error hadnling
# Date: 2023-04-07

import sys

class code:
    ERR_PARAMS = 10
    ERR_INPUT = 11
    ERR_OUTPUT = 12
    ERR_XML_FORMAT = 31
    ERR_XML_SYNTAX = 32
    ERR_XML_SEMANTIC = 52
    ERR_CODE_TYPE = 53
    ERR_CODE_VARIABLE = 54
    ERR_CODE_FRAME = 55
    ERR_CODE_VALUE = 56 
    ERR_CODE_ZERO = 57
    ERR_CODE_STRING = 58
    ERR_INTERNAL = 99

def exit(err_code: code, err_msg: str = ""):
    sys.stdout.flush()
    if err_msg:
        sys.stderr.write(f'Error: {err_msg}')
    sys.exit(err_code)

def print(err_msg: str):
    sys.stdout.flush()
    sys.stderr.write(f'Error: {err_msg}')
