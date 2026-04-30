import json
import random
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AnswerResult:
    is_correct: bool
    correct_answer: str
    user_answer: str
    current_word: Dict[str, str]
    is_empty: bool = False


@dataclass
class QuestionResult:
    has_question: bool
    english_word: str = ""
    message: str = ""


class QuizEngine:
    def __init__(self, json_file: str = 'words.json'):
        self.json_file = json_file
        self.words = self._load_words()
        self.current_word: Optional[Dict[str, str]] = None
        self._used_words: set = set()

    def _load_words(self) -> list:
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('words', [])
        except FileNotFoundError:
            print(f"文件 {self.json_file} 未找到")
            return []
        except json.JSONDecodeError:
            print(f"文件 {self.json_file} 格式错误")
            return []

    def has_words(self) -> bool:
        return len(self.words) > 0

    def get_total_words(self) -> int:
        return len(self.words)

    def start_new_quiz(self) -> None:
        self._used_words.clear()
        self.current_word = None

    def next_question(self) -> QuestionResult:
        if not self.has_words():
            return QuestionResult(
                has_question=False,
                message="没有可用的单词"
            )

        available_words = [w for w in self.words if w['english'] not in self._used_words]

        if not available_words:
            self._used_words.clear()
            available_words = self.words

        self.current_word = random.choice(available_words)
        self._used_words.add(self.current_word['english'])

        return QuestionResult(
            has_question=True,
            english_word=self.current_word['english']
        )

    def get_current_english(self) -> Optional[str]:
        if self.current_word:
            return self.current_word.get('english')
        return None

    def submit_answer(self, user_answer: str) -> AnswerResult:
        if not self.current_word:
            return AnswerResult(
                is_correct=False,
                correct_answer="",
                user_answer=user_answer,
                current_word={},
                is_empty=True
            )

        user_answer_stripped = user_answer.strip()

        if not user_answer_stripped:
            return AnswerResult(
                is_correct=False,
                correct_answer=self.current_word['chinese'],
                user_answer=user_answer,
                current_word=self.current_word,
                is_empty=True
            )

        correct_answer = self.current_word['chinese'].strip()
        is_correct = correct_answer == user_answer_stripped

        return AnswerResult(
            is_correct=is_correct,
            correct_answer=correct_answer,
            user_answer=user_answer_stripped,
            current_word=self.current_word
        )

    def check_answer(self, word: Dict[str, str], user_answer: str) -> bool:
        if not word or 'chinese' not in word:
            return False
        correct_answer = word['chinese'].strip()
        user_answer = user_answer.strip()
        return correct_answer == user_answer

    def get_random_word(self) -> Optional[Dict[str, str]]:
        if not self.words:
            return None
        return random.choice(self.words)
