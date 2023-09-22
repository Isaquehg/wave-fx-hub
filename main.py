import pyaudio
import numpy as np
import scipy.signal as ss

# PyAudio basic config
n_channels_input = 1
n_channels_output = 2
sample_rate = 44100  # Sampling Rate [Hz]
chunk_size = 1024   # Audio Buffer Size
input_device = 1
output_device = 0

# PyAudio object
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")
    print((info['name'], info['maxInputChannels']))

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


# Overdrive Effect
def apply_overdrive(input_data, gain=2.0):
    return input_data * gain

'''
# Chorus Effect
def apply_chorus(input_data, depth=500, rate=1):
    num_delayed_signals = 3  # Number of delayed signals (adjust as needed)
    max_delay = int(depth * sample_rate / 1000)  # Maximum delay in samples
    
    # Initialize the delayed signals
    delayed_signals = [np.zeros_like(input_data) for _ in range(num_delayed_signals)]
    
    # Apply modulation to each delayed signal
    for i in range(num_delayed_signals):
        delay = max_delay - (i * max_delay // (num_delayed_signals - 1))
        modulator = np.sin(2 * np.pi * rate * np.arange(len(input_data)))
        delayed_signals[i] = np.roll(input_data, delay) * modulator
        
    # Combine the original and delayed signals
    combined_signal = np.mean([input_data] + delayed_signals, axis=0)
    
    return combined_signal
'''
# Wah Wah Effect
def apply_wah_wah(input_data, depth=1000, rate=0.5):
    # Create a modulating wave (sine wave) for the wah-wah effect
    modulator = np.sin(2 * np.pi * rate * np.arange(len(input_data)))

    # Create a bandpass filter
    cutoff = depth * modulator + 1000  # Adjust the center frequency and depth as needed
    nyquist = 0.5 * sample_rate
    width = 0.1  # Width of the bandpass filter (adjust as needed)
    order = 21  # Filter order (adjust as needed)
    b = ss.firwin(order, [cutoff[0] - 0.5 * width, cutoff[0] + 0.5 * width], nyq=nyquist)
    
    # Apply the filter to the input data
    wah_wah_data = ss.lfilter(b, 1.0, input_data)
    
    return wah_wah_data

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
def apply_equalizer(input_data, low_gain=1.0, mid_gain=1.0, high_gain=1.0, sample_rate=44100):
    # Design bandpass filters for low, mid, and high frequencies
    low_cutoff = 100  # Adjust as needed
    low_width = 100   # Adjust as needed
    low_b = ss.firwin(31, [low_cutoff - low_width / 2, low_cutoff + low_width / 2], fs=sample_rate)
    
    mid_cutoff = 1000  # Adjust as needed
    mid_width = 200    # Adjust as needed
    mid_b = ss.firwin(31, [mid_cutoff - mid_width / 2, mid_cutoff + mid_width / 2], fs=sample_rate)
    
    high_cutoff = 5000  # Adjust as needed
    high_width = 1000   # Adjust as needed
    high_b = ss.firwin(31, [high_cutoff - high_width / 2, high_cutoff + high_width / 2], fs=sample_rate)
    
    # Apply the filters and adjust gains
    low_output = ss.lfilter(low_b, 1.0, input_data) * low_gain
    mid_output = ss.lfilter(mid_b, 1.0, input_data) * mid_gain
    high_output = ss.lfilter(high_b, 1.0, input_data) * high_gain
    
    # Combine the outputs
    output_data = low_output + mid_output + high_output
    
    return output_data

# Volume Boost Effect
def apply_volume_boost(input_data, gain=2.0):
    return input_data * gain

# Pitch Shift Effect
def apply_pitch_shift(input_data, semitones=2.0, sample_rate=44100):
    # Calculate the pitch shift factor
    pitch_shift_factor = 2 ** (semitones / 12.0)
    
    # Resample the input audio
    output_data = ss.resample(input_data, int(len(input_data) / pitch_shift_factor))
    
    return output_data

# Main loop
try:
    print("Iniciando a pedaleira de guitarra. Pressione Ctrl+C para sair.")
    while True:
        # Real time audio input
        input_data = np.frombuffer(input_stream.read(chunk_size), dtype=np.float32)
        print(input_data)
        print(type(input_data))
        print(input_data.shape)
        print(input_data[1])

        # Applying effects
        processed_data = apply_compressor(input_data)
        #processed_data = apply_overdrive(processed_data)
        #processed_data = apply_wah_wah(processed_data)
        #processed_data = apply_equalizer(processed_data)
        #processed_data = apply_volume_boost(processed_data)
        processed_data = apply_pitch_shift(processed_data)

        # Received audio output
        output_stream.write(processed_data.tobytes())

except KeyboardInterrupt:
    print("Effects interface stopped.")

finally:
    # Close stream
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()