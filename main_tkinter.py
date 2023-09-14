import pyaudio
import numpy as np
import scipy.signal as ss
from tkinter import *
import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super()__init__()

        self.title("Audio Effects Application")
        self.geometry(f"{1100}x{580}")
        customtkinter.set_dafault_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Creating Effects Buttons
        compressor_button = customtkinter.CTkButton(master=self, text='Compressor')
        overdrive_button = customtkinter.CTkButton(master=self, text='Overdrive')
        wah_wah_button = customtkinter.CTkButton(master=self, text='Wah Wah')
        Chorus_button = customtkinter.CTkButton(master=self, text='Chorus')

        # Place Buttons
        compressor_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Overdrive Effect
    def apply_overdrive(self, input_data, gain=2.0):
        return input_data * gain
    
    # Compressor Effect
    def apply_compressor(self, input_data, threshold=-20, ratio=4, attack_time=10):
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


    # Wah Wah Effect
    def apply_wah_wah(self, input_data, depth=1000, rate=0.5):
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

    # Chorus Effect
    def apply_chorus(self, input_data, depth=500, rate=1):
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

# PyAudio basic config
n_channels_input = 1
n_channels_output = 2
sample_rate = 44100  # Sampling Rate [Hz]
chunk_size = 1024   # Audio Buffer Size
input_device = 1
output_device = 0

# PyAudio object
p = pyaudio.PyAudio()
app = App()

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

# Main loop
try:
    print("Iniciando a pedaleira de guitarra. Pressione Ctrl+C para sair.")
    while True:
        # Real time audio input
        input_data = np.frombuffer(input_stream.read(chunk_size), dtype=np.float32)

        app.update()

        # Received audio output
        output_stream.write(processed_data.tobytes())

except KeyboardInterrupt:
    print("Pedaleira de guitarra encerrada.")

finally:
    # Close stream
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()


if __name__ == "__main__":
    app.mainloop()