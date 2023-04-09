# IPP 2023, project 2
# Author: Marek Gergel, xgerge01
# File: program.py
# Description: Program data manipulation
# Date: 2023-04-07

from . import instruction
import sys

class Program:

    class DataType:
        INT = "int"
        BOOL = "bool"
        STRING = "string"
        NIL = "nil"
        LABEL = "label"
        TYPE = "type"
        VAR = "var"

    class _Frame:
        GF = "GF"
        LF = "LF"
        TF = "TF"

    instructions = []
    frame_global = {}
    frame_local = {}
    frame_temp = {}
    frame_stack = []
    labels = {}
    _instruction_executed = 0
    _instruction_next_index = 0

    def var_set(self, var, value):
        if f"{self._Frame.GF}@" in var[0]:
            self.frame_global[var[1]] = value
        elif f"{self._Frame.LF}@" in var[0]:
            self.frame_local[var[1]] = value
        elif f"{self._Frame.TF}@" in var[0]:
            self.frame_temp[var[1]] = value

    def var_get(self, var):
        if f"{self._Frame.GF}@" in var[0]:
            return self.frame_global[var[1]]
        elif f"{self._Frame.LF}@" in var[0]:
            return self.frame_local[var[1]]
        elif f"{self._Frame.TF}@" in var[0]:
            return self.frame_temp[var[1]]

    def var_type(self, var):
        pass

    def var_defined(self, var) -> bool:
        if f"{self._Frame.GF}@" in var[0]:
            if var[1] in self.frame_global:
                return True
        elif f"{self._Frame.LF}@" in var[0]:
            if var[1] in self.frame_local:
                return True
        elif f"{self._Frame.TF}@" in var[0]:
            if var[1] in self.frame_temp:
                return True
        return False

    def var_delete(self, var):
        pass

    def label_set(self, label, index):
        self.labels[label] = index

    def label_get(self, label) -> int:
        return self.labels[label]

    def label_defined(self, label) -> bool:
        if label in self.labels:
            return True
        return False

    def frame_set(self, frame):
        pass

    def frame_get(self):
        pass

    def frame_delete(self):
        pass

    def instruction_next(self):
        self._instruction_executed += 1
        self._instruction_next_index += 1

    def instruction_next_set(self, index):
        self._instruction_executed += 1
        self._instruction_next_index = index

    def instruction_next_get(self) -> int:
        return self._instruction_next_index

    def instructions_executed(self) -> int:
        return self._instruction_executed

    def execute(self):
        while self.instruction_next_get() < len(self.instructions):
            self.instructions[self.instruction_next_get()].execute(self)