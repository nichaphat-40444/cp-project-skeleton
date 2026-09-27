"""pages/team.py — the team page. Already works: it shows team.json.

Week 0 task: open team.json, put in your group name, topic, and every member's
name / student id / role / task. Then look at /team. You may also change this file
and templates/team.html to make the page your own.
"""
import json
import os

TITLE = "ทีม"

TITLES = ["นางสาว", "นาย", "นาง", "ว่าที่ร้อยตรี", "Mr.", "Ms.", "Miss"]


def initial_of(name):
    """First letter of the given name, skipping Thai/English titles."""
    name = name.strip()
    for t in TITLES:
        if name.startswith(t):
            name = name[len(t):].strip()
    if name == "":
        return "?"
    return name[0]


def build():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "team.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    members = []
    for m in data["members"]:
        m["initial"] = initial_of(m["name"])
        members.append(m)
    return {"group": data["group"], "members": members, "count": len(members)}
