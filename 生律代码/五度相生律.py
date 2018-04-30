notes = 'CDEFGAB'

pool = {('C', 0): 1}

# 3/2上升
index = 0
factor2, factor3, freq = 0, 0, 1
offset = 0
print(notes[index], offset, factor2, factor3, freq)
for i in range(19):
    index += 4
    factor2 += 1
    factor3 += 1
    freq *= 3 / 2
    if index >= 7:
        index -= 7
        factor2 += 1
        freq /= 2
    if index == 3:
        offset += 1
    pool[notes[index], offset] = freq
    print(notes[index], offset, factor2, factor3, freq)

# 2/3下降
index = 0
factor2, factor3, freq = 0, 0, 1
offset = 0
print(notes[index], offset, factor2, factor3, freq)

for i in range(15):
    index -= 4
    factor2 += 1
    factor3 += 1
    freq *= 2 / 3
    if index < 0:
        index += 7
        factor2 += 1
        freq *= 2
    if index == 6:
        offset -= 1
    pool[notes[index], offset] = freq
    print(notes[index], offset, factor2, factor3, freq)


# 结果分组排序
def cmp(a, b):
    return ([0, 1, -1, 2, -2].index(a[1]) - [0, 1, -1, 2, -2].index(b[1])
            ) * 1000 + 'CDEFGAB'.index(a[0]) - 'CDEFGAB'.index(b[0])
tmp=sorted(pool.items(),key=lambda a:[0,1,-1,2,-2].index(a[0][1])*1000+'CDEFGAB'.index(a[0][0]))
print(dict(tmp))