# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: instruction.py
# Description: Code instruction interpretation
# Date: 2023-04-07

from . import error,params,program
import sys,re

class Instruction:

    def __init__(self, opcode, args):
        self.opcode = opcode
        self.args = args

    def execute(self, prog: program.Program):
        pass

# --------------------------------------------

class MOVE(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()
        type, value = _get_type_and_value(prog, self.args['2'])
        prog.var_set(self.args['1'][1], type, value)

class CREATEFRAME(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()
        prog.frame_create()

class PUSHFRAME(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()
        prog.frame_push()

class POPFRAME(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()
        prog.frame_pop()

class DEFVAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Check if variable is already defined
        if prog.var_is_defined(self.args['1'][1]):
            error.exit(error.code.ERR_CODE_VARIABLE, "Variable is already defined")

        #TODO default value ? nil@nil
        # Define variable
        prog.var_set(self.args['1'][1], "", "")
        

class CALL(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Push next instruction index to call stack
        prog.call_stack_push(prog.instruction_index_get())

        # Jump
        prog.instruction_index_set(prog.label_get_index(self.args['1'][1]))

class RETURN(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_set(prog.call_stack_pop())

class PUSHS(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Get symbol type and value and push to data stack
        type, value = _get_type_and_value(prog, self.args['1'])
        prog.data_stack_push(type, value)

class POPS(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Pop type and value from data stack and assign to variable
        type, value = prog.data_stack_pop()
        prog.var_set(self.args['1'][1], type, value)

class ADD(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        if type1 != program.Program.DataType.INT or type2 != program.Program.DataType.INT:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires INT type\n")

        try:
            result = str(int(value1) + int(value2))
        except ValueError:
            error.exit(error.code.ERR_XML_SYNTAX, f"Operation '{self.opcode}' requires correct INT value\n")

        prog.var_set(self.args['1'][1], program.Program.DataType.INT, result)

class SUB(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        if type1 != program.Program.DataType.INT or type2 != program.Program.DataType.INT:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires INT type\n")

        try:
            result = str(int(value1) - int(value2))
        except ValueError:
            error.exit(error.code.ERR_XML_SYNTAX, f"Operation '{self.opcode}' requires correct INT value\n")

        prog.var_set(self.args['1'][1], program.Program.DataType.INT, result)

class MUL(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        if type1 != program.Program.DataType.INT or type2 != program.Program.DataType.INT:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires INT type\n")
        
        try:
            result = str(int(value1) * int(value2))
        except ValueError:
            error.exit(error.code.ERR_XML_SYNTAX, f"Operation '{self.opcode}' requires correct INT value\n")

        prog.var_set(self.args['1'][1], program.Program.DataType.INT, result)

class IDIV(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        if type1 != program.Program.DataType.INT or type2 != program.Program.DataType.INT:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires INT type\n")
        
        try:
            result = str(int(value1) // int(value2))
        except ValueError:
            error.exit(error.code.ERR_XML_SYNTAX, f"Operation '{self.opcode}' requires correct INT value\n")
        except ZeroDivisionError:
            error.exit(error.code.ERR_CODE_ZERO, f"Operation '{self.opcode}' cannot divide by zero\n")

        prog.var_set(self.args['1'][1], program.Program.DataType.INT, result)

class LT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        match type1:
            case program.Program.DataType.INT:
                if type2 != program.Program.DataType.INT:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = int(value1) < int(value2)
            case program.Program.DataType.STRING:
                if type2 != program.Program.DataType.STRING:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = bool(value1) < bool(value2)
            case program.Program.DataType.BOOL:
                if type2 != program.Program.DataType.BOOL:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = value1 < value2
            case _:
                error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires arguments same type (INT, STR, BOOL) \n")
        
        prog.var_set(self.args['1'][1], program.Program.DataType.BOOL, str(result).lower())

class GT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        match type1:
            case program.Program.DataType.INT:
                if type2 != program.Program.DataType.INT:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = int(value1) > int(value2)
            case program.Program.DataType.STRING:
                if type2 != program.Program.DataType.STRING:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = bool(value1) > bool(value2)
            case program.Program.DataType.BOOL:
                if type2 != program.Program.DataType.BOOL:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = value1 > value2
            case _:
                error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires arguments same type (INT, STR, BOOL) \n")

        prog.var_set(self.args['1'][1], program.Program.DataType.BOOL, str(result).lower())

class EQ(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        match type1:
            case program.Program.DataType.INT:
                if type2 != program.Program.DataType.INT:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = int(value1) == int(value2)
            case program.Program.DataType.STRING:
                if type2 != program.Program.DataType.STRING:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = bool(value1) == bool(value2)
            case program.Program.DataType.BOOL:
                if type2 != program.Program.DataType.BOOL:
                    error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type\n")
                result = value1 == value2
            case _:
                error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires arguments same type (INT, STR, BOOL) \n")
            
        prog.var_set(self.args['1'][1], program.Program.DataType.BOOL, str(result).lower())

        #TODO eq nil

class AND(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        if type1 != program.Program.DataType.BOOL or type2 != program.Program.DataType.BOOL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires BOOL type\n")

        result = bool(bool(value1) & bool(value2))

        prog.var_set(self.args['1'][1], program.Program.DataType.BOOL, str(result).lower())


class OR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        if type1 != program.Program.DataType.BOOL or type2 != program.Program.DataType.BOOL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires BOOL type\n")

        result = bool(bool(value1) | bool(value2))

        prog.var_set(self.args['1'][1], program.Program.DataType.BOOL, str(result).lower())

class NOT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        type1, value1 = _get_type_and_value(prog, self.args['2'])

        if type1 != program.Program.DataType.BOOL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires BOOL type\n")

        result = not bool(value1)

        prog.var_set(self.args['1'][1], program.Program.DataType.BOOL, str(result).lower())

class INT2CHAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class STRI2INT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class READ(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Read input
        value = params.input.read()

        # Set variable
        prog.var_set(self.args['1'][1], self.args['2'][1], value)

class WRITE(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()
        
        # Get symbol
        type, value = _get_type_and_value(prog, self.args['1'])

        # Nil
        if type == program.Program.DataType.NIL or value is None:
            value = ""

        # Convert escape sequences
        value = re.compile(rb"\\(\d{1,3})").sub(lambda m: bytes([int(m.group(1))]), value.encode()).decode()

        # Print
        print(value, end='')

class CONCAT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class STRLEN(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class GETCHAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class SETCHAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class TYPE(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Get symbol
        type, value = _get_type_and_value(prog, self.args['2'])
        prog.var_set(self.args['1'][1], program.Program.DataType.STRING, type)

class LABEL(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

class JUMP(Instruction):

    def execute(self, prog: program.Program):
        # Jump
        prog.instruction_index_set(prog.label_get_index(self.args['1'][1]))

class JUMPIFEQ(Instruction):

    def execute(self, prog: program.Program):
        # Get symbols
        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        # Compare types
        if type1 != type2 and type1 != 'nil' and type2 != 'nil':
            error.exit(error.code.ERR_CODE_TYPE, "Different data types of arguments\n")

        # Jump
        if value1 == value2:
            prog.instruction_index_set(prog.label_get_index(self.args['1'][1]))
        else:
            prog.instruction_index_next()

class JUMPIFNEQ(Instruction):

    def execute(self, prog: program.Program):
        # Get symbols
        type1, value1 = _get_type_and_value(prog, self.args['2'])
        type2, value2 = _get_type_and_value(prog, self.args['3'])

        # Compare types
        if type1 != type2 and type1 != 'nil' and type2 != 'nil':
            error.exit(error.code.ERR_CODE_TYPE, "Different data types of arguments\n")

        # Jump
        if value1 != value2:
            prog.instruction_index_set(prog.label_get_index(self.args['1'][1]))
        else:
            prog.instruction_index_next()

class EXIT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()

        # Get symbol
        type, value = _get_type_and_value(prog, self.args['1'])

        if type != program.Program.DataType.INT:
            error.exit(error.code.ERR_CODE_ZERO, f"Operation '{self.opcode}' requires INT type\n")

        if int(value) < 0 or int(value) > 49:
            error.exit(error.code.ERR_CODE_ZERO, f"Operation '{self.opcode}' requires value in range 0-49\n")

        # Exit
        prog.exit(int(value))


class DPRINT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_index_next()
        # Get value
        value = re.sub(r'^.*@', '', self.args['1'][1])
        if self.args['1'][0] == program.Program.DataType.VAR:
            if not prog.var_is_defined(self.args['1'][1]):
                error.print("Variable not defined\n")
                return
            value = prog.var_get_value(self.args['1'][1])
            
        # Print
        sys.stderr.write(f"{value}")

class BREAK(Instruction):

    def execute(self, prog: program.Program):
        sys.stderr.write(f"BREAK - {prog.instruction_index_get()}. instruction line, {prog.instructions_executed()} instructions executed\n")
        sys.stderr.write(f"Global frame: {prog.frame_global}\n")
        sys.stderr.write(f"Local frame: {prog.frame_local}\n")
        sys.stderr.write(f"Temporary frame: {prog.frame_temp}\n")
        sys.stderr.write(f"Stack: {prog.frame_stack}\n")
        sys.stderr.flush()
        prog.instruction_index_next()

# --------------------------------------------

def _get_type_and_value(prog: program.Program, symb) -> tuple:
    # Symbol is variable
    if symb[0] == program.Program.DataType.VAR:
        return prog.var_get_type(symb[1]), prog.var_get_value(symb[1])
    # Symbol is constant
    else:
        return symb[0], symb[1]
