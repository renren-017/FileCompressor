def rle_encode(data):
    encoded_data = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + count < len(data) and data[i] == data[i + count]:
            count += 1

        if count > 255:
            encoded_data.append(255)
            encoded_data.append(data[i])
            encoded_data.append(count - 255)
        else:
            encoded_data.append(count)
            encoded_data.append(data[i])

        i += count

    return bytes(encoded_data)
