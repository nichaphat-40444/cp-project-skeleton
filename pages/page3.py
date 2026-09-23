"""หน้าสรุปคะแนนและตารางอันดับผู้เล่น."""
import storage

TITLE = "สถิติและอันดับ"


def build():
    games = [row for row in storage.load() if row.get("type") == "game"]
    players = {}
    wins = 0
    total_score = 0
    for game in games:
        player = game.get("player", "ผู้เล่น")
        players[player] = players.get(player, 0) + game.get("score", 0)
        total_score += game.get("score", 0)
        if game.get("status") == "won":
            wins += 1
    ranking = sorted(players.items(), key=lambda item: item[1], reverse=True)
    return {"games": games, "ranking": ranking, "total_games": len(games), "wins": wins, "total_score": total_score}
