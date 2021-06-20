#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_huffman_compression.py

Utilities for Huffman compression of text (8 bit / symbol)
"""

from huffman_compression_utils import HuffmanEncode, HuffmanDecode

# Huffman encoding
file_source = "sample_text_source.txt";
file_encoded = "sample_text_encoded";
HuffmanEncode(file_source, file_encoded);

# Huffman decoding
file_encoded = "sample_text_encoded";
file_decoded = "sample_text_decoded.txt";
HuffmanDecode(file_encoded, file_decoded);

# Load the original version
file_source = "sample_text_source.txt";
file_source = open(file_source,"r");
text1 = file_source.read();
file_source.close();

# Load the decoded version
file_decoded = "sample_text_decoded.txt";
file_decoded = open(file_decoded,"r");
text2 = file_decoded.read();
file_decoded.close();

# Compare the original and decoded versions
if text1 == text2:
    print('SUCCESS. The original and decoded versions are identical!');
else:
    print('FAILURE. The original and decoded versions are NOT identical!');
        