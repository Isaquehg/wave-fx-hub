import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import scipy.interpolate as si
from scipy.io.wavfile import read, write

class Effects():
    def __init__(self, path_to_file: str) -> None:
        # Import audio file -> 48kHz sample rate
        sample_rate, audio_data = read(path_to_file)

        self.sample_rate = sample_rate
        self.audio_data = audio_data

        print(sample_rate)
        print(audio_data.shape)

        plt.plot(audio_data)
        plt.show()

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
    def apply_equalizer(self, low_gain=1.0, mid_gain=1.0, high_gain=25.0):
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

        print(equalized_audio.shape)

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

    def apply_reverb(self, delay_lengths=[44100, 48000, 53700], feedback=0.5):
        audio_data = self.audio_data.astype(np.float32)

        # Ensure stereo audio has shape (n_samples, 2)
        if audio_data.shape[1] != 2:
            raise ValueError("Input audio data should have shape (n_samples, 2) for stereo audio.")

        # Normalize audio to the range [-1, 1]
        audio_data /= np.max(np.abs(audio_data))

        # Initialize the reverb taps with lists
        reverb_taps = [list(np.zeros(delay_length)) for delay_length in delay_lengths]

        # Create an empty array to store the reverb output
        reverb_output = np.zeros_like(audio_data)

        # Apply the reverb effect
        for i in range(len(audio_data)):
            for j, delay_length in enumerate(delay_lengths):
                # Calculate the output for each tap (comb filter)
                if i >= delay_length:
                    reverb_taps[j].append(audio_data[i] + feedback * reverb_taps[j].pop(0))
                else:
                    reverb_taps[j].append(audio_data[i] + feedback * reverb_taps[j][-1])

                # Sum the outputs from all taps
                reverb_output[i] += reverb_taps[j][-1]

        self.audio_data = reverb_output

    def save_audio(self):
        write("output/output_audio.wav", 48000, self.audio_data.astype(np.int16))
        plt.plot(self.audio_data)
        plt.show()


effects = Effects("audios/audio_file.wav")
#effects.apply_compressor()
#effects.apply_distortion()
#effects.apply_equalizer()
effects.apply_reverb()

effects.save_audio()