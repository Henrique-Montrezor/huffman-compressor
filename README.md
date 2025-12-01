# Text File Compressor (Huffman Coding)

This project is a Python implementation of the Huffman Coding algorithm. Its goal is to demonstrate fundamental Computer Science concepts, including bit manipulation, data structures (priority queues/heaps), and binary data serialization.

The script is capable of compressing text files (.txt) into significantly smaller binary files (.bin) and decompressing them back to their original state without any data loss (lossless compression).

🚀 Features

Frequency Analysis: Maps the occurrence of each character in the text.

Huffman Tree: Constructs the optimal binary tree to generate bit prefixes.

Bit Padding: Manages the necessary padding to align bits into full bytes (8 bits).

Smart Header: Stores the frequency table at the beginning of the binary file to allow tree reconstruction during decompression.

📋 Prerequisites

Python 3.6 or higher.

There are no external dependencies. The project uses only Python's standard libraries:

heapq: For the priority queue.

os & sys: For file manipulation and command-line arguments.

struct: For binary data packing (header size).

json: For serializing the frequency map in the header.

🛠️ How to Use

The script works via the Command Line Interface (CLI).

1. Compress a file

python huffman_compressor.py compress <input_file.txt> <output_file.bin>


Example:

python huffman_compressor.py compress big_book.txt compressed_book.bin


Expected Output: The script will show the original size, compressed size, and the compression percentage.

2. Decompress a file

python huffman_compressor.py decompress <input_file.bin> <output_file.txt>


Example:

python huffman_compressor.py decompress compressed_book.bin recovered_book.txt


🧠 Technical Implementation Details

For those studying the code, here are the crucial points to pay attention to:

Binary File Structure (.bin)

The generated file is not just a soup of bits. It follows a strict structure to ensure it can be read later:

Header Size (4 bytes): An integer (Big Endian) that states how many bytes the JSON header occupies.

Header (JSON): The frequency map (e.g., {"a": 10, "b": 5}). Necessary to reconstruct the tree.

Content: The compressed text in bits.

Padding

Since operating systems write data in Bytes (8 bits) and Huffman compression generates variable-length sequences (e.g., 13 bits), the script adds extra "zeros" at the end to complete the byte.

The first byte of the compressed content stores an integer indicating how many "padding" bits were added to the end, so they can be discarded during decompression.

Author: Generated via Gemini
