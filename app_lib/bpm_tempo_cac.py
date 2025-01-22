import csv
def tempolist(BPM, _time_list:list):
    _time_list = list_to_int(_time_list)
    _return_list = []
    for i in _time_list:
        if type(i) == list:
            _return_list.append(sum([_playtime(BPM, j) for j in i]))
    return _return_list

def list_to_int(_list):
    _temp_list = []
    for i in _list:
        if type(i) == str:
            _temp_list.append(int(i))
        elif type(i) == list:
            _temp_list.append([int(j) for j in i])
    return _temp_list

def _playtime(BPM, _time_list:int):
    after_second = {
        1: (60 / BPM) * 4,
        2: (60 / BPM) * 2,
        3: ((60 / BPM) * 2) + (60 / BPM),
        4: 60 / BPM,
        5: 60 / BPM + ((60 / BPM) / 2),
        8: (60 / BPM) / 2,
        12: ((60 / BPM) * 2) + (60 / BPM) / 2,
        13: ((60 / BPM) / 2) + (60 / BPM + ((60 / BPM) / 2)),
        16: (60 / BPM) / 4,
        32: (60 / BPM) / 8,
    }
    ans = after_second[_time_list]
    return ans


if __name__ == "__main__":
    # print(tempolist(120, [[1], 2, 3, 4, 5, 8, 12, 13, 16]))
    with open("a.csv", "r") as f:
        a = csv.reader(f)
        print(tempolist(168, a))