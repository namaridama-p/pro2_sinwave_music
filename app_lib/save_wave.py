import struct


def make_wav(data, path='out.wav'):
        """ make_wav

        WAVファイルを生成する．

        Args:
            data (numpy.ndarray): 音声データ
            path (str): 出力ファイルパス

        Returns:
            なし

        """

        SAMPLING_FREQUENCY = 44100
        QUANTIZATION_BITS = 16
        CHANNEL = 1

        # データ型をint16にする
        if data.dtype != 'int16':
            data = data.astype('int16')

        # NumPy配列からリストに変換
        data = data.tolist()

        # 2Byte リトルエンディアンに変換
        fmt = 'h' * len(data)
        data = struct.pack(fmt, *data)

        # WAVファイルヘッダ
        DataSize = len(data)
        RIFF = "RIFF"
        FileSize = DataSize + 44 - 8
        WAVE = "WAVE"
        FmtChunk = "fmt "
        FmtChunkSize = 16
        FormatID = 1
        DataSpeed = int(SAMPLING_FREQUENCY * CHANNEL * QUANTIZATION_BITS / 8)
        BlockSize = int(CHANNEL * QUANTIZATION_BITS / 8)
        DataChunk = "data"

        with open(path, mode='wb') as f_out:
            f_out.write(RIFF.encode())
            f_out.write(FileSize.to_bytes(4, byteorder='little'))
            f_out.write(WAVE.encode())
            f_out.write(FmtChunk.encode())
            f_out.write(FmtChunkSize.to_bytes(4, byteorder='little'))
            f_out.write(FormatID.to_bytes(2, byteorder='little'))
            f_out.write(CHANNEL.to_bytes(2, byteorder='little'))
            f_out.write(SAMPLING_FREQUENCY.to_bytes(4, byteorder='little'))
            f_out.write(DataSpeed.to_bytes(4, byteorder='little'))
            f_out.write(BlockSize.to_bytes(2, byteorder='little'))
            f_out.write(QUANTIZATION_BITS.to_bytes(2, byteorder='little'))
            f_out.write(DataChunk.encode())
            f_out.write(DataSize.to_bytes(4, byteorder='little'))
            f_out.write(data)