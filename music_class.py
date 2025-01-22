import numpy as np
import matplotlib.pyplot as plt
import app_lib.bpm_tempo_cac as btc
import app_lib.frequency_return as fr
import app_lib.make_sinewave as msw
import app_lib.make_amplitude_ratio as mar
import app_lib.save_wave as sw
import csv

class Music:
    def __init__(self,BPM:int, music_freq_path: str = "", tempo_path: str = "",output_path: str = "",base_freq_path:str = "",base_tempo:str = "", debug_path:str = "", debug_dist_path:str = "", debug:bool = False, A:int = 10000):
        self.BPM = BPM
        self.music_freq_patb = music_freq_path
        self.tempo_path = tempo_path
        self.output_path = output_path
        self.base_freq_path = base_freq_path
        self.base_tempo = base_tempo
        self.debug_path = debug_path
        self.debug_dist_path = debug_dist_path
        self.debug = debug
        self.SAMPLING_FREQUENCY = 44100
        self.QUANTIZATION_BITS = 16
        self.CHANNEL = 1
        self.A = A
    
    def main(self):
        if self.debug != True:
            with open(self.music_freq_patb, "r") as f:
                music_freq_row = csv.reader(f)
                _music_freq = [int(i[0]) for i in fr.freq_list(music_freq_row)]
            with open(self.tempo_path, "r") as f:
                tempo_row = csv.reader(f)
                _tempo = btc.tempolist(self.BPM, tempo_row)
            if self.base_freq_path:
                with open(self.base_freq_path, "r") as f:
                    base_freq_row = csv.reader(f)
                    _base_freq = [int(i[0]) for i in fr.freq_list(base_freq_row)]
            if self.base_tempo:
                with open(self.base_tempo, "r") as f:
                    base_tempo_row = csv.reader(f)
                    _base_tempo = btc.tempolist(self.BPM, base_tempo_row)
            if self.base_freq_path and self.base_tempo:
                sw.make_wav(np.concatenate(self._non_processing_merody(_music_freq, _tempo))+np.concatenate(self._non_processing_merody(_base_freq, _base_tempo)), f"./wav_output/{self.output_path}_non_processing.wav")
                sw.make_wav(np.concatenate(self._zero_normalize_decre(_music_freq, _tempo))+np.concatenate(self._zero_normalize_decre(_base_freq, _base_tempo)), f"./wav_output/{self.output_path}_zero_normalize_decre.wav")
                sw.make_wav(np.concatenate(self._zero_normalized(_music_freq, _tempo))+np.concatenate(self._zero_normalized(_base_freq, _base_tempo)), f"./wav_output/{self.output_path}_zero_normalized.wav")
                sw.make_wav(np.concatenate(self._sync_wave(_music_freq, _tempo))+np.concatenate(self._sync_wave(_base_freq, _base_tempo)), f"./wav_output/{self.output_path}_sub2.wav")
                sw.make_wav(np.concatenate(self._sync_wave_decre(_music_freq, _tempo))+np.concatenate(self._sync_wave_decre(_base_freq, _base_tempo)), f"./wav_output/{self.output_path}_sub3.wav")
                # ここに処理を書く
            else:
                sw.make_wav(self._non_processing_merody(_music_freq, _tempo), f"./wav_output/{self.output_path}_non_processing.wav")
                sw.make_wav(self._zero_normalize_decre(_music_freq, _tempo), f"./wav_output/{self.output_path}_zero_normalize_decre.wav")
                sw.make_wav(self._zero_normalized(_music_freq, _tempo), f"./wav_output/{self.output_path}_zero_normalized.wav")
                sw.make_wav(self._sync_wave(_music_freq, _tempo), f"./wav_output/{self.output_path}_sync_decre.wav")
                sw.make_wav(self._sync_wave_decre(_music_freq, _tempo), f"./wav_output/{self.output_path}_sync_wave_decre.wav")
                # ここに処理を書く
        if self.debug == True:
            print("debug")
            with open(self.debug_path, "r") as f:
                debug_row = csv.reader(f)
                _debug = [int(i[0]) for i in fr.freq_list(debug_row)]
            with open(self.debug_dist_path, "r") as f:
                debug_dist_row = csv.reader(f)
                _debug_dist = btc.tempolist(self.BPM, debug_dist_row)
            self.debug_matplotlib(self._non_processing_merody(_debug, _debug_dist), "./png_output/debug_non_processing.png")
            self.debug_matplotlib(self._zero_normalize_decre(_debug, _debug_dist), "./png_output/debug_zero_normalize_decre.png")
            self.debug_matplotlib(self._zero_normalized(_debug, _debug_dist), "./png_output/debug_zero_normalized.png")
            self.debug_matplotlib(self._sync_wave(_debug, _debug_dist), "./png_output/debug_sync_wave.png")
            self.debug_matplotlib(self._sync_wave_decre(_debug, _debug_dist), "./png_output/debug_sync_wave_decre.png")

    def _non_processing_merody(self, melody_line:list[int],melody_sec:list[float]) -> np.ndarray:
        """
        何も加工されていない音楽データを生成する．(おそらくみんなが使ってるやつ)

        Args:
            melody_line (list): 音楽の音階
            melody_sec (list): 音楽の秒数
        Returns:
            numpy.ndarray: 音声データ
        """
        data = []
        for i in range(len(melody_line)):
            if melody_line[i]:
                data.append((msw.sine_wave(f=melody_line[i],A = self.A, sec=melody_sec[i])))
            else:
                data.append(msw.sine_wave(f=melody_line[i],A = self.A, sec=melody_sec[i]))
            print(msw.sine_wave(f=melody_line[i],A = self.A, sec=melody_sec[i]))
        return np.concatenate(data)

    def _zero_normalize_decre(self,melody_line,melody_sec):
        """
        音の終わりの波から符号が入れ替わっているところまで0で埋めて、デクレッシェンドをつけた音楽データを生成する．(一番綺麗)

        Args:
            melody_line (list): 音楽の音階
            melody_sec (list): 音楽の秒数
        Returns:
            numpy.ndarray: 音声データ
        """
        # 全て終わりを０に近づけている
        data = []
        for i in range(len(melody_line)):
            # print(melody_line[i])
            if melody_line[i] and melody_line[i] != "n":
                # メロディの生成、最後に0を入れる処理をする(ぷつぷつ鳴る対策)
                status_num = 0
                a = (msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i])* mar.make_amplitude_ratio(0, -10, len(msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i]))))
                if a[-1] > 0:
                    status_num = 1
                elif a[-1] == 0:
                    status_num = 0
                else:
                    status_num = -1
                if status_num == 1:
                    count = 1
                    while True:
                        if a[-count] < 0:
                            break
                        a[-count] = 0
                        count += 1
                elif status_num == -1:
                    count = 1
                    while True:
                        if a[-count] > 0:
                            break
                        a[-count] = 0
                        count += 1
                # print(list(a))
                data.append(a)       
            if melody_line[i] == False:
                data.append(msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i]))
        return np.concatenate(data)
    
    def _zero_normalized(self, melody_line,melody_sec):
        """
        音の終わりの波から符号が入れ替わっているところまで0で埋めた音楽データを生成する．(まあまあきれい)

        Args:
            melody_line (list): 音楽の音階
            melody_sec (list): 音楽の秒数
        Returns:
            numpy.ndarray: 音声データ
        """
        # 全て終わりを０に近づけている
        data = []
        for i in range(len(melody_line)):
            # print(melody_line[i])
            if melody_line[i] and melody_line[i] != "n":
                # メロディの生成、最後に0を入れる処理をする(ぷつぷつ鳴る対策)
                status_num = 0
                a = (msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i]))
                if a[-1] > 0:
                    status_num = 1
                elif a[-1] == 0:
                    status_num = 0
                else:
                    status_num = -1
                if status_num == 1:
                    count = 1
                    while True:
                        if a[-count] <0:
                            break
                        a[-count] = 0
                        count += 1
                elif status_num == -1:
                    count = 1
                    while True:
                        if a[-count] >0:
                            break
                        a[-count] = 0
                        count += 1
                # print(list(a))
                data.append(a)       
            if melody_line[i] == False:
                data.append(msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i]))
        return np.concatenate(data)
    
    def _sync_wave(self,melody_line,melody_sec):
        """
        初期相異をいじって滑らかに再生する関数→MUTEがあるとぷつぷつ鳴る

        Args:
            melody_line (list): 音楽の音階
            melody_sec (list): 音楽の秒数
        Returns:
            numpy.ndarray: 音声データ
        """
        data = []
        temp_me = 0
        A = 15000
        for i in range(len(melody_line)):
            if melody_line[i]:
                temp_merody = msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i], pre_data=temp_me) 
                data.append(temp_merody)
                t = np.arange(self.SAMPLING_FREQUENCY * melody_sec[i]) / self.SAMPLING_FREQUENCY
                theta = 2 * np.pi * melody_line[i] * t +temp_me
                temp_me = (theta[-1] % (2*np.pi))
            else:
                data.append(msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i], pre_data=temp_me))
        return np.concatenate(data)
    
    def _sync_wave_decre(self, melody_line,melody_sec):
        """
        初期相異をいじって滑らかに再生する関数muteの前にデクレッシェンドと0にする処理を入れて滑らかに聞こえるようにしている
        
        Args:
            melody_line (list): 音楽の音階
            melody_sec (list): 音楽の秒数
        Returns:
            numpy.ndarray: 音声データ
        """
        data = []
        temp_me = 0
        for i in range(len(melody_line)):
            if melody_line[i]:
                if len(melody_line)-1 != i:
                    print(melody_line[i+1])
                    if melody_line[i+1] != 0:
                        temp_merody = msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i], pre_data=temp_me)
                        data.append(temp_merody)
                        # print(temp_merody)
                        t = np.arange(self.SAMPLING_FREQUENCY * melody_sec[i]) / self.SAMPLING_FREQUENCY
                        θ = 2 * np.pi * melody_line[i] * t +temp_me
                        temp_me = (θ[-1] % (2*np.pi))
                    else:
                        status_num = 0
                        print("MUTE")
                        a = (msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i], pre_data=temp_me)* mar.make_amplitude_ratio(0, -12, len(msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i], pre_data=temp_me))))
                        if a[-1] > 0:
                            status_num = 1
                        elif a[-1] == 0:
                            status_num = 0
                        else:
                            status_num = -1
                        if status_num == 1:
                            count = 1
                            while True:
                                if a[-count] <0:
                                    break
                                a[-count] = 0
                                count += 1
                        elif status_num == -1:
                            count = 1
                            while True:
                                if a[-count] >0:
                                    break
                                a[-count] = 0
                                count += 1
                        data.append(a)
                        
                else:
                    print("Last")
                    temp_merody = msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i], pre_data=temp_me)
                    data.append(temp_merody)
                    # print(temp_merody)
                    if len(melody_line)-1 != i:
                        temp_me = (temp_merody/self.A)[-1] % (2*np.pi)
                        print(temp_me)
                    
            else:
                data.append(msw.sine_wave(melody_line[i],A = self.A, sec=melody_sec[i]))
                temp_me = 0
        return np.concatenate(data)
    
    def debug_matplotlib(self, data, path):
        plt.cla()
        print(data)
        print("plot")
        plt.plot(data,linestyle=None,linewidth=0,marker="o")
        print("save")
        plt.savefig(f"{path}")

if __name__ == "__main__":
    a = Music(168, music_freq_path="./load_csv_folder/main_melody.csv",tempo_path= "./load_csv_folder/main_melody_dist.csv", output_path = "output")
    b = Music(1000, debug_path="./load_csv_folder/a.csv",debug_dist_path= "./load_csv_folder/b.csv", debug = True, A=100)
    print(a.main())
    b.main()