

s = "0300222200" \
    "0300000000" \
    "0310000000" \
    "0010005000" \
    "0010005000" \
    "0010044400" \
    "0010000000" \
    "0000000000" \
    "0000000000" \
    "0000000000"

row = 1
col = 5

position = col + (row-1) * 10
print(position)
# print(s[position-1])

hit_character = s[position-1]
print(f"{hit_character=}")
print(s)
s = f"{s[0:position-1]}X{s[position:]}"
print(s)