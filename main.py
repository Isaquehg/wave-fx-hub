from matplotlib import pyplot as plt
import pyaudio
import numpy as np
import scipy.signal as ss
import scipy.interpolate as si

# PyAudio basic config
n_channels_input = 1
n_channels_output = 2
sample_rate = 44100  # Sampling Rate [Hz]
chunk_size = 1024   # Audio Buffer Size
input_device = 1
output_device = 0

# PyAudio object
p = pyaudio.PyAudio()
'''
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")
    print((info['name'], info['maxInputChannels']))
'''

# Opening Audio Input Stream with the built-in microphone
input_stream = p.open(format=pyaudio.paFloat32,
                      channels=n_channels_input, # Adjust the number of channels as needed
                      rate=sample_rate,
                      input=True)

# Opening Audio Output Stream with the built-in laptop speaker
output_stream = p.open(format=pyaudio.paFloat32,
                       channels=n_channels_output,
                       rate=sample_rate,
                       output=True)

duration = 5  # Duration of the noise-only recording in seconds




# Compressor Effect
def apply_compressor(input_data, threshold=-20, ratio=4, attack_time=10):
    output_data = np.zeros_like(input_data)
    envelope = 0.0  # Initialize envelope value

    for i in range(len(input_data)):
        # Calculate the envelope (average amplitude)
        envelope = max(abs(input_data[i]), envelope * (1.0 - 1.0 / attack_time))

        # Calculate the compression gain
        if envelope > threshold:
            gain = 1 + (threshold - envelope) / (threshold * (ratio - 1))
        else:
            gain = 1.0

        # Apply the gain to the input signal
        output_data[i] = input_data[i] * gain

    return output_data

# Equalizer Effect
def apply_equalizer(input_audio, low_gain=1.0, mid_gain=1.0, high_gain=1.0, sample_rate=44100):
    # Define filter parameters for each band (frequency range, bandwidth, and order)
    low_freq_range = [20, 200]  # Adjust as needed
    mid_freq_range = [200, 2000]  # Adjust as needed
    high_freq_range = [2000, 20000]  # Adjust as needed
    
    # Design bandpass filters for each band
    low_b = ss.butter(4, [f / (sample_rate / 2) for f in low_freq_range], btype='band')
    mid_b = ss.butter(4, [f / (sample_rate / 2) for f in mid_freq_range], btype='band')
    high_b = ss.butter(4, [f / (sample_rate / 2) for f in high_freq_range], btype='band')
    
    # Apply the filters to the input audio
    low_output = ss.lfilter(low_b[0], low_b[1], input_audio) * low_gain
    mid_output = ss.lfilter(mid_b[0], mid_b[1], input_audio) * mid_gain
    high_output = ss.lfilter(high_b[0], high_b[1], input_audio) * high_gain
    
    # Combine the outputs to create the equalized audio
    equalized_audio = low_output + mid_output + high_output
    
    return equalized_audio

# Volume Boost Effect
def apply_volume_boost(input_data, gain=1000.0):
    return input_data * gain

# Distortion Effect
def apply_distortion(input_audio, gain=100.0):
    # Rectify the audio signal
    rectified_signal = np.abs(input_audio)

    # Amplify the rectified signal
    distorted_signal = rectified_signal * gain

    return distorted_signal

# Pitch Shift Effect
def apply_pitch_shift(input_data, desired_length=1024):
    # Calculate the pitch shift factor
    
    # Calculate the desired output length
    output_length = int(desired_length)
    
    # Create a time array for the input data
    input_time = np.arange(len(input_data))
    
    # Create a time array for the output data
    output_time = np.arange(output_length) * (len(input_data) / output_length)
    
    # Use interpolation to resample the input audio to the desired length
    interpolator = si.interp1d(input_time, input_data, kind='linear', fill_value="extrapolate")
    output_data = interpolator(output_time)
    
    return output_data

def apply_low_pass_filter(input_audio, cutoff_frequency=3000, sample_rate=44100, order=4):
    # Calculate the Nyquist frequency
    nyquist = 0.5 * sample_rate

    # Calculate the normalized cutoff frequency
    normalized_cutoff = cutoff_frequency / nyquist

    # Design the low-pass filter
    b, a = ss.butter(order, normalized_cutoff, btype='low')

    # Apply the filter to the input audio
    filtered_audio = ss.lfilter(b, a, input_audio)

    return filtered_audio

# Calculating the average signal
received = 0
frame_size = 1024  # Adjust the frame size as needed

# Initialize an array to store the mean values
mean_signal = np.zeros(frame_size)

# Main loop
try:
    print("Starting Wave FX Hub. Press Ctrl+C to exit.")
    while True:
        # Real time audio input
        input_data = np.frombuffer(input_stream.read(chunk_size), dtype=np.float32)
        print(input_data[-1])
        #print(type(input_data))
        #print(input_data.shape)
        #print(len(input_data))
        #print(input_data[1])

        # Applying effects
        processed_data = apply_compressor(input_data)
        #processed_data = apply_equalizer(processed_data)
        processed_data = apply_volume_boost(processed_data)
        #processed_data = apply_pitch_shift(processed_data)
        #processed_data = apply_low_pass_filter(input_data)
        #processed_data = apply_distortion(input_data)
        
        # Average Signal
        mean_signal += processed_data
        received += 1.0

        # Received audio output
        output_stream.write(processed_data.tobytes())

except KeyboardInterrupt:
    print("Effects interface stopped.")

finally:
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()

    # Perform FFT
    fft_result = np.fft.fft(processed_data)

    # Calculate the magnitude spectrum
    magnitude_spectrum = np.abs(fft_result)

    # Convert frequency bins to Hertz
    n = len(processed_data)
    frequencies = np.fft.fftfreq(n, 1.0 / sample_rate)

    # Set the frequency range to zoom in (adjust as needed)
    start_freq = 1000  # Start frequency (Hz)
    end_freq = 13000  # End frequency (Hz)

    # Find the corresponding indices in the frequency array
    start_index = np.argmax(frequencies >= start_freq)
    end_index = np.argmax(frequencies >= end_freq)

    # Plot the magnitude spectrum with zoomed-in x-axis
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies[start_index:end_index], magnitude_spectrum[start_index:end_index])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Zoomed-In Frequency Spectrum of Audio Signal')
    plt.grid()
    plt.show()