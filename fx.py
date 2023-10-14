import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from scipy.io.wavfile import read, write

class Effects():
    def __init__(self) -> None:
        pass

    def set_file_path(self, path_to_file: str):
        sample_rate, audio_data = read(path_to_file)
        self.sample_rate = sample_rate
        self.audio_data = audio_data

        # Plotting the original signal
        #plt.plot(audio_data)
        #plt.show()

    def increase_amplitude(self, scaling_factor):
        # Ensure the audio_data is in float32 format
        amplified_audio = self.audio_data.astype(np.float32)

        # Increase the amplitude by multiplying with the scaling factor
        amplified_audio *= scaling_factor

        self.audio_data = amplified_audio

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
    def apply_equalizer(self, low_gain=10.0, mid_gain=1.0, high_gain=1.0):
        # Ensure the audio_data is in float32 format
        audio_data = self.audio_data.astype(np.float32)

        # Ensure stereo audio has shape (n_samples, 2)
        if audio_data.shape[1] != 2:
            raise ValueError("Input audio data should have shape (n_samples, 2) for stereo audio.")

        # Normalize audio to the range [-1, 1]
        audio_data /= np.max(np.abs(audio_data))

        # Calculate the frequency axis for the FFT
        n_samples = audio_data.shape[0]
        freq_axis = np.fft.fftfreq(n_samples, d=1.0 / self.sample_rate)

        # Initialize an array to store the frequency response
        freq_response = np.ones(n_samples)

        # Define frequency bands for low, mid, and high frequencies
        low_freq_range = (0, 1000)  # Adjust as needed
        mid_freq_range = (1000, 5000)  # Adjust as needed
        high_freq_range = (5000, 20000)  # Adjust as needed

        # Apply gain adjustments for each frequency band
        for freq_range, gain in [(low_freq_range, low_gain), (mid_freq_range, mid_gain), (high_freq_range, high_gain)]:
            low_freq, high_freq = freq_range
            # Create a filter that boosts or attenuates the specified frequency range
            filter_mask = (freq_axis >= low_freq) & (freq_axis <= high_freq)
            freq_response[filter_mask] *= gain

        # Apply the frequency response to the audio signal using inverse FFT
        equalized_audio = np.fft.ifft(np.fft.fft(audio_data, axis=0) * freq_response[:, np.newaxis], axis=0).real

        self.audio_data = equalized_audio

    # Distortion Effect
    def apply_distortion(self, gain=50.0):
        audio_data = self.audio_data.astype(np.float32)

        # Normalize audio to the range [-1, 1]
        audio_data /= np.max(np.abs(audio_data))

        # Apply distortion (clipping)
        distorted_audio = np.clip(audio_data * gain, -1.0, 1.0)

        self.audio_data = distorted_audio

    # Pitch Shift Effect
    def apply_pitch_shift(self, pitch_shift_factor=1.5):
        # Ensure the audio_data is in float32 format
        audio_data = self.audio_data.astype(np.float32)

        # Normalize audio to the range [-1, 1]
        audio_data /= np.max(np.abs(audio_data))

        # Calculate the desired output length
        output_length = int(len(audio_data) / pitch_shift_factor)

        # Use the scipy.signal.resample function for pitch shifting
        output_data = ss.resample(audio_data, output_length)

        self.audio_data = output_data

    def apply_delay(self, delay_ms=800, feedback=0.1):
        # Ensure the audio_data is in float32 format
        audio_data = self.audio_data.astype(np.float32)

        # Ensure stereo audio has shape (n_samples, 2)
        if audio_data.shape[1] != 2:
            raise ValueError("Input audio data should have shape (n_samples, 2) for stereo audio.")

        # Normalize audio to the range [-1, 1]
        audio_data /= np.max(np.abs(audio_data))

        # Calculate the delay in samples
        delay_samples = int((delay_ms / 1000) * self.sample_rate)

        # Create an empty array to store the delayed audio
        delayed_audio = np.zeros_like(audio_data)

        # Apply the delay effect
        for i in range(len(audio_data)):
            if i >= delay_samples:
                delayed_audio[i] = audio_data[i] + feedback * delayed_audio[i - delay_samples]

        self.audio_data = delayed_audio


    def save_audio(self):
        write("output/output_audio.wav", 48000, self.audio_data.astype(np.int16))

        # Plotting the resulted signal
        plt.plot(self.audio_data)
        plt.show()

        return True
