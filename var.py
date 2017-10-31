import context
import instruction
from enum import Enum

class Variable(instruction.Instruction):

    class Type(Enum):
        Array = 0
        Variable = 1
        Pair = 2
        String = 3

    def __init__(self, variable, init=""):
        self.text = variable
        self.initiation = init

    def init(self):
        return instruction.Instruction(self.initiation)


    def __call__(self, output, enclosure):
        output = self.putOffset(output)
        output += self.text
        output += "\n"
        return output