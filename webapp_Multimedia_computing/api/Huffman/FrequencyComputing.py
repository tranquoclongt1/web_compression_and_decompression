import heapq

from api.Huffman.SelfDefineStructs import Leaf, InternalNode, CodeTree


class FrequencyTable(object):
    # Constructs a frequency table from the given sequence of frequencies.
    # The sequence length must be at least 2, and each value must be non-negative.
    def __init__(self, _frequencies):
        self.frequencies = list(_frequencies)  # copy
        if len(self.frequencies) < 2:
            raise ValueError('At least 2 symbols needed')
        for value in self.frequencies:
            if value < 0:
                raise ValueError('Negative frequency - frequency has to be non-negative')

    # Return the number of symbols in this frequency table
    def get_symbol_limit(self):
        return len(self.frequencies)

    # Check if symbol is in table;
    def _check_symbol(self, symbol):
        if 0 <= symbol <= len(self.frequencies):
            return
        else:
            raise ValueError('Symbol is out of range')

    # Return frequency of given symbol in this table
    def get_frequency(self, symbol):
        self._check_symbol(symbol)
        return self.frequencies[symbol]

    # Set the frequency of given symbol in this table to the given frequency
    def set_frequency(self, symbol, _frequency):
        self._check_symbol(symbol)
        if _frequency < 0:
            raise ValueError('Nagative frequency')
        self.frequencies[symbol] = _frequency

    # Increment the frequency of the gien symbol in this frequency table
    def increment(self, symbol):
        self._check_symbol(symbol)
        self.frequencies[symbol] += 1

    #   BUILDING CODE TREE
    # Returns a code tree that is optimal for the symbol frequencies in this table.
    # The tree always contains at least 2 leaves (even if they come from symbols with
    # 0 frequency), to avoid degenerate trees. Note that optimal trees are not unique.

    def build_code_tree(self):
        pqueue = []

        # Add leaves for symbols with none-zero frequency
        # The enumerate() function adds a counter to an iterable.
        # So for each element in cursor, a tuple is produced
        # with (counter, element); the for loop binds that to row_number and row,
        # respectively.
        for (i, freq) in enumerate(self.frequencies):
            if freq > 0:
                heapq.heappush(pqueue, (freq, i, Leaf(i)))

        # Pad with zero-frequency symbols until queue has at least 2 iteams
        for (i, freq) in enumerate(self.frequencies):
            if len(pqueue) >= 2:
                break
            if freq == 0:
                heapq.heappush((pqueue, (freq, i, Leaf(i))))

        assert len(pqueue) >= 2

        # Repeatedly tie together two nodes with the lowest frequency
        while len(pqueue) > 1:
            x = heapq.heappop(pqueue) # Tuple of (frequency, lowest symbol, node object)
            y = heapq.heappop(pqueue) # Tuple of (frequency, lowest symbol, node object)
            z = (x[0] + y[0], min(x[1], y[1]), InternalNode(_leftChild=x[2], _rightChild=y[2]))
            heapq.heappush(pqueue, z)

        # Return the remaining node
        return CodeTree(pqueue[0][2], len(self.frequencies))