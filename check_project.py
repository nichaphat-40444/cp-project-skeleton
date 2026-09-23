"""check_project.py — GIVEN, DO NOT EDIT.   Run anytime:  python check_project.py

Prints the automated part of your grade (60 of 100):
  pages running      30   page1, page2, page3 each load without error and their source has no TODO left
  Python foundations 30   if/else 7 · loop 7 · function 7 · class 9   found in pages/page*.py + models.py
The other 40 (teamwork + presentation) is given by your teacher.

Also prints WARNINGS that cost no points here but that your teacher will look at:
  - a page whose Python has no loop and no if (may not count as one of pages 1–3)
  - a handle(form) that crashes on an empty form
  - a given file that was edited
"""
import ast
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REQUIRED_PAGES = ["page1", "page2", "page3"]
GIVEN_FILES = ["app.py", "storage.py", "check_project.py", "test_pages.py",
               "templates/base.html", "templates/_not_built.html"]
HASH_FILE = os.path.join(HERE, ".given_hashes.json")
NOT_BUILT_MARK = "ยังไม่พร้อม"
POINTS = {"if": 7, "loop": 7, "function": 7, "class": 9}


def sha(rel):
    with open(os.path.join(HERE, *rel.split("/")), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def mark(ok):
    return "✓" if ok else "✗"


def read(rel):
    with open(os.path.join(HERE, *rel.split("/")), encoding="utf-8") as f:
        return f.read()


def student_python_files():
    files = ["models.py"]
    for name in sorted(os.listdir(os.path.join(HERE, "pages"))):
        if name.startswith("page") and name.endswith(".py"):
            files.append("pages/" + name)
    return files


def source_has_todo(name):
    """TODO left in the page's own source files (not in data, not in rendered output)."""
    for rel in ["pages/" + name + ".py", "templates/" + name + ".html"]:
        p = os.path.join(HERE, *rel.split("/"))
        if os.path.exists(p) and "TODO" in read(rel):
            return True
    return False


def page_constructs(name):
    """(has_loop_or_if, has_handle, handle_crash_text) for pages/<name>.py"""
    rel = "pages/" + name + ".py"
    p = os.path.join(HERE, *rel.split("/"))
    if not os.path.exists(p):
        return False, False, ""
    try:
        tree = ast.parse(read(rel))
    except Exception:
        return False, False, ""
    logic = any(isinstance(n, (ast.If, ast.For, ast.While)) for n in ast.walk(tree))
    has_handle = any(isinstance(n, ast.FunctionDef) and n.name == "handle" for n in ast.walk(tree))
    crash = ""
    if has_handle:
        import app as webapp
        module, err = webapp.load_page(name)
        if module is not None:
            try:
                module.handle({})
            except NotImplementedError:
                crash = "handle() is still a TODO"
            except Exception as e:
                crash = type(e).__name__ + ": " + str(e)[:60]
            finally:
                # handle({}) may have written data — put the sample back if one exists
                try:
                    import storage
                    storage.reset()
                except Exception:
                    pass
    return logic, has_handle, crash


# ---------- pages running ----------
def check_pages():
    import app as webapp
    client = webapp.app.test_client()
    rows, warnings = [], []
    total = 0
    all_pages = webapp.page_names()
    for name in REQUIRED_PAGES + [p for p in all_pages if p not in REQUIRED_PAGES and p != "team"]:
        required = name in REQUIRED_PAGES
        try:
            r = client.get("/" + name)
            html = r.get_data(as_text=True)
            status = r.status_code
        except Exception as e:
            html, status = "", "crash: " + type(e).__name__
        loads = status == 200 and NOT_BUILT_MARK not in html
        todo = source_has_todo(name)
        note = ""
        if status != 200:
            note = "HTTP " + str(status)
        elif NOT_BUILT_MARK in html:
            start = html.find('class="reason">')
            note = html[start + 15: html.find("<", start + 15)].strip() if start > 0 else "not built"
        elif todo:
            note = "TODO still in pages/" + name + ".py or templates/" + name + ".html"
        ok = loads and not todo
        pts = 10 if ok else 0
        if required:
            total += pts
            rows.append((name, mark(ok), note, f"{pts}/10"))
        else:
            rows.append((name, mark(ok), note or "extra page", "bonus"))
        if loads:
            logic, has_handle, crash = page_constructs(name)
            if not logic:
                warnings.append(f"/{name}: no loop and no if in pages/{name}.py — a page with no Python work may not count as one of pages 1–3")
            if crash:
                warnings.append(f"/{name}: handle() crashes on an empty form ({crash}) — use form.get(...) and check values")
    return rows, total, warnings


# ---------- foundations ----------
def check_foundations():
    found = {"if": [], "loop": [], "function": [], "class": []}
    class_details = []
    import_errors = []
    for rel in student_python_files():
        try:
            src = read(rel)
            tree = ast.parse(src)
        except Exception as e:
            import_errors.append(f"{rel}: {type(e).__name__}: {e}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                found["if"].append(rel)
            elif isinstance(node, (ast.For, ast.While)):
                found["loop"].append(rel)
            elif isinstance(node, ast.FunctionDef) and node.name != "__init__":
                found["function"].append(rel + ":" + node.name)
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                if "__init__" in methods and len(methods) >= 2:
                    still_todo = "TODO" in ast.get_source_segment(src, node)
                    class_details.append((rel, node.name, len(methods) - 1, still_todo))
                    if not still_todo:
                        found["class"].append(rel + ":" + node.name)

    def uniq(xs):
        out = []
        for x in xs:
            if x not in out:
                out.append(x)
        return out

    rows = []
    total = 0
    labels = {"if": "if / else", "loop": "loop (for / while)", "function": "function (def)", "class": "class + method"}
    for key in ["if", "loop", "function", "class"]:
        where = uniq(found[key])
        ok = len(where) > 0
        pts = POINTS[key] if ok else 0
        total += pts
        if key == "class" and not ok and class_details:
            rel, name, _, _ = class_details[0]
            note = f"{rel} {name} still has a TODO — finish it"
        elif key == "class" and ok:
            note = ", ".join(where)
        elif key == "function":
            note = f"{len(where)} found" if ok else "no def found"
        else:
            note = ", ".join(where[:3]) + (" …" if len(where) > 3 else "") if ok else "none found"
        rows.append((labels[key], mark(ok), note, f"{pts}/{POINTS[key]}"))
    return rows, total, import_errors


# ---------- given files ----------
def check_given():
    if not os.path.exists(HASH_FILE):
        return None, [], []
    expected = json.load(open(HASH_FILE))
    changed, checked = [], []
    for rel, h in expected.items():
        rel = rel.replace("\\", "/")
        p = os.path.join(HERE, *rel.split("/"))
        if not os.path.exists(p):
            changed.append(rel + " (missing)")
        elif sha(rel) != h:
            changed.append(rel)
        else:
            checked.append(rel.split("/")[-1])
    return True, changed, checked


def main():
    group = "?"
    try:
        group = json.load(open(os.path.join(HERE, "team.json"), encoding="utf-8"))["group"]["name"]
    except Exception:
        pass

    print(f"check_project · {group}")
    page_rows, page_total, warnings = check_pages()
    print("  pages running")
    for name, m, note, pts in page_rows:
        print(f"    /{name:<8} {m}  {note:<52} {pts:>6}")
    print(f"    {'':<9}    {'':<52} {page_total:>3}/30")

    f_rows, f_total, errors = check_foundations()
    print("  Python foundations (pages/page*.py + models.py)")
    for label, m, note, pts in f_rows:
        print(f"    {label:<20} {m}  {note:<40} {pts:>6}")
    for e in errors:
        print(f"    ! cannot read: {e}")
    print(f"    {'':<20}    {'':<40} {f_total:>3}/30")

    has_hashes, changed, checked = check_given()
    if has_hashes is None:
        print("  given files ............ (no .given_hashes.json — skipped)")
    else:
        shown = ", ".join(changed) if changed else ", ".join(checked)
        print(f"  given files unchanged .. {mark(not changed)}  {shown}")
        if changed:
            warnings.append("given files were edited: " + ", ".join(changed) + " — restore them from the original skeleton")

    score = page_total + f_total
    print("  " + "-" * 64)
    print(f"  automated score: {score} / 60   (+ teamwork & presentation 40, from your teacher)")
    if warnings:
        print("  warnings (no points lost here, but your teacher will see them)")
        for w in warnings:
            print(f"    ! {w}")
    return 0 if score == 60 else 1


if __name__ == "__main__":
    if "--write-hashes" in sys.argv:
        json.dump({rel: sha(rel) for rel in GIVEN_FILES if os.path.exists(os.path.join(HERE, *rel.split("/")))},
                  open(HASH_FILE, "w"), indent=1)
        print("hashes written to .given_hashes.json")
        sys.exit(0)
    sys.exit(main())
