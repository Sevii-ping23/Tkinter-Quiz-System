import os
import random
import tkinter as tk
from tkinter import messagebox

QUESTIONS = [
    {
        "question": "Choose the word closest in meaning to EPHEMERAL.",
        "choices": [
        "A. Short-lived", 
        "B. Lasting", 
        "C. Ancient", 
        "D. Hidden"
        ],
        "answer": "A"
    },
    {
        "question": "Choose the correct word to complete the sentence: "
                    "Neither of the applicants ___ submitted the requirements.",
        "choices": [
        "A. have", 
        "B. were", 
        "C. has", 
        "D. are"
        ],
        "answer": "C"
    },
    {
        "question": "What is 15% of 240?",
        "choices": ["A. 32", "B. 40", "C. 38", "D. 36"],
        "answer": "D"
    },
    {
        "question": "A clerk encodes 45 pages in 3 hours. At the same rate, "
                    "how many pages can the clerk encode in 8 hours?",
        "choices": ["A. 105", "B. 135", "C. 120", "D. 360"],
        "answer": "C"
    },
    {
        "question": "Find the next number in the series: 2, 6, 18, 54, ___",
        "choices": ["A. 162", "B. 108", "C. 148", "D. 216"],
        "answer": "A"
    },
    {
        "question": "Doctor is to hospital as teacher is to ___.",
        "choices": ["A. student", "B. book", "C. lesson", "D. school"],
        "answer": "D"
    },
    {
        "question": "Under the 1987 Philippine Constitution, what is the "
                    "term of office of the President?",
        "choices": ["A. Four years, with one reelection",
                    "B. Six years, with one reelection",
                    "C. Six years, without reelection",
                    "D. Five years, without reelection"],
        "answer": "C"
    },
    {
        "question": "Republic Act No. 6713 is also known as the ___.",
        "choices": ["A. Code of Conduct and Ethical Standards for Public "
                    "Officials and Employees",
                    "B. Anti-Graft and Corrupt Practices Act",
                    "C. Government Procurement Reform Act",
                    "D. Civil Service Decree of the Philippines"],
        "answer": "A"
    },
    {
        "question": "All civil servants are government employees. Maria is a "
                    "civil servant. Which conclusion must be true?",
        "choices": ["A. Maria is a volunteer.",
                    "B. Maria is a government employee.",
                    "C. All government employees are civil servants.",
                    "D. Maria is not employed by the government."],
        "answer": "B"
    },
    {
        "question": "Which constitutional body serves as the central "
                    "personnel agency of the Philippine government?",
        "choices": ["A. Commission on Audit (COA)",
                    "B. Department of Budget and Management (DBM)",
                    "C. Civil Service Commission (CSC)",
                    "D. Commission on Elections (COMELEC)"],
        "answer": "C"
    },
]

TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

NAVY = "#14213D"
GOLD = "#FCA311"
PAPER = "#FFFFFF"
SOFT = "#E5E5E5"
CORRECT_COLOR = "#2E7D32"
WRONG_COLOR = "#C62828"

FONT = "Georgia"

root = tk.Tk()
root.title("Civil Service Exam Reviewer")
root.geometry("760x680")
root.configure(bg=NAVY)
root.resizable(False, False)


quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []       
timer_job = None         
answered = False         
selected_answer = tk.StringVar()

timer_label = None
timer_bar = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

main_frame = tk.Frame(root, bg=PAPER)
main_frame.pack(fill="both", expand=True, padx=25, pady=25)


def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(new_score):
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False

def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()


def get_choice_text(question, letter):
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def make_button(parent, text, command, bg=NAVY, fg="white", width=16):
    return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                     font=(FONT, 13, "bold"), width=width, relief="flat",
                     activebackground=GOLD, cursor="hand2", pady=6)


def on_close():
    stop_timer()
    root.destroy()

def show_start_screen():
    clear_screen()
    tk.Label(main_frame, text="CIVIL SERVICE", font=(FONT, 14, "bold"),
             bg=PAPER, fg=GOLD).pack(pady=(70, 0))
    tk.Label(main_frame, text="Exam Reviewer", font=(FONT, 36, "bold"),
             bg=PAPER, fg=NAVY).pack()
    tk.Label(main_frame,
             text="Verbal  |  Numerical  |  Analytical  |  General Information",
             font=(FONT, 11, "italic"), bg=PAPER, fg="gray30").pack(pady=8)

    info = tk.Frame(main_frame, bg=SOFT)
    info.pack(pady=30, ipadx=30, ipady=12)
    tk.Label(info,
             text=f"{len(QUESTIONS)} questions   •   {TIME_LIMIT} seconds each",
             font=(FONT, 13), bg=SOFT, fg=NAVY).pack(pady=(6, 2))
    tk.Label(info,
             text=f"High Score: {get_high_score()} / {len(QUESTIONS)}",
             font=(FONT, 16, "bold"), bg=SOFT, fg=NAVY).pack(pady=(2, 6))

    make_button(main_frame, "Start Quiz", start_quiz, bg=GOLD,
                fg=NAVY, width=18).pack(pady=10)
    make_button(main_frame, "Exit", on_close, bg="gray40",
                width=18).pack(pady=5)


def start_quiz():
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


def show_question():
    global time_left, answered, timer_label, timer_bar, feedback_label
    global submit_button, next_button, choice_buttons

    stop_timer()
    clear_screen()
    answered = False
    selected_answer.set("")          
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    
    header = tk.Frame(main_frame, bg=NAVY)
    header.pack(fill="x")
    tk.Label(header,
             text=f"Question {current_question + 1} of {len(quiz_questions)}",
             font=(FONT, 13, "bold"), bg=NAVY, fg="white").pack(
                 side="left", padx=15, pady=8)
    timer_label = tk.Label(header, text="", font=(FONT, 13, "bold"),
                           bg=NAVY, fg=GOLD)
    timer_label.pack(side="right", padx=15)

    timer_bar = tk.Canvas(main_frame, height=8, bg=SOFT,
                          highlightthickness=0)
    timer_bar.pack(fill="x")

    tk.Label(main_frame, text=f"Score: {score}", font=(FONT, 11),
             bg=PAPER, fg="gray30").pack(anchor="e", padx=20, pady=(8, 0))

    body = tk.Frame(main_frame, bg=PAPER)
    body.pack(fill="both", expand=True, padx=25)

    tk.Label(body, text=question["question"], font=(FONT, 16, "bold"),
             wraplength=640, justify="left", bg=PAPER,
             fg=NAVY).pack(pady=(10, 18), anchor="w")

    
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(body, text=choice, variable=selected_answer,
                                value=letter, font=(FONT, 13), bg=PAPER,
                                activebackground=SOFT, anchor="w",
                                justify="left", wraplength=620,
                                selectcolor=GOLD)
        button.pack(fill="x", pady=4)
        choice_buttons.append(button)

    feedback_label = tk.Label(body, text="", font=(FONT, 12, "bold"),
                              bg=PAPER, wraplength=640, justify="left")
    feedback_label.pack(pady=12, anchor="w")

    button_frame = tk.Frame(body, bg=PAPER)
    button_frame.pack(side="bottom", pady=15)
    submit_button = make_button(button_frame, "Submit Answer", submit_answer,
                                bg=GOLD, fg=NAVY)
    submit_button.pack(side="left", padx=10)

    last_question = current_question == len(quiz_questions) - 1
    next_button = make_button(
        button_frame, "See Results" if last_question else "Next Question",
        next_question)
    next_button.config(state="disabled")
    next_button.pack(side="left", padx=10)

    update_timer()


def update_timer():
    global time_left, timer_job
    if answered:                     
        return

    timer_label.config(text=f"Time left: {time_left}s")
    timer_label.config(fg=WRONG_COLOR if time_left <= 5 else GOLD)
    timer_bar.delete("all")
    timer_bar.update_idletasks()     
    width = timer_bar.winfo_width()
    timer_bar.create_rectangle(
        0, 0, width * time_left / TIME_LIMIT, 8,
        fill=WRONG_COLOR if time_left <= 5 else GOLD, width=0)

    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    global score, answered
    if answered:                     
        return

    choice = selected_answer.get()
    if choice == "":                 
        messagebox.showwarning("No answer", "Please select an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct_text = get_choice_text(question, question["answer"])

    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct! Well done.", fg=CORRECT_COLOR)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": correct_text,
        })
        feedback_label.config(
            text=f"Wrong. The correct answer is {correct_text}",
            fg=WRONG_COLOR)

    next_button.config(state="normal")


def time_up():
    global answered
    if answered:
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct_text = get_choice_text(question, question["answer"])
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": correct_text,
    })
    feedback_label.config(
        text=f"Time is up! The correct answer is {correct_text}",
        fg=WRONG_COLOR)
    next_button.config(state="normal")


def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


def get_message(percentage):
    if percentage == 100:
        return "Perfect! You are ready for the exam!"
    if percentage >= 80:
        return "Excellent! You are well prepared."
    if percentage >= 60:
        return "Good job! A little more review will help."
    return "Keep studying. Review the topics and try again."


def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = score / total * 100
    new_record = save_high_score(score)

    tk.Label(main_frame, text="RESULTS", font=(FONT, 14, "bold"),
             bg=NAVY, fg=GOLD).pack(fill="x", ipady=8)
    tk.Label(main_frame, text=f"{score} / {total}", font=(FONT, 40, "bold"),
             bg=PAPER, fg=NAVY).pack(pady=(15, 0))
    tk.Label(main_frame, text=f"{percentage:.0f}%", font=(FONT, 18),
             bg=PAPER, fg="gray30").pack()
    tk.Label(main_frame, text=get_message(percentage),
             font=(FONT, 13, "italic"), bg=PAPER, fg=NAVY).pack(pady=5)

    if new_record:
        high_text = f"New High Score: {get_high_score()} / {total}!"
        high_color = CORRECT_COLOR
    else:
        high_text = f"High Score: {get_high_score()} / {total}"
        high_color = "gray30"
    tk.Label(main_frame, text=high_text, font=(FONT, 12, "bold"),
             bg=PAPER, fg=high_color).pack(pady=(0, 8))

    tk.Label(main_frame, text="Answer Review (incorrect answers)",
             font=(FONT, 12, "bold"), bg=PAPER, fg=NAVY).pack(anchor="w",
                                                              padx=25)
    review_frame = tk.Frame(main_frame, bg=PAPER)
    review_frame.pack(fill="both", expand=True, padx=25, pady=5)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, height=8, wrap="word", bg=SOFT,
                         font=(FONT, 11), yscrollcommand=scrollbar.set,
                         relief="flat")
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "No mistakes. All answers were correct!")
    for number, item in enumerate(wrong_answers, start=1):
        review_box.insert("end", f"{number}. {item['question']}\n")
        review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
        review_box.insert("end",
                          f"   Correct answer: {item['correct_answer']}\n\n")
    review_box.config(state="disabled")

    button_frame = tk.Frame(main_frame, bg=PAPER)
    button_frame.pack(pady=12)
    make_button(button_frame, "Restart Quiz", start_quiz, bg=GOLD,
                fg=NAVY).pack(side="left", padx=10)
    make_button(button_frame, "Exit", on_close, bg="gray40").pack(
        side="left", padx=10)


root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()