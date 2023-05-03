import pickle

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
import io
import os
import heapq

app = FastAPI()


class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def compress_huffman(upload_file: UploadFile) -> StreamingResponse:
    if not upload_file.filename.endswith('.txt'):
        return 'File is not a text file'

        # Read the file content
    file_content = upload_file.file.read()

    # Get the frequency of each character in the file
    char_frequency = {}
    for char in file_content:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1

    # Build the Huffman tree
    heap = [[freq, [char, '']] for char, freq in char_frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Convert the Huffman tree to a dictionary
    huffman_tree = dict(heapq.heappop(heap)[1:])

    # Compress the file content using the Huffman tree
    compressed_content = ''.join(huffman_tree[char] for char in file_content)

    # Write the compressed content to a buffer
    compressed_buffer = io.BytesIO()
    pickle.dump(huffman_tree, compressed_buffer)
    compressed_buffer.write(int(compressed_content, 2).to_bytes((len(compressed_content) + 7) // 8, byteorder='big'))

    # Seek to the beginning of the buffer
    compressed_buffer.seek(0)

    return compressed_buffer

