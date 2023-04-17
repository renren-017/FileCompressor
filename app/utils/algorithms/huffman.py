import zlib
import heapq
import os
from collections import Counter
import io
from PIL import Image


class Nodes:
    def __init__(self, probability, symbol, left=None, right=None):
        self.probability = probability

        self.symbol = symbol
        self.left = left
        self.right = right

        # the tree direction (0 or 1)
        self.code = ""


def CalculateProbability(the_data):
    the_symbols = dict()
    for item in the_data:
        if not the_symbols.get(item):
            the_symbols[item] = 1
        else:
            the_symbols[item] += 1
    return the_symbols


the_codes = dict()


def CalculateCodes(node, value=""):
    newValue = value + str(node.code)

    if node.left:
        CalculateCodes(node.left, newValue)
    if node.right:
        CalculateCodes(node.right, newValue)

    if not node.left and not node.right:
        the_codes[node.symbol] = newValue

    return the_codes


def OutputEncoded(the_data, coding):
    encodingOutput = []
    for element in the_data:
        print(coding[element], end="")
        encodingOutput.append(coding[element])

    the_string = "".join([str(item) for item in encodingOutput])
    return the_string


def TotalGain(the_data, coding):
    # total bit space to store the data before compression
    beforeCompression = len(the_data) * 8
    afterCompression = 0
    the_symbols = coding.keys()
    for symbol in the_symbols:
        the_count = the_data.count(symbol)
        # calculating how many bit is required for that symbol in total
        afterCompression += the_count * len(coding[symbol])
    print("Space usage before compression (in bits):", beforeCompression)
    print("Space usage after compression (in bits):", afterCompression)


def compress_huffman(the_data):
    symbolWithProbs = CalculateProbability(the_data)
    the_symbols = symbolWithProbs.keys()
    the_probabilities = symbolWithProbs.values()
    print("symbols: ", the_symbols)
    print("probabilities: ", the_probabilities)

    the_nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for symbol in the_symbols:
        the_nodes.append(Nodes(symbolWithProbs.get(symbol), symbol))

    while len(the_nodes) > 1:
        # sorting all the nodes in ascending order based on their probability
        the_nodes = sorted(the_nodes, key=lambda x: x.probability)
        # for node in nodes:
        #      print(node.symbol, node.prob)

        # picking two smallest nodes
        right = the_nodes[0]
        left = the_nodes[1]

        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create new node
        newNode = Nodes(
            left.probability + right.probability,
            left.symbol + right.symbol,
            left,
            right,
        )

        the_nodes.remove(left)
        the_nodes.remove(right)
        the_nodes.append(newNode)

    huffmanEncoding = CalculateCodes(the_nodes[0])
    print("symbols with codes", huffmanEncoding)
    TotalGain(the_data, huffmanEncoding)
    encoded_output = OutputEncoded(the_data, huffmanEncoding)
    return encoded_output, the_nodes[0]
