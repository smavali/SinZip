import re
import struct


def decoder(name, out, window_size, pow_size):
    file = open(name, "rb")
    input = file.read()

    chararray = ""
    i = 6

    while i < len(input):

        (offset_and_length, char) = struct.unpack(">HB", input[i:i + 3])
        char = chr(char)

        offset = offset_and_length >> pow_size

        length = offset_and_length - (offset << pow_size)


        i = i + 3

        if (offset == 0) and (length == 0):
            chararray += char

        else:
            iterator = len(chararray) - window_size
            if iterator < 0:
                iterator = offset
            else:
                iterator += offset
            for pointer in range(length):
                chararray += (chararray[iterator + pointer])
            chararray += char

    out.write((chararray.encode("utf-8")))

def getData(name):
    file = open(name, "rb")
    input = file.read()
    (win_pow, buf_pow, password) = struct.unpack('>BBI', input[0:6])
    comp_data = (win_pow, buf_pow, password)
    return comp_data



def main(file_name):
    comp_data = getData(file_name)
    win_pow = int(comp_data[0])
    buf_pow = int(comp_data[1])
    MAX_SEARCH = 2 ** win_pow

    name = file_name
    name_without_suffix = re.search(".*(?=\.)", file_name).group(0)
    name_without_suffix = name_without_suffix[:len(name_without_suffix) - 4]
    print(name_without_suffix)

    print(name)
    processed = open(name_without_suffix + "_D" + ".txt", "wb")
    decoder(name, processed, MAX_SEARCH, buf_pow)
    processed.close()


if __name__ == "__main__":
    main()
