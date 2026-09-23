"""test_pages.py — GIVEN, DO NOT EDIT.   Run:  pytest

Four tests: page1, page2, page3 each load (not a "not built yet" page, no TODO left in
their source), and team.json has been filled in.
This is the "pages running" part of check_project.py, in pytest form.
"""
import os

import pytest

import app as webapp

HERE = os.path.dirname(os.path.abspath(__file__))
NOT_BUILT_MARK = "ยังไม่พร้อม"


@pytest.fixture
def client():
    return webapp.app.test_client()


def _source(rel):
    with open(os.path.join(HERE, *rel.split("/")), encoding="utf-8") as f:
        return f.read()


@pytest.mark.parametrize("name", ["page1", "page2", "page3"])
def test_page_loads(client, name):
    r = client.get("/" + name)
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert NOT_BUILT_MARK not in html, f"/{name} is not built yet — see PAGES.md"
    assert "TODO" not in _source("pages/" + name + ".py"), f"pages/{name}.py still has a TODO"
    assert "TODO" not in _source("templates/" + name + ".html"), f"templates/{name}.html still has a TODO"


def test_team_page_filled(client):
    html = client.get("/team").get_data(as_text=True)
    assert "66xxxxxxx" not in html, "team.json still has the placeholder student ids"
