import pickle
import os
def pdm_save_user_data_to_file(filename, instaloader, ghunter, sherlock, dorking):
    os.makedirs(os.path.join("core", "user", filename), exist_ok=True)
    
    filepath = os.path.join("core", "user", filename, "instaloader.pkl")
    with open(filepath, "wb") as file:
        pickle.dump(instaloader, file)

    filepath = os.path.join("core", "user", filename, "ghunter.pkl")
    with open(filepath, "wb") as file:
        pickle.dump(ghunter, file)
    
    filepath = os.path.join("core", "user", filename, "sherlock.pkl")
    with open(filepath, "wb") as file:
        pickle.dump(sherlock, file)

    filepath = os.path.join("core", "user", filename, "dorking.pkl")
    with open(filepath, "wb") as file:
        pickle.dump(dorking, file)

    return True
def pdm_load_user_data_from_files(directory):
    data = {}

    file_names = {
        "instaloader": "instaloader.pkl",
        "ghunter": "ghunter.pkl",
        "sherlock": "sherlock.pkl",
        "dorking": "dorking.pkl",
    }

    for key, filename in file_names.items():
        filepath = os.path.join("core", "user", directory, filename)
        try:
            with open(filepath, "rb") as file:
                data[key] = pickle.load(file)
        except FileNotFoundError:
            return "FILE_NOT_FOUND"

    return data

def pdm_list_avalible_files():
    all = os.listdir("core\\user")
    if ".gitkeep" in all:
        all.remove(".gitkeep")

    return all
