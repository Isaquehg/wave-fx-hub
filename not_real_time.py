import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import scipy.interpolate as si
from scipy.io.wavfile import read, write

class Effects():
    def __init__(self, path_to_file: str) -> None:
        # Import audio file -> 48kHz sample rate
        sample_rate, audio_data = read(path_to_file)
        self.audio_data = audio_data

        print(sample_rate)
        print(audio_data.shape)

        plt.plot(audio_data)
        #plt.show()

    # Compressor Effect
    def apply_compressor(self, threshold=-20, ratio=4, attack_time=10):
        output_data = np.zeros_like(self.audio_data)
        envelope = 0.0  # Initialize envelope value

        for i in range(len(self.audio_data)):
            # Calculate the envelope (average amplitude)
            envelope = max(abs(self.audio_data[i].all()), envelope * (1.0 - 1.0 / attack_time))

            # Calculate the compression gain
            if envelope > threshold:
                gain = 1 + (threshold - envelope) / (threshold * (ratio - 1))
            else:
                gain = 1.0

            # Apply the gain to the input signal
            output_data[i] = self.audio_data[i] * gain

        self.audio_data = output_data

    # Equalizer Effect
    def apply_equalizer(self, low_gain=1.0, mid_gain=1.0, high_gain=1.0, sample_rate=44100):
        # Define filter parameters for each band (frequency range, bandwidth, and order)
        low_freq_range = [20, 200]  # Adjust as needed
        mid_freq_range = [200, 2000]  # Adjust as needed
        high_freq_range = [2000, 20000]  # Adjust as needed
        
        # Design bandpass filters for each band
        low_b = ss.butter(4, [f / (sample_rate / 2) for f in low_freq_range], btype='band')
        mid_b = ss.butter(4, [f / (sample_rate / 2) for f in mid_freq_range], btype='band')
        high_b = ss.butter(4, [f / (sample_rate / 2) for f in high_freq_range], btype='band')
        
        # Apply the filters to the input audio
        low_output = ss.lfilter(low_b[0], low_b[1], self.audio_data) * low_gain
        mid_output = ss.lfilter(mid_b[0], mid_b[1], self.audio_data) * mid_gain
        high_output = ss.lfilter(high_b[0], high_b[1], self.audio_data) * high_gain
        
        # Combine the outputs to create the equalized audio
        equalized_audio = low_output + mid_output + high_output
        
        self.audio_data = equalized_audio

    # Volume Boost Effect
    def apply_volume_boost(self, gain=1000.0):
        self.audio_data *= gain

    # Distortion Effect
    def apply_distortion(self, gain=100.0):
        # Rectify the audio signal
        rectified_signal = np.abs(self.audio_data)

        # Amplify the rectified signal
        distorted_signal = rectified_signal * gain

        self.audio_data = distorted_signal

    # Pitch Shift Effect
    def apply_pitch_shift(self, desired_length=1024):
        # Calculate the pitch shift factor
        
        # Calculate the desired output length
        output_length = int(desired_length)
        
        # Create a time array for the input data
        input_time = np.arange(len(self.audio_data))
        
        # Create a time array for the output data
        output_time = np.arange(output_length) * (len(self.audio_data) / output_length)
        
        # Use interpolation to resample the input audio to the desired length
        interpolator = si.interp1d(input_time, self, kind='linear', fill_value="extrapolate")
        output_data = interpolator(output_time)
        
        self.audio_data = output_data

    def apply_low_pass_filter(self, cutoff_frequency=500, sample_rate=44100, order=2):
        # Calculate the Nyquist frequency
        nyquist = 0.5 * sample_rate

        # Calculate the normalized cutoff frequency
        normalized_cutoff = cutoff_frequency / nyquist

        # Design the low-pass filter
        b, a = ss.butter(order, normalized_cutoff, btype='low')

        # Apply the filter to the input audio
        filtered_audio = ss.lfilter(b, a, self.audio_data)

        self.audio_data = filtered_audio

    def save_audio(self):
        write("output/output_audio.wav", 48000, self.audio_data)
    
effects = Effects("audios/audio_file.wav")
effects.apply_compressor()

#effects.save_audio()