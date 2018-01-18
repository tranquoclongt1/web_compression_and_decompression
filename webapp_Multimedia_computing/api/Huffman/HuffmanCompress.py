# TEXT COMPESSION
# Compression application using static Huffman coding
#

import sys, os
import api.Huffman.HuffmanCore as HuffmanCore
import api.Huffman.FrequencyComputing as FrequencyComputing
import api.Huffman.CanoncialHuffmanCode as CanoncialHuffmanCode
import api.Huffman.IOStreamSolution as IOStreamSolution
python3 = sys.version_info.major >= 3


# Command line main application function.
def huffman_compress_main_process(_input_file_path, _output_file_path):
    # Handle command line arguments
    # if len(args) != 2:
    #     sys.exit("Usage: python huffman-compress.py InputFilePath OutputFilePath")
    inputfile = _input_file_path
    outputfile = _output_file_path

    # Read input file once to compute symbol frequencies.
    # The resulting generated code is optimal for static Huffman coding and also canonical.
    freqs = get_frequencies(inputfile)
    freqs.increment(256)  # EOF symbol gets a frequency of 1
    code = freqs.build_code_tree()
    canoncode = CanoncialHuffmanCode.CanonicalCode(tree=code, symbollimit=257)
    # Replace code tree with canonical one. For each symbol,
    # the code value may change but the code length stays the same.
    code = canoncode.to_code_tree()

    # Read input file again, compress with Huffman coding, and write output file
    inp = open(inputfile, "rb")
    bitout = IOStreamSolution.BitOutputStream(open(outputfile, "wb"))
    try:
        write_code_len_table(bitout, canoncode)
        compress(code, inp, bitout)
    finally:
        bitout.close()
        inp.close()

    # Compute compression ratio:
    compression_ratio = os.path.getsize(inputfile)/os.path.getsize(outputfile)
    print('Compression Ratio = ', compression_ratio)


# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(filepath):
    freqs = FrequencyComputing.FrequencyTable([0] * 257)
    i = 1
    with open(filepath, "rb") as input:
        while True:
            print(str(i), end='', flush=True)
            b = input.read(1)
            print(str(b), ' -- len: ', len(b))
            if len(b) == 0:
                break
            b = b[0] if python3 else ord(b)
            freqs.increment(b)
            i += 1
    return freqs


def write_code_len_table(bitout, canoncode):
    for i in range(canoncode.get_symbol_limit()):
        val = canoncode.get_code_length(i)
        # For this file format, we only support codes up to 255 bits long
        if val >= 256:
            raise ValueError("The code for a symbol is too long")

        # Write value as 8 bits in big endian
        for j in reversed(range(8)):
            bitout.write((val >> j) & 1)


def compress(code, inp, bitout):
    enc = HuffmanCore.HuffmanEncoder(bitout)
    enc.codetree = code
    while True:
        b = inp.read(1)
        if len(b) == 0:
            break
        enc.write(b[0] if python3 else ord(b))
    enc.write(256)  # EOF

#
# # Main launcher
# if __name__ == "__main__":
#     main(sys.argv[1:])


# Ref: www.nayuki.io