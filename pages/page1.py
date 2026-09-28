"""หน้าเล่นเกม Hangman: เริ่มเกม รับตัวอักษร และบันทึกผลเมื่อจบเกม."""
import json
import random
import re
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import models
import storage

TITLE = "เล่นเกม Hangman"
WORD_TIME_LIMITS = {"ง่าย": 60, "กลาง": 90, "ยาก": 120}
ROUND_HINT_LIMIT = 3

CATEGORIES = {
    "สัตว์": "Animals",
    "สิ่งของ": "Tools",
    "ของใช้ในบ้าน": "Furniture",
    "ประเทศ": "Countries",
    "จังหวัดไทย": "Provinces of Thailand",
}
DIFFICULTIES = ["ง่าย", "กลาง", "ยาก"]
THAI_HINTS = {
    "สัตว์": "เป็นชื่อสัตว์ภาษาอังกฤษ",
    "สิ่งของ": "เป็นชื่อสิ่งของหรือเครื่องมือภาษาอังกฤษ",
    "ของใช้ในบ้าน": "เป็นของใช้ที่พบได้ในบ้าน",
    "ประเทศ": "เป็นชื่อประเทศภาษาอังกฤษ",
    "จังหวัดไทย": "เป็นชื่อจังหวัดของประเทศไทยภาษาอังกฤษ",
}


def difficulty_for(word):
    if len(word) <= 5:
        return "ง่าย"
    if len(word) <= 8:
        return "กลาง"
    return "ยาก"


def translate_word(word):
    query = urlencode({"q": word, "langpair": "en|th"})
    request = Request(
        "https://api.mymemory.translated.net/get?" + query,
        headers={"User-Agent": "HangmanClassProject/1.0"},
    )
    try:
        with urlopen(request, timeout=4) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, TimeoutError, ValueError):
        return "ไม่พบคำแปล"
    translation = payload.get("responseData", {}).get("translatedText", "").strip()
    if not translation or translation.lower() == word.lower():
        return "ไม่พบคำแปล"
    return translation


def thai_hint(word, category):
    category_hint = THAI_HINTS.get(category, "เป็นคำศัพท์ภาษาอังกฤษ")
    return f"{category_hint} ขึ้นต้นด้วย {word[0].upper()} และมี {len(word)} ตัวอักษร"


def dictionary_words(category, difficulty):
    for start_letter in (random.choice("abcdefghijklmnopqrstuvwxyz"), ""):
        query = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:en:" + CATEGORIES[category],
            "cmtype": "page",
            "cmnamespace": 0,
            "cmlimit": 500,
            "format": "json",
        }
        if start_letter:
            query["cmstartsortkeyprefix"] = start_letter
        request = Request(
            "https://en.wiktionary.org/w/api.php?" + urlencode(query),
            headers={"User-Agent": "HangmanClassProject/1.0"},
        )
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))

        words = []
        for item in payload.get("query", {}).get("categorymembers", []):
            word = item.get("title", "").lower()
            if re.fullmatch(r"[a-z]{3,}", word) and difficulty_for(word) == difficulty:
                words.append({"word": word, "category": category, "difficulty": difficulty})
        if words:
            return words
    return []


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


def choose_word(rows, category="ทั้งหมด", difficulty="ง่าย"):
    if category == "ทั้งหมด":
        category = random.choice(list(CATEGORIES))
    pool = dictionary_words(category, difficulty)
    if not pool:
        return None
    used_words = {row.get("word") for row in rows if row.get("word")}
    available = [item for item in pool if item["word"] not in used_words]
    if not available:
        last_word = latest_game(rows)
        available = [item for item in pool if not last_word or item["word"] != last_word.get("word")]
    available = available or pool
    selected = random.choice(available)
    selected["_remaining_words"] = [item["word"] for item in available if item["word"] != selected["word"]]
    selected["_word_pool"] = [item["word"] for item in available]
    selected["translation"] = translate_word(selected["word"])
    selected["thai_hint"] = thai_hint(selected["word"], selected["category"])
    return selected


def display_game(row):
    game = models.HangmanGame(row["word"], row["category"], row["difficulty"], row.get("player"))
    game.guessed = row.get("guessed", [])
    game.hint_letters = row.get("hint_letters", [])
    game.wrong = row.get("wrong", 0)
    game.status = row.get("status", "active")
    game.score = row.get("score", 0)
    return game


def archive_game(rows, row, game):
    row.update(game.to_dict())
    row["type"] = "game"
    rows.remove(row)
    rows.append(row)


def next_word(row, rows):
    used_words = set(row.get("round_words", []))
    if not used_words:
        used_words.update(set(row.get("word_pool", [])) - set(row.get("remaining_words", [])))
        used_words.add(row["word"])

    word_pool = row.get("word_pool", [])
    remaining = [word for word in row.get("remaining_words", []) if word not in used_words]
    if remaining:
        word = remaining.pop(random.randrange(len(remaining)))
    else:
        try:
            fresh_pool = dictionary_words(row["category"], row["difficulty"])
        except (OSError, TimeoutError, ValueError):
            fresh_pool = []
        fresh_pool = [item for item in fresh_pool if item["word"] not in used_words]
        if not fresh_pool:
            return None
        selected = random.choice(fresh_pool)
        word = selected["word"]
        word_pool = [item["word"] for item in fresh_pool]
        remaining = [item for item in word_pool if item != word]

    used_words.add(word)
    return {
        "word": word,
        "category": row["category"],
        "difficulty": row["difficulty"],
        "translation": translate_word(word),
        "thai_hint": thai_hint(word, row["category"]),
        "_remaining_words": remaining,
        "_word_pool": word_pool,
        "_round_words": sorted(used_words),
    }


def advance_after_win(rows, row, game):
    archive_game(rows, row, game)
    selected = next_word(row, rows)
    if selected is None:
        storage.save(rows)
        return "ชนะแล้ว แต่ไม่มีคำถัดไปในหมวดนี้ กรุณาเริ่มเกมใหม่"
    rows.append({
        "type": "active",
        "player": row.get("player", "ผู้เล่น"),
        **{key: value for key, value in selected.items() if not key.startswith("_")},
        "remaining_words": selected.get("_remaining_words", []),
        "word_pool": selected.get("_word_pool", []),
        "round_words": selected.get("_round_words", [selected["word"]]),
        "round_hints_used": row.get("round_hints_used", 0),
        "last_result": {
            "word": row["word"],
            "translation": row.get("translation", "ไม่พบคำแปล"),
            "status": "won",
        },
        "guessed": [],
        "hint_letters": [],
        "wrong": 0,
        "status": "active",
        "score": 0,
        "deadline": time.time() + WORD_TIME_LIMITS.get(row["difficulty"], 60),
    })
    storage.save(rows)
    return "ชนะแล้ว! คำถัดไปเริ่มแล้ว"


def expire_game(rows, row):
    game = display_game(row)
    game.status = "lost"
    game.score = 0
    archive_game(rows, row, game)
    storage.save(rows)


def build():
    rows = storage.load()
    row = active_game(rows)
    if row and row.get("status", "active") == "active":
        if not row.get("deadline"):
            row["deadline"] = time.time() + WORD_TIME_LIMITS.get(row.get("difficulty"), 60)
            storage.save(rows)
        elif row["deadline"] <= time.time():
            expire_game(rows, row)
            row = None
    row = row or latest_game(rows)
    game = display_game(row) if row else None
    remaining_seconds = max(0, int(row["deadline"] - time.time() + 0.999)) if row and row.get("type") == "active" else 0
    if row and row.get("type") == "active":
        last_result = row.get("last_result")
        word_hint = row.get("thai_hint", thai_hint(row["word"], row["category"]))
    elif row:
        last_result = {
            "word": row["word"],
            "translation": row.get("translation", "ไม่พบคำแปล"),
            "status": row.get("status", "lost"),
        }
        word_hint = ""
    else:
        last_result = None
        word_hint = ""
    return {
        "game": game,
        "letters": list("abcdefghijklmnopqrstuvwxyz"),
        "max_wrong": 6,
        "categories": list(CATEGORIES),
        "difficulties": DIFFICULTIES,
        "can_hint": bool(game and set(game.word) - set(game.guessed) and row.get("round_hints_used", 0) < ROUND_HINT_LIMIT),
        "hint_limit": ROUND_HINT_LIMIT,
        "hints_used": row.get("round_hints_used", 0) if row else 0,
        "remaining_seconds": remaining_seconds,
        "deadline": row.get("deadline", 0) if row and row.get("type") == "active" else 0,
        "word_hint": word_hint,
        "last_result": last_result,
    }


def handle(form):
    rows = storage.load()
    action = form.get("action", "")
    if action == "start":
        category = form.get("category", "ทั้งหมด")
        difficulty = form.get("difficulty", "ง่าย")
        if category not in CATEGORIES and category != "ทั้งหมด":
            return "กรุณาเลือกหมวดหมู่ที่มีให้"
        if difficulty not in DIFFICULTIES:
            return "กรุณาเลือกระดับความยากที่มีให้"
        try:
            selected = choose_word(rows, category, difficulty)
        except (OSError, TimeoutError, ValueError):
            return "ซิงค์คำศัพท์ไม่สำเร็จ กรุณาตรวจสอบอินเทอร์เน็ตแล้วลองอีกครั้ง"
        if selected is None:
            return "หมวดนี้ไม่มีคำระดับที่เลือก กรุณาเลือกระดับอื่น"
        rows = [row for row in rows if row.get("type") != "active"]
        rows.append({
            "type": "active",
            "player": form.get("player", "ผู้เล่น").strip() or "ผู้เล่น",
            **{key: value for key, value in selected.items() if not key.startswith("_")},
            "remaining_words": selected.get("_remaining_words", []),
            "word_pool": selected.get("_word_pool", []),
            "round_words": [selected["word"]],
            "round_hints_used": 0,
            "guessed": [],
            "hint_letters": [],
            "wrong": 0,
            "status": "active",
            "score": 0,
            "deadline": time.time() + WORD_TIME_LIMITS.get(difficulty, 60),
        })
        storage.save(rows)
        return "เริ่มเกมใหม่แล้ว"
    if action in ("hint", "guess", "timeout"):
        row = active_game(rows)
        if row is None:
            return "กรุณาเริ่มเกมก่อน"
        if not row.get("deadline"):
            row["deadline"] = time.time() + WORD_TIME_LIMITS.get(row.get("difficulty"), 60)
        if row["deadline"] <= time.time():
            expire_game(rows, row)
            return "หมดเวลา เกมจบแล้ว"
        if action == "timeout":
            storage.save(rows)
            return "ยังมีเวลาเล่นอยู่"
    if action == "hint":
        if row.get("round_hints_used", 0) >= ROUND_HINT_LIMIT:
            return "ใช้คำใบ้ครบ 3 ครั้งของรอบนี้แล้ว"
        game = display_game(row)
        available = sorted(set(game.word) - set(game.guessed))
        if not available:
            return "ไม่มีตัวอักษรให้ใบ้แล้ว"
        letters_to_reveal = random.sample(available, random.randint(1, min(2, len(available))))
        row["round_hints_used"] = row.get("round_hints_used", 0) + 1
        for letter in letters_to_reveal:
            game.hint_letters.append(letter)
            game.guess(letter)
        if game.status == "won":
            return advance_after_win(rows, row, game)
        row.update(game.to_dict())
        row["type"] = "active"
        storage.save(rows)
        return "คำใบ้เปิดตัวอักษร " + ", ".join(letter.upper() for letter in letters_to_reveal)
    if action == "guess":
        game = display_game(row)
        result = game.guess(form.get("letter", ""))
        if result == "invalid":
            return "กรุณาเลือกตัวอักษรที่ยังไม่เคยทาย"
        if game.status == "won":
            return advance_after_win(rows, row, game)
        row.update(game.to_dict())
        if game.status == "lost":
            archive_game(rows, row, game)
            message = "เกมจบแล้ว ลองใหม่อีกครั้ง"
        else:
            row["type"] = "active"
            message = "ทายถูก" if result == "correct" else "ทายผิด"
        storage.save(rows)
        return message
    return "คำสั่งไม่ถูกต้อง"
