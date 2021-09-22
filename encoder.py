import struct
import math

global password

def search_algorithm(search, look_ahead):
    ls = len(search)
    llh = len(look_ahead)

    if (ls == 0):
        return (0, 0, look_ahead[0])

    if (llh) == 0:
        return (-1, -1, "")

    best_length = 0
    best_offset = 0
    buf = search + look_ahead

    search_pointer = ls
    for i in range(0, ls):
        length = 0
        while buf[i + length] == buf[search_pointer + length]:
            length = length + 1
            if search_pointer + length == len(buf):
                length = length - 1
                break
            if i + length >= search_pointer:
                break
        if length > best_length:
            best_offset = i
            best_length = length

    return (best_offset, best_length, (buf[search_pointer + best_length]))

def main(a,b,c,d):
    if d != '':
        password = int(d)
    else:
        password = 0
    win_pow = int(a)
    buf_pow = int(b)
    x = win_pow + buf_pow
    MAXSEARCH = int(2**win_pow)
    MAXLH = int(math.pow(2, (x - (math.log(MAXSEARCH, 2)))))

    file_to_read = c
    inp = parse(file_to_read)
    file = open(file_to_read + ".sinzip", "wb")
    searchiterator = 0
    lhiterator = 0

    data = struct.pack(">BBI", win_pow, buf_pow, password)
    print(data)
    file.write(data)

    while lhiterator < len(inp):
        search = inp[searchiterator:lhiterator]
        look_ahead = inp[lhiterator:lhiterator + MAXLH]
        (offset, length, char) = search_algorithm(search, look_ahead)
        print (offset, length, char)

        shifted_offset = offset << buf_pow
        offset_and_length = shifted_offset + length
        ol_bytes = struct.pack(">HB", offset_and_length, char)
        print(offset_and_length,"  ", char)
        file.write(ol_bytes)

        lhiterator = lhiterator + length + 1
        searchiterator = lhiterator - MAXSEARCH

        if searchiterator < 0:
            searchiterator = 0

    file.close()


def parse(file):
    r = []
    f = open(file, "rb")
    text = f.read()
    return text


if __name__ == "__main__":
    main()
