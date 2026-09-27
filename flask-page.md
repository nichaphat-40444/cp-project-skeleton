# flask-page — หน้าเว็บ 1 หน้าทำงานอย่างไร

ในโปรเจกต์นี้ **ไม่ต้องเขียน Flask เอง** — `app.py` (ห้ามแก้) ทำให้ทุกไฟล์ใน `pages/` กลายเป็นหน้าเว็บ

```
pages/page1.py  +  templates/page1.html   →   http://localhost:5000/page1
```

## ไฟล์ Python ของหน้า ต้องมีอะไร
```python
import storage

TITLE = "รายการอุปกรณ์"      # ชื่อที่โชว์ในเมนู

def build():                 # ทำงานทุกครั้งที่มีคนเปิดหน้า
    items = storage.load()   # อ่าน data.json
    ...                      # คำนวณอะไรก็ได้ตรงนี้: loop, if, นับ, รวม
    return {"items": items}  # ทุก key ใน dict → ตัวแปรใน page1.html
```

## ถ้าหน้าต้องรับค่าจาก URL (เช่น ?q=arduino หรือ ?months=12)
```python
def build(query):            # เพิ่ม parameter 1 ตัว → app.py ส่ง dict ของค่าหลัง ? มาให้
    keyword = query.get("q", "")          # ค่าเป็น "ข้อความ" เสมอ
    months = int(query.get("months", "12"))   # ตัวเลขต้องแปลงเอง (ดู catalog/calculator)
```
ใน html ใช้ `<form method="get">` → ค่าไปอยู่ใน URL

## ถ้าหน้ามีฟอร์ม (กด submit แล้วเปลี่ยนข้อมูล)
```python
def handle(form):            # form = dict; key = name="..." ของแต่ละช่องใน html
    name = form.get("name", "")           # ใช้ .get เสมอ — ช่องที่ไม่ถูกส่งมาจะไม่มี key
    if name == "":
        return "✗ กรุณากรอกชื่อ"           # ข้อความที่ return จะโชว์เป็นแถบเหลืองด้านบน
    items = storage.load()
    items.append({"name": name})
    storage.save(items)
    return "✓ บันทึกแล้ว"
```
ใน html: `<form method="post">` ส่งมาที่ `handle` — หลังจากนั้น app.py พากลับมาหน้าเดิม (รวม `?q=` ที่ค้างอยู่ — อาศัยเบราว์เซอร์ส่ง Referer; ถ้าทดสอบด้วย curl จะกลับมาที่ `/pageN` เฉย ๆ) พร้อมแถบเหลือง
หลายปุ่มในหน้าเดียว? ทุกปุ่มเป็นฟอร์มเล็ก ๆ ส่ง `<input type="hidden" name="action" value="delete">` แล้วใน `handle` ใช้ `if form.get("action") == "delete":` (ดู catalog/form, catalog/cart)

## แถบเหลืองจาก build() ก็ได้
`return {"items": items, "notice": "แสดงแค่ 20 รายการแรก"}` — key ชื่อ `notice` ขึ้นเป็นแถบเหลืองอัตโนมัติ

## อัปโหลดรูป
```html
<form method="post" enctype="multipart/form-data">
  <input type="file" name="photo" accept="image/*">
```
app.py บันทึกไฟล์ลง `static/img/` ให้เอง แล้ว `form["photo"]` = ชื่อไฟล์ที่บันทึก (หรือ `""` ถ้าไม่ได้เลือก/ไม่ใช่รูป) — ดู catalog/gallery
เก็บชื่อไฟล์ลง data.json แล้วแสดงด้วย `url_for('static', filename='img/' + item.image)`
ถ้า `handle()` ปฏิเสธฟอร์ม (ไม่ได้บันทึกชื่อไฟล์ลง data.json) app.py จะลบไฟล์ที่เพิ่งอัปโหลดทิ้งให้เอง — ไม่มีไฟล์ค้าง

## กับดักที่เจอบ่อย
| อาการ | สาเหตุ / ทางแก้ |
|---|---|
| `KeyError: 'x'` ใน handle | ช่องนั้นไม่ถูกส่งมา (radio/checkbox ไม่ได้ติ๊ก, input ที่ `disabled`) → ใช้ `form.get("x", "")` และใช้ `readonly` แทน `disabled` |
| ตัวแปรบนหัวไฟล์ (`cart = []`) กลับเป็นค่าเดิมทุกครั้ง | app.py โหลดไฟล์หน้าใหม่ทุกคลิก — ค่าใน .py ไม่จำ ต้องเก็บใน data.json (ดู catalog/cart) |
| ตัวเลขจากฟอร์มบวกกันเป็นข้อความ (`"1"+"2"="12"`) | ค่าจากฟอร์ม/URL เป็น str เสมอ → `int()` / `float()` ใน `try/except` |
| กด refresh แล้วแถบเหลืองยังอยู่ | ข้อความอยู่ใน URL (`?msg=`) — ปกติ ลบออกจาก URL ได้ |
| หน้าขึ้น "ยังไม่พร้อม" | อ่านเหตุผลและบรรทัดล่างสุดของ traceback แล้วถาม Copilot `/explain-error` |

แก้ไฟล์แล้ว **แค่ refresh** ไม่ต้องรัน `python app.py` ใหม่

## JavaScript
ไม่จำเป็นสำหรับโปรเจกต์นี้ ถ้าหัวข้อต้องมี (เกม, แอนิเมชัน) ให้ใส่ใน `{% block scripts %}` ท้าย html ของหน้า หรือไฟล์ `static/js/pageN.js`
กติกา: JS **ไม่ได้คะแนน** และไม่ต้องอธิบายทีละบรรทัด แต่หน้านั้นยังต้องมีงาน Python (loop/if กับ data.json) จึงจะนับเป็นหน้า 1–3 — ดู PROJECT.md
**JS ส่งผลให้ Python อย่างไร:** ไม่มี API พิเศษ — ให้ JS เติมค่าลง `<input>` ของฟอร์มธรรมดา (เช่น คะแนน) แล้วผู้ใช้กด submit → `handle(form)` ตรวจและบันทึกตามปกติ (ใช้ `readonly` ไม่ใช่ `disabled`)

## อื่น ๆ
- เพิ่มหน้า 4: สร้าง `pages/page4.py` + `templates/page4.html` — เมนูเพิ่มให้เอง
- เปลี่ยน port (เครื่องเดียวรันสองโปรเจกต์): `python app.py 5001`
- ใช้ standard library ของ Python ได้ (`datetime`, `random`, `math`) — ที่ห้ามคือ package ที่ต้อง pip ติดตั้งเพิ่ม
