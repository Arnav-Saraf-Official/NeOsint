import subprocess
import threading
import customtkinter as ctk

class CommandOutput(Exception):
    def __init__(self, output, stderr, stdout, returncode):
        super().__init__("Command output data")
        self.output = output
        self.stderr = stderr
        self.stdout = stdout
        self.returncode = returncode

def SH_parse_instaloader(data):
    command = ["instaloader"]
    targets = []

    for section, options in data.items():
        if isinstance(options, dict):
            for key, value in options.items():
                if key == "target":
                    if isinstance(value, str):
                        targets.extend(t.strip() for t in value.split(",") if t.strip())
                    elif isinstance(value, list):
                        targets.extend(t.strip() for t in value if isinstance(t, str) and t.strip())
                else:
                    if isinstance(value, bool):
                        if value:
                            command.append(f"{key}")
                    elif isinstance(value, (int, float)):
                        if value != 0:
                            command.append(f"{key}")
                            command.append(str(value))
                    elif isinstance(value, str):
                        stripped = value.strip()
                        if stripped:
                            command.append(f"{key}")
                            command.append(stripped)
        elif isinstance(options, list):
            targets.extend([t.strip() for t in options if isinstance(t, str) and t.strip()])

    command.extend(targets)
    return command


def SH_execute_stream(command_list, output_frame=None, cwd=None):
    warning_keywords = [
        "unable to fetch",
        "skipping",
        "retrying",
        "deprecated",
        "warning",
        "slow down",
        "rate limited",
        "could not retrieve",
        "not found",
        "temporarily unavailable",
        "connection reset",
        "timed out",
        "ssl certificate",
        "incomplete",
        "partial",
        "using cached",
        "falling back",
        "ignored",
        "redirected",
        "unauthorized",
        "notice",
        "failed attempt",
        "retry after",
    ]

    error_keywords = [
        "error",
        "failed",
        "exception",
        "traceback",
        "fatal",
        "cannot",
        "denied",
        "unreachable",
        "connection refused",
        "invalid",
        "corrupt",
        "no such file",
        "permission denied",
        "segmentation fault",
        "out of memory",
        "crashed",
        "not recognized",
        "broken pipe",
        "unhandled",
        "panic",
        "assertion failed",
    ]

    def run_and_stream():
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1, 
            cwd=cwd
        )

        def append_label(text, color):
            if output_frame:
                label = ctk.CTkLabel(
                    output_frame,
                    text=text,
                    text_color=color,
                    anchor="w",
                    justify="left",
                    font=("Consolas", 12),
                    wraplength=600
                )
                label.pack(fill="x", padx=5, pady=1, anchor="w")
                output_frame.update_idletasks()
                # Scroll to bottom
                output_frame._canvas.yview_moveto(1)
            else:
                print(text)

        def classify_line(line):
            lower_line = line.lower()
            for kw in error_keywords:
                if kw in lower_line:
                    return "red"
            for kw in warning_keywords:
                if kw in lower_line:
                    return "yellow"
            return "white"

        def stream(pipe):
            for line in iter(pipe.readline, ''):
                clean_line = line.strip().strip('"')
                if clean_line:
                    color = classify_line(clean_line)
                    append_label(clean_line, color)
            pipe.close()

        # Run stdout and stderr in separate threads
        stdout_thread = threading.Thread(target=stream, args=(process.stdout,))
        stderr_thread = threading.Thread(target=stream, args=(process.stderr,))

        stdout_thread.start()
        stderr_thread.start()
        stdout_thread.join()
        stderr_thread.join()
        process.wait()

        if process.returncode != 0:
            raise CommandOutput(
                output=" ".join(command_list),
                stdout="See GUI output",
                stderr="See GUI output",
                returncode=process.returncode
            )

    thread = threading.Thread(target=run_and_stream)
    thread.start()
