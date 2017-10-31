class Context:

    def __init__(self, text=""):
        self.text = text
        self.subcontexts = list()
        self.offset = 0

    def __iadd__(self, other):
        self.subcontexts.append(other)
        other.offset = self.offset + 1
        return self

    def putOffset(self, output):
        for i in range(self.offset):
            output += "\t"

        return output

    def __call__(self, output, enclosure):
        if self.text:
            output = self.putOffset(output)
            output += self.text

        if enclosure:
            output += "\n"
            output = self.putOffset(output)
            output += enclosure[0]
            output += "\n"

        for i in self.subcontexts:
            output = i(output, enclosure)

        if enclosure:
            output = self.putOffset(output)
            output += enclosure[1]
            output += "\n"

        return output