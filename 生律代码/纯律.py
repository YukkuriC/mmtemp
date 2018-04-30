''''''

# BFS所用记录字典
# (base, offset) => (dividend, divisor)
search_map = {(0, 0): (1, 1)}

# 半音升降偏移
search_offset = {
    2: [0, 1, 1, 0, 0, 1, 1],
    3: [0, 0, 0, -1, 0, 0, 0],
    4: [0, 0, 0, 0, 0, 0, 1]
}


# 约分结果
def simplify(freq):
    for i in (2, 3, 5):
        while freq[0] % i == 0 and freq[1] % i == 0:
            freq[0] //= i
            freq[1] //= i


# 向字典中添加结果
def add_result(pos, offset, freq):
    if not (pos, offset) in search_map:
        search_map[pos, offset] = freq


# 搜索2个升降号以内的所有音程
for offset in [0, 1, -1, 2, -2]:
    for pos_cur in range(7):
        if (pos_cur, offset) in search_map:
            num, base = search_map[pos_cur, offset]

            for step in [2, 3, 4]:
                # 向上
                pos_up = pos_cur + step
                freq_up = [num * (7 - step), base * (6 - step)]
                if pos_up >= 7:
                    pos_up -= 7
                    freq_up[1] *= 2
                simplify(freq_up)
                add_result(pos_up, offset + search_offset[step][pos_cur],
                           freq_up)

                # 向下
                pos_down = pos_cur - step
                freq_down = [num * (6 - step), base * (7 - step)]
                if pos_down < 0:
                    pos_down += 7
                    freq_down[0] *= 2
                simplify(freq_down)
                add_result(pos_down, offset - search_offset[step][pos_down],
                           freq_down)

# 整理输出结果
result_raw = sorted(
    (i for i in search_map.items() if abs(i[0][1]) < 3),
    key=lambda x: [0, 1, -1, 2, -2].index(x[0][1]) + x[0][0] * 1000)
result_output = {}
name_map = 'CDEFGAB'
for k, v in result_raw:
    result_output[name_map[k[0]], k[1]] = '%d/%d' % tuple(v)

print('{')
for k, v in result_output.items():
    print('    %r:%s,' % (k, v))
print('}')
