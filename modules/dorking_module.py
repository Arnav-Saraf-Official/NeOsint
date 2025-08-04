import subprocess

def generate_google_dork(user_data):
    prompt = f"Generate Google Dorks to find data about this topic/person. The data is attached below. Only repond with dorking query"
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma", f"{prompt}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error generating dork: {e}"

def run(user_data):
    dork = generate_google_dork(user_data)
    print("[+] Dork Generated:\n", dork)
