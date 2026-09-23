"""storage.py — GIVEN, DO NOT EDIT.

Your data lives in data.json as a list of dicts. Two functions:

    items = storage.load()      # read the list  (empty list if the file is missing)
    storage.save(items)         # write the list back, nicely formatted

Open data.json in VS Code to see or edit the data by hand.
Broke it while testing?  storage.reset()  copies data.sample.json back over data.json
(or just copy the file yourself).
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "data.json")
SAMPLE_FILE = os.path.join(HERE, "data.sample.json")


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def reset():
    """Put data.json back to data.sample.json (your own starting data — keep it updated)."""
    if os.path.exists(SAMPLE_FILE):
        shutil.copyfile(SAMPLE_FILE, DATA_FILE)
        return True
    return False
