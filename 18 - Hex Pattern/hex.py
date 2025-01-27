# since mentioned in the document name, might as well explain binary and hex literals in code
# both use notation before the number:
# 0b0010 – 2 written in binary, with 0b preceding the number
# 0x00a1 – 161 written in hexadecimal, with 0x preceding the number

# hexadecimal refers to base-16 number system uses 16 digits 0-f, that is 0123456789abcdef
# it is useful because combination of two digits gives 256 possible values, equal to the size of a byte
# therefore it is very convenient for representing colours, usually 32-bit
# 00 00 00 (00) is 32 bits split into four components, R G B and A, for Red, Green, Blue and Alpha (transparency)
# ... where #000000 is black and #FFFFFF is white

# therefore, hex color #AA1022 is red-ish 

# 20 x 12
w = 0x14
h = 0b1100

for i in range(h):
    print((' ' if (i & 1) == 1 else '') + '* ' * (w - (i & 1)))

# i & 3 == 2 is equivalent to i % 4 == 2, it exists for all mod a power of 2