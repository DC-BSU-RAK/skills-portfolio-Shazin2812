import random
import time
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox, Frame, Canvas

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Math Quiz Challenge")
        self.root.geometry("600x500")
        self.root.config(bg="#e3f2fd")

# Core quiz data
        self.score = 0
        self.question_num = 0
        self.total_questions = 10
        self.num1 = self.num2 = 0
        self.operation = ""
        self.correct_answer = 0
        self.attempt = 1
        self.start_time = 0
        self.difficulty = 1
        self.bg_phase = 0

# Canvas for background animation
        self.bg_canvas = Canvas(self.root, width=600, height=500, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.animate_background()

#The Frames
        self.main_frame = Frame(self.bg_canvas, bg="#e3f2fd")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.quiz_frame = Frame(self.bg_canvas, bg="#e3f2fd")

        self.create_main_menu()

# BACKGROUND ANIMATION

    def animate_background(self):
        """Creates a subtle pulsing gradient effect."""
        self.bg_phase += 1
        color_value = 230 + int(20 * abs((self.bg_phase % 100) / 50 - 1))
        color = f"#{color_value:02x}{245:02x}{255:02x}"
        self.bg_canvas.configure(bg=color)
        self.root.after(120, self.animate_background)

# UI HELPERS

    def create_button(self, parent, text, color, hover_color, command):
        btn = Button(parent, text=text, font=("Arial Rounded MT Bold", 13),
                     bg=color, fg="white", activebackground=hover_color,
                     width=18, height=1, relief="flat", bd=0, command=command)
        btn.config(cursor="hand2")
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=hover_color))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=color))
        return btn

    def animated_title(self, label, colors, index=0):
        """Cycle through title colors."""
        label.config(fg=colors[index])
        self.root.after(200, lambda: self.animated_title(label, colors, (index + 1) % len(colors)))

# MAIN MENU

    def create_main_menu(self):
        title = Label(self.main_frame, text="🧮 Math Quiz Challenge",
                      font=("Comic Sans MS", 28, "bold"), bg="#e3f2fd", fg="#0d47a1")
        title.pack(pady=30)
        self.animated_title(title, ["#0d47a1", "#1565c0", "#42a5f5", "#1e88e5"])

        Label(self.main_frame, text="Select Difficulty Level:", font=("Arial", 15, "bold"),
              bg="#e3f2fd", fg="#1565c0").pack(pady=10)

        self.create_button(self.main_frame, "Easy", "#66bb6a", "#43a047",
                           lambda: self.start_quiz(1)).pack(pady=5)
        self.create_button(self.main_frame, "Moderate", "#ffb300", "#ffa000",
                           lambda: self.start_quiz(2)).pack(pady=5)
        self.create_button(self.main_frame, "Advanced", "#ef5350", "#e53935",
                           lambda: self.start_quiz(3)).pack(pady=5)
        self.create_button(self.main_frame, "Quit Game", "#c62828", "#b71c1c",
                           self.root.destroy).pack(pady=15)

# QUIZ LOGIC

    def random_int(self, difficulty):
        """Generate random numbers based on difficulty."""
        if difficulty == 1:
            return random.randint(1, 9)
        elif difficulty == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decide_operation(self):
        return random.choice(['+', '-'])

    def start_quiz(self, difficulty):
        self.score = 0
        self.question_num = 0
        self.start_time = time.time()
        self.difficulty = difficulty
        self.main_frame.place_forget()
        self.setup_quiz_screen()
        self.next_question()

    def setup_quiz_screen(self):
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.question_label = Label(self.quiz_frame, text="", font=("Arial", 26, "bold"),
                                    fg="#1a237e", bg="#e3f2fd")
        self.question_label.pack(pady=30)

        self.answer_var = StringVar()
        self.answer_entry = Entry(self.quiz_frame, textvariable=self.answer_var,
                                  font=("Arial", 16), width=10, justify="center")
        self.answer_entry.pack(pady=10)

        self.submit_button = self.create_button(self.quiz_frame, "Submit Answer",
                                                "#1e88e5", "#1565c0", self.check_answer)
        self.submit_button.pack(pady=10)

        self.feedback_label = Label(self.quiz_frame, text="", font=("Arial", 14),
                                    bg="#e3f2fd")
        self.feedback_label.pack(pady=10)

        self.progress_canvas = Canvas(self.quiz_frame, width=300, height=20,
                                      bg="#bbdefb", highlightthickness=0)
        self.progress_canvas.pack(pady=10)

        self.score_label = Label(self.quiz_frame, text="", font=("Arial", 12, "bold"),
                                 bg="#e3f2fd", fg="#004d40")
        self.score_label.pack(pady=5)

        self.quit_button = self.create_button(self.quiz_frame, "Quit", "#c62828",
                                              "#b71c1c", self.quit_quiz)
        self.quit_button.pack(pady=10)

# FULL SCREEN COLOR FLASH
    def flash_screen(self, color):
        """Flash full screen with color for ~2 seconds before fading."""
        original_color = "#e3f2fd"

# Change everything to flash color
        self.bg_canvas.config(bg=color)
        self.quiz_frame.config(bg=color)
        for widget in self.quiz_frame.winfo_children():
            if isinstance(widget, Label):
                widget.config(bg=color)
        self.root.update()

# Hold the color for 2 seconds, then fade back
        self.root.after(2000, lambda: self.fade_back(original_color))

    def fade_back(self, target_color):
        """Fade background back to normal."""
        self.bg_canvas.config(bg=target_color)
        self.quiz_frame.config(bg=target_color)
        for widget in self.quiz_frame.winfo_children():
            if isinstance(widget, Label):
                widget.config(bg=target_color)
        self.root.update()

    def draw_progress(self):
        """Progress bar fill."""
        target = (self.question_num / self.total_questions) * 300
        self.progress_canvas.delete("bar")
        for x in range(0, int(target), 15):
            self.progress_canvas.create_rectangle(0, 0, x, 20, fill="#42a5f5", width=0, tags="bar")
            self.progress_canvas.update()

    def fade_in_question(self, text):
        """Smooth fade-in for question text."""
        for opacity in range(0, 255, 15):
            self.question_label.config(fg=f"#{opacity:02x}{opacity:02x}{255-opacity:02x}")
            self.question_label.config(text=text)
            self.quiz_frame.update()
            time.sleep(0.02)
        self.question_label.config(fg="#1a237e")

    def next_question(self):
        if self.question_num < self.total_questions:
            self.num1 = self.random_int(self.difficulty)
            self.num2 = self.random_int(self.difficulty)
            self.operation = self.decide_operation()
            if self.operation == '-' and self.num1 < self.num2:
                self.num1, self.num2 = self.num2, self.num1
            self.correct_answer = self.num1 + self.num2 if self.operation == '+' else self.num1 - self.num2

            self.question_num += 1
            self.attempt = 1
            question_text = f"Q{self.question_num}:  {self.num1} {self.operation} {self.num2} = ?"
            self.fade_in_question(question_text)
            self.answer_var.set("")
            self.feedback_label.config(text="")
            self.score_label.config(text=f"⭐ Score: {self.score}")
            self.draw_progress()
        else:
            self.end_quiz()

    def check_answer(self):
        try:
            user_answer = int(self.answer_var.get())
        except ValueError:
            self.feedback_label.config(text="⚠️ Please enter a valid number.", fg="red")
            return

        if user_answer == self.correct_answer:
            self.flash_screen("lightgreen")  # green flash
            if self.attempt == 1:
                self.score += 10
                self.feedback_label.config(text="✅ Correct! (+10 points)", fg="green")
            else:
                self.score += 5
                self.feedback_label.config(text="✅ Correct on second try! (+5 points)", fg="green")

            self.animate_score()
            self.root.after(2200, self.next_question)  # wait until color fades
        else:
            self.flash_screen("#ff9999")  # red flash
            if self.attempt == 1:
                self.attempt = 2
                self.feedback_label.config(text="❌ Try again...", fg="red")
                self.answer_var.set("")
            else:
                self.feedback_label.config(text=f"❌ Wrong! Answer: {self.correct_answer}", fg="red")
                self.root.after(2200, self.next_question)

    def animate_score(self):
        """Pop animation on score change."""
        for size in range(12, 16):
            self.score_label.config(font=("Arial", size, "bold"))
            self.score_label.update()
            time.sleep(0.03)
        self.score_label.config(font=("Arial", 12, "bold"), text=f"⭐ Score: {self.score}")

    def end_quiz(self):
        elapsed = time.time() - self.start_time
        grade, msg = self.calculate_grade()
        self.quiz_frame.place_forget()

        result_frame = Frame(self.bg_canvas, bg="#e3f2fd")
        result_frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(result_frame, text="🎉 Quiz Completed!", font=("Arial Rounded MT Bold", 26),
              bg="#e3f2fd", fg="#0d47a1").pack(pady=20)
        Label(result_frame, text=f"Final Score: {self.score}/100", font=("Arial", 16),
              bg="#e3f2fd").pack(pady=10)
        Label(result_frame, text=f"Grade: {grade}", font=("Arial", 16, "bold"),
              fg="#2e7d32", bg="#e3f2fd").pack(pady=5)
        Label(result_frame, text=msg, font=("Arial", 13, "italic"),
              bg="#e3f2fd").pack(pady=5)
        Label(result_frame, text=f"Time Taken: {elapsed:.2f} seconds",
              font=("Arial", 12), bg="#e3f2fd").pack(pady=10)

        self.create_button(result_frame, "Play Again", "#1e88e5", "#1565c0",
                           self.reset_quiz).pack(pady=10)
        self.create_button(result_frame, "Exit", "#b71c1c", "#8e0000",
                           self.root.destroy).pack()

    def calculate_grade(self):
        if self.score >= 90:
            return "A+", "🌟 Amazing! You're a Math Genius!"
        elif self.score >= 80:
            return "A", "👏 Great job! Keep it up!"
        elif self.score >= 70:
            return "B", "👍 Nice work! Keep practicing!"
        elif self.score >= 60:
            return "C", "🙂 Good effort!"
        else:
            return "D", "💪 Don't give up — practice more!"

    def quit_quiz(self):
        if messagebox.askyesno("Exit Quiz", "Are you sure you want to quit?"):
            self.root.destroy()

    def reset_quiz(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main()

def main():
    root = Tk()
    app = MathQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
