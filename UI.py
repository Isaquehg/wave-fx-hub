from tkinter import *
import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modificador de Audio")
        self.geometry("600x350")

        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, command=self.slider_event)
        self.slider.place(relx=0.5, rely=0.5, anchor=S)

        self.check_var_equalizer = customtkinter.StringVar(value="on")
        self.check_var_distortion = customtkinter.StringVar(value="on")
        self.check_var_compressor = customtkinter.IntVar(value=1)
        self.check_var_volboost = customtkinter.StringVar(value="on")
        self.check_var_LowPass = customtkinter.StringVar(value="on")
        self.check_var_pitch = customtkinter.StringVar(value="on")

        self.equalizer_checkbox = customtkinter.CTkCheckBox(self, text="Equalizador", command=self.checkbox_event_equalizer,
                                     variable=self.check_var_equalizer, onvalue="on", offvalue="off")
        self.equalizer_checkbox.place(relx=0.3, rely=0.35, anchor=CENTER)

        self.distortion_checkbox = customtkinter.CTkCheckBox(self, text="Distorcao", command=self.checkbox_event_distortion,
                                     variable=self.check_var_distortion, onvalue="on", offvalue="off")
        self.distortion_checkbox.place(relx=0.3, rely=0.25, anchor=CENTER)

        self.compressor_checkbox = customtkinter.CTkCheckBox(self, text="Compressor", command=self.checkbox_event_compressor,
                                     variable=self.check_var_compressor, onvalue=1, offvalue=0)
        self.compressor_checkbox.place(relx=0.3, rely=0.15, anchor=CENTER)

        self.vol_boost_checkbox = customtkinter.CTkCheckBox(self, text="Volume Boost", command=self.checkbox_event_volboost,
                                     variable=self.check_var_volboost, onvalue="on", offvalue="off")
        self.vol_boost_checkbox.place(relx=0.705, rely=0.35, anchor=CENTER)

        self.low_pass_checkbox = customtkinter.CTkCheckBox(self, text="Low pass", command=self.checkbox_event_LowPass,
                                     variable=self.check_var_LowPass, onvalue="on", offvalue="off")
        self.low_pass_checkbox.place(relx=0.7, rely=0.25, anchor=CENTER)

        self.pitch_shift_checkbox = customtkinter.CTkCheckBox(self, text="Pitch Shift", command=self.checkbox_event_pitch,
                                     variable=self.check_var_pitch, onvalue="on", offvalue="off")
        self.pitch_shift_checkbox.place(relx=0.7, rely=0.15, anchor=CENTER)

        self.button_abrir = customtkinter.CTkButton(self, text="Escolher Arquivo", command=self.button_event)
        self.button_abrir.place(relx=0.3, rely=0.8, anchor=CENTER)
        self.button_fechar = customtkinter.CTkButton(self, text="Processar", command=self.button_event)
        self.button_fechar.place(relx=0.7, rely=0.8, anchor=CENTER)

    def slider_event(value):
        print(value)

    def button_event():
        print("button pressed")

    def checkbox_event_equalizer():
        print("checkbox toggled, current value:", check_var_equalizer.get())
    
    def checkbox_event_distortion():
        print("checkbox distortion toggled, current value:", check_var_distortion.get())

    def checkbox_event_compressor():
        print("checkbox compressor toggled, current value:", check_var_compressor.get())

    def checkbox_event_volboost():
        print("checkbox vol boost toggled, current value:", check_var_volboost.get())

    def checkbox_event_LowPass():
        print("checkbox low pass toggled, current value:", check_var_LowPass.get())

    def checkbox_event_pitch():
        print("checkbox pitch toggled, current value:", check_var_pitch.get())

app = App()
app.mainloop()