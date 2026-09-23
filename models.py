"""Domain model for one Hangman game."""


class HangmanGame:
    def __init__(self, word, category, difficulty, player="ผู้เล่น"):
        self.word = word.lower()
        self.category = category
        self.difficulty = difficulty
        self.player = player or "ผู้เล่น"
        self.guessed = []
        self.hint_letters = []
        self.wrong = 0
        self.status = "active"
        self.score = 0

    def guess(self, letter):
        letter = (letter or "").strip().lower()
        if len(letter) != 1 or not letter.isalpha() or letter in self.guessed or self.status != "active":
            return "invalid"
        self.guessed.append(letter)
        if letter not in self.word:
            self.wrong += 1
        if all(character in self.guessed for character in self.word):
            self.status = "won"
            self.score = max(10, 100 - self.wrong * 10)
        elif self.wrong >= 6:
            self.status = "lost"
            self.score = 0
        return "correct" if letter in self.word else "wrong"

    def masked_word(self):
        return " ".join(character if character in self.guessed else "_" for character in self.word)

    def drawing(self):
        stages = [
            "  +---+\n  |   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n=========",
        ]
        return stages[min(self.wrong, len(stages) - 1)]

    def to_dict(self):
        return {
            "type": "game",
            "player": self.player,
            "word": self.word,
            "category": self.category,
            "difficulty": self.difficulty,
            "guessed": self.guessed,
            "hint_letters": self.hint_letters,
            "wrong": self.wrong,
            "status": self.status,
            "score": self.score,
        }
