#Generate pallet colors from info grabbed from Bulbapedia

def rgb_to_hex(rgb): return '0x%02x%02x%02x' % rgb

#RED 
# a = (31, 29, 31); r1,g1,b1 = list(v*8 for v in a)
# b = (31, 20, 10); r2,g2,b2 = list(v*8 for v in b)
# c = (26, 10, 6); r3,g3,b3 = list(v*8 for v in c)
# d = (3, 2, 2); r4,g4,b4 = list(v*8 for v in d)

#GREEN (0xf8e8f8,0x80d0a0,0x58a048,0x101018)
# a = (31, 29, 31); r1,g1,b1 = list(v*8 for v in a)
# b = (20, 26, 16); r2,g2,b2 = list(v*8 for v in b)
# c = (9, 20, 11); r3,g3,b3 = list(v*8 for v in c)
# d = (3, 2, 2); r4,g4,b4 = list(v*8 for v in d)

#BLUE 
# a = (31, 29, 31); r1,g1,b1 = list(v*8 for v in a)
# b = (18, 20, 27); r2,g2,b2 = list(v*8 for v in b)
# c = (11, 15, 23); r3,g3,b3 = list(v*8 for v in c)
# d = (3, 2, 2); r4,g4,b4 = list(v*8 for v in d)

#YELLOW
# a = (31, 29, 31); r1,g1,b1 = list(v*8 for v in a)
# b = (31, 28, 14); r2,g2,b2 = list(v*8 for v in b)
# c = (26, 20, 0); r3,g3,b3 = list(v*8 for v in c)
# d = (3, 2, 2); r4,g4,b4 = list(v*8 for v in d)

#GOLD
a = (31, 31, 31); r1,g1,b1 = list(v*8 for v in a)
b = (20, 23, 10); r2,g2,b2 = list(v*8 for v in b)
c = (11, 11, 5); r3,g3,b3 = list(v*8 for v in c)
d = (3, 3, 3); r4,g4,b4 = list(v*8 for v in d)

print(f"({rgb_to_hex((b1,g1,r1))},{rgb_to_hex((b2,g2,r2))},{rgb_to_hex((b3,g3,r3))},{rgb_to_hex((b4,g4,r4))})")