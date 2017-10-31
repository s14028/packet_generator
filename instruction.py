from enum import Enum
import context


class Instruction(context.Context):

    def __init__(self, text):
        self.text = text
        self.offset = 0

    def __call__(self, output, enclosure):
        output = self.putOffset(output)
        output += self.text
        output += "\n"
        return output