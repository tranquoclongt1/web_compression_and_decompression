
class Node(object):
    pass


# A leaf node of code_tree . Contain a symbol value
class Leaf(Node):
    def __init__(self, _symbol):
        if _symbol < 0:
            # print("symbol value need to be a non-nagative!")
            raise ValueError("symbol value need to be a non-nagative!")

        self.symbol = _symbol


class InternalNode(Node):
    def __init__(self, _leftChild, _rightChild):
        if not isinstance(_leftChild, Node) or not isinstance(_rightChild, Node):
            raise TypeError()
        self.leftchild = _leftChild
        self.rightchild = _rightChild


class CodeTree(object):
    # Constructs a code tree from the given tree of nodes and given symbol limit.
    # Each symbol in the tree must have value strictly less than the symbol limit.
    def __init__(self, root, symbollimit):
        def build_code_list(node, prefix):
            if isinstance(node, InternalNode):
                build_code_list(node.leftchild, prefix + (0,))
                build_code_list(node.rightchild, prefix + (1,))
            elif isinstance(node, Leaf):
                if node.symbol >= symbollimit:
                    raise ValueError('Symbol exceeds symbol limit')
                if self.codes[node.symbol] is not None:
                    raise ValueError('Symbol has more than one code')
                self.codes[node.symbol] = prefix
            else:
                raise AssertionError('Illegal node type')
        if symbollimit < 2:
            raise ValueError("At least 2 symbols needed!")
        self.root = root
        # with each symbol, given a code to for represent (stored), return None value fi symbol has no code
        # Ex: symbol 5 has the code 1001 => codes[5] = tuple (1,0,0,1)
        self.codes = [None] * symbollimit  # generate a Null array with dim = symbol limit number
        build_code_list(root, ())  # Fill codes with appropriate data

    # Return the Huffman code for a given symbol - q sequence of 0s and 1s
    def get_code(self,symbol):
        if symbol<0:
            raise  ValueError("Illegal symbol")
        elif self.codes[symbol] is None:
            raise ValueError('No code for given symbol')
        else:
            return self.codes[symbol]

    # return a string representing for this code tree,
    # Using for debugging
    def __str__(self):
        # Recursive helper function
        def to_str(prefix, node):
            if isinstance(node, InternalNode):
                return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
            elif isinstance(node, Leaf):
                return "Code {}: Symbol {}\n".format(prefix, node.symbol)
            else:
                raise AssertionError("Illegal node type")

        return to_str("", self.root)


