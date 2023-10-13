import os
from tkinter import *
import customtkinter
from not_real_time import Effects

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # FX Config.
        self.effects = Effects()
        self.params = {}

        # CustomTkinter config.
        self.title("WaveFX")
        self.geometry("1600x900")

        self.check_var_equalizer = customtkinter.StringVar(value="off")
        self.check_var_distortion = customtkinter.StringVar(value="off")
        self.check_var_compressor = customtkinter.StringVar(value="off")
        self.check_var_volboost = customtkinter.StringVar(value="off")
        self.check_var_delay = customtkinter.StringVar(value="off")
        self.check_var_pitch = customtkinter.StringVar(value="off")

        # Equalizer
        self.equalizer_checkbox = customtkinter.CTkCheckBox(self, text="Equalizer", command=self.checkbox_event_equalizer, variable=self.check_var_equalizer, onvalue="on", offvalue="off")
        self.equalizer_checkbox.place(relx=0.15, rely=0.25, anchor=CENTER)
        # Equalizer sliders
        self.equalizer_low_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event, orientation='vertical')
        self.equalizer_low_slider.place(relx=0.1, rely=0.5, anchor=CENTER)
        self.equalizer_med_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event, orientation='vertical')
        self.equalizer_med_slider.place(relx=0.15, rely=0.5, anchor=CENTER)
        self.equalizer_high_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event, orientation='vertical')
        self.equalizer_high_slider.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Distortion
        self.distortion_checkbox = customtkinter.CTkCheckBox(self, text="Distortion", command=self.checkbox_event_distortion, variable=self.check_var_distortion, onvalue="on", offvalue="off")
        self.distortion_checkbox.place(relx=0.3, rely=0.25, anchor=CENTER)
        self.distortion_slider = customtkinter.CTkSlider(master=self, from_=1, to=100, command=self.distortion_slider_event, orientation='vertical')
        self.distortion_slider.place(relx=0.3, rely=0.5, anchor=CENTER)

        # Compressor
        self.compressor_checkbox = customtkinter.CTkCheckBox(self, text="Compressor", command=self.checkbox_event_compressor, variable=self.check_var_compressor, onvalue=1, offvalue=0)
        self.compressor_checkbox.place(relx=0.45, rely=0.25, anchor=CENTER)
        # Compressor sliders
        self.compressor_threshold_slider = customtkinter.CTkSlider(master=self, from_=-50, to=50, command=self.compressor_slider_event, orientation='vertical')
        self.compressor_threshold_slider.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.compressor_ratio_slider = customtkinter.CTkSlider(master=self, from_=1, to=10, command=self.compressor_slider_event, orientation='vertical')
        self.compressor_ratio_slider.place(relx=0.45, rely=0.5, anchor=CENTER)
        self.compressor_attack_slider = customtkinter.CTkSlider(master=self, from_=1, to=30, command=self.compressor_slider_event, orientation='vertical')
        self.compressor_attack_slider.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Delay
        self.delay_checkbox = customtkinter.CTkCheckBox(self, text="Delay", command=self.checkbox_event_delay, variable=self.check_var_delay, onvalue="on", offvalue="off")
        self.delay_checkbox.place(relx=0.62, rely=0.25, anchor=CENTER)
        # Delay sliders
        self.delay_ms_slider = customtkinter.CTkSlider(master=self, from_=100, to=2500, command=self.delay_slider_event, orientation='vertical')
        self.delay_ms_slider.place(relx=0.58, rely=0.5, anchor=CENTER)
        self.delay_feedback_slider = customtkinter.CTkSlider(master=self, from_=0, to=1, command=self.delay_slider_event, orientation='vertical')
        self.delay_feedback_slider.place(relx=0.63, rely=0.5, anchor=CENTER)

        # Pitch Shift
        self.pitch_shift_checkbox = customtkinter.CTkCheckBox(self, text="Pitch Shift", command=self.checkbox_event_pitch, variable=self.check_var_pitch, onvalue="on", offvalue="off")
        self.pitch_shift_checkbox.place(relx=0.75, rely=0.25, anchor=CENTER)
        self.pitch_shift_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.pitch_shift_slider_event, orientation='vertical')
        self.pitch_shift_slider.place(relx=0.75, rely=0.5, anchor=CENTER)

        # Increse signal amplitude
        self.vol_boost_checkbox = customtkinter.CTkCheckBox(self, text="Volume Boost", command=self.checkbox_event_volboost, variable=self.check_var_volboost, onvalue="on", offvalue="off")
        self.vol_boost_checkbox.place(relx=0.87, rely=0.25, anchor=CENTER)
        self.vol_boost_slider = customtkinter.CTkSlider(master=self, from_=0, to=4000, command=self.vol_boost_slider_event, orientation='vertical')
        self.vol_boost_slider.place(relx=0.87, rely=0.5, anchor=CENTER)

        # Input file path str
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Insert .wav audio file path")
        self.entry.place(relx=0.4, rely=0.1, anchor=CENTER)
        # Input set path button
        self.button_set_path = customtkinter.CTkButton(self, text="Set Path", command=self.button_event_set_path)
        self.button_set_path.place(relx=0.6, rely=0.1, anchor=CENTER)

        # Process file
        self.button_fechar = customtkinter.CTkButton(self, text="Process Effects!", command=self.button_event_processar)
        self.button_fechar.place(relx=0.5, rely=0.8, anchor=CENTER)

        # Progress Bar
        self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal", mode='determinate', determinate_speed=2)
        self.progressbar.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.progressbar.set(0)


    def button_event_set_path(self):
        self.effects.set_file_path(self.entry.get())
        self.initial_modification_time = os.path.getmtime("output/output_audio.wav")

    def checkbox_event_equalizer(self):
       pass

    def checkbox_event_distortion(self):
        pass

    def checkbox_event_compressor(self):
        pass

    def checkbox_event_volboost(self):
        pass

    def checkbox_event_delay(self):
        pass

    def checkbox_event_pitch(self):
        pass

    def equalizer_slider_event(self, value):
        pass

    def distortion_slider_event(self, value):
        pass

    def compressor_slider_event(self, value):
        pass

    def delay_slider_event(self, value):
        pass

    def pitch_shift_slider_event(self, value):
        pass

    def vol_boost_slider_event(self, value):
        pass

    def button_event_processar(self):
        # Starting progress bar
        self.progressbar.start()

        # Applying all parameters from the sliders and saving it
        if(self.equalizer_checkbox.get() == 1):
            self.params['eq_low'] = self.equalizer_low_slider.get()
            self.params['eq_med'] = self.equalizer_med_slider.get()
            self.params['eq_high'] = self.equalizer_high_slider.get()

            self.effects.apply_equalizer(self.params['eq_low'], self.params['eq_med'], self.params['eq_high'])

        if(self.compressor_checkbox.get() == 1):
            self.params['comp_threshold'] = self.compressor_threshold_slider.get()
            self.params['comp_ratio'] = self.compressor_ratio_slider.get()
            self.params['comp_attack'] = self.compressor_attack_slider.get()

            self.effects.apply_compressor(self.params['comp_threshold'], self.params['comp_ratio'], self.params['comp_attack'])

        if(self.distortion_checkbox.get() == 1):
            self.params['dist_gain'] = float(self.distortion_slider.get())

            self.effects.apply_distortion(self.params['dist_gain'])

        if(self.delay_checkbox.get() == 1):
            self.params['delay_ms'] = self.delay_ms_slider.get()
            self.params['delay_feedback'] = self.delay_feedback_slider.get()

            self.effects.apply_delay(self.params['delay_ms'], self.params['delay_feedback'])

        if(self.pitch_shift_checkbox.get() == 1):
            self.params['ps_factor'] = self.pitch_shift_slider.get()

            self.effects.apply_pitch_shift(self.params['ps_factor'])

        processed = self.effects.save_audio()

        if(processed):
            # Checking if the file was completely processed...
            current_modification_time = os.path.getmtime("output/output_audio.wav")
            if(current_modification_time > self.initial_modification_time):
                print("File processed!")
                self.progressbar.stop()

app = App()
app.mainloop()