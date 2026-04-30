import tkinter as tk
from tkinter import messagebox
from quiz_engine import QuizEngine, AnswerResult, QuestionResult


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("单词测验系统")
        self.root.geometry("500x350")
        self.root.resizable(True, True)
        self.root.minsize(450, 320)

        self.quiz_engine = QuizEngine()
        self.quiz_engine.start_new_quiz()

        self.create_widgets()
        self.next_word()

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.title_label = tk.Label(
            self.main_frame,
            text="单词测验系统",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(0, 15))

        self.english_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 24, "bold"),
            fg="blue"
        )
        self.english_label.pack(pady=(0, 15))

        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(pady=(0, 15))

        self.input_label = tk.Label(
            self.input_frame,
            text="请输入中文：",
            font=("Arial", 12)
        )
        self.input_label.pack(side=tk.LEFT, padx=5)

        self.answer_entry = tk.Entry(
            self.input_frame,
            font=("Arial", 12),
            width=20
        )
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=(0, 15))

        self.submit_button = tk.Button(
            self.button_frame,
            text="提交答案",
            font=("Arial", 12),
            command=self.check_answer,
            bg="#4CAF50",
            fg="white",
            width=10
        )
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(
            self.button_frame,
            text="下一个",
            font=("Arial", 12),
            command=self.next_word,
            bg="#2196F3",
            fg="white",
            width=10
        )
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.result_frame = tk.Frame(self.main_frame)
        self.result_frame.pack(fill=tk.X, expand=True)

        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 14),
            fg="green",
            wraplength=400,
            justify="center"
        )
        self.result_label.pack(pady=10, fill=tk.X, expand=True)

    def next_word(self):
        result: QuestionResult = self.quiz_engine.next_question()

        if result.has_question:
            self.english_label.config(text=result.english_word)
            self.answer_entry.delete(0, tk.END)
            self.result_label.config(text="", fg="black")
            self.answer_entry.focus_set()
        else:
            messagebox.showerror("错误", result.message)

    def check_answer(self):
        user_answer = self.answer_entry.get()
        result: AnswerResult = self.quiz_engine.submit_answer(user_answer)

        if result.is_empty:
            messagebox.showwarning("提示", "请输入答案")
            return

        if result.is_correct:
            self.result_label.config(text="✅ 回答正确！", fg="green")
        else:
            self.result_label.config(
                text=f"❌ 回答错误，正确答案是：{result.correct_answer}",
                fg="red"
            )


def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
