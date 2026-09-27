# pytest — "หน้า 3 หน้าของเราเปิดได้ไหม" ในรูปแบบ test

```
pytest
```
ไฟล์ `test_pages.py` (ห้ามแก้) มี test 4 ตัว: page1, page2, page3 เปิดได้และไม่เหลือ TODO ในไฟล์ของหน้า, และ team.json กรอกแล้ว

## อ่านผล
```
test_pages.py ..F.                                   [100%]
FAILED test_pages.py::test_page_loads[page3] - AssertionError: /page3 is not built yet — see PAGES.md
```
- `.` = ผ่าน · `F` = ไม่ผ่าน · อ่านบรรทัด `FAILED ... - ` จะบอกว่าหน้าไหนและเพราะอะไร
- ทดสอบหน้าเดียว: `pytest -k page2`
- เขียวทั้งหมด = ส่วน "pages running" ใน check_project.py ได้ 30/30

pytest ทำงานโดยไม่ต้องเปิด `python app.py` ค้างไว้ (มันเรียกหน้าเว็บในหน่วยความจำ)

## ทดสอบฟอร์มของตัวเองจาก Python (ไม่ต้องเปิดเบราว์เซอร์, ไม่ต้อง curl)
```python
# test_mine.py  (ไฟล์ของกลุ่มเอง — ตั้งชื่ออะไรก็ได้ที่ขึ้นต้น test_)
from app import app
client = app.test_client()

def test_add_rejects_empty_name():
    r = client.post("/page2", data={"name": "", "price": "10"})
    assert "กรุณากรอก" in r.headers["Location"]        # ข้อความแถบเหลืองอยู่ใน URL ที่ redirect ไป

def test_upload():
    with open("static/img/book.svg", "rb") as f:
        r = client.post("/page2", data={"name": "Book", "price": "50", "photo": (f, "book.svg")},
                        content_type="multipart/form-data")
    assert r.status_code == 302
```
ใช้ `storage.reset()` ท้าย test เพื่อคืน data.json (ดู docs/tools/json-storage.md) · บน Windows อย่าใช้ `curl -F` กับภาษาไทย — มันเพี้ยน
บน Windows ถ้าเห็น `UnicodeEncodeError` ตอน print ภาษาไทย: ใช้ `run.bat` / `check.bat` ที่ตั้งค่าไว้ให้แล้ว หรือ `set PYTHONIOENCODING=utf-8` ก่อน
