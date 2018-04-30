import wave
import numpy as np
from math import sin, pi

__all__ = ['note', 'temperament', 'wav_writer']


class note:
    '''音符对象

    参数 : 
    name : 音名
    octave : 音组
    duration : 持续时长
    offset : 升降半音数
    '''

    def __init__(self, name, octave, duration, offset):
        self.name = name
        self.octave = octave
        self.duration = duration
        self.offset = offset

    def __str__(self):
        name = self.name
        if name != 'R':
            name += ('bb', 'b', '', '#', '##')[self.offset + 2] + str(
                self.octave)

        return '%s:%s' % (name, self.duration)

    def __repr__(self):
        return 'note(%r, %r, %r, %r)' % (self.name, self.octave, self.duration,
                                         self.offset)


class temperament:
    '''律制模块
    包含十二平均律、五度相生律与纯律
    '''

    # 十二平均律 twelvetone equal temperament
    _equal_offset = {
        'C': -9,
        'D': -7,
        'E': -5,
        'F': -4,
        'G': -2,
        'A': 0,  # A4 => 440Hz
        'B': 2
    }

    # 五度相生律 Pythagorean Intonation
    _pyth_map = {
        ('C', 0): 1,
        ('D', 0): 1.125,
        ('E', 0): 1.265625,
        ('F', 0): 1.3333333333333333,
        ('G', 0): 1.5,
        ('A', 0): 1.6875,
        ('B', 0): 1.8984375,
        ('C', 1): 1.06787109375,
        ('D', 1): 1.20135498046875,
        ('E', 1): 1.3515243530273438,
        ('F', 1): 1.423828125,
        ('G', 1): 1.601806640625,
        ('A', 1): 1.802032470703125,
        ('B', 1): 2.0272865295410156,
        ('C', -1): 0.9364426154549609,
        ('D', -1): 1.0534979423868311,
        ('E', -1): 1.1851851851851851,
        ('F', -1): 1.2485901539399478,
        ('G', -1): 1.4046639231824414,
        ('A', -1): 1.5802469135802468,
        ('B', -1): 1.7777777777777777,
        ('C', 2): 1.1403486728668213,
        ('D', 2): 1.282892256975174,
        ('E', 2): 1.4432537890970707,
        ('F', 2): 1.5204648971557617,
        ('G', 2): 1.710523009300232,
        ('A', 2): 1.924338385462761,
        ('B', 2): 2.164880683645606,
        ('C', -2): 0.8769247720401276,
        ('D', -2): 0.9865403685451437,
        ('E', -2): 1.1098579146132868,
        ('F', -2): 1.1692330293868367,
        ('G', -2): 1.3153871580601915,
        ('A', -2): 1.4798105528177157,
        ('B', -2): 1.6647868719199304
    }

    # 纯律 Pure law
    _pure_map = {
        ('C', 0): 1 / 1,
        ('C', 1): 25 / 24,
        ('C', -1): 24 / 25,
        ('C', 2): 1125 / 1024,
        ('C', -2): 1024 / 1125,
        ('D', 0): 9 / 8,
        ('D', 1): 75 / 64,
        ('D', -1): 16 / 15,
        ('D', 2): 625 / 512,
        ('D', -2): 2048 / 2025,
        ('E', 0): 5 / 4,
        ('E', 1): 125 / 96,
        ('E', -1): 6 / 5,
        ('E', 2): 5625 / 4096,
        ('E', -2): 256 / 225,
        ('F', 0): 4 / 3,
        ('F', 1): 45 / 32,
        ('F', -1): 32 / 25,
        ('F', 2): 375 / 256,
        ('F', -2): 4096 / 3375,
        ('G', 0): 3 / 2,
        ('G', 1): 25 / 16,
        ('G', -1): 64 / 45,
        ('G', 2): 625 / 384,
        ('G', -2): 512 / 375,
        ('A', 0): 5 / 3,
        ('A', 1): 225 / 128,
        ('A', -1): 8 / 5,
        ('A', 2): 1875 / 1024,
        ('A', -2): 1024 / 675,
        ('B', 0): 15 / 8,
        ('B', 1): 125 / 64,
        ('B', -1): 16 / 9,
        ('B', 2): 16875 / 8192,
        ('B', -2): 128 / 75
    }

    @staticmethod
    def convert(type, note, length, base=440):
        '''将音符转换为三种律制下的(频率,时长)元组

        参数 :   
        type : 律制类型的符号，此处分别记为"equal", "pyth", "pure"  
        note : 音符对象  
        length : 单位音符duration对应的秒数  
        base : A4对应的频率，单位为Hz，默认为440  
        '''
        if not type in ("equal", "pyth", "pure"):
            raise ValueError('请从("equal", "pyth", "pure")中选择一种类型')
        dur = note.duration * length
        if note.name in 'ABCDEFG':
            if type == 'equal':
                freq = base * 2**(
                    note.octave - 4 +
                    (temperament._equal_offset[note.name] + note.offset) / 12)
            else:
                map = temperament._pyth_map if type == 'pyth' else temperament._pure_map
                freq = base / map['A', 0] * map[note.name, note.offset] *\
                 2**(note.octave - 4)
        else:
            freq = 0

        return (freq, dur)


class wav_writer:
    '''音频合成模块

    参数 :  
    name : 输出文件名  
    framerate : 采样率  
    volumn : 音量，范围为(0,32767)  
    '''
    _bw_dict = {1: np.int8, 2: np.int16, 4: np.int32, 8: np.int64}

    def __init__(self,
                 name='output.wav',
                 framerate=48000,
                 bytewidth=4,
                 volumn=50):
        '''初始化'''
        assert isinstance(framerate, int) and framerate > 0
        assert bytewidth in wav_writer._bw_dict
        assert 0 < volumn <= 100

        self.name = name
        self.rate = framerate
        self.bytewidth = bytewidth
        self.volumn = volumn * (256**bytewidth) / 200
        self.buffer = []

    def play(self, freq, duration, overtone=[10000], fade=None):
        '''向缓冲区中添加音符

        参数 :   
        freq : 频率，单位为Hz  
        duration : 持续时长，单位为秒  
        overtone : 泛音列强度，输入为列表  
            其中第i个元素(overtone[i-1])对应频率为i倍基频的泛音强度(i=1为基频)
            
        fade : 衰减系数，输入数字时强度将按fade次方衰减，否则为恒定强度  
        '''
        process = np.linspace(0, 1, int(duration * self.rate), False)
        phase = process * freq * duration

        # 泛音列强度标准化
        volumn_sum = 0
        for i in range(len(overtone)):
            overtone[i] = abs(overtone[i])
            volumn_sum += overtone[i]
        for i in range(len(overtone)):
            overtone[i] *= self.volumn / volumn_sum

        # 合成泛音波形
        base_wave = np.sin(phase * 2 * pi) * overtone[0]
        for i in range(1, len(overtone)):
            if overtone[i] != 0:
                base_wave += np.sin((i + 1) * phase * 2 * pi) * overtone[i]

        # 处理衰减
        if fade:
            base_wave *= (1 - process**fade)

        # sample = base_wave.astype(wav_writer._bw_dict[self.bytewidth])
        # self.buffer.append(sample.tostring())
        self.buffer.append(base_wave)

    def done(self):
        '''写入文件并清空缓冲区'''

        file = wave.open(self.name, 'wb')
        file.setnchannels(1)
        file.setsampwidth(self.bytewidth)
        file.setframerate(self.rate)

        stream = np.concatenate(self.buffer)
        file.writeframesraw(stream.astype(wav_writer._bw_dict[self.bytewidth]))
        file.close()
        self.buffer = np.array([])


if __name__ == '__main__':

    def parse(seq):
        octave, duration, res = 4, 4, []
        for s in seq:
            try:
                tmp = s.split(':')
                assert len(tmp) in (1, 2)

                # parse duration
                if len(tmp) == 2:
                    duration = int(tmp[1])
                tmp = tmp[0]

                # parse octave
                if tmp[-1].isdigit():
                    octave = int(tmp[-1])
                    tmp = tmp[:-1]

                # parse frequency
                assert len(tmp) <= 2
                if tmp == 'R':  # rest
                    res.append(note('R', None, duration, None))
                elif 'A' <= tmp[0] <= 'G':  # note
                    offset = 0
                    if len(tmp) == 2:
                        if tmp[1] == '#':
                            offset = 1
                        elif tmp[1] == 'b':
                            offset = -1
                        else:
                            raise
                    res.append(note(tmp[0], octave, duration, offset))
                else:  # illegal
                    raise

            except:
                raise ValueError('%r is not a valid note' % s)
        return res

    seq = [
        'F#5:2', 'G#', 'C#:1', 'D#:2', 'B4:1', 'D5:1', 'C#', 'B4:2', 'B',
        'C#5', 'D', 'D:1', 'C#', 'B4:1', 'C#5:1', 'D#', 'F#', 'G#', 'D#', 'F#',
        'C#', 'D', 'B4', 'C#5', 'B4', 'D#5:2', 'F#', 'G#:1', 'D#', 'F#', 'C#',
        'D#', 'B4', 'D5', 'D#', 'D', 'C#', 'B4', 'C#5', 'D:2', 'B4:1', 'C#5',
        'D#', 'F#', 'C#', 'D', 'C#', 'B4', 'C#5:2', 'B4', 'C#5', 'B4', 'F#:1',
        'G#', 'B:2', 'F#:1', 'G#', 'B', 'C#5', 'D#', 'B4', 'E5', 'D#', 'E',
        'F#', 'B4:2', 'B', 'F#:1', 'G#', 'B', 'F#', 'E5', 'D#', 'C#', 'B4',
        'F#', 'D#', 'E', 'F#', 'B:2', 'F#:1', 'G#', 'B:2', 'F#:1', 'G#', 'B',
        'B', 'C#5', 'D#', 'B4', 'F#', 'G#', 'F#', 'B:2', 'B:1', 'A#', 'B',
        'F#', 'G#', 'B', 'E5', 'D#', 'E', 'F#', 'B4:2', 'C#5'
    ]
    notes = parse(seq)

    for type in 'equal', 'pyth', 'pure':
        wav = wav_writer('nyan_%s.wav' % type)
        for n in notes:
            wav.play(*temperament.convert(type, n, 0.12), [100, 5, 0, 2, 0, 1],
                     2)
        wav.done()