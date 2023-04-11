# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: program.py
# Description: Program data manipulation
# Date: 2023-04-07

from . import params,error
import re

class Program:

    class DataType:
        INT = "int"
        BOOL = "bool"
        STRING = "string"
        NIL = "nil"
        LABEL = "label"
        TYPE = "type"
        VAR = "var"

    class Frame:
        GF = "GF"
        LF = "LF"
        TF = "TF"

    instructions = []
    frame_global = {}
    frame_local = None
    frame_temp = None
    frame_stack = []
    data_stack = []
    call_stack = []
    labels = {}
    _instruction_executed = 0
    _instruction_next_index = 0
    exit_code = 0

    close_input = False

    def __init__(self):
        # Open input file
        if not hasattr(params.input, "read"):
            try:
                params.input = open(params.input, "r")
                self.close_input = True
            except:
                error.exit(error.code.ERR_INPUT, f"Input file '{params.input}' does not exist or could not be read\n")

    def __del__(self):
        # Close input file
        if self.close_input:
            params.input.close()

    def var_define(self, var, type=None, value=None):
        # Check if variable is already defined
        if self.var_is_defined(var):
            error.exit(error.code.ERR_XML_SEMANTIC, "Variable is already defined\n")

        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self.Frame.GF:
                self.frame_global[var_name] = type, value
            case self.Frame.LF:
                if self.frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                self.frame_local[var_name] = type, value
            case self.Frame.TF:
                if self.frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                self.frame_temp[var_name] = type, value

    def var_set(self, var, type, value):
        if not self.var_is_defined(var):
            error.exit(error.code.ERR_CODE_VARIABLE, "Variable is not defined\n")
        
        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self.Frame.GF:
                self.frame_global[var_name] = type, value
            case self.Frame.LF:
                if self.frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                self.frame_local[var_name] = type, value
            case self.Frame.TF:
                if self.frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                self.frame_temp[var_name] = type, value

    def var_get_value(self, var, must=False) -> str:
        if not self.var_is_defined(var):
            error.exit(error.code.ERR_CODE_VARIABLE, "Variable is not defined\n")
        if must and not self.var_is_initialized(var):
            error.exit(error.code.ERR_CODE_VALUE, f"Variable is not initialized\n")

        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self.Frame.GF:
                return self.frame_global[var_name][1]
            case self.Frame.LF:
                if self.frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                return self.frame_local[var_name][1]
            case self.Frame.TF:
                if self.frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                return self.frame_temp[var_name][1]

    def var_get_type(self, var, must=False) -> str:
        if not self.var_is_defined(var):
            error.exit(error.code.ERR_CODE_VARIABLE, "Variable is not defined\n")
        if must and not self.var_is_initialized(var):
            error.exit(error.code.ERR_CODE_VALUE, f"Variable is not initialized\n")

        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self.Frame.GF:
                return self.frame_global[var_name][0]
            case self.Frame.LF:
                if self.frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                return self.frame_local[var_name][0]
            case self.Frame.TF:
                if self.frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                return self.frame_temp[var_name][0]

    def var_is_defined(self, var) -> bool:
        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self.Frame.GF:
                if var_name in self.frame_global:
                    return True
            case self.Frame.LF:
                if self.frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                if var_name in self.frame_local:
                    return True
            case self.Frame.TF:
                if self.frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                if var_name in self.frame_temp:
                    return True
        return False
    
    def var_is_initialized(self, var) -> bool:
        var_frame = re.split(r'@', var)[0]
        var_name = re.split(r'@', var)[1]
        match var_frame:
            case self.Frame.GF:
                return self.frame_global[var_name][0] != None and self.frame_global[var_name][1] != None
            case self.Frame.LF:
                if self.frame_local is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
                return self.frame_local[var_name][0] != None and self.frame_local[var_name][1] != None
            case self.Frame.TF:
                if self.frame_temp is None:
                    error.exit(error.code.ERR_CODE_FRAME, "Temporary frame is not defined\n")
                return self.frame_temp[var_name][0] != None and self.frame_temp[var_name][1] != None

    def label_create(self, label, index):
        self.labels[label] = index

    def label_get_index(self, label) -> int:
        # Label verification
        if not self.label_is_defined(label):
            error.exit(error.code.ERR_XML_SEMANTIC, "Label is not defined\n")
        # Return label index
        return self.labels[label]

    def label_is_defined(self, label) -> bool:
        return label in self.labels

    def frame_create(self):
        # Create new temp frame
        self.frame_temp = {}

    def frame_push(self):
        # Check if temp frame is defined (empty temp frame)
        if self.frame_temp is None:
            error.exit(error.code.ERR_CODE_FRAME, "Temp frame is not defined\n")
        
        # Push local frame to stack
        if self.frame_local is not None:
            self.frame_stack.append(self.frame_local)

        # Push temp frame to local frame
        self.frame_local = self.frame_temp
        self.frame_temp = None

    def frame_pop(self):
        # Check if local frame is defined (empty local frame, local frame is top from stack)
        if self.frame_local is None:
            error.exit(error.code.ERR_CODE_FRAME, "Local frame is not defined\n")
        
        # Pop temp frame from local frame
        self.frame_temp = self.frame_local

        # Pop local frame from stack
        if len(self.frame_stack) != 0:
            self.frame_local = self.frame_stack.pop()
        else:
            self.frame_local = None

    def call_stack_push(self, index):
        self.call_stack.append(index)

    def call_stack_pop(self):
        if len(self.call_stack) == 0:
            error.exit(error.code.ERR_CODE_VALUE, "Call stack is empty\n")
        return self.call_stack.pop()

    def data_stack_push(self, value, type):
        self.data_stack.append((value, type))

    def data_stack_pop(self):
        if len(self.data_stack) == 0:
            error.exit(error.code.ERR_CODE_VALUE, "Data stack is empty\n")
        return self.data_stack.pop()

    def instruction_index_next(self):
        self._instruction_executed += 1
        self._instruction_next_index += 1

    def instruction_index_set(self, index):
        self._instruction_executed += 1
        self._instruction_next_index = index

    def instruction_index_get(self) -> int:
        return self._instruction_next_index

    def instructions_executed(self) -> int:
        return self._instruction_executed

    def execute(self):
        while self.instruction_index_get() < len(self.instructions):
            self.instructions[self.instruction_index_get()].execute(self)
        
    def exit(self, code):
        self.exit_code = code
        self.instruction_index_set(len(self.instructions))