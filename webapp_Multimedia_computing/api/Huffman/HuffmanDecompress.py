import sys
import HuffmanCore
import CanoncialHuffmanCode
import IOStreamSolution

python3 = sys.version_info.major >= 3


# Command line main application function.
def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python HuffmanDecompress.py InputFilePath OutputFilePath")
    inputfile = args[0]
    outputfile = args[1]

    # Perform file decompression
    bitin = IOStreamSolution.BitInputStream(open(inputfile, "rb"))
    out = open(outputfile, "wb")
    try:
        canoncode = read_code_len_table(bitin)
        code = canoncode.to_code_tree()
        decompress(code, bitin, out)
    finally:
        out.close()
        bitin.close()


def read_code_len_table(bitin):
    codelengths = []
    for i in range(257):
        # For this file format, we read 8 bits in big endian
        val = 0
        for j in range(8):
            val = (val << 1) | bitin.read_no_eof()
        codelengths.append(val)
    return CanoncialHuffmanCode.CanonicalCode(codelengths=codelengths)


def decompress(code, bitin, out):
    dec = HuffmanCore.HuffmanDecoder(bitin)
    dec.codetree = code
    while True:
        symbol = dec.read()
        if symbol == 256:  # EOF symbol
            break
        out.write(bytes((symbol,)) if python3 else chr(symbol))


# Main launcher
if __name__ == "__main__":
    main(sys.argv[1:])