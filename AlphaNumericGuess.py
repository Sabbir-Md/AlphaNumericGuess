import tkinter as tk
from tkinter import messagebox
import random


class GuessingGame:

    def __init__(self, root):

        self.root = root
        self.root.title("🔠AlphaNumeric Guess")
        self.root.geometry("750x600")
        self.root.config(bg="#1f1f2e")
        self.root.resizable(False, False)

        # ================= COLORS =================

        self.bg = "#121222"
        self.white = "white"
        self.green = "#00b894"
        self.red = "#d63031"
        self.blue = "#0984e3"
        self.purple = "#6c5ce7"
        self.yellow = "#ffd166"
        self.cyan = "#00ffcc"

        # ================= VARIABLES =================

        self.level = 1
        self.total_levels = 5
        self.score = 0
        self.tries = 0

        self.start_limit = 1
        self.end_limit = 20

        self.alpha_start = "A"
        self.alpha_end = "Z"

        self.custom_limit = False
        self.game_mode = ""

        self.random_number = 0
        self.random_letter = ""

        # ================= MAIN FRAME =================

        self.main_frame = tk.Frame(root, bg=self.bg)
        self.main_frame.pack(expand=True, fill="both")

        self.original_start_limit = 1
        self.original_end_limit = 20
        tk.Label(
            self.main_frame,
            text="🔠AlphaNumeric Guess",
            font=("Arial", 30, "bold"),
            bg=self.bg,
            fg=self.cyan
        ).pack(pady=20)

        self.content_frame = tk.Frame(
            self.main_frame,
            bg=self.bg
        )

        self.content_frame.pack(expand=True)

        self.select_game_screen()

    # =====================================================
    # COMMON FUNCTIONS
    # =====================================================

    def clear_frame(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def make_label(self, text, size=16, color="white", pady=10):

        label = tk.Label(
            self.content_frame,
            text=text,
            font=("Arial", size, "bold"),
            bg=self.bg,
            fg=color
        )

        label.pack(pady=pady)

        return label

    def make_button(self, text, color, command, pady=10):

        button = tk.Button(
            self.content_frame,
            text=text,
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white",
            width=15,
            command=command
        )

        button.pack(pady=pady)

        return button

    def make_entry(self, width=5):

        entry = tk.Entry(
            self.content_frame,
            font=("Arial", 20),
            justify="center",
            width=width
        )

        entry.pack(pady=5,padx=5)

        return entry

    # =====================================================
    # FIRST SCREEN
    # =====================================================

    def select_game_screen(self):

        self.clear_frame()

        self.make_label(
            "Choose What You Want To Guess",
            22,
            pady=30
        )

        button_frame = tk.Frame(
            self.content_frame,
            bg=self.bg
        )

        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="🔢 Number Guessing",
            font=("Arial", 16, "bold"),
            bg=self.green,
            fg="white",
            width=18,
            height=2,
            command=self.number_limit_question
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            button_frame,
            text="🔤 Alphabet Guessing",
            font=("Arial", 16, "bold"),
            bg=self.purple,
            fg="white",
            width=18,
            height=2,
            command=self.alphabet_limit_question
        ).grid(row=0, column=1, padx=20)

    # =====================================================
    # LIMIT QUESTION
    # =====================================================

    def limit_question(self, mode):

        self.game_mode = mode

        self.clear_frame()

        text = (
            "Do you want to set your own limit?"
            if mode == "NUMBER"
            else "Do you want to set alphabet limit?"
        )

        self.make_label(text, 20, pady=30)

        button_frame = tk.Frame(
            self.content_frame,
            bg=self.bg
        )

        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="YES",
            font=("Arial", 14, "bold"),
            bg=self.green,
            fg="white",
            width=12,
            command=self.custom_limit_screen
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            button_frame,
            text="NO",
            font=("Arial", 14, "bold"),
            bg=self.red,
            fg="white",
            width=12,
            command=self.default_game
        ).grid(row=0, column=1, padx=20)

    def number_limit_question(self):

        self.limit_question("NUMBER")

    def alphabet_limit_question(self):

        self.limit_question("ALPHABET")

    # =====================================================
    # CUSTOM LIMIT SCREEN
    # =====================================================

    def custom_limit_screen(self):

        self.clear_frame()

        title = (
            "Set Your Custom Number Range"
            if self.game_mode == "NUMBER"
            else "Set Alphabet Range"
        )

        self.make_label(title, 20, self.cyan, 20)

        label1 = (
            "Starting Limit:"
            if self.game_mode == "NUMBER"
            else "Starting Letter:"
        )

        label2 = (
            "Ending Limit:"
            if self.game_mode == "NUMBER"
            else "Ending Letter:"
        )

        self.make_label(label1, 14)

        self.entry1 = self.make_entry(8)

        self.make_label(label2, 14)

        self.entry2 = self.make_entry(8)

        self.root.bind("<Return>", lambda event: self.set_limits())

        self.make_button(
            "Start Game",
            self.blue,
            self.set_limits,
            20
        )

    # =====================================================
    # SET LIMITS
    # =====================================================

    def set_limits(self):

        if self.game_mode == "NUMBER":

            try:

                self.start_limit = int(self.entry1.get())
                self.end_limit = int(self.entry2.get())
                self.original_start_limit = self.start_limit
                self.original_end_limit = self.end_limit

                if self.start_limit >= self.end_limit:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Input",
                    "Starting limit must be smaller."
                )

                return

            self.custom_limit = True

            self.start_number_level()

        else:

            self.alpha_start = self.entry1.get().upper()
            self.alpha_end = self.entry2.get().upper()

            if (
                len(self.alpha_start) != 1 or
                len(self.alpha_end) != 1 or
                not self.alpha_start.isalpha() or
                not self.alpha_end.isalpha() or
                self.alpha_start > self.alpha_end
            ):

                messagebox.showerror(
                    "Invalid Input",
                    "Enter valid letters A-Z."
                )

                return

            self.start_alphabet_game()

    # =====================================================
    # DEFAULT GAME
    # =====================================================

    def default_game(self):

        if self.game_mode == "NUMBER":

            self.custom_limit = False
            self.start_limit = 1
            self.end_limit = 20
            self.original_start_limit = 1
            self.original_end_limit = 20

            self.start_number_level()

        else:

            self.alpha_start = "A"
            self.alpha_end = "Z"

            self.start_alphabet_game()

    # =====================================================
    # NUMBER GAME
    # =====================================================

    def start_number_level(self):

        self.clear_frame()

        self.random_number = random.randint(
            self.start_limit,
            self.end_limit
        )

        self.make_label(
            f"LEVEL {self.level}",
            26,
            self.yellow
        )

        self.make_label(
            f"Guess Number Between {self.start_limit} and {self.end_limit}"
        )

        self.score_label = self.make_label(
            f"Score: {self.score}",
            15,
            self.cyan,
            5
        )

        self.try_label = self.make_label(
            f"Tries: {self.tries}",
            15,
            "#ff7675",
            5
        )

        self.number_entry = self.make_entry()

        self.number_entry.focus()

        self.root.bind(
            "<Return>",
            lambda event: self.check_number_guess()
        )

        self.feedback_label = self.make_label("", 15)

        self.make_button(
            "Submit Guess",
            self.green,
            self.check_number_guess,
            10
        )

        self.make_button(
        "Reset Game",
        self.red,
        self.reset_number_game
        )

        self.make_button(
        "Main Menu",
        self.blue,
        self.restart_game
        )
    # =====================================================
    # CHECK NUMBER
    # =====================================================

    def check_number_guess(self):

        try:

            guess = int(self.number_entry.get())

        except ValueError:

            self.feedback_label.config(
                text="❌ Enter valid integer",
                fg="red"
            )

            return

        if guess < self.start_limit or guess > self.end_limit:

            self.feedback_label.config(
                text="❌ Number outside range",
                fg="red"
            )

            return

        self.tries += 1

        self.try_label.config(
            text=f"Tries: {self.tries}"
        )

        if guess == self.random_number:

            gained_score = max(
                100 - (self.tries * 5),
                10
            )

            self.score += gained_score

            self.feedback_label.config(
                text=f"🎉 Correct! +{gained_score} Points",
                fg="#00ff99"
            )

            self.score_label.config(
                text=f"Score: {self.score}"
            )

            if self.level == self.total_levels:

                self.number_game_completed()

            else:

                self.feedback_label.config(
                text=f"🎉 Level {self.level} Complete! +{gained_score} Points",
                fg="#00ff99"
    )

                self.root.after(1500, self.next_level)

                return

        elif guess < self.random_number:

            self.feedback_label.config(
                text="📈 Number is HIGHER",
                fg=self.yellow
            )

        else:

            self.feedback_label.config(
                text="📉 Number is LOWER",
                fg=self.yellow
            )

        self.number_entry.delete(0, tk.END)

    # =====================================================
    # NEXT LEVEL
    # =====================================================

    def next_level(self):

        self.level += 1
        self.tries = 0

        range_size = self.original_end_limit - self.original_start_limit
        self.end_limit = self.original_end_limit + (self.level - 1) * (range_size // 2)

        self.start_number_level()

    # =====================================================
    # NUMBER GAME COMPLETE
    # =====================================================

    def number_game_completed(self):

        self.clear_frame()

        self.make_label(
            "🏆 YOU COMPLETED ALL LEVELS!",
            26,
            "#00ff99",
            30
        )

        self.make_label(
            f"Final Score: {self.score}",
            20,
            self.yellow,
            20
        )

        self.make_button(
        "Reset Game",
        self.green,
        self.reset_number_game,
        20
        )

        self.make_button(
        "Main Menu",
        self.blue,
        self.restart_game,
        10
        )

    # =====================================================
    # ALPHABET GAME
    # =====================================================

    def start_alphabet_game(self):

        self.clear_frame()

        self.random_letter = chr(
            random.randint(
                ord(self.alpha_start),
                ord(self.alpha_end)
            )
        )
        self.alpha_tries = 0       
        self.alpha_score = 0

        self.make_label(
            f"Guess Letter Between {self.alpha_start} and {self.alpha_end}",
            20,
            self.cyan,
            30
        )
        self.alpha_score_label = self.make_label(f"Score: {self.alpha_score}", 15, self.cyan, 5)   
        self.alpha_try_label = self.make_label(f"Tries: {self.alpha_tries}", 15, "#ff7675", 5)     

        self.alpha_entry = self.make_entry(5)

        self.alpha_entry.focus()

        self.root.bind(
            "<Return>",
            lambda event: self.check_alphabet_guess()
        )

        self.alpha_feedback = self.make_label("", 15)

        self.submit_alpha_btn = self.make_button(
            "Submit Guess",
            self.purple,
            self.check_alphabet_guess,
            20
        )

        self.make_button(
            "Reset Game",
            self.red,
            self.reset_alphabet_game
        )
        self.make_button(
        "Main Menu",
        self.blue,
        self.restart_game
        )

    # =====================================================
    # CHECK ALPHABET
    # =====================================================

    def check_alphabet_guess(self):

        guess = self.alpha_entry.get().upper()

        if (
            len(guess) != 1 or
            not guess.isalpha()
        ):

            self.alpha_feedback.config(
                text="❌ Enter valid letter",
                fg="red"
            )

            return

        if guess < self.alpha_start or guess > self.alpha_end:

            self.alpha_feedback.config(
                text="❌ Letter outside range",
                fg="red"
            )

            return
        
        self.alpha_tries += 1                                          
        self.alpha_try_label.config(text=f"Tries: {self.alpha_tries}")

        if guess == self.random_letter:
            gained = max(100 - (self.alpha_tries * 5), 10)  
            self.alpha_score += gained                        
            self.alpha_score_label.config(text=f"Score: {self.alpha_score}")  
            self.alpha_feedback.config(
                text=f"🎉 Correct! +{gained} Points",          
                fg="#00ff99"
            )

            self.alpha_entry.config(state="disabled")
            self.submit_alpha_btn.destroy()
            self.root.unbind("<Return>") 
            return

        elif guess < self.random_letter:

            self.alpha_feedback.config(
                text="➡ Letter comes AFTER",
                fg=self.yellow
            )

        else:

            self.alpha_feedback.config(
                text="⬅ Letter comes BEFORE",
                fg=self.yellow
            )

        self.alpha_entry.delete(0, tk.END)

        #=====================================================
        # Reset number guess
        #=====================================================
    def reset_number_game(self):

        self.level = 1
        self.score = 0
        self.tries = 0

        self.start_limit = self.original_start_limit
        self.end_limit = self.original_end_limit

        self.start_number_level()


    def reset_alphabet_game(self):

        self.start_alphabet_game()

    def restart_game(self):

        self.level = 1
        self.score = 0
        self.tries = 0

        self.root.unbind("<Return>")

        self.select_game_screen()


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = GuessingGame(root)

    root.mainloop()