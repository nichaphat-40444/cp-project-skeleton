"""หน้าเล่นเกม Hangman: เริ่มเกม รับตัวอักษร และบันทึกผลเมื่อจบเกม."""
import random

import models
import storage

TITLE = "เล่นเกม Hangman"

WORDS = [
    {"word": "python", "category": "ภาษาโปรแกรม", "difficulty": "ง่าย"},
    {"word": "computer", "category": "เทคโนโลยี", "difficulty": "ง่าย"},
    {"word": "internet", "category": "เทคโนโลยี", "difficulty": "ง่าย"},
    {"word": "keyboard", "category": "อุปกรณ์คอมพิวเตอร์", "difficulty": "ง่าย"},
    {"word": "monitor", "category": "อุปกรณ์คอมพิวเตอร์", "difficulty": "ง่าย"},
    {"word": "algorithm", "category": "การเขียนโปรแกรม", "difficulty": "กลาง"},
    {"word": "database", "category": "เทคโนโลยี", "difficulty": "กลาง"},
    {"word": "function", "category": "การเขียนโปรแกรม", "difficulty": "กลาง"},
    {"word": "variable", "category": "การเขียนโปรแกรม", "difficulty": "กลาง"},
    {"word": "software", "category": "เทคโนโลยี", "difficulty": "กลาง"},
    {"word": "javascript", "category": "ภาษาโปรแกรม", "difficulty": "ยาก"},
    {"word": "programming", "category": "ภาษาโปรแกรม", "difficulty": "ยาก"},
    {"word": "development", "category": "ภาษาโปรแกรม", "difficulty": "ยาก"},
    {"word": "cybersecurity", "category": "เทคโนโลยี", "difficulty": "ยาก"},
    {"word": "microprocessor", "category": "อุปกรณ์คอมพิวเตอร์", "difficulty": "ยาก"},
]

CATEGORIES = sorted({item["category"] for item in WORDS})
DIFFICULTIES = ["ง่าย", "กลาง", "ยาก"]


def active_game(rows):
    for row in rows:
        if row.get("type") == "active":
            return row
    return None


def latest_game(rows):
    for row in reversed(rows):
        if row.get("type") == "game":
            return row
    return None


def choose_word(rows, category="ทั้งหมด", difficulty="ทั้งหมด"):
    pool = [
        item for item in WORDS
        if (category == "ทั้งหมด" or item["category"] == category)
        and (difficulty == "ทั้งหมด" or item["difficulty"] == difficulty)
    ]
    pool = pool or WORDS
    used_words = {row.get("word") for row in rows if row.get("word")}
    available = [item for item in pool if item["word"] not in used_words]
    if not available:
        last_word = latest_game(rows)
        available = [item for item in pool if not last_word or item["word"] != last_word.get("word")]
    return random.choice(available or pool)


def display_game(row):
    game = models.HangmanGame(row["word"], row["category"], row["difficulty"], row.get("player"))
    game.guessed = row.get("guessed", [])
    game.hint_letters = row.get("hint_letters", [])
    game.wrong = row.get("wrong", 0)
    game.status = row.get("status", "active")
    game.score = row.get("score", 0)
    return game


def build():
    rows = storage.load()
    row = active_game(rows) or latest_game(rows)
    game = display_game(row) if row else None
    return {
        "game": game,
        "letters": list("abcdefghijklmnopqrstuvwxyz"),
        "max_wrong": 6,
        "categories": CATEGORIES,
        "difficulties": DIFFICULTIES,
    }


def handle(form):
    rows = storage.load()
    action = form.get("action", "")
    if action == "start":
        rows = [row for row in rows if row.get("type") != "active"]
        category = form.get("category", "ทั้งหมด")
        difficulty = form.get("difficulty", "ทั้งหมด")
        selected = choose_word(rows, category, difficulty)
        hint_count = 2 if selected["difficulty"] == "ง่าย" else 1
        hint_letters = random.sample(sorted(set(selected["word"])), min(hint_count, len(set(selected["word"]))))
        rows.append({"type": "active", "player": form.get("player", "ผู้เล่น").strip() or "ผู้เล่น", **selected, "guessed": hint_letters, "hint_letters": hint_letters, "wrong": 0, "status": "active", "score": 0})
        storage.save(rows)
        return "เริ่มเกมใหม่แล้ว"
    if action == "guess":
        row = active_game(rows)
        if row is None:
            return "กรุณาเริ่มเกมก่อน"
        game = display_game(row)
        result = game.guess(form.get("letter", ""))
        if result == "invalid":
            return "กรุณาเลือกตัวอักษรที่ยังไม่เคยทาย"
        row.update(game.to_dict())
        if game.status != "active":
            row["type"] = "game"
            rows.remove(row)
            rows.append(row)
            message = "ชนะแล้ว!" if game.status == "won" else "เกมจบแล้ว ลองใหม่อีกครั้ง"
        else:
            row["type"] = "active"
            message = "ทายถูก" if result == "correct" else "ทายผิด"
        storage.save(rows)
        return message
    return "คำสั่งไม่ถูกต้อง"
