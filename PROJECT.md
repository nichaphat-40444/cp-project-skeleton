# Computer Programming Project · 1309102 การเขียนโปรแกรมคอมพิวเตอร์

คณะวิศวกรรมศาสตร์ มหาวิทยาลัยอุบลราชธานี — โครงงานกลุ่ม 3 สัปดาห์ · กลุ่มละ 3–4 คน · Python + Flask · GitHub Copilot เป็นผู้ช่วย

## สร้างอะไร
เว็บไซต์เล็ก ๆ 3 หน้า (+ หน้าทีม) เกี่ยวกับเรื่องที่กลุ่มเลือกเอง ข้อมูลเก็บใน `data.json`
หัวข้อเป็นของกลุ่ม เช่น รายชื่อสมาชิกชมรม · เมนูร้านกาแฟ + ยอดขาย · อุปกรณ์ห้องแล็บ + ฟอร์มยืม · ร้านมือสอง + ตะกร้า ·
คลังบอร์ดเกม · บันทึกเซอร์วิสมอเตอร์ไซค์ · ทีมฟุตบอล + หน้าตัวจริง · รายรับรายจ่าย + แผนออม · ตารางคะแนนเกม

## เริ่มวันแรก (5 นาที)
| | Windows | macOS / Linux |
|---|---|---|
| ครั้งแรก: สร้าง `.venv` + ติดตั้ง (ไม่ต้องต่อเน็ต) | ดับเบิลคลิก `setup.bat` | `bash setup.sh` |
| รันเว็บ | `run.bat` → http://localhost:5000 | `bash run.sh` |
| ดูคะแนน + pytest | `check.bat` | `bash check.sh` |

เว็บรันได้ทันที: หน้าแรก, page1–3 (ยังว่าง), หน้าทีม (อ่านจาก `team.json`) · รายละเอียดใน `docs/tools/setup.md`

## ไฟล์ไหนแก้ได้
| ไฟล์ | สถานะ |
|---|---|
| `pages/page1.py` `page2.py` `page3.py` + `templates/page1.html` … | ★ งานของกลุ่ม — หน้าละ 1 คู่ |
| `models.py` | ★ class 1 ตัวของกลุ่ม |
| `data.json` `data.sample.json` `team.json` | ★ ข้อมูลของกลุ่ม (sample = สำเนาไว้คืนค่า) |
| `templates/home.html` `templates/team.html` `pages/team.py` `static/style.css` (ส่วนล่าง) `static/img/` `static/js/` | แก้ได้ตามใจ |
| `app.py` `storage.py` `templates/base.html` `templates/_not_built.html` `check_project.py` `test_pages.py` | **ห้ามแก้** — check_project ตรวจ |

## หน้าเว็บ 1 หน้า = ไฟล์ 2 ไฟล์
```python
# pages/page1.py
import storage
TITLE = "รายการอุปกรณ์"          # ชื่อในเมนู

def build():                     # ทำงานทุกครั้งที่เปิดหน้า → คืน dict ให้ page1.html ใช้
    items = storage.load()
    return {"items": items}

def handle(form):                # (ถ้ามีฟอร์ม) ทำงานตอนกด submit → return ข้อความ = แถบเหลือง
    ...
```
ไม่ต้องเขียน route, ไม่ต้องรู้จัก Flask — `app.py` จัดการให้ (รวมถึงอัปโหลดรูป) อ่านเพิ่มใน `docs/tools/flask-page.md`
**อย่าเริ่มจากศูนย์** — คัดลอกจาก `catalog/` (list, form, detail, search, stats, ranking, calculator, cart, gallery, text) แล้วดัดแปลง ผสมสองแบบได้

## วงจรทำงาน (ทำทีละหน้า)
1. เปิด `PAGES.md` ดูว่าหน้านี้ใครทำ แบบไหน
2. คัดลอก `catalog/<แบบ>/page.py` → `pages/pageN.py`, `page.html` → `templates/pageN.html`
3. แก้ให้เป็นของกลุ่ม (ชื่อ field ใน data.json, ข้อความ, หน้าตา) — ถาม Copilot ได้: `/new-page`
4. เปิด `localhost:5000/pageN` ดู → พังก็อ่านข้อความบนหน้า → `/explain-error`
5. `check.bat` → หน้านี้ ✓ แล้ว commit: `git commit -m "page1: รายการอุปกรณ์"`
6. ติ๊กใน `PAGES.md` → หน้าถัดไป

## กติกา
- **1 หน้า = 1 คน = 1 commit เป็นอย่างน้อย** — ทุกคนต้องปรากฏใน `git log`
- ข้อความ commit: `page1: <หน้านี้แสดงอะไร>` · `models: <ชื่อ class>` · `team: <อะไร>`
- ใช้ Copilot ได้เต็มที่ (นั่นคือหัวใจของโครงงาน) — **แต่ทุกบรรทัด Python ที่ commit ต้องอธิบายได้** เมื่ออาจารย์ถามในคาบ และตอนนำเสนอ
- **หน้าที่นับเป็นหน้า 1–3 ต้องมีงาน Python** = ใน `pages/pageN.py` มี loop หรือ if ที่ทำงานกับข้อมูล — หน้า `text` ล้วนไม่นับ (ใช้เป็นหน้า 4 ได้) · `check_project.py` เตือนให้
- **JavaScript** ไม่จำเป็น ถ้าหัวข้อต้องมีจริง ๆ (เกม, แอนิเมชัน) ใส่ใน `{% block scripts %}` หรือ `static/js/` — JS ไม่ได้คะแนน ไม่ต้องอธิบายทีละบรรทัด แต่หน้านั้นยังต้องมีงาน Python
- ใช้ standard library ของ Python ได้ (`datetime`, `random`, `math`) — ห้ามติดตั้ง package เพิ่ม
- ห้ามมีคำว่า `TODO` เหลือใน `pages/pageN.py` / `templates/pageN.html` / class ใน `models.py` (ในข้อมูล data.json มีได้)

## คะแนน (100)
| ส่วน | คะแนน | ใครให้ / อย่างไร |
|---|---|---|
| การทำงานเป็นทีม + การนำเสนอ | 40 | อาจารย์ ให้รายคน จากการสังเกตในคาบ + การนำเสนอ/วิดีโอ |
| หน้าเว็บทำงานได้ | 30 | อัตโนมัติ: page1, page2, page3 เปิดได้ ไม่เหลือ TODO — หน้าละ 10 |
| พื้นฐาน Python | 30 | อัตโนมัติ ใน `pages/page*.py` + `models.py`: if/else 7 · loop 7 · function 7 · class 9 |
| **รวม** | **100** | `check_project.py` แสดง 60 คะแนนอัตโนมัติ + คำเตือนที่อาจารย์จะดู |

โบนัส (อาจารย์พิจารณา): หน้า 4 ที่มีงาน Python, หน้าตาสวย, ไอเดียเด่น +5

## ไทม์ไลน์
| สัปดาห์ | ทำอะไร | จุดตรวจ |
|---|---|---|
| 0 · เตรียม (วันที่ ______) | `setup.bat`, `run.bat`, กรอก `team.json`, เห็นชื่อตัวเองที่ /team, commit + push | ภาพหน้าจอ /team ที่มีชื่อตัวเอง |
| 1 · วางแผน (วันที่ ______) | เลือกหัวข้อ, เขียน `data.json` 5–10 แถว (คัดลอกเป็น `data.sample.json`), แบ่งหน้าให้สมาชิก, กรอก `PAGES.md` | อาจารย์ดู data.json + PAGES.md อนุมัติ (5 นาที/กลุ่ม) |
| 2 · สร้าง (วันที่ ______) | page1 → page2 → page3 ทีละหน้า | กลางสัปดาห์: page1 ✓ และ commit แล้ว |
| 3 · เก็บงาน (วันที่ ______) | `models.py`, ขัดเกลา, หน้า 4 (ถ้ามี), เตรียมนำเสนอ | `check_project.py` 60/60 ไม่มี warning + นำเสนอ |

## ติดขัด? บันไดขอความช่วยเหลือ
1. อ่านข้อความบนหน้า "ยังไม่พร้อม" — มันบอกไฟล์และบรรทัด
2. ถาม Copilot: `/explain-error` (วาง error) — ให้มันอธิบายก่อน ค่อยขอวิธีแก้
3. ถามเพื่อนในกลุ่ม
4. ยกมือ — อาจารย์ช่วยปลดล็อก ไม่ใช่บรรยาย · นั่งติดเงียบ ๆ เกิน 30 นาทีคือสิ่งเดียวที่ผิด
