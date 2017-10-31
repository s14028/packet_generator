import ilanguage
import context
import instruction
import var

class Interpreter:
    def __init__(self, metaData):
        self.metaData = metaData
        self.enumName = "{}Members".format(self.metaData.structName)
        self.bufferName = "m_buffer"
        self.mapName = "global"

    def insertToEnum(self, enum, numereted):
        if numereted:
            counter = 0
            for i, j in self.metaData.membersBits:
                enum += instruction.Instruction("{} = {},".format(i, str(counter)))
                counter += 1
            lastInstruction = enum.subcontexts[-1:][0]
            lastInstruction.text = lastInstruction.text[:-1]
        else:
            for i, j in self.metaData.membersBits:
                enum += instruction.Instruction("{},".format(i))
            lastInstruction = enum.subcontexts[-1:][0]
            lastInstruction.text = lastInstruction.text[:-1]

    def countBytes(self):
        memberSet = self.metaData.membersBits
        return memberSet[-1:][0][1]["upperBound"] + 1

    def members(self, language):
        members = []
        static = []

        members.append(language.reserve(self.bufferName, var.Variable.Type.Array, 8, "{}".format(self.countBytes())))
        language.setVisibility(members[0], ilanguage.ILanguage.Visibility.private)

        map = language.map(
            language.typeName(self.enumName), language.type(var.Variable.Type.Array, 32), self.mapName)

        static.append(map)

        for i in static: i.text = language.static() + " " + i.text
        language.setVisibility(map, ilanguage.ILanguage.Visibility.private)

        return members, static, map

    def constructor(self, members, language, context):
        constructorContext = language.defaultConstructor(self.metaData.structName)
        context += constructorContext
        for i in members:
            constructorContext += i.init()
        return constructorContext

    def destructor(self, structContext, language):
        pass

    def appendMembers(self, structContext, members, static, glue):
        for i in members:
            structContext += i

        for i in static:
            structContext += i

    def read(self, language, context):
        function = language.createMethod(ilanguage.ILanguage.Visibility.public, "read", "void", ("buffer", var.Variable.Type.Array, 8))
        context += function
        function += language.copy(self.bufferName, "buffer", ilanguage.ILanguage.Copy.Full)

    def write(self, language, context):
        function = language.createMethod(ilanguage.ILanguage.Visibility.public, "write", "void", ("buffer", var.Variable.Type.Array, 8))
        context += function
        function += language.copy("buffer", self.bufferName, ilanguage.ILanguage.Copy.Full)

    def get(self, language, context):
        function = language.createMethod(ilanguage.ILanguage.Visibility.public, "get", "void", (self.enumName, "member"),
                                         ("buffer", var.Variable.Type.Array, 8))
        context += function

        function += language.mapaccess(self.mapName, "member", "array", var.Variable.Type.Array, 32)
        function += language.reserve("bound", var.Variable.Type.Array, 32, 2)
        function += function.subcontexts[-1:][0].init()

        function += language.glue()

        function += language.setarray("bound", 0, "0")
        function += language.setarray("bound", 1, "0")

        function += language.glue()

        function += language.exec("copy", language.objectmember(self.bufferName), "array", "buffer", "bound")




    def set(self, language, context):
        function = language.createMethod(ilanguage.ILanguage.Visibility.public, "set", "void", (self.enumName, "member"),
                                         ("buffer", var.Variable.Type.Array, 8))
        context += function

        function += language.mapaccess(self.mapName, "member", "array", var.Variable.Type.Array, 32)
        function += language.reserve("memberBounds", var.Variable.Type.Array, 32, 2)
        function += language.reserve("bufferBounds", var.Variable.Type.Array, 32, 4)
        function += function.subcontexts[-2:][0].init()
        function += function.subcontexts[-2:][0].init()

        function += language.glue()

        function += language.setarray("memberBounds", 0, language.arrayaccess("array", 0))
        function += language.setarray("memberBounds", 1, language.arrayaccess("array", 1))

        function += language.glue()

        function += language.reserve("l", var.Variable.Type.Variable, 32, language.arrayaccess("array", 3) +  " - " + language.arrayaccess("array", 1))
        function += language.reserve("upperBound", var.Variable.Type.Variable, 32, language.arrayaccess("array", 2) + " - " + language.arrayaccess("array", 0))
        function += function.subcontexts[-2:][0].init()
        function += function.subcontexts[-2:][0].init()

        ifsection = language.ifsection("l", "0", ilanguage.ILanguage.Compare.LessEq)
        function += ifsection

        ifsection += language.set("l", "8 + l")
        ifsection += language.set("upperBound", "upperBound - 1")

        function += language.glue()

        function += language.setarray("bufferBounds", 0, "0")
        function += language.setarray("bufferBounds", 1, "0")
        function += language.setarray("bufferBounds", 2, "upperBound")
        function += language.setarray("bufferBounds", 3, "l")

        function += language.exec(language.objectmember("clear"), "member")
        function += language.exec(language.objectmember("copy"), "buffer", "bufferBounds", language.objectmember(self.bufferName), "memberBounds")

    def clear(self, language, context):
        function = language.createMethod(ilanguage.ILanguage.Visibility.protected, "clear", "void", (self.enumName, "member"))
        context += function

        function += language.mapaccess(self.mapName, "member", "array", var.Variable.Type.Array, 32)
        function += language.reserve("i", var.Variable.Type.Variable, 32, language.arrayaccess("array", 0) + " + 1")
        function += function.subcontexts[-1:][0].init()

        function += language.glue()

        loopContext = language.loop("i", language.arrayaccess("array", 3), ilanguage.ILanguage.Compare.Less)
        function += loopContext

        loopContext += language.set(language.arrayaccess(language.objectmember(self.bufferName), "i"), "0")
        loopContext += language.assign(language.add("i", "1"))

        ifsection = language.ifsection(language.arrayaccess("array", 0), language.arrayaccess("array", 0), ilanguage.ILanguage.Compare.Eq)
        function += ifsection

        ifsection += language.arrayaccessassign(language.objectmember(self.bufferName), language.arrayaccess("array", 0), "copy", var.Variable.Type.Variable, 32)
        ifsection += language.assign(language.rightshift("copy", "8 - {}".format(language.arrayaccess("array", 1))))
        ifsection += language.assign(language.leftshift("copy", "8 - {}".format(language.arrayaccess("array", 1))))

        ifsection += language.glue()

        ifsection += language.assign(
            language.leftshift(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                language.arrayaccess("array", 3)))
        ifsection += language.assign(
            language.rightshift(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                language.arrayaccess("array", 3)))
        ifsection += language.assign(
            language.add(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                "copy"))

        elsesection = language.elsesection()
        function += elsesection

        elsesection += language.assign(
            language.rightshift(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                "8 - {}".format(language.arrayaccess("array", 1))))
        elsesection += language.assign(
            language.leftshift(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                "8 - {}".format(language.arrayaccess("array", 1))))
        elsesection += language.assign(
            language.leftshift(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                "8 - {}".format(language.arrayaccess("array", 3))))
        elsesection += language.assign(
            language.rightshift(
                language.arrayaccess(language.objectmember(self.bufferName), language.arrayaccess("array", 0)),
                "8 - {}".format(language.arrayaccess("array", 3))))


    def copy(self, language, context):
        function = language.createMethod(ilanguage.ILanguage.Visibility.protected, "copy", "void", ("source", var.Variable.Type.Array, 8),
                                         ("sourceBounds", var.Variable.Type.Array, 32),
                                         ("destination", var.Variable.Type.Array, 8),
                                         ("destinationBounds", var.Variable.Type.Array, 32))
        context += function

        sourceLowerBound = language.arrayaccess("sourceBounds", 0)
        sourceLowerBit = language.arrayaccess("sourceBounds", 1)

        sourceUpperBound = language.arrayaccess("sourceBounds", 2)
        sourceUpperBit = language.arrayaccess("sourceBounds", 3)

        destinationLowerBound = language.arrayaccess("destinationBounds", 0)
        destinationLowerBit = language.arrayaccess("destinationBounds", 1)

        loopContext = language.loop(sourceLowerBound, sourceUpperBound,
                                    ilanguage.ILanguage.Compare.LessEq)
        function += loopContext

        maximum = language.reserve("max", var.Variable.Type.Variable, 32,
                                   language.max(sourceLowerBit, destinationLowerBit))
        loopContext += maximum
        loopContext += maximum.init()

        loopContext += language.arrayaccessassign("source", sourceLowerBound, "chunk", var.Variable.Type.Variable, 32)
        loopContext += language.assign(language.leftshift("chunk", sourceLowerBit))
        loopContext += language.assign(language.rightshift("chunk", destinationLowerBit))
        loopContext += language.assign(language.add(language.arrayaccess("destination", destinationLowerBound), "chunk"))

        loopContext += language.assign(language.add(sourceLowerBit, "8 - max"))
        loopContext += language.assign(language.add(destinationLowerBit, "8 - max"))

        loopContext += language.glue()

        ifsection = language.ifsection(sourceLowerBit, 8, ilanguage.ILanguage.Compare.Eq)
        loopContext += ifsection
        ifsection += language.assign(language.add(sourceLowerBound, 1))

        loopContext += language.glue()

        ifsection = language.ifsection(destinationLowerBit, 8, ilanguage.ILanguage.Compare.Eq)
        loopContext += ifsection
        ifsection += language.assign(language.add(destinationLowerBound, 1))

    def initStatic(self, language, static, context=None):
        staticontext = language.staticontext()
        if context:
            context += staticontext
        for i in static: staticontext += i.init()
        for i, j in self.metaData.membersBits:
            array = language.init(var.Variable.Type.Array, 32, j["lowerBound"], j["lowerBit"], j["upperBound"], j["upperBit"])
            staticontext += language.putEntry(self.mapName, language.getFromClass(self.enumName, i), array)
        return staticontext

    def produceCode(self, language):
        globalContext = []
        globalContext.extend(language.includes())
        staticInitContext = language.staticInit()

        enum = language.enum(self.enumName)
        self.insertToEnum(enum, language.enumValuesNumereted())

        globalContext.append(enum)

        structContext = language.struct(self.metaData.structName)
        globalContext.append(structContext)

        members, static, map = self.members(language)
        self.appendMembers(structContext, members, static, language.glue())

        if staticInitContext == ilanguage.ILanguage.StaticScope.Outer:
            globalContext.append(self.initStatic(language, static))
        else:
            self.initStatic(language, static, structContext)

        structContext += language.glue()
        constructor = self.constructor(members, language, structContext)
        structContext += language.glue()

        self.clear(language, structContext)
        structContext += language.glue()

        self.copy(language, structContext)
        structContext += language.glue()

        self.read(language, structContext)
        structContext += language.glue()

        self.write(language, structContext)
        structContext += language.glue()

        self.get(language, structContext)
        structContext += language.glue()

        self.set(language, structContext)
        structContext += language.glue()
        output = ""
        for i in globalContext:
            output = i(output, ("{", "}"))
            output += "\n"
        output = output[:-1]

        return output