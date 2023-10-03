from tkinter import *
import customtkinter


def button_event():
    print("button pressed")

app = customtkinter.CTk()
app.title("Modificador de Audio")
app.geometry("600x350")

def slider_event(value):
    print(value)

slider = customtkinter.CTkSlider(master=app, from_=0, to=100, command=slider_event)
slider.place(relx=0.5, rely=0.5, anchor=S)

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

check_var_equalizer = customtkinter.StringVar(value="on")
check_var_distortion = customtkinter.StringVar(value="on")
check_var_compressor = customtkinter.IntVar(value=1)
check_var_volboost = customtkinter.StringVar(value="on")
check_var_LowPass = customtkinter.StringVar(value="on")
check_var_pitch = customtkinter.StringVar(value="on")

equalizer_checkbox = customtkinter.CTkCheckBox(app, text="Equalizador", command=checkbox_event_equalizer,
                                     variable=check_var_equalizer, onvalue="on", offvalue="off")
equalizer_checkbox.place(relx=0.3, rely=0.35, anchor=CENTER)

distortion_checkbox = customtkinter.CTkCheckBox(app, text="Distorcao", command=checkbox_event_distortion,
                                     variable=check_var_distortion, onvalue="on", offvalue="off")
distortion_checkbox.place(relx=0.3, rely=0.25, anchor=CENTER)

compressor_checkbox = customtkinter.CTkCheckBox(app, text="Compressor", command=checkbox_event_compressor,
                                     variable=check_var_compressor, onvalue=1, offvalue=0)
compressor_checkbox.place(relx=0.3, rely=0.15, anchor=CENTER)

vol_boost_checkbox = customtkinter.CTkCheckBox(app, text="Volume Boost", command=checkbox_event_volboost,
                                     variable=check_var_volboost, onvalue="on", offvalue="off")
vol_boost_checkbox.place(relx=0.705, rely=0.35, anchor=CENTER)

low_pass_checkbox = customtkinter.CTkCheckBox(app, text="Low pass", command=checkbox_event_LowPass,
                                     variable=check_var_LowPass, onvalue="on", offvalue="off")
low_pass_checkbox.place(relx=0.7, rely=0.25, anchor=CENTER)

pitch_shift_checkbox = customtkinter.CTkCheckBox(app, text="Pitch Shift", command=checkbox_event_pitch,
                                     variable=check_var_pitch, onvalue="on", offvalue="off")
pitch_shift_checkbox.place(relx=0.7, rely=0.15, anchor=CENTER)

button_abrir = customtkinter.CTkButton(app, text="Escolher Arquivo", command=button_event)
button_abrir.place(relx=0.3, rely=0.8, anchor=CENTER)
button_fechar = customtkinter.CTkButton(app, text="Processar", command=button_event)
button_fechar.place(relx=0.7, rely=0.8, anchor=CENTER)

app.mainloop()