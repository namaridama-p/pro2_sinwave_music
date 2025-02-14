import csv
def freq_list(melody_key:list[list[str]]) -> list:
    _freq_list = []
    for i in melody_key:
        if len(i) != 1:
            _freq_list.append(_freq_return(i))
        else:
            _freq_list.append(_freq_return(i))
    return _freq_list


def _freq_return(melody_key:list[str]) -> list:
        """
        自動的に入れたいキーをstrで入れたら周波数帰ってくるやつ
        例)
        freq_return("A4") -> [440]

        C: ド
        C#: ド#、レ♭
        D: レ
        D#: レ#、ミ♭
        E: ミ
        F: ファ
        F#: ファ#、ソ♭
        G: ソ
        G#: ソ#、ラ♭
        A: ラ
        A#: ラ#、シ♭
        B: シ
        """
        Frequency_dict = {
            "A0": 27.5,
            "A#0": 29.135,
            "B0": 30.868,
            "C1": 32.703,
            "C#1": 34.648,
            "D1": 36.708,
            "D#1": 38.891,
            "E1": 41.203,
            "F1": 43.654,
            "F#1": 46.249,
            "G1": 48.999,
            "G#1": 51.913,
            "A1": 55.0,
            "A#1": 58.27,
            "B1": 61.735,
            "C2": 65.406,
            "C#2": 69.296,
            "D2": 73.416,
            "D#2": 77.782,
            "E2": 82.407,
            "F2": 87.307,
            "F#2": 92.499,
            "G2": 97.999,
            "G#2": 103.826,
            "A2": 110.0,
            "A#2": 116.541,
            "B2": 123.471,
            "C3": 130.813,
            "C#3": 138.591,
            "D3": 146.832,
            "D#3": 155.563,
            "E3": 164.814,
            "F3": 174.614,
            "F#3": 184.997,
            "G3": 195.998,
            "G#3": 207.652,
            "A3": 220.0,
            "A#3": 233.082,
            "B3": 246.942,
            "C4": 261.626,
            "C#4": 277.183,
            "D4": 293.665,
            "D#4": 311.127,
            "E4": 329.628,
            "F4": 349.228,
            "F#4": 369.994,
            "G4": 391.995,
            "G#4": 415.305,
            "A4": 440.0,
            "A#4": 466.164,
            "B4": 493.883,
            "C5": 523.251,
            "C#5": 554.365,
            "D5": 587.33,
            "D#5": 622.254,
            "E5": 659.255,
            "F5": 698.456,
            "F#5": 739.989,
            "G5": 783.991,
            "G#5": 830.609,
            "A5": 880.0,
            "A#5": 932.328,
            "B5": 987.767,
            "C6": 1046.502,
            "C#6": 1108.731,
            "D6": 1174.659,
            "D#6": 1244.508,
            "E6": 1318.51,
            "F6": 1396.913,
            "F#6": 1479.978,
            "G6": 1567.982,
            "G#6": 1661.219,
            "A6": 1760.0,
            "A#6": 1864.655,
            "B6": 1975.533,
            "C7": 2093.005,
            "C#7": 2217.461,
            "D7": 2349.318,
            "D#7": 2489.016,
            "E7": 2637.02,
            "F7": 2793.826,
            "F#7": 2959.955,
            "G7": 3135.963,
            "G#7": 3322.438,
            "A7": 3520.0,
            "A#7": 3729.31,
            "B7": 3951.066,
            "C8": 4186.009,
            "mute": 0
        }
        return [int(Frequency_dict[i]) for i in melody_key]


if __name__ == "__main__":
    print(freq_list([["A4", "B4", "C4"], ["A4", "B4", "C4"]]))
    with open("a.csv", "r") as f:
        a = csv.reader(f)
        print(freq_list(a))