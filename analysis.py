import sys
from os import path
from music import *

if len(sys.argv) < 2:
    print('Usage: python analysis.py file')
    sys.exit(0)

orig = path.abspath(sys.argv[1])
folder, filename = path.split(orig)
filename = path.splitext(filename)[0]

# 逐行读谱
print('============ 1. 读谱 ============')
song = []
with open(orig) as file:
    lines = file.readlines()

sec_count, sec_len = 0, 0
for i in range(len(lines)):
    try:
        line = lines[i].rstrip('\n')

        # 空行
        if not line:
            continue

        # 注释行作为小节分界
        elif line[0] == '#':
            if sec_len > 0:
                sec_count += 1
                print('第%d小节长度为%.1f拍' % (sec_count, sec_len))
                sec_len = 0
            continue

        # 音符行
        else:
            args = line.split(',')
            name = args[0]
            octave = int(args[1])
            offset = 1 if args[2] == '#' else -1 if args[2] == 'b' else 0
            duration = float(args[3])
            song.append(note(name, octave, duration, offset))
            sec_len += duration
    except Exception as e:
        print('在读取第%d节，第%d行 %r 时出错：%s' % (sec_count + 1, i, line, e))
        sys.exit(1)

print('共读取%d小节，%d个音符' % (sec_count, len(song)))

# 转换不同律制
print('============ 2. 律制转换 ============')
temp_list = ['equal', 'pyth', 'pure']
while 1:
    try:
        bpm = int(input('BPM: ', ))
        if bpm <= 0:
            raise
    except:
        pass
    else:
        break

print('进行律制转换')
temps = {}
for type in temp_list:
    temps[type] = [temperament.convert(type, n, 60 / bpm) for n in song]

print('输出律制时值信息至: %s.csv' % filename)
with open(path.join(folder, filename + '_freq.csv'), 'w') as file:
    file.write(','.join(temps.keys()) + ',length\n')
    for cmp, dur in zip(zip(*temps.values()), song):
        file.write('%s,%s\n' % (','.join(str(x[0]) for x in cmp),
                                dur.duration))

# 输出波形文件
print('============ 3. 输出波形文件 ============')
for type in temp_list:
    output = path.join(folder, '%s(%s, %d bpm).wav' % (filename, type, bpm))
    print('输出 ' + output)
    writer = wav_writer(output)
    for freq, dur in temps[type]:
        writer.play(freq, dur, [100, 5, 0, 2, 0, 1], 2)
    writer.done()
