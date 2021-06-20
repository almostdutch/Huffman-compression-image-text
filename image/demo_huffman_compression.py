#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_huffman_compression.py

Demo: Huffman compression of images (8 bit / symbol)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
from huffman_compression_utils import HuffmanEncode, HuffmanDecode

# load sample image
image_original = np.array(mpimg.imread('sample_image_source.tif'));
image_original = image_original.astype(np.uint8);

# generate .png image
plt.imsave('sample_image_source.png', image_original, cmap='gray')

# Huffman encoding
file_source = "sample_image_source.png";
file_encoded = "sample_image_encoded";
HuffmanEncode(file_source, file_encoded);

# Huffman decoding
file_encoded = "sample_image_encoded";
file_decoded = "sample_image_decoded.png";
HuffmanDecode(file_encoded, file_decoded);

# Load the original version
image1= np.array(mpimg.imread('sample_image_source.png'));
image1 = image1.astype(np.float32);
image1 = (image1[:, :, 0] * (256 - 1)).round().astype(np.uint8);

# Load the decoded version
image2 = np.array(mpimg.imread('sample_image_decoded.png'));
image2 = image2.astype(np.float32);
image2 = (image2[:, :, 0] * (256 - 1)).round().astype(np.uint8);

# Compare the original and decoded versions
if (image1 == image2).all():
    print('SUCCESS. The original and decoded versions are identical!');
else:
    print('FAILURE. The original and decoded versions are NOT identical!');
        
# show images: original and decoded
fig_width, fig_height = 5, 5;
fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(fig_width, fig_height));

ax1.imshow(image1, cmap='gray')
ax1.set_title("image original")
ax1.set_axis_off()

ax2.imshow(image2, cmap='gray')
ax2.set_title("image decoded")
ax2.set_axis_off()
plt.tight_layout()
