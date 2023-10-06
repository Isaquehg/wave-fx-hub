from tkinter import *
import customtkinter
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import scipy.interpolate as si
from scipy.io.wavfile import read, write
from not_real_time import Effects

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # FX Config.
        self.effects = Effects()

        # CustomTkinter config.
        self.title("WaveFX")
        self.geometry("1600x900")

        self.check_var_equalizer = customtkinter.StringVar(value="on")
        self.check_var_distortion = customtkinter.StringVar(value="on")
        self.check_var_compressor = customtkinter.IntVar(value=1)
        self.check_var_volboost = customtkinter.StringVar(value="on")
        self.check_var_delay = customtkinter.StringVar(value="on")
        self.check_var_pitch = customtkinter.StringVar(value="on")

        # Equalizer
        self.equalizer_checkbox = customtkinter.CTkCheckBox(self, text="Equalizador", command=self.checkbox_event_equalizer, variable=self.check_var_equalizer, onvalue="on", offvalue="off")
        self.equalizer_checkbox.place(relx=0.3, rely=0.35, anchor=CENTER)
        # Equalizer slides
        self.equalizer_low_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.equalizer_low_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.equalizer_med_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.equalizer_med_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.equalizer_high_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.equalizer_high_slider.place(relx=0.5, rely=0.5, anchor=S)

        # Distortion
        self.distortion_checkbox = customtkinter.CTkCheckBox(self, text="Distorcao", command=self.checkbox_event_distortion, variable=self.check_var_distortion, onvalue="on", offvalue="off")
        self.distortion_checkbox.place(relx=0.3, rely=0.25, anchor=CENTER)
        self.distortion_slider = customtkinter.CTkSlider(master=self, from_=1, to=100, command=self.equalizer_slider_event)
        self.distortion_slider.place(relx=0.1, rely=0.1, anchor=S)

        # Compressor
        self.compressor_checkbox = customtkinter.CTkCheckBox(self, text="Compressor", command=self.checkbox_event_compressor, variable=self.check_var_compressor, onvalue=1, offvalue=0)
        self.compressor_checkbox.place(relx=0.3, rely=0.15, anchor=CENTER)
        # Compressor sliders
        self.compressor_threshold_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.compressor_threshold_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.compressor_radio_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.compressor_radio_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.compressor_attack_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.compressor_attack_slider.place(relx=0.5, rely=0.5, anchor=S)

        # Increse signal amplitude
        self.vol_boost_checkbox = customtkinter.CTkCheckBox(self, text="Volume Boost", command=self.checkbox_event_volboost, variable=self.check_var_volboost, onvalue="on", offvalue="off")
        self.vol_boost_checkbox.place(relx=0.705, rely=0.35, anchor=CENTER)

        # Delay
        self.delay_checkbox = customtkinter.CTkCheckBox(self, text="Delay", command=self.checkbox_event_delay, variable=self.check_var_delay, onvalue="on", offvalue="off")
        self.delay_checkbox.place(relx=0.7, rely=0.25, anchor=CENTER)

        # Pitch Shift
        self.pitch_shift_checkbox = customtkinter.CTkCheckBox(self, text="Pitch Shift", command=self.checkbox_event_pitch, variable=self.check_var_pitch, onvalue="on", offvalue="off")
        self.pitch_shift_checkbox.place(relx=0.7, rely=0.15, anchor=CENTER)


        # Choose file
        self.button_abrir = customtkinter.CTkButton(self, text="Escolher Arquivo", command=self.button_event_escolher_arq)
        self.button_abrir.place(relx=0.3, rely=0.8, anchor=CENTER)

        # Process file
        self.button_fechar = customtkinter.CTkButton(self, text="Processar", command=self.button_event_processar)
        self.button_fechar.place(relx=0.7, rely=0.8, anchor=CENTER)

        # Input file path str
        self.entry = customtkinter.CTkEntry(app, placeholder_text="CTkEntry")
        self.entry.place(relx=0.9, rely=0.5, anchor=CENTER)

    def button_event_escolher_arq(self):
        self.effects.set_file_path(self.entry.get())

    def button_event_processar(self):
        self.effects.save_audio()

    def checkbox_event_equalizer(self):
        if (self.equalizer_low_slider.get() and self.equalizer_med_slider.get() and self.equalizer_high_slider.get()) <= 1:
            self.effects.apply_equalizer()
        else:
            self.effects.apply_equalizer(self.equalizer_low_slider.get(), self.equalizer_med_slider.get(), self.equalizer_high_slider.get())
    
    def checkbox_event_distortion(self):
        if(self.distortion_slider.get() <= 1):
            self.effects.apply_distortion()
        else:
            self.effects.apply_distortion(self.distortion_slider.get())

    def checkbox_event_compressor(self):
        self.effects.apply_compressor()

    def checkbox_event_volboost(self):
        self.effects.increase_amplitude()

    def checkbox_event_delay(self):
        self.effects.apply_delay()

    def checkbox_event_pitch(self):
        self.effects.apply_pitch_shift()

app = App()
app.mainloop()