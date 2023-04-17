import struct
import io


def compress_lzw(data):
    dictionary = {bytes([i]): i for i in range(256)}
    current_code = 256
    result = []
    prefix = b""
    for byte in data:
        current_prefix = prefix + bytes([byte])
        if current_prefix in dictionary:
            prefix = current_prefix
        else:
            result.append(dictionary[prefix])
            dictionary[current_prefix] = current_code
            current_code += 1
            prefix = bytes([byte])
    if prefix in dictionary:
        result.append(dictionary[prefix])
    compressed_data = bytearray()
    for code in result:
        compressed_data.extend(code.to_bytes(2, byteorder="little"))
    return compressed_data


def decompress_lzw(compressed_data):
    dictionary = {i: bytes([i]) for i in range(256)}
    current_code = 256
    result = []
    previous_code = None
    for i in range(0, len(compressed_data), 2):
        code = int.from_bytes(compressed_data[i : i + 2], byteorder="little")
        if code in dictionary:
            result.extend(dictionary[code])
            if previous_code is not None:
                dictionary[current_code] = (
                    dictionary[previous_code] + dictionary[code][:1]
                )
                current_code += 1
        else:
            prefix = dictionary[previous_code] + dictionary[previous_code][:1]
            result.extend(prefix)
            dictionary[code] = prefix
            current_code += 1
        previous_code = code
    return bytes(result)
