#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
huffman_compression_utils.py

Utilities for Huffman compression of images (8 bit / symbol)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.image as mpimg 
import math

encoding_dict = dict();
decoding_dict = dict();
N1_dim = 0;
N2_dim = 0;

class node:
    # node object for Huffman binary tree
    def __init__(self, symbol = '', prob = 0, codeword = '', left_child = None, right_child = None):
        self.symbol = symbol;
        self.prob = prob;
        self.codeword = codeword;
        self.left_child = left_child;
        self.right_child = right_child;
    
    def __add__(self, x):
        symbol = self.symbol + x.symbol;
        prob = self.prob + x.prob;
        codeword = '';
        left_child = self;
        right_child = x;    
            
        return node(symbol, prob, codeword, left_child, right_child);
    
def _BuildHuffmanTree(s, p):
    # Builds the Huffman binary tree
    # s - symbol
    # p - probability
    # Going from the bottom of the binary tree (child node) to the top (parent node)
    
    nodes = [node(s[i], p[i]) for i in range(len(s))];
    while len(nodes) != 1:
        nodes.sort(key = lambda x : x.prob);
        parent_node = nodes[0] + nodes[1];
        
        nodes.remove(nodes[0]);
        nodes[0] = parent_node;
        
    parent_node = nodes[0];
    parent_node.codeword = '';
    
    return parent_node;
    
def _CreateHuffmanLookupTable(node):
    # Creates the lookup tables for encoding and decoding
    # node - top parent node
    # Going from the top of the binary tree (parent node) to the bottom (child node)
    
    global encoding_dict, decoding_dict;
    left_child_codeword = '0';
    right_child_codeword = '1';
    
    if node.left_child != None:
        node.left_child.codeword = node.codeword + left_child_codeword;
        _CreateHuffmanLookupTable(node.left_child);
    else:
        encoding_dict[node.symbol] = node.codeword;
        decoding_dict[node.codeword] = node.symbol;
        
    if node.right_child != None:
        node.right_child.codeword = node.codeword + right_child_codeword;
        _CreateHuffmanLookupTable(node.right_child);
    else:
        encoding_dict[node.symbol] = node.codeword;
        decoding_dict[node.codeword] = node.symbol;
        
    return None;

def _CalculateEntropy(s, p, endocoding_dict):
    # Calculates the enthropy and the average codeword length of the source [bits per symbol]
    # s - symbol
    # p - probability
        
    entropy = 0;
    codeword_avg_length = 0;
    for i in range(len(s)):
        codeword = endocoding_dict[s[i]];
        codeword_length = len(codeword);
        codeword_avg_length += codeword_length * p[i];
        entropy += -p[i] * math.log2(p[i]);
        
    return entropy, codeword_avg_length;

def _PrintHuffmanLookupTable(s, p, encoding_dict):
    # Prints the Huffman lookup table
    # s - symbol
    # p - probability    
    
    nodes = [node(s[i], p[i]) for i in range(len(s))];
    nodes.sort(key = lambda x : x.prob, reverse = True);

    n = 10;
    print('-' * n + 'Huffman table' + '-' * n);
    print('Symbol Probability Codeword')
    for i in range(len(s)):
        symbol = nodes[i].symbol;
        prob = nodes[i].prob;
        codeword = encoding_dict[symbol];
        print(repr(symbol).ljust(10), repr(round(prob, 4)).ljust(10), repr(codeword).ljust(10));   
        
    entropy, codeword_avg_length = _CalculateEntropy(s, p, encoding_dict);
    print('\nEntropy of the source: {0: 0.5f} [bits per symbol]'.format(round(entropy, 5)));
    print('Codeword average length: {0: 0.5f} [bits per symbol]'.format(round(codeword_avg_length, 5)));
    print('Efficiency [%] : {0: 0.5f}\n'.format(round(entropy / codeword_avg_length * 100, 5)));   
    
    return None;
    
def _SymbolCounter(text):
    # text - text string
    # Counts and returns a list of symbols (s) and a list of symbols' probabilities (p)
    
    temp = dict();
    for i in range(len(text)):
        symbol = text[i];
        if symbol in temp:
            temp[symbol] += 1 / len(text);
        else:
            temp[symbol] = 1 / len(text);
            
    s = list(temp.keys());
    p = list(temp.values());
    
    return s, p;

def HuffmanEncode(file_source, file_encoded, show_lookup_table = True):
    
    global N1_dim, N2_dim;
    
    file_source = np.array(mpimg.imread(file_source));
    file_source = file_source.astype(np.float32);
    image = (file_source[:, :, 0] * (2 ** 8 - 1)).round().astype(np.uint8);     
    [N1_dim, N2_dim] = image.shape;
    file_encoded = open(file_encoded, "wb");  
    text = image.flatten().tolist();

    s, p = _SymbolCounter(text);    
    parent_node = _BuildHuffmanTree(s, p);
    _CreateHuffmanLookupTable(parent_node);
    
    if show_lookup_table == True:
        _PrintHuffmanLookupTable(s, p, encoding_dict);    
    
    # the actual Huffman encoding
    code_string = ''; # bitstream (a string of 0s and 1s)
    for i in range(len(text)):
        symbol = text[i];
        codeword = encoding_dict[symbol];
        code_string += str(codeword);

    # break bitstream into the groups of 8 bits each (an integer number 0 - 255) and write these \
    #   integer number in binary format into the output file   
    n = int(8 - 8 * (len(code_string) / 8 - math.floor(len(code_string) / 8))); # n-bits are missing from the final group of 8 bits
    decoding_dict['1' * (n + 8)] = ''; # ignore end flag
    code_string = code_string + '1' * (n + 8); # add ignore end flag
        
    for i in range(int(len(code_string) / 8)): 
        eight_bits = code_string[i * 8: i * 8 + 8];
        integer = int(eight_bits, 2);
        integer_binary = integer.to_bytes(1, byteorder = 'big', signed = False);
        file_encoded.write(integer_binary);
    
    file_encoded.close();
    
    text_bytes = len(text);
    code_string_bytes = int(len(code_string) / 8);
    print(f'Size of the original file: {text_bytes} [bytes]')
    print(f'Size of the encoded file: {code_string_bytes} [bytes]')
    print(f'Compression ratio: {text_bytes / code_string_bytes : 0.5f}\n');
    
    return None;

def HuffmanDecode(file_encoded, file_decoded):
    
    file_encoded = open(file_encoded,"rb");
    binary_string = file_encoded.read();
    file_encoded.close();
    
    code_string = ''; # bitstream (a string of 0s and 1s)
    for i in range(len(binary_string)):
        integer = binary_string[i];  
        code_string += f'{integer:08b}';
    
    # remove ignore end flag
    ignore_end_flag = '1' * 8;
    for i in range(8):
        ignore_end_flag += '1';
        if ignore_end_flag in decoding_dict:
            code_string = code_string[0:-len(ignore_end_flag)];      
            break;

    # preallocate memory for image array
    image_decoded = np.zeros((N1_dim * N2_dim, 1), dtype = np.uint8, order = 'C');
    
    # the actual Huffman decoding
    codeword = '';
    count = 0;
    for i in range(len(code_string)):
        codeword += code_string[i];
        if codeword in decoding_dict:
            symbol = decoding_dict[codeword];
            image_decoded[count] = symbol
            count += 1;
            codeword = '';
    
    image_decoded = image_decoded.reshape(N1_dim, N2_dim);
    # save array image
    plt.imsave(file_decoded, image_decoded, cmap='gray');  
    
    return None;