import tkinter as tk
import random
import os
from tkinter import messagebox


def load_jokes():
    """Load jokes from randomjokes.txt located in the same or resources folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(base_dir, "randomjokes.txt"),
        os.path.join(base_dir, "resources", "randomjokes.txt")
    ]

    jokes = []
    file_found = None
    for path in possible_paths:
        if os.path.exists(path):
            file_found = path
            break

    if file_found:
        with open(file_found, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "?" in line and len(line) > 3:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup.strip() + "?", punchline.strip()))
    else:
        jokes = [("File not found!", "Make sure randomJokes.txt exists in this folder or in 'resources'.")]
    return jokes


class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" Alexa Tell Me a Joke")
        self.root.geometry("600x420")
        self.root.config(bg="#F6F8FA")
        self.root.eval('tk::PlaceWindow . center')

        # Shadow background frame
        self.shadow_frame = tk.Frame(self.root, bg="#D1D9E6", bd=5)
        self.shadow_frame.place(relx=0.5, rely=0.5, anchor="center", width=560, height=380)

        # Main frame
        self.main_frame = tk.Frame(self.shadow_frame, bg="#FFFFFF", bd=2, relief="ridge")
        self.main_frame.pack(expand=True, fill="both")

        self.jokes = load_jokes()
        self.current_joke = None

        # Title
        self.title_label = tk.Label(
            self.main_frame, text="Alexa, Tell Me a Joke! ",
            font=("Comic Sans MS", 20, "bold"), bg="#FFFFFF", fg="#333333"
        )
        self.title_label.pack(pady=15)

        # Separator line
        tk.Frame(self.main_frame, bg="#90EE90", height=3).pack(fill="x", padx=40, pady=5)

        # Joke setup
        self.setup_label = tk.Label(
            self.main_frame, text="", font=("Arial", 14, "bold"),
            wraplength=500, bg="#FFFFFF", fg="#444444", justify="center"
        )
        self.setup_label.pack(pady=20)

        # Punchline
        self.punchline_label = tk.Label(
            self.main_frame, text="", font=("Arial", 13, "italic"),
            fg="#555555", wraplength=480, bg="#FFFFFF", justify="center"
        )
        self.punchline_label.pack(pady=5)

        # --- Middle Section Buttons ---
        middle_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        middle_frame.pack(pady=15)

        # Top buttons above "Next Joke"
        top_btn_frame = tk.Frame(middle_frame, bg="#FFFFFF")
        top_btn_frame.pack(pady=5)

        self.tell_joke_btn = tk.Button(
            top_btn_frame, text="🎤 Tell Me a Joke", command=self.show_joke,
            bg="#90EE90", font=("Arial", 12, "bold"), width=15, bd=0,
            relief="ridge", activebackground="#77dd77", cursor="hand2"
        )
        self.tell_joke_btn.grid(row=0, column=0, padx=10)

        self.show_punchline_btn = tk.Button(
            top_btn_frame, text="😄 Show Punchline", command=self.show_punchline,
            bg="#ADD8E6", font=("Arial", 12, "bold"), width=15, bd=0,
            relief="ridge", activebackground="#7ec8e3", cursor="hand2"
        )
        self.show_punchline_btn.grid(row=0, column=1, padx=10)

        # Next joke button just below the above two
        self.next_joke_btn = tk.Button(
            middle_frame, text="🔁 Next Joke", command=self.show_joke,
            bg="#FFD700", font=("Arial", 13, "bold"), width=15, bd=0,
            relief="ridge", activebackground="#f7d64e", cursor="hand2"
        )
        self.next_joke_btn.pack(pady=12)

        # --- Bottom Quit Button ---
        self.quit_btn = tk.Button(
            self.main_frame, text="❌ Quit", command=root.quit,
            bg="#FF6961", font=("Arial", 10, "bold"), width=8, bd=0,
            relief="ridge", activebackground="#ff4f4f", fg="white", cursor="hand2"
        )
        self.quit_btn.pack(side="bottom", pady=10)


    def show_joke(self):
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke[0])
        self.punchline_label.config(text="")

    def show_punchline(self):
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])
        else:
            messagebox.showinfo("Hint", "Click 'Tell Me a Joke' first!")


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
