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
        self.equalizer_checkbox.place(relx=0.3, rely=0.35, anchor=CENTER)
        # Equalizer sliders
        self.equalizer_low_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event, orientation='vertical')
        self.equalizer_low_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.equalizer_med_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.equalizer_med_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.equalizer_high_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.equalizer_slider_event)
        self.equalizer_high_slider.place(relx=0.5, rely=0.5, anchor=S)

        # Distortion
        self.distortion_checkbox = customtkinter.CTkCheckBox(self, text="Distortion", command=self.checkbox_event_distortion, variable=self.check_var_distortion, onvalue="on", offvalue="off")
        self.distortion_checkbox.place(relx=0.3, rely=0.25, anchor=CENTER)
        self.distortion_slider = customtkinter.CTkSlider(master=self, from_=1, to=100, command=self.distortion_slider_event)
        self.distortion_slider.place(relx=0.1, rely=0.1, anchor=S)

        # Compressor
        self.compressor_checkbox = customtkinter.CTkCheckBox(self, text="Compressor", command=self.checkbox_event_compressor, variable=self.check_var_compressor, onvalue=1, offvalue=0)
        self.compressor_checkbox.place(relx=0.3, rely=0.15, anchor=CENTER)
        # Compressor sliders
        self.compressor_threshold_slider = customtkinter.CTkSlider(master=self, from_=-50, to=50, command=self.compressor_slider_event)
        self.compressor_threshold_slider.place(relx=0.5, rely=0.5, anchor=S)
        self.compressor_ratio_slider = customtkinter.CTkSlider(master=self, from_=1, to=10, command=self.compressor_slider_event)
        self.compressor_ratio_slider.place(relx=0.5, rely=0.6, anchor=S)
        self.compressor_attack_slider = customtkinter.CTkSlider(master=self, from_=1, to=30, command=self.compressor_slider_event)
        self.compressor_attack_slider.place(relx=0.5, rely=0.7, anchor=S)

        # Increse signal amplitude
        self.vol_boost_checkbox = customtkinter.CTkCheckBox(self, text="Volume Boost", command=self.checkbox_event_volboost, variable=self.check_var_volboost, onvalue="on", offvalue="off")
        self.vol_boost_checkbox.place(relx=0.705, rely=0.35, anchor=CENTER)
        self.vol_boost_slider = customtkinter.CTkSlider(master=self, from_=0, to=4000, command=self.vol_boost_slider_event)
        self.vol_boost_slider.place(relx=0.5, rely=0.5, anchor=S)

        # Delay
        self.delay_checkbox = customtkinter.CTkCheckBox(self, text="Delay", command=self.checkbox_event_delay, variable=self.check_var_delay, onvalue="on", offvalue="off")
        self.delay_checkbox.place(relx=0.7, rely=0.25, anchor=CENTER)
        # Delay sliders
        self.delay_ms_slider = customtkinter.CTkSlider(master=self, from_=100, to=2500, command=self.delay_slider_event)
        self.delay_ms_slider.place(relx=0.6, rely=0.6, anchor=S)
        self.delay_feedback_slider = customtkinter.CTkSlider(master=self, from_=0, to=1, command=self.delay_slider_event)
        self.delay_feedback_slider.place(relx=0.6, rely=0.6, anchor=S)

        # Pitch Shift
        self.pitch_shift_checkbox = customtkinter.CTkCheckBox(self, text="Pitch Shift", command=self.checkbox_event_pitch, variable=self.check_var_pitch, onvalue="on", offvalue="off")
        self.pitch_shift_checkbox.place(relx=0.7, rely=0.15, anchor=CENTER)
        self.pitch_shift_slider = customtkinter.CTkSlider(master=self, from_=0, to=5, command=self.pitch_shift_slider_event)
        self.pitch_shift_slider.place(relx=0.9, rely=0.9, anchor=S)

        # Input file path str
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Insert .wav audio file path")
        self.entry.place(relx=0.9, rely=0.5, anchor=CENTER)

        # Process file
        self.button_fechar = customtkinter.CTkButton(self, text="Process Effects!", command=self.button_event_processar)
        self.button_fechar.place(relx=0.7, rely=0.8, anchor=CENTER)

    def button_event_escolher_arq(self):
        self.effects.set_file_path(self.entry.get())

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

    def equalizer_slider_event(self):
        pass

    def distortion_slider_event(self):
        pass

    def compressor_slider_event(self):
        pass

    def delay_slider_event(self):
        pass

    def pitch_shift_slider_event(self):
        pass

    def vol_boost_slider_event(self):
        pass

    def button_event_processar(self):
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

        self.effects.save_audio()

app = App()
app.mainloop()