# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: parser.py
# Description: Script xml structure parsing
# Date: 2023-04-07

from . import error,params,instruction,program
from collections import Counter
import sys
import xml.etree.ElementTree as et
import re

# XML structure class with constants
class _XML:
    class Elem:
        program="program"
        instruction="instruction"
        arg1="arg1"
        arg2="arg2"
        arg3="arg3"

    class Attr:
        name="name"
        description="description"
        order="order"
        opcode="opcode"
        type="type"
        value="value"
        language="language"

    class AttrValue:
        label="label"
        var="var"
        type="type"
        IPPCODE23="IPPCODE23"

class parser:

    close_source = False

    def __init__(self):
        # Open source file 
        if not hasattr(params.source, "read"):
            try:
                params.source = open(params.source, "r")
                self.close_source = True
            except:
                error.exit(error.code.ERR_INPUT, f"Source file '{params.source}' does not exist or could not be read\n")

    def __del__(self):
        # Close source file 
        if self.close_source:
            params.source.close()

    def parseXML(self, prog: program.Program):
        # Parse xml structure
        try:
            tree = et.parse(params.source)
        except:
            error.exit(error.code.ERR_XML_FORMAT, "XML structure is not valid\n")

        # Get root element
        root = tree.getroot()

        # Check root element (program)
        if root.tag != _XML.Elem.program:
            error.exit(error.code.ERR_XML_SYNTAX, "Root element is not 'program'\n")
        if root.attrib[_XML.Attr.language].upper() != _XML.AttrValue.IPPCODE23:
            error.exit(error.code.ERR_XML_SYNTAX, "Code language is not 'IPPcode23'\n")

        # Check order attribute of child elements (instructions)
        try:
            values = [int(child.attrib[_XML.Attr.order]) for child in root]
        except:
            error.exit(error.code.ERR_XML_SYNTAX, "Order attribute does not exist\n")
        if any(not isinstance(value, int) for value in values):
            error.exit(error.code.ERR_XML_SYNTAX, "Order attribute value is not integer\n")
        if any(value < 1 for value in values):
            error.exit(error.code.ERR_XML_SYNTAX, "Order attribute value is less than 1\n")
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        if duplicates:
            error.exit(error.code.ERR_XML_SYNTAX, "Order attribute value is not unique\n")

        # Sort child elements (instructions) by order attribute
        root[:] = sorted(root, key=lambda child: int(child.attrib[_XML.Attr.order]))

        # Check child elements (instructions)
        for child in root:
            instruction_in = self._parse_instruction(child)
            
            # Set label
            if isinstance(instruction_in, instruction.LABEL):
                # Check label not defined
                if prog.label_is_defined(instruction_in.args['1'][1]):
                    error.exit(error.code.ERR_XML_SEMANTIC, "Label already defined\n")
                prog.label_create(instruction_in.args['1'][1], len(prog.instructions))
                
            # Add instruction to program
            prog.instructions.append(instruction_in)

    def _parse_instruction(self, root) -> instruction.Instruction:

        if root.tag != _XML.Elem.instruction:
            error.exit(error.code.ERR_XML_SYNTAX, f"Invalid instruction element '{root.tag}'\n")

        # Collect instruction arguments
        arg_count = len(root.findall("*"))
        args = {}

        if arg_count > 0:
            try:
                arg = root.find(_XML.Elem.arg1)
                args['1'] = arg.attrib[_XML.Attr.type], arg.text
            except:
                error.exit(error.code.ERR_XML_SYNTAX, f"Invalid argument element, '{_XML.Elem.arg1}' does not exist\n")

            if arg_count > 1:
                try:
                    arg = root.find(_XML.Elem.arg2)
                    args['2'] = arg.attrib[_XML.Attr.type], arg.text
                except:
                    error.exit(error.code.ERR_XML_SYNTAX, f"Invalid argument element, '{_XML.Elem.arg2}' does not exist\n")

                if arg_count > 2:
                    try:
                        arg = root.find(_XML.Elem.arg3)
                        args['3'] = arg.attrib[_XML.Attr.type], arg.text
                    except:
                        error.exit(error.code.ERR_XML_SYNTAX, f"Invalid argument element, '{_XML.Elem.arg3}' does not exist\n")

                    if arg_count > 3:
                        error.exit(error.code.ERR_XML_SYNTAX, f"Invalid instruction element, too many arguments\n")

        # Create instruction
        try:
            opcode = root.attrib[_XML.Attr.opcode].upper()
        except:
            error.exit(error.code.ERR_XML_SYNTAX, "Opcode attribute does not exist\n")

        match arg_count:
            case 0:
                if opcode not in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:
                    error.exit(error.code.ERR_XML_SYNTAX, f"Invalid instruction '{opcode}' with {arg_count} arguments\n")
            case 1:
                if opcode not in ["DEFVAR", "CALL", "PUSHS", "POPS", "WRITE", "LABEL", "JUMP", "EXIT", "DPRINT"]:
                    error.exit(error.code.ERR_XML_SYNTAX, f"Invalid instruction '{opcode}' with {arg_count} arguments\n")
            case 2:
                if opcode not in ["MOVE", "NOT", "INT2CHAR", "READ", "STRLEN", "TYPE"]:
                    error.exit(error.code.ERR_XML_SYNTAX, f"Invalid instruction '{opcode}' with {arg_count} arguments\n")
            case 3:
                if opcode not in ["ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "STRI2INT", "CONCAT", "GETCHAR", "SETCHAR", "JUMPIFEQ", "JUMPIFNEQ"]:
                    error.exit(error.code.ERR_XML_SYNTAX, f"Invalid instruction '{opcode}' with {arg_count} arguments\n")

        match opcode:
            case "MOVE":
                return instruction.MOVE(opcode, args)
            case "CREATEFRAME":
                return instruction.CREATEFRAME(opcode, args)
            case "PUSHFRAME":
                return instruction.PUSHFRAME(opcode, args)
            case "POPFRAME":
                return instruction.POPFRAME(opcode, args)
            case "DEFVAR":
                return instruction.DEFVAR(opcode, args)
            case "CALL":
                return instruction.CALL(opcode, args)
            case "RETURN":
                return instruction.RETURN(opcode, args)
            case "PUSHS":
                return instruction.PUSHS(opcode, args)
            case "POPS":
                return instruction.POPS(opcode, args)
            case "ADD":
                return instruction.ADD(opcode, args)
            case "SUB":
                return instruction.SUB(opcode, args)
            case "MUL":
                return instruction.MUL(opcode, args)
            case "IDIV":
                return instruction.IDIV(opcode, args)
            case "LT":
                return instruction.LT(opcode, args)
            case "GT":
                return instruction.GT(opcode, args)
            case "EQ":
                return instruction.EQ(opcode, args)
            case "AND":
                return instruction.AND(opcode, args)
            case "OR":
                return instruction.OR(opcode, args)
            case "NOT":
                return instruction.NOT(opcode, args)
            case "INT2CHAR":
                return instruction.INT2CHAR(opcode, args)
            case "STRI2INT":
                return instruction.STRI2INT(opcode, args)
            case "READ":
                return instruction.READ(opcode, args)
            case "WRITE":
                return instruction.WRITE(opcode, args)
            case "CONCAT":
                return instruction.CONCAT(opcode, args)
            case "STRLEN":
                return instruction.STRLEN(opcode, args)
            case "GETCHAR":
                return instruction.GETCHAR(opcode, args)
            case "SETCHAR":
                return instruction.SETCHAR(opcode, args)
            case "TYPE":
                return instruction.TYPE(opcode, args)
            case "LABEL":
                return instruction.LABEL(opcode, args)
            case "JUMP":
                return instruction.JUMP(opcode, args)
            case "JUMPIFEQ":
                return instruction.JUMPIFEQ(opcode, args)
            case "JUMPIFNEQ":
                return instruction.JUMPIFNEQ(opcode, args)
            case "EXIT":
                return instruction.EXIT(opcode, args)
            case "DPRINT":
                return instruction.DPRINT(opcode, args)
            case "BREAK":
                return instruction.BREAK(opcode, args)
            case _: # Should never happen
                error.exit(error.code.ERR_XML_SYNTAX, f"Unknown opcode '{opcode}'\n")