import ilanguage
import context
import instruction
import var


class JavaLanguage(ilanguage.ILanguage):

    def __init__(self, destructable=False):
        super().__init__()
        self.destructable = False
        self.chunks = {8 : "byte",
                       32 : "int"}
        self.operators = {ilanguage.ILanguage.Compare.Less : "<",
                          ilanguage.ILanguage.Compare.LessEq : "<=",
                          ilanguage.ILanguage.Compare.Greater : ">",
                          ilanguage.ILanguage.Compare.GreaterEq : ">=",
                          ilanguage.ILanguage.Compare.Eq : "=="}
        self.visibility = {ilanguage.ILanguage.Visibility.public : "public",
                           ilanguage.ILanguage.Visibility.protected: "protected",
                           ilanguage.ILanguage.Visibility.private: "private"}


    def includes(self):
        includeContext = []
        includeKeyWord = "import"

        includeList = ["java.util.Map", "java.util.HashMap"]

        for i in includeList:
            include = instruction.Instruction("{} {};".format(includeKeyWord, i))
            includeContext.append(include)

        return includeContext

    def reserve(self, name, type, chunksize, assign=""):
        typeName = self.chunks[chunksize]
        if type == var.Variable.Type.Array:
            return var.Variable("{}[] {};".format(typeName, name), "{} = new {}[{}];".format(name, typeName, assign))
        return var.Variable("{} {};".format(typeName, name), "{} = {};".format(name, assign))


    def struct(self, name):
        return context.Context("class {}".format(name))

    def parseParams(self, *params):
        string = ""

        if params:
            for i in params:
                if len(i) == 3:
                    if i[1] == var.Variable.Type.Array:
                        string += "{}[] {}, ".format(self.chunks[i[2]], i[0])
                    else:
                        string += "{} {}, ".format(self.chunks[i[2]], i[0])
                else:
                    string += "{} {}, ".format(i[0], i[1])
            string = string[:-2]

        return string


    def createMethod(self, visibility, name, _return,*params):
        string = self.parseParams(*params)

        visibility = self.visibility[visibility]

        if _return != "void":
            return context.Context("{} {} {}({})".format(visibility, self.chunks[_return], name, string))
        return context.Context("{} void {}({})".format(visibility, name, string))

    def glue(self):
        return super().glue()

    def static(self):
        return "static"

    def enum(self, name):
        return context.Context("enum {}".format(name))

    def copy(self, destination, source, type=ilanguage.ILanguage.Copy.Assign, size=0):
        if type == ilanguage.ILanguage.Copy.Full:
            return instruction.Instruction("System.arraycopy({}, {}, {}, {}, {});".format(source, 0, destination, 0, size))
        return instruction.Instruction("{} = {};".format(destination, source))

    def map(self, key, value, name):
        return var.Variable("Map<{}, {}> {};".format(key.text, value.text, name), "{} = new HashMap<>();".format(name))

    def type(self, type, chunkSize):
        if type == var.Variable.Type.Array:
            return instruction.Instruction("{}[]".format(self.chunks[chunkSize]))
        return instruction.Instruction(self.chunks[chunkSize])


    def typeName(self, name):
        return instruction.Instruction(name)

    def defaultConstructor(self, structName):
        return context.Context("{} {}()".format(self.visibility[ilanguage.ILanguage.Visibility.public], structName))

    def staticInit(self):
        return ilanguage.ILanguage.StaticScope.Inner

    def staticontext(self):
        return context.Context("static")

    def getFromClass(self, className, member):
        return "{}.{}".format(className, member)

    def init(self, type, chunkSize, *values):
        if type == var.Variable.Type.Array:
            arguments = ""
            for i in values:
                arguments += str(i) + ", "
            arguments = arguments[:-2]
            return "new {}[]".format(self.chunks[chunkSize]) + " {" + arguments + "}"

    def putEntry(self, map, key, value):
        return instruction.Instruction("{}.put({}, {});".format(map, key, value))

    def max(self, left, right):
        return "Math.max({}, {})".format(left, right)

    def loop(self, left, right, compare):
        return context.Context("while({} {} {})".format(left, self.operators[compare], right))

    def arrayaccessassign(self, array, index, output, type, chunksize):
        index = str(index)
        if type == var.Variable.Type.Variable:
            return var.Variable("{} {} = {}[{}];".format(self.chunks[chunksize], output, array, index))
        return var.Variable("{}[] {} = {}[{}];".format(self.chunks[chunksize], output, array, index))

    def mapaccess(self, map, key, output, type, chunksize):
        if type == var.Variable.Type.Variable:
            return var.Variable("{} {} = {}.get({});".format(self.chunks[chunksize], output, map, key))
        return var.Variable("{}[] {} = {}.get({});".format(self.chunks[chunksize], output, map, key))

    def assign(self, instruction):
        text = instruction.text
        indexToPlace = text.find(" ")
        indexToPlace = text[indexToPlace + 1:].find(" ") + indexToPlace + 1
        text = text[:indexToPlace] + "=" + text[indexToPlace:]
        instruction.text = text
        return instruction

    def set(self, left, right):
        return instruction.Instruction("{} = {};".format(left, right))

    def leftshift(self, left, right):
        return instruction.Instruction("{} << {};".format(left, right))

    def rightshift(self, left, right):
        return instruction.Instruction("{} >>> {};".format(left, right))

    def add(self, left, right):
        return instruction.Instruction("{} + {};".format(left, right))

    def ifsection(self, left, right, operator):
        return context.Context("if({} {} {})".format(left, self.operators[operator], right))

    def arrayaccess(self, array, index):
        index = str(index)
        return "{}[{}]".format(array, index)

    def objectmember(self, member):
        return "this.{}".format(member)

    def elsesection(self):
        return context.Context("else")

    def exec(self, methodName, *params):
        string = ""
        for i in params:
            string += i + ", "
        string = string[:-2]
        return instruction.Instruction("{}({});".format(methodName, string))

    def setarray(self, array, index, value):
        return instruction.Instruction("{}[{}] = {};".format(array, index, value))

    def enumValuesNumereted(self):
        return False

    def setVisibility(self, variable, visibility):
        variable.text = "{} {}".format(self.visibility[visibility], variable.text)