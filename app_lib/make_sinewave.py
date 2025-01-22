import numpy as np
def sine_wave(f:int, A=0, sec:float=None, sampling:int=None, pre_data:float=0) -> np.ndarray:
        """ make_wav

        正弦波を生成する．

        Args:
            f (float): 周波数（Hz）
            A (float): 最大振幅値
            sec (float): 音の長さ（秒）
            sampling (int): 標本値の数

        Returns:
            numpy.ndarray (int16): 音声データ

        """
        SAMPLING_FREQUENCY = 44100
        QUANTIZATION_BITS = 16
        CHANNEL = 1
        global temp
        if sec != None and sampling == None:
            # 音の長さで時刻のリストを生成
            t = np.arange(SAMPLING_FREQUENCY * sec) / SAMPLING_FREQUENCY
        elif sec == None and sampling != None:
            # 標本値の数で時刻のリストを生成
            t = np.arange(SAMPLING_FREQUENCY * (sampling / SAMPLING_FREQUENCY)) / SAMPLING_FREQUENCY
        else:
            return np.empty(0)

        # print(pre_data/A)
        θ = 2 * np.pi * f * t + pre_data  # 位相の計算
        y = A * np.sin(θ)
        temp = θ[-1] % (2 * np.pi)

        # 16bit整数に変換
        y = y.astype(np.int16)

        return y