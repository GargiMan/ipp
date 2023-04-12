# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: interpret.py
# Description: Interpret script for IPPcode23
# Date: 2023-04-07

import libs.python.params as params
import libs.python.parser as parser
import libs.python.program as program

if __name__ == '__main__':

    # Parse script parameters
    params.parse()
    
    # Parse code from xml structure
    program_i = program.Program()
    parser.parser().parseXML(program_i)

    # Execute code instructions
    program_i.execute()

    # Exit with program exit code
    exit(program_i.get_exit_code())
