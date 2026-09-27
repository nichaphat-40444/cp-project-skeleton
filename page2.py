"""หน้าค้นหาประวัติการเล่น Hangman."""
import storage

TITLE = "ประวัติการเล่น"


def build(query):
    keyword = query.get("q", "").strip().lower()
    games = []
    for row in storage.load():
        if row.get("type") != "game":
            continue
        text = " ".join(str(row.get(field, "")) for field in ("player", "word", "category"))
        if keyword == "" or keyword in text.lower():
            games.append(row)
    games.reverse()
    return {"games": games, "keyword": keyword}
