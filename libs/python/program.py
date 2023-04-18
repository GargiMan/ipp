# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: program.py
# Description: Program data manipulation
# Date: 2023-04-07

from . import error
import re

class Program:

    class DataType:
        INT = "int"
        BOOL = "bool"
        STRING = "string"
        NIL = "nil"
        VAR = "var"

    class _Frame:
        GF = "GF"
        LF = "LF"
        TF = "TF"

    _labels = {}
    instructions = []
    _frame_global = {}
    _frame_local = None
    _frame_temp = None
    _frame_stack = []
    _data_stack = []
    _call_stack = []
    _instruction_executed = 0
    _instruction_next_index = 0
    _exit_code = 0

    input_file = None
    input_close = False

    def __init__(self, input=None):

        self.input_file = input

        # Open input file
        if not hasattr(self.input_file, "read"):
            try:
                self.input_file = open(self.input_file, "r")
                self.input_close = True
            except:
                error.exit(error.code.ERR_INPUT, f"Input file '{self.input_file}' does not exist or could not be read\n")

    def __del__(self):
        # Close input file
        if self.input_close:
            self.input_file.close()

    def var_define(self, var, type=None, value=None):
        # Check if variable is already defined
        if self.var_is_defined(var):
            error.exit(error.code.ERR_XML_SEMANTIC, "Variable is already defined\n")

        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self._Frame.GF:
                self._frame_global[var_name] = type, value
            case self._Frame.LF:
                if self._frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                self._frame_local[var_name] = type, value
            case self._Frame.TF:
                if self._frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                self._frame_temp[var_name] = type, value

    def var_set(self, var, type, value):
        if not self.var_is_defined(var):
            error.exit(error.code.ERR_CODE_VARIABLE, "Variable is not defined\n")
        
        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self._Frame.GF:
                self._frame_global[var_name] = type, value
            case self._Frame.LF:
                if self._frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                self._frame_local[var_name] = type, value
            case self._Frame.TF:
                if self._frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                self._frame_temp[var_name] = type, value

    def var_get(self, var, must=False) -> tuple:
        if not self.var_is_defined(var):
            error.exit(error.code.ERR_CODE_VARIABLE, "Variable is not defined\n")
        if must and not self.var_is_initialized(var):
            error.exit(error.code.ERR_CODE_VALUE, f"Variable is not initialized\n")

        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self._Frame.GF:
                return self._frame_global[var_name]
            case self._Frame.LF:
                if self._frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                return self._frame_local[var_name]
            case self._Frame.TF:
                if self._frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                return self._frame_temp[var_name]

    def var_is_defined(self, var) -> bool:
        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self._Frame.GF:
                if var_name in self._frame_global:
                    return True
            case self._Frame.LF:
                if self._frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                if var_name in self._frame_local:
                    return True
            case self._Frame.TF:
                if self._frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                if var_name in self._frame_temp:
                    return True
        return False
    
    def var_is_initialized(self, var) -> bool:
        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self._Frame.GF:
                return self._frame_global[var_name][0] != None
            case self._Frame.LF:
                if self._frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                return self._frame_local[var_name][0] != None
            case self._Frame.TF:
                if self._frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                return self._frame_temp[var_name][0] != None

    def label_create(self, label, index):
        self._labels[label] = index

    def label_get_index(self, label) -> int:
        # Label verification
        if not self.label_is_defined(label):
            error.exit(error.code.ERR_XML_SEMANTIC, "Label is not defined\n")
        # Return label index
        return self._labels[label]

    def label_is_defined(self, label) -> bool:
        return label in self._labels

    def frame_create(self):
        # Create new temp frame
        self._frame_temp = {}

    def frame_push(self):
        # Check if temp frame is defined (empty temp frame)
        if self._frame_temp is None:
            error.exit(error.code.ERR_CODE_FRAME, "Temp frame is not defined\n")
        
        # Push local frame to stack
        if self._frame_local is not None:
            self._frame_stack.append(self._frame_local)

        # Push temp frame to local frame
        self._frame_local = self._frame_temp
        self._frame_temp = None

    def frame_pop(self):
        # Check if local frame is defined (empty local frame, local frame is top from stack)
        if self._frame_local is None:
            error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
        
        # Pop temp frame from local frame
        self._frame_temp = self._frame_local

        # Pop local frame from stack
        if len(self._frame_stack) != 0:
            self._frame_local = self._frame_stack.pop()
        else:
            self._frame_local = None

    def call_stack_push(self, index):
        self._call_stack.append(index)

    def call_stack_pop(self):
        if len(self._call_stack) == 0:
            error.exit(error.code.ERR_CODE_VALUE, "Call stack is empty\n")
        return self._call_stack.pop()

    def data_stack_push(self, type, value):
        self._data_stack.append((type, value))

    def data_stack_pop(self) -> tuple:
        if len(self._data_stack) == 0:
            error.exit(error.code.ERR_CODE_VALUE, "Data stack is empty\n")
        return self._data_stack.pop()

    def data_stack_clear(self):
        self._data_stack = []

    def instruction_counter_inc(self):
        self._instruction_executed += 1
        self._instruction_next_index += 1

    def instruction_counter_set(self, index):
        self._instruction_executed += 1
        self._instruction_next_index = index

    def instruction_counter_get(self) -> int:
        return self._instruction_next_index

    def instructions_executed(self) -> int:
        return self._instruction_executed

    def instruction_add(self, instruction):
        self.instructions.append(instruction)

    def instructions_count(self) -> int:
        return len(self.instructions)

    def execute(self):
        while self.instruction_counter_get() < self.instructions_count():
            self.instructions[self.instruction_counter_get()].execute(self)
        
    def exit(self, code):
        self._exit_code = code
        self.instruction_counter_set(self.instructions_count())

    def get_exit_code(self) -> int:
        return self._exit_code

    def get_status(self):
        return "DEBUG:\n"\
        +f"Instruction line: {self.instruction_counter_get()}\n"\
        +f"Instructions executed: {self.instructions_executed()}\n"\
        +f"Global frame: {self._frame_global}\n"\
        +f"Local frame: {self._frame_local}\n"\
        +f"Temporary frame: {self._frame_temp}\n"\
        +f"Stack: {self._frame_stack}\n"\
        +f"Data stack: {self._data_stack}\n"\
        +f"Call stack: {self._call_stack}\n"
        