import subprocess
from tkinter import messagebox
def ghunt_login(cwd):

    messagebox.showinfo("Ghunt Companion Limitations for Google", """
                        Due to recent changes in google extention policy, Ghunt Companion, the tool used to authenticate to ghunt,
                        has been removed from the chrome web store. You will need to use a different method of authentication, (3 or 4)

                        For instructions on how, read the Ghunt section of the readme.
""")
    subprocess.run(["ghunt", "login"], cwd=cwd, creationflags=subprocess.CREATE_NEW_CONSOLE)
