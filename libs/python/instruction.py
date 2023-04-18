# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: instruction.py
# Description: Code instruction interpretation
# Date: 2023-04-07

from . import error,program
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
        prog.instruction_counter_inc()
        type, value = _get_value(prog, self.args[1], True)
        prog.var_set(self.args[0][1], type, value)

class CREATEFRAME(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        prog.frame_create()

class PUSHFRAME(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        prog.frame_push()

class POPFRAME(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        prog.frame_pop()

class DEFVAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        # Define variable
        prog.var_define(self.args[0][1])

class CALL(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        # Push next instruction index to call stack
        prog.call_stack_push(prog.instruction_counter_get())

        # Jump
        prog.instruction_counter_set(prog.label_get_index(self.args[0][1]))

class RETURN(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_set(prog.call_stack_pop())

class PUSHS(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        # Get symbol type and value and push to data stack
        type, value = _get_value(prog, self.args[0], True)
        prog.data_stack_push(type, value)

class POPS(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        # Pop type and value from data stack and assign to variable
        type, value = prog.data_stack_pop()
        prog.var_set(self.args[0][1], type, value)

class CLEARS(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        prog.data_stack_clear()

class ADD(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != int or type2 != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments INT type\n")

        if (len(self.args) == 0):
            prog.data_stack_push(int, value1 + value2)
        else:
            prog.var_set(self.args[0][1], int, value1 + value2)

class SUB(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != int or type2 != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments INT type\n")

        if (len(self.args) == 0):
            prog.data_stack_push(int, value1 - value2)
        else:
            prog.var_set(self.args[0][1], int, value1 - value2)

class MUL(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != int or type2 != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments INT type\n")

        if (len(self.args) == 0):
            prog.data_stack_push(int, value1 * value2)
        else:
            prog.var_set(self.args[0][1], int, value1 * value2)

class IDIV(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != int or type2 != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments INT type\n")
        
        try:
            if (len(self.args) == 0):
                prog.data_stack_push(int, value1 // value2)
            else:
                prog.var_set(self.args[0][1], int, value1 // value2)
        except ZeroDivisionError:
            error.exit(error.code.ERR_CODE_ZERO, f"Operation '{self.opcode}' cannot divide by zero\n")

class LT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != type2 or type1 == program.Program.DataType.NIL or type2 == program.Program.DataType.NIL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type (INT, STRING, BOOL) \n")
        
        if (len(self.args) == 0):
            prog.data_stack_push(bool, value1 < value2)
        else:
            prog.var_set(self.args[0][1], bool, value1 < value2)

class GT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != type2 or type1 == program.Program.DataType.NIL or type2 == program.Program.DataType.NIL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type (INT, STRING, BOOL) \n")

        if (len(self.args) == 0):
            prog.data_stack_push(bool, value1 > value2)
        else:
            prog.var_set(self.args[0][1], bool, value1 > value2)

class EQ(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != type2 and type1 != program.Program.DataType.NIL and type2 != program.Program.DataType.NIL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type (INT, STRING, BOOL) or NIL \n")

        if (len(self.args) == 0):
            prog.data_stack_push(bool, type1 == type2 and value1 == value2)
        else:
            prog.var_set(self.args[0][1], bool, type1 == type2 and value1 == value2)

class AND(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != bool or type2 != bool:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments BOOL type\n")

        if (len(self.args) == 0):
            prog.data_stack_push(bool, value1 & value2)
        else:
            prog.var_set(self.args[0][1], bool, value1 & value2)

class OR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != bool or type2 != bool:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments BOOL type\n")

        if (len(self.args) == 0):
            prog.data_stack_push(bool, value1 | value2)
        else:
            prog.var_set(self.args[0][1], bool, value1 | value2)

class NOT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type, value = prog.data_stack_pop()
        else:
            type, value = _get_value(prog, self.args[1], True)

        if type != bool:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments BOOL type\n")

        if (len(self.args) == 0):
            prog.data_stack_push(bool, not value)
        else:
            prog.var_set(self.args[0][1], bool, not value)

class INT2CHAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type, value = prog.data_stack_pop()
        else:
            type, value = _get_value(prog, self.args[1], True)

        if type != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires argument INT type\n")

        try:
            if (len(self.args) == 0):
                prog.data_stack_push(str, chr(value))
            else:
                prog.var_set(self.args[0][1], str, chr(value))
        except ValueError:
            error.exit(error.code.ERR_CODE_STRING, f"Operation '{self.opcode}' requires argument INT with unicode valid value\n")

class STRI2INT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        if (len(self.args) == 0):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != str or type2 != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires arguments STRING and INT type\n")

        try:
            if value2 < 0 or value2 >= len(value1):
                error.exit(error.code.ERR_CODE_STRING, f"Index out of range, must be in range 0..{len(value1) - 1}\n")
            if (len(self.args) == 0):
                prog.data_stack_push(int, ord(value1[value2]))
            else:
                prog.var_set(self.args[0][1], int, ord(value1[value2]))
        except ValueError:
            error.exit(error.code.ERR_CODE_TYPE, f"Index {value2} is not valid integer\n")

class READ(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        type = self.args[1][1]

        # Type conversion
        match type:
            case program.Program.DataType.INT:
                type = int
            case program.Program.DataType.STRING:
                type = str
            case program.Program.DataType.BOOL:
                type = bool
            case _:
                error.exit(error.code.ERR_XML_SEMANTIC, f"Operation '{self.opcode}' requires argument INT, STRING or BOOL type\n")

        # Read input
        try:
            value = prog.input_file.readline()
            if not value:
                raise EOFError
            value = value.strip()
            
            if type == int:
                value = int(value)
            elif type == bool:
                if value == '':
                    raise ValueError
                elif value.lower() == 'true':
                    value = True
                else:
                    value = False
        except:
            type = program.Program.DataType.NIL
            value = program.Program.DataType.NIL

        # Set variable
        prog.var_set(self.args[0][1], type, value)

class WRITE(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        
        # Get symbol
        type, value = _get_value(prog, self.args[0], True)

        # Nil
        if type == program.Program.DataType.NIL:
            value = ""
        elif type == bool:
            value = str(value).lower()

        # Print
        print(value, end='')

class CONCAT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        type1, value1 = _get_value(prog, self.args[1], True)
        type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != str or type2 != str:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments STRING type\n")

        prog.var_set(self.args[0][1], str, value1 + value2)

class STRLEN(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        type, value = _get_value(prog, self.args[1], True)

        if type != str:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires argument STRING type\n")

        prog.var_set(self.args[0][1], int, len(value))

class GETCHAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
    
        type1, value1 = _get_value(prog, self.args[1], True)
        type2, value2 = _get_value(prog, self.args[2], True)

        if type1 != str or type2 != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires arguments STRING and INT type\n")

        try:
            if value2 < 0 or value2 >= len(value1):
                error.exit(error.code.ERR_CODE_STRING, f"Index out of range, must be in range 0..{len(value1) - 1}\n")
            prog.var_set(self.args[0][1], str, value1[value2])
        except ValueError:
            error.exit(error.code.ERR_CODE_TYPE, f"Index {value2} is not valid integer\n")

class SETCHAR(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        type1, value1 = _get_value(prog, self.args[0], True)
        type2, value2 = _get_value(prog, self.args[1], True)
        type3, value3 = _get_value(prog, self.args[2], True)

        if type1 != str or type2 != int or type3 != str:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires arguments STRING, INT and STRING type\n")

        try:
            if value2 < 0 or value2 >= len(value1):
                error.exit(error.code.ERR_CODE_STRING, f"Index out of range, must be in range 0..{len(value1) - 1}\n")
            if len(value3) == 0:
                error.exit(error.code.ERR_CODE_STRING, f"Operation '{self.opcode}' requires not empty STRING value\n")
            value1_chars = list(value1)
            value1_chars[value2] = value3[0]
            prog.var_set(self.args[0][1], str, ''.join(value1_chars))
        except ValueError:
            error.exit(error.code.ERR_CODE_TYPE, f"Index {value2} is not valid integer\n")

class TYPE(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        type, value = _get_value(prog, self.args[1])

        if type == str:
            type = program.Program.DataType.STRING
        elif type == int:
            type = program.Program.DataType.INT
        elif type == bool:
            type = program.Program.DataType.BOOL
        elif type == program.Program.DataType.NIL:
            type = program.Program.DataType.NIL
        else:
            type = ""

        prog.var_set(self.args[0][1], str, type)

class LABEL(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

class JUMP(Instruction):

    def execute(self, prog: program.Program):
        # Jump
        prog.instruction_counter_set(prog.label_get_index(self.args[0][1]))

class JUMPIFEQ(Instruction):

    def execute(self, prog: program.Program):
        # Get symbols
        if (len(self.args) == 1):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        # Compare types
        if type1 != type2 and type1 != program.Program.DataType.NIL and type2 != program.Program.DataType.NIL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type (INT, STRING, BOOL) or NIL \n")

        # Get label index and verify
        label_index = prog.label_get_index(self.args[0][1])

        # Jump
        if type1 == type2 and value1 == value2:
            prog.instruction_counter_set(label_index)
        else:
            prog.instruction_counter_inc()

class JUMPIFNEQ(Instruction):

    def execute(self, prog: program.Program):
        # Get symbols
        if (len(self.args) == 1):
            type2, value2 = prog.data_stack_pop()
            type1, value1 = prog.data_stack_pop()
        else:
            type1, value1 = _get_value(prog, self.args[1], True)
            type2, value2 = _get_value(prog, self.args[2], True)

        # Compare types
        if type1 != type2 and type1 != program.Program.DataType.NIL and type2 != program.Program.DataType.NIL:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires both arguments same type (INT, STRING, BOOL) or NIL \n")

        # Get label index and verify
        label_index = prog.label_get_index(self.args[0][1])

        # Jump
        if type1 != type2 or value1 != value2:
            prog.instruction_counter_set(label_index)
        else:
            prog.instruction_counter_inc()

class EXIT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()

        # Get symbol
        type, value = _get_value(prog, self.args[0], True)

        if type != int:
            error.exit(error.code.ERR_CODE_TYPE, f"Operation '{self.opcode}' requires INT type\n")

        if value < 0 or value > 49:
            error.exit(error.code.ERR_CODE_ZERO, f"Operation '{self.opcode}' requires INT value in range 0-49\n")

        # Exit
        prog.exit(value)

class DPRINT(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        
        # Get value
        if self.args[0][0] == program.Program.DataType.VAR:
            if not prog.var_is_defined(self.args[0][1]):
                error.print("Variable is not defined\n")
                return
            type, value = prog.var_get(self.args[0][1])
        else:
            value = _convert_str_to_value(self.args[0][0], self.args[0][1])

        # Print
        sys.stderr.write(f"{value}")

class BREAK(Instruction):

    def execute(self, prog: program.Program):
        prog.instruction_counter_inc()
        sys.stderr.write(prog.get_status())
        sys.stderr.flush()

# --------------------------------------------

def _get_value(prog: program.Program, symb, must=False) -> tuple:
    # Symbol is variable
    if symb[0] == program.Program.DataType.VAR:
        return prog.var_get(symb[1], must)
    # Symbol is constant
    else:
        return symb[0], _convert_str_to_value(symb[0], symb[1])

def _convert_str_to_value(type, string: str):
    if type == str:
        if string == None:
            return ""
        return re.compile(rb"\\(\d{1,3})").sub(lambda m: bytes([int(m.group(1))]), string.encode()).decode()
    elif type == bool:
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            error.exit(error.code.ERR_CODE_VALUE, f"Invalid value of bool: {string}\n")
    elif type == int:
        try:
            return int(string)
        except ValueError:
            error.exit(error.code.ERR_XML_SYNTAX, f"Value '{string}' is not valid INT value\n")
    else:
        return program.Program.DataType.NIL