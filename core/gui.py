import customtkinter as ctk
import tkinter as tk
from persistent_data_manager import *
import PIL.Image, PIL.ImageTk
from subprocess_handler import *
# Global Variable Declarations

instaloader_preferences = {
    "Target": [],  # List of targets: usernames, hashtags, post URLs, etc.

    "Login Options": {
        "--login": "",             # Username for logging in
        "--password": "",          # Plaintext password (not recommended)
        "--sessionfile": "",       # Path to session file
        "--load-cookies": "",      # Browser name or path
        "--no-cookies": False,
        "--login-captcha": False,
    },

    "Filters": {
        "--comments": False,
        "--geotags": False,
        "--stories": False,
        "--highlights": False,
        "--tagged": False,
        "--reels": False,
        "--igtv": False,
        "--no-posts": False,
        "--no-videos": False,
        "--no-video-thumbnails": False,
        "--post-filter": "",       # Python expression filter
        "--storyitem-filter": "",  # Python expression filter
        "--slide": "",             # e.g. "1", "last", "1-3"
        "--count": 1,              # integer limit for hashtags/feeds
        "--location": "",          # NEW: Instagram location ID as string
    },

    "Save Options": {
        "--dirname-pattern": "",
        "--filename-pattern": "",
        "--title-pattern": "",
        "--save-metadata": False,
        "--post-metadata-txt": "",
        "--storyitem-metadata-txt": "",
        "--sanitize-paths": False,
        "--no-profile-pic": False,
        "--include-profile-metadata": False,
        "--profile-pic-only": False,
    },

    "Update Control": {
        "--fast-update": False,
        "--latest-stamps": False,
        "--resume-prefix": "",
    },

    "Output Control": {
        "--quiet": False,
        "--no-captions": False,
        "--no-metadata-json": False,
        "--no-compress-json": False,
    },

    "Network": {
        "--user-agent": "",
        "--request-timeout": 300,       # seconds
        "--max-connection-attempts": 3, # default
        "--abort-on": "",               # e.g. "429,404"
    },

    "Advanced": {
        "--rich-metadata": False,
    }
}

ghunter_preferences = {}
dorking_preferences = {}
sherlock_preferences = {}



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x200")

def clear_gui(master):
    for widget in master.winfo_children():
        widget.destroy()

def load_gui():    
    app.title("Initializing")
    label = ctk.CTkLabel(app, text="Loading OSINT Tool", font=("Calibri", 20))
    label.pack(pady=20)
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def start_gui():
    clear_gui(app)
    app.title("Home")
    app.geometry("900x600")

    tabview = ctk.CTkTabview(master=app, width=880, height=580, corner_radius=10)
    tabview.pack(padx=10, pady=10)

    tabview.add("Home")
    tabview.add("Dorking")
    tabview.add("Ghunter")
    tabview.add("Instaloader") 
    tabview.add("Sherlock")

    tabview.set("Home")
    
    def tab_change():
        selected_tab = tabview.get()
        if selected_tab == "Instaloader":
            clear_gui(tabview.tab("Instaloader")) 
            Instaloader(tabview.tab("Instaloader"), instaloader_preferences)

    tabview.configure(command=tab_change)

    Home(tabview.tab("Home"))
    Instaloader(tabview.tab("Instaloader"), instaloader_preferences)

def Home(master):
    ctk.CTkLabel(master, text="Home", font=("Calibri", 50)).pack(pady=10)

    scroll = ctk.CTkScrollableFrame(master, width=880, height=580, corner_radius=10, fg_color="#282929")
    scroll.pack(padx=10, pady=10, fill="both", expand=True)

    # Container for left and right
    container = ctk.CTkFrame(scroll, fg_color="#282929", width=880, height=500)
    container.pack(pady=10, fill="both", expand=True)
    
    # Left Frame
    frameL = ctk.CTkScrollableFrame(container, width=400, height=500, label_text="Inputs")
    frameL.pack(side="left", padx=10, pady=5)

    frameR = ctk.CTkScrollableFrame(container, width=400, height=500, label_text="Results")
    frameR.pack(side="right", padx=10, pady=5)
    
    inst_enable = ctk.CTkSwitch(frameL, text="Enable Instaloader", width=380, height=30, corner_radius=10)
    inst_enable.pack(pady=5)

    ctk.CTkButton(frameL, text="Execute Enabled Programs", width=380, height=30, corner_radius=10, command=lambda: (execute(inst_enable, frameR))).pack(pady=5)

    # Bottom Frame
    frameBottom = ctk.CTkFrame(scroll, width=880, height=200, corner_radius=10, fg_color="#393939")
    frameBottom.pack(padx=10, pady=10, fill="x")
    frameBottom.pack_propagate(True)

    # Bottom Frame Title
    refresh_image = ctk.CTkImage(light_image=PIL.Image.open("core/assets/refresh-cw.png"), dark_image=PIL.Image.open("core/assets/refresh-cw.png"))
    subframe = ctk.CTkFrame(frameBottom, fg_color="transparent")
    subframe.pack(fill="x", pady=5, padx=10)
    ctk.CTkLabel(subframe, text="Save Settings", font=("Calibri", 25)).pack(pady=(5, 0))
    ctk.CTkButton(subframe, text="",image=refresh_image, width=20, height=20, command=lambda:(clear_gui(master), Home(master))).pack(side="right", padx=5)

    # Create a subframe for "Save To"
    save_to_frame = ctk.CTkFrame(frameBottom, fg_color="transparent")
    save_to_frame.pack(fill="x", pady=5, padx=10)

    ctk.CTkLabel(save_to_frame, text="Save Settings To: ", font=("Calibri", 16)).pack(side="left", padx=5)
    save_to = ctk.CTkOptionMenu(save_to_frame, values=pdm_list_avalible_files(), width=150)
    btn1 = ctk.CTkButton(save_to_frame, text="Save", command=lambda: pref_save_to(save_to, btn1))
    btn1.pack(side="right", padx=5)
    save_to.pack(side="right", padx=5)

    # Create a subframe for "Save As"
    save_as_frame = ctk.CTkFrame(frameBottom, fg_color="transparent")
    save_as_frame.pack(fill="x", pady=5, padx=10)

    ctk.CTkLabel(save_as_frame, text="Save Settings As: ", font=("Calibri", 16)).pack(side="left", padx=5)
    save_as = ctk.CTkEntry(save_as_frame, width=150)
    btn2 = ctk.CTkButton(save_as_frame, text="Save", command=lambda: pref_save_as(save_as, btn2))
    btn2.pack(side="right", padx=5)
    save_as.pack(side="right", padx=5)    

    load_frame = ctk.CTkFrame(frameBottom, fg_color="transparent")
    load_frame.pack(fill="x", pady=5, padx=10)

    ctk.CTkLabel(load_frame, text="Load Settings From File: ", font=("Calibri", 16)).pack(side="left", padx=5)
    load = ctk.CTkOptionMenu(load_frame, values=pdm_list_avalible_files(), width=150)
    btn3 = ctk.CTkButton(load_frame, text="Load", command=lambda: pref_load(load, btn3))
    btn3.pack(side="right", padx=5)
    load.pack(side="right", padx=5)



    

def Instaloader(parent, preferences):
    # Clear existing widgets (optional)
    clear_gui(parent)

    ctk.CTkLabel(parent, text="Instaloader", font=("Calibri", 50)).pack(pady=10)

    master = ctk.CTkScrollableFrame(parent, width=880, height=580, corner_radius=10, fg_color="#282929")
    master.pack(padx=10, pady=10)

    for section, prefs in preferences.items():
        # Section Header Label
        section_label = ctk.CTkLabel(master, text=section, font=("Calibri", 24, "bold"))
        section_label.pack(anchor="w", pady=(15, 5), padx=10)

        # Special case: 'target' is not a dict, it's a list of usernames
        if section == "Target" and isinstance(prefs, list):
            row_frame = ctk.CTkFrame(master)
            row_frame.pack(fill="x", padx=10, pady=3)

            label = ctk.CTkLabel(row_frame, text="Target usernames", width=200, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(row_frame)
            # Insert joined usernames or empty string if list is empty
            entry.insert(0, ", ".join(prefs) if prefs else "")
            entry.pack(side="right", fill="x", expand=True, padx=5)

        # Normal flag:value pairs
        elif isinstance(prefs, dict):
            for flag, value in prefs.items():
                row_frame = ctk.CTkFrame(master)
                row_frame.pack(fill="x", padx=10, pady=3)

                # Clean up flag name for UI
                label_text = flag.lstrip("-").replace("-", " ").capitalize()
                label = ctk.CTkLabel(row_frame, text=label_text, width=200, anchor="w")
                label.pack(side="left", padx=5)

                if isinstance(value, bool):
                    var = tk.BooleanVar(value=value)
                    toggle = ctk.CTkSwitch(row_frame, text="", variable=var, onvalue=True, offvalue=False)
                    toggle.pack(side="right", padx=5)

                elif isinstance(value, str) and value.strip().isdigit():
                    entry = ctk.CTkEntry(row_frame, width=100)
                    entry.insert(0, str(value))
                    entry.pack(side="right", fill="x", expand=False, padx=5)

                else:
                    entry = ctk.CTkEntry(row_frame)
                    entry.insert(0, str(value))
                    entry.pack(side="right", fill="x", expand=True, padx=5)

    # Save Preferences Button
    save_button = ctk.CTkButton(
        master, 
        text="Save Preferences", 
        command=lambda: get_instaloader_preferences(master, preferences)
    )
    save_button.pack(pady=10)


def get_instaloader_preferences(parent, preferences):
    current_section = None

    for widget in parent.winfo_children():

        if isinstance(widget, ctk.CTkLabel) and widget.cget("font")[1] == 24:
            current_section = widget.cget("text")
            continue

        if isinstance(widget, ctk.CTkFrame):
            label_widget = widget.winfo_children()[0]
            input_widget = widget.winfo_children()[-1]

            flag_label = label_widget.cget("text").lower().replace(" ", "-")
            flag_key = f"--{flag_label}"  # match original flag style

            # Handle Target section (which is a list)
            if isinstance(preferences[current_section], list):
                # For the target entry, split by comma and strip whitespace
                new_list = [x.strip() for x in input_widget.get().split(",") if x.strip()]
                preferences[current_section].clear()
                preferences[current_section].extend(new_list)
            else:
                if isinstance(input_widget, ctk.CTkSwitch):
                    preferences[current_section][flag_key] = input_widget.get()
                elif isinstance(input_widget, ctk.CTkEntry):
                    preferences[current_section][flag_key] = input_widget.get()

    print(preferences)


def pref_save_as(save_as, btn):
    btn.configure(state="disabled")
    while not pdm_save_user_data_to_file(save_as.get(), instaloader_preferences, ghunter_preferences, sherlock_preferences, dorking_preferences):
        pass
    btn.configure(text="Saved!", fg_color="green")
    save_as.delete(0, tk.END)
    app.after(2000, lambda: (btn.configure(state="normal"), btn.configure(text="Save", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])))

def pref_save_to(save_to, btn):
    while not pdm_save_user_data_to_file(save_to.get(), instaloader_preferences, ghunter_preferences, sherlock_preferences, dorking_preferences):
        pass
    btn.configure(text="Saved!", fg_color="green", hover_color="green")
    app.after(2000, lambda: (btn.configure(state="normal"), btn.configure(text="Save", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"])))
    
def pref_load(load_from, btn):
    btn.configure(state="disabled")
    while not (data := pdm_load_user_data_from_files(load_from.get())):
        pass
    
    global instaloader_preferences
    instaloader_preferences = data["instaloader"]
    global ghunter_preferences
    ghunter_preferences = data["ghunter"]
    global sherlock_preferences
    sherlock_preferences = data["sherlock"]
    global dorking_preferences
    dorking_preferences = data["dorking"]


    btn.configure(text="Loaded!", fg_color="green")
    app.after(2000, lambda: (btn.configure(state="normal"), btn.configure(text="Load", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])))

def execute(inst, output_frame=None):
    if inst:
        try:
            cmd_list = SH_parse_instaloader(instaloader_preferences)
            print("Command:", cmd_list)
            SH_execute_stream(cmd_list, output_frame=output_frame, cwd="output/instaloader")
        except CommandOutput as e:
            print(f"[!] Failed (code {e.returncode}):")
            print(f"STDERR:\n{e.stderr}")
            print(f"STDOUT:\n{e.stdout}")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")













def init():
    load_gui()
    app.after(1000, start_gui)
    app.mainloop()

if __name__ == "__main__":
    init()
