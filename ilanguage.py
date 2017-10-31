import context
import instruction

from enum import Enum


class ILanguage:

    class Copy(Enum):
        Assign = 0
        Full = 1


    class StaticScope(Enum):
        Outer = 0
        Inner = 1

    class Compare(Enum):
        Less = 0
        LessEq = 1
        Greater = 2
        GreaterEq = 3
        Eq = 4

    class Visibility(Enum):
        public = 0
        protected = 1
        private = 2

    def __init__(self, destructable=False):
        self.destructable = destructable
        self.chunks = {}

    def createMethod(self, visibility, name, _return, *params):
        raise NotImplementedError()
    def includes(self):
        raise NotImplementedError()
    def reserve(self, name, type, size, assign=""):
        raise NotImplementedError()
    def struct(self, name):
        raise NotImplementedError()
    def glue(self):
        return instruction.Instruction("")
    def static(self):
        raise NotImplementedError()
    def enum(self, name):
        raise NotImplementedError()
    def map(self, key, value, name):
        raise NotImplementedError()
    def copy(self, destination, source, type=Copy.Assign, bytes=0):
        raise NotImplementedError()
    def type(self, type, chunkSize):
        raise NotImplementedError()
    def typeName(self, name):
        raise NotImplementedError()
    def defaultConstructor(self, structName):
        raise NotImplementedError()
    def staticInit(self):
        raise NotImplementedError()
    def staticontext(self):
        raise NotImplementedError()
    def putEntry(self, map, key, value):
        raise NotImplementedError()
    def getFromClass(self, className, member):
        raise NotImplementedError()
    def init(self, type, chunkSize, *values):
        raise NotImplementedError()
    def max(self, left, right):
        raise NotImplementedError()
    def loop(self, left, right, compare):
        raise NotImplementedError()
    def arrayaccess(self, array, index):
        raise NotImplementedError()
    def mapaccess(self, map, key, output, type, chunksize):
        raise NotImplementedError()
    def assign(self, instruction):
        raise NotImplementedError()
    def leftshift(self, left, right):
        raise NotImplementedError()
    def rightshift(self, left, right):
        raise NotImplementedError()
    def add(self, left, right):
        raise NotImplementedError()
    def ifsection(self, left, right, operator):
        raise NotImplementedError()
    def arrayaccessassign(self, array, index, output, type, chunksize):
        raise NotImplementedError()
    def objectmember(self, member):
        raise NotImplementedError()
    def set(self, left, right):
        raise NotImplementedError()
    def elsesection(self):
        raise NotImplementedError()
    def exec(self, methodName, *params):
        raise NotImplementedError()
    def setarray(self, array, index, value):
        raise NotImplementedError()
    def enumValuesNumereted(self):
        raise NotImplementedError()
    def setVisibility(self, variable, visibility):
        raise NotImplementedError()