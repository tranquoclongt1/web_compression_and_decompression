from api.Huffman.SelfDefineStructs import *

# A canonical Huffman code, which only describes the code length
# of each symbol. Code length 0 means no code for the symbol.
# The binary codes for each symbol can be reconstructed from the length information.
# In this implementation, lexicographically lower binary codes are assigned to symbols
# with lower code lengths, breaking ties by lower symbol values. For example:
#   Code lengths (canonical code):
#     Symbol A: 1
#     Symbol B: 3
#     Symbol C: 0 (no code)
#     Symbol D: 2
#     Symbol E: 3
#   Sorted lengths and symbols:
#     Symbol A: 1
#     Symbol D: 2
#     Symbol B: 3
#     Symbol E: 3
#     Symbol C: 0 (no code)
#   Generated Huffman codes:
#     Symbol A: 0
#     Symbol D: 10
#     Symbol B: 110
#     Symbol E: 111
#     Symbol C: None
#   Huffman codes sorted by symbol:
#     Symbol A: 0
#     Symbol B: 110
#     Symbol C: None
#     Symbol D: 10
#     Symbol E: 111
class CanonicalCode(object):
    # Constructs a canonical code in one of two ways:
    # - CanonicalCode(codelengths):
    #   Builds a canonical Huffman code from the given array of symbol code lengths.
    #   Each code length must be non-negative. Code length 0 means no code for the symbol.
    #   The collection of code lengths must represent a proper full Huffman code tree.
    #   Examples of code lengths that result in under-full Huffman code trees:
    #   * [1]
    #   * [3, 0, 3]
    #   * [1, 2, 3]
    #   Examples of code lengths that result in correct full Huffman code trees:
    #   * [1, 1]
    #   * [2, 2, 1, 0, 0, 0]
    #   * [3, 3, 3, 3, 3, 3, 3, 3]
    #   Examples of code lengths that result in over-full Huffman code trees:
    #   * [1, 1, 1]
    #   * [1, 1, 2, 2, 3, 3, 3, 3]
    # - CanonicalCode(tree, symbollimit):
    #   Builds a canonical code from the given code tree.
    def __init__(self, codelengths=None, tree=None, symbollimit=None):
        if codelengths is not None and tree is None and symbollimit is None:
            # Check basic validity
            if len(codelengths) < 2:
                raise ValueError("At least 2 symbols needed")
            for code_lenght in codelengths:
                if code_lenght < 0:
                    raise ValueError("Illegal code length")

            # Copy once and check for tree validity
            codelens = sorted(codelengths, reverse=True)
            currentlevel = codelens[0]
            numnodesatlevel = 0
            for cl in codelens:
                if cl == 0:
                    break
                while cl < currentlevel:
                    if numnodesatlevel % 2 != 0:
                        raise ValueError("Under-full Huffman code tree")
                    numnodesatlevel //= 2
                    currentlevel -= 1
                numnodesatlevel += 1
            while cl < currentlevel:
                if numnodesatlevel % 2 != 0:
                    raise ValueError("Under-full Huffman code tree")
                numnodesatlevel //= 2
                currentlevel -= 1
            if numnodesatlevel < 1:
                raise ValueError("Under-full Huffman code tree")
            if numnodesatlevel > 1:
                raise ValueError("Over-full Huffman code tree")

            # Copy again
            self.codelengths = list(codelengths)

        elif tree is not None and symbollimit is not None and codelengths is None:
            # Recursive helper method
            def build_code_lengths(node, depth):
                if isinstance(node, InternalNode):
                    build_code_lengths(node.leftchild, depth + 1)
                    build_code_lengths(node.rightchild, depth + 1)
                elif isinstance(node, Leaf):
                    # Note: CodeTree already has a checked constraint that disallows a symbol in multiple leaves
                    if self.codelengths[node.symbol] != 0:
                        raise AssertionError("Symbol has more than one code")
                    if node.symbol >= len(self.codelengths):
                        raise ValueError("Symbol exceeds symbol limit")
                    self.codelengths[node.symbol] = depth
                else:
                    raise AssertionError("Illegal node type")

            if symbollimit < 2:
                raise ValueError("At least 2 symbols needed")
            self.codelengths = [0] * symbollimit
            build_code_lengths(tree.root, 0)

        else:
            raise ValueError("Invalid arguments")

    # Returns the symbol limit for this canonical Huffman code.
    # Thus this code covers symbol values from 0 to symbolLimit-1.
    def get_symbol_limit(self):
        return len(self.codelengths)

    # Returns the code length of the given symbol value. The result is 0
    # if the symbol has node code; otherwise the result is a positive number.
    def get_code_length(self, symbol):
        if 0 <= symbol < len(self.codelengths):
            return self.codelengths[symbol]
        else:
            raise ValueError("Symbol out of range")

    # Returns the canonical code tree for this canonical Huffman code.
    def to_code_tree(self):
        nodes = []
        for i in range(max(self.codelengths), -1, -1):  # Descend through code lengths
            assert len(nodes) % 2 == 0
            newnodes = []

            # Add leaves for symbols with positive code length i
            if i > 0:
                for (j, codelen) in enumerate(self.codelengths):
                    if codelen == i:
                        newnodes.append(Leaf(j))

            # Merge pairs of nodes from the previous deeper layer
            for j in range(0, len(nodes), 2):
                newnodes.append(InternalNode(nodes[j], nodes[j + 1]))
            nodes = newnodes

        assert len(nodes) == 1
        return CodeTree(nodes[0], len(self.codelengths))

