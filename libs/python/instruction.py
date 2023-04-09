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
        prog.instruction_next()

# --------------------------------------------

class MOVE(Instruction):

    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class CREATEFRAME(Instruction):

    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class PUSHFRAME(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class POPFRAME(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class DEFVAR(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class CALL(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class RETURN(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class PUSHS(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class POPS(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class ADD(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class SUB(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class MUL(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class IDIV(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class LT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class GT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class EQ(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class AND(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class OR(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class NOT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class INT2CHAR(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class STRI2INT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class READ(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class WRITE(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()
        # Get value
        value = re.sub(r'^.*@', '', self.args['1'][1])
        if self.args['1'][0] == program.Program.DataType.VAR:
            if not prog.var_defined(self.args['1'][1]):
                error.print("Variable not defined\n")
                return
            value = prog.var_get(self.args['1'][1])
            
        if "nil" in value:
            value = ""

        # Print
        sys.stdout.write(f"{value}")

class CONCAT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class STRLEN(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class GETCHAR(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class SETCHAR(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class TYPE(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class LABEL(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        if prog.label_defined(self.args['1'][1]):
            error.exit(error.code.ERR_XML_SEMANTIC, "Label already defined\n")
        prog.label_set(self.args['1'][1], prog.instruction_next_get())

class JUMP(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        # Label verification
        if not prog.label_defined(self.args['1'][1]):
            error.exit(error.code.ERR_XML_SEMANTIC, "Label not defined\n")

        # Jump
        prog.instruction_next_set(prog.label_get(self.args['1'][1]))

class JUMPIFEQ(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        # Label verification
        if not prog.label_defined(self.args['1'][1]):
            error.exit(error.code.ERR_XML_SEMANTIC, "Label not defined\n")
        
        # Get types and values
        type1 = self.args['2'][0]
        value1 = re.sub(r'^.*@', '', self.args['2'][1])
        if self.args['2'][0] == program.Program.DataType.VAR:
            if not prog.var_defined(self.args['2'][1]):
                error.exit(error.code.ERR_CODE_VARIABLE, "Variable not defined\n")
            type1 = prog.var_type(self.args['2'][1])
            value1 = prog.var_get(self.args['2'][1])
        type2 = self.args['3'][0]
        value2 = re.sub(r'^.*@', '', self.args['3'][1])
        if self.args['3'][0] == program.Program.DataType.VAR:
            if not prog.var_defined(self.args['3'][1]):
                error.exit(error.code.ERR_CODE_VARIABLE, "Variable not defined\n")
            type2 = prog.var_type(self.args['3'][1])
            value2 = prog.var_get(self.args['3'][1])

        # Compare types
        if type1 != type2 and type1 != 'nil' and type2 != 'nil':
            error.exit(error.code.ERR_CODE_TYPE, "Different data types of arguments\n")

        # Jump
        if value1 == value2:
            prog.instruction_next_set(prog.label_get(self.args['1'][1]))

class JUMPIFNEQ(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        # Label verification
        if not prog.label_defined(self.args['1'][1]):
            error.exit(error.code.ERR_XML_SEMANTIC, "Label not defined\n")

        # Get types and values
        type1 = self.args['2'][0]
        value1 = re.sub(r'^.*@', '', self.args['2'][1])
        if self.args['2'][0] == program.Program.DataType.VAR:
            if not prog.var_defined(self.args['2'][1]):
                error.exit(error.code.ERR_CODE_VARIABLE, "Variable not defined\n")
            type1 = prog.var_type(self.args['2'][1])
            value1 = prog.var_get(self.args['2'][1])
        type2 = self.args['3'][0]
        value2 = re.sub(r'^.*@', '', self.args['3'][1])
        if self.args['3'][0] == program.Program.DataType.VAR:
            if not prog.var_defined(self.args['3'][1]):
                error.exit(error.code.ERR_CODE_VARIABLE, "Variable not defined\n")
            type2 = prog.var_type(self.args['3'][1])
            value2 = prog.var_get(self.args['3'][1])

        # Compare types
        if type1 != type2 and type1 != 'nil' and type2 != 'nil':
            error.exit(error.code.ERR_CODE_TYPE, "Different data types of arguments\n")

        # Jump
        if value1 != value2:
            prog.instruction_next_set(prog.label_get(self.args['1'][1]))


class EXIT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()

class DPRINT(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        prog.instruction_next()
        # Get value
        value = re.sub(r'^.*@', '', self.args['1'][1])
        if self.args['1'][0] == program.Program.DataType.VAR:
            if not prog.var_defined(self.args['1'][1]):
                error.print("Variable not defined\n")
                return
            value = prog.var_get(self.args['1'][1])
            
        # Print
        sys.stderr.write(f"{value}")

class BREAK(Instruction):
    
    def __init__(self, opcode, args):
        super().__init__(opcode, args)

    def execute(self, prog: program.Program):
        sys.stderr.write(f"BREAK - {prog.instruction_next_get()}. instruction line, {prog.instructions_executed()} instructions executed\n")
        sys.stderr.write(f"Global frame: {prog.frame_global}\n")
        sys.stderr.write(f"Local frame: {prog.frame_local}\n")
        sys.stderr.write(f"Temporary frame: {prog.frame_temp}\n")
        sys.stderr.write(f"Stack: {prog.frame_stack}\n")
        sys.stderr.flush()
        prog.instruction_next()
