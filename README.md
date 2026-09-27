# catalog/ — แบบหน้าเว็บสำเร็จรูป ให้คัดลอกไปใช้

ทุกแบบมี 3 ไฟล์: `page.py` (Python), `page.html` (หน้าเว็บ), `README.md` (วิธีใช้)
ทุกแบบเขียนกับข้อมูลตัวอย่างใน `data.json` (name, category, qty, price) — เปลี่ยนชื่อ field ให้ตรงกับของกลุ่ม

| แบบ | แสดงอะไร | พื้นฐานที่ได้ใช้ |
|---|---|---|
| `list` | ตารางทุกรายการใน data.json | loop |
| `form` | ฟอร์มเพิ่มรายการ + ตรวจข้อมูล + ปุ่มลบต่อแถว | if/else, function |
| `detail` | รายการเดียว เลือกด้วย `?i=` ผ่าน class | class |
| `search` | ช่องค้นหา → ตารางที่กรองแล้ว | loop + if |
| `stats` | นับ, รวม, เฉลี่ย, มากสุด, น้อยสุด + กราฟแท่ง | loop + สะสมค่า |
| `ranking` | เรียงลำดับตามตัวเลข (ไม่ใช้ sorted) | loop ซ้อน |
| `calculator` | ใส่ตัวเลข → loop คำนวณ → ตาราง + กราฟ (ออม, กู้, แปลงหน่วย) | loop, if, function |
| `cart` | หยิบของ/เลือก → สรุปราคาหรือจำนวน (สถานะข้ามหน้า) | loop, if, function |
| `gallery` | รูปจาก static/img/ + อัปโหลดรูป | loop, if |
| `text` | หน้าข้อความล้วน (เกี่ยวกับเรา / กติกา) | ไม่มี — ใช้เป็นหน้า 4 ได้ **ไม่นับเป็นหน้า 1–3** |

หน้าที่นับเป็นหน้า 1–3 ต้องมี **งาน Python** = ใน `pages/pageN.py` มี loop หรือ if อย่างน้อยหนึ่งอย่างที่ทำงานกับข้อมูล
(`check_project.py` จะเตือนถ้าไม่มี)

## วิธีใช้ (ตัวอย่าง: ทำ page1 เป็นหน้า list)
1. คัดลอก `catalog/list/page.py` → `pages/page1.py`
2. คัดลอก `catalog/list/page.html` → `templates/page1.html`
3. แก้ `TITLE` และชื่อ field ให้ตรงกับ data.json ของกลุ่ม
4. เปิด `localhost:5000/page1` → แก้จนพอใจ → `python check_project.py` → commit

ผสมสองแบบได้ (เช่น การ์ดจาก `cart` + ช่องค้นหาจาก `search`) — เริ่มจากแบบที่ใกล้ที่สุดแล้วค่อยเติม
หรือถาม Copilot ใน Chat: `/new-page`
