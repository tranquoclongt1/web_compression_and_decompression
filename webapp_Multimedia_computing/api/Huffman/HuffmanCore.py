from api.Huffman.SelfDefineStructs import *

class HuffmanEncoder(object):
    # Constructs a Huffman encoder based on the given bit output stream
    def __init__(self, _bitout):
        # The underlying bit output stream:
        self.output = _bitout
        # given value must be suitable
        # value before calling write()
        # The tree can be changed after each symbol encoded, as long as the encoder and decoder have the same tree
        # at the same point in the code stream.
        self.codetree = None  # initial

    # Encodes the given symbol and writes to the Huffman-coded output stream
    def write(self, symbol):
        if not isinstance(self.codetree, CodeTree):
            raise ValueError('Current code tree is invalid')
        bits = self.codetree.get_code(symbol)
        for bit in bits:
            self.output.write(bit)


# Reads frin a Huffman-coded bit stream and decodes symbols
class HuffmanDecoder(object):
    def __init__(self, _bitin):
        # The unbderlying bit input stream
        self.input = _bitin
        self.codetree = None

    def read(self):
        if not isinstance(self.codetree, CodeTree):
            raise ValueError('Invalid current code tree')
        currentnode = self.codetree.root
        while True:
            temp = self.input.read_no_eof()
            if temp == 0:
                nextnode = currentnode.leftchild
            elif temp == 1:
                nextnode = currentnode.rightchild
            else:
                raise AssertionError('Invalid value from read_no_eof()')
            if isinstance(nextnode, Leaf):
                return nextnode.symbol
            elif isinstance(nextnode, InternalNode):
                currentnode = nextnode
            else:
                raise AssertionError('Illegal node type')
