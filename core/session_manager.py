import os
import customtkinter as ctk
from datetime import datetime

def SM_get_available_sessions():
    path = "output"
    sessions = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    return sessions

def SM_create_session(current_session_indicator, session_button, app, session_name_entry):
    path = "output"
    if session_name_entry.get() == "":
        session_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    else:
        session_name = session_name_entry.get()
    try:
        os.makedirs(os.path.join(path, session_name), exist_ok=False)
        os.makedirs(os.path.join(path, session_name, "Instaloader"), exist_ok=False)
        os.makedirs(os.path.join(path, session_name, "Ghunt"), exist_ok=False)
        os.makedirs(os.path.join(path, session_name, "Dorking"), exist_ok=False)
        os.makedirs(os.path.join(path, session_name, "Sherlock"), exist_ok=False)

        current_session_indicator.configure(text=session_name)
        
        session_button.configure(text="Created!", fg_color="green", hover_color="green", text_color="white", state="disabled")
        app.after(2000, lambda: (session_button.configure(state="normal", text="Create", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"], text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"])))


    except FileExistsError:
        raise FileExistsError

    return session_name

def SM_load_session(current_session_indicator, session_button, app, session_name):
    
    current_session_indicator.configure(text=session_name)
        
    session_button.configure(text="Loaded!", fg_color="green", hover_color="green", text_color="white", state="disabled")
    app.after(2000, lambda: (session_button.configure(state="normal", text="Load", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"], text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"])))

    return session_name
