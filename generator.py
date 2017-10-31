import argparse
import string
import collections
from collections import Counter

import interpreter
import languages
'''

Package
{
    atribute[A-Za-z]\w*:size\d+
}

'''

class MetaData:
    def __init__(self):
        self.structName = ""
        self.membersBits = []

def parse():
    parser = argparse.ArgumentParser("Packet generator")
    parser.add_argument("-i", "--input", dest="input", type=str, help="Path to config.")
    parser.add_argument("-o", "--output", dest="output", type=str, help="Output file path.")
    parser.add_argument("-l", "--language", dest="language", type=str, help="Language for output.")
    parser = parser.parse_args()
    return parser

def retrieveStruct(input):
    indexLeft = input.index("{")
    structName = input[0:indexLeft].strip()
    if not structName:
        raise SyntaxError("You forgot structure name.")

    if structName[0] in string.digits:
        raise SyntaxError("Name of structure should start with letter.")
    return structName, indexLeft

def retrieveMembers(input):
    input = [i.strip().split(":") for i in input.split("\n") if i]
    members = []

    upperBound = 0
    upperBit = 0

    for i, j in input:
        bitCount = int(j)
        if bitCount > 1024:
            raise AttributeError("The bit count of {} is overhead.".format(j))
        elif bitCount == 0:
            raise AttributeError("Bit count can't be 0")

        lowerBound = upperBound
        lowerBit = upperBit

        freeSpace = 8 - upperBit
        chunksNeeded = bitCount // 8
        bitsLeft = bitCount % 8

        if bitsLeft <= freeSpace:
            left = freeSpace - bitsLeft
            if bitsLeft == 7:
                upperBit = 8
            else:
                upperBit = 8 - left
        else:
            bitsLeft -= freeSpace
            upperBit = bitsLeft
            chunksNeeded += 1

        upperBound = lowerBound + chunksNeeded
        members.append((i, Counter(lowerBound=lowerBound, lowerBit=lowerBit, upperBound=upperBound, upperBit=upperBit)))

    return members

def createMetaInput(input):
    metaInput = MetaData()

    structName, left = retrieveStruct(input)
    right = input.index("}")

    input = input[left + 1 : right]
    members = retrieveMembers(input)
    metaInput.membersBits = members
    metaInput.structName = structName

    return metaInput


def main():
    args = parse()

    try:
        with open(args.input, "r") as file:
            input = file.read()
    except:
        print("Couldn't open the file {}".format(args.input))
        exit(1)

    try:
        metaInput = createMetaInput(input)
    except SyntaxError as error:
        print("Couldn't parse file.\n{}".format(error.text))
    except AttributeError as error:
        print(error)
    except:
        print("Something is wrong with file.")

    interpret = interpreter.Interpreter(metaInput)
    language = languages.languages[args.language]

    if not language:
        print("Language \"{}\" is not supported.".format(args.language))

    output = interpret.produceCode(language)

    with open(args.output, "w") as file:
        file.write(output)


if __name__ == '__main__':
    main()