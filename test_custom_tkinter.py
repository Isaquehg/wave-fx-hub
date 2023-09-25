import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1080x720")
app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
app.grid_rowconfigure(0, weight=1) # Header and Title
app.grid_rowconfigure(1, weight=5) # Pedal buttons
app.grid_rowconfigure(2, weight=1) # Footer and pedal names

def button_function():
    print("button pressed")
def compressor_event():
    print("Compressor activated!")

app.title_label = customtkinter.CTkLabel(master=app, width=500, height=30, text_font=('Arial', 13))
app.title_label.grid(row=0, column=1, columnspan=4, padx=(5, 5), pady=(20, 0), sticky="nsew")

# Creating Effects Buttons
compressor_button = customtkinter.CTkButton(master=app, text='Compressor', fg_color=("black", "lightgray"), command = compressor_event)
compressor_button.grid(row=1, column=0, padx=(10, 10), pady=(0, 0), sticky="nsew")

equalizer_button = customtkinter.CTkButton(master=app, text='Equalizer')
equalizer_button.grid(row=1, column=1, padx=(10, 10), pady=(0, 0), sticky="nsew")

vol_boost_button = customtkinter.CTkButton(master=app, text='Volume Boost')
vol_boost_button.grid(row=1, column=2, padx=(10, 10), pady=(0, 0), sticky="nsew")

pitch_shift_button = customtkinter.CTkButton(master=app, text='Pitch Shift')
pitch_shift_button.grid(row=1, column=3, padx=(10, 10), pady=(0, 0), sticky="nsew")

low_pass_button = customtkinter.CTkButton(master=app, text='Low Pass Filter')
low_pass_button.grid(row=1, column=4, padx=(10, 10), pady=(5, 5), sticky="nsew")

distortion_button = customtkinter.CTkButton(master=app, text='Distortion')
distortion_button.grid(row=1, column=5, padx=(10, 10), pady=(5, 5), sticky="nsew")


app.mainloop()