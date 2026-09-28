"""หน้าสรุปผลเกมและให้ผู้เล่นเลือกเล่นต่อหรือจบการเล่น."""
import storage

TITLE = "สรุปผลเกม"


def build():
    games = [row for row in storage.load() if row.get("type") == "game"]
    latest_game = games[-1] if games else None
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
    return {
        "latest_game": latest_game,
        "games": list(reversed(games[-5:])),
        "ranking": ranking,
        "total_games": len(games),
        "wins": wins,
        "total_score": total_score,
        "total_players": len(players),
    }
