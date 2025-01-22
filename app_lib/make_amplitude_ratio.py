import numpy as np
def make_amplitude_ratio(start=0, end=0, sampling=None):
    """ make_wav

    振幅比の数列を生成する．
    （クレッシェンド，デクレッシェンドを生成するために使用する）

    Args:
        start (float): 開始時の音圧（dB）
        end (float): 終了時の音圧（dB）
        sampling (int): 標本値の数

    Returns:
        numpy.ndarray: 振幅比の数列

    """

    # 音圧（dB）のリスト
    L = np.linspace(start, end, sampling)

    # 振幅比の数列
    amp_ratio = np.power(10, L / 20)

    return amp_ratio
