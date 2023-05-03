# import numpy as np

def rle_encode(image):
    # Flatten the image into a 1D array
    flat_image = image.ravel()

    # Initialize the compressed data list with the first pixel
    compressed_data = [(flat_image[0], 1)]

    # Loop through the remaining pixels and compress them
    for i in range(1, len(flat_image)):
        if flat_image[i] == compressed_data[-1][0]:
            # If the current pixel is the same as the previous pixel, increment the count
            compressed_data[-1] = (compressed_data[-1][0], compressed_data[-1][1] + 1)
        else:
            # If the current pixel is different from the previous pixel, add it to the compressed data list
            compressed_data.append((flat_image[i], 1))

    # Convert the compressed data list to a bytearray
    compressed_bytes = bytearray()
    for pixel, count in compressed_data:
        # Encode each pixel and count as two bytes in little-endian order
        compressed_bytes += bytearray([pixel & 0xff, pixel >> 8, count & 0xff, count >> 8])

    return compressed_bytes
