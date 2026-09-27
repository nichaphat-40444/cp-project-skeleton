# json-storage — ข้อมูลของกลุ่มอยู่ใน data.json

ไม่มีฐานข้อมูล ข้อมูลทั้งหมดคือ **list ของ dict** ในไฟล์ `data.json` เปิดดู/แก้ใน VS Code ได้เลย

```json
[
  {"name": "Multimeter", "category": "measure", "qty": 12, "price": 850},
  {"name": "Arduino Uno", "category": "board", "qty": 30, "price": 390, "image": "arduino.svg"}
]
```

## ใน Python ใช้แค่ 2 ฟังก์ชัน (จาก storage.py — ห้ามแก้)
```python
import storage
items = storage.load()          # → list ของ dict
items.append({"name": "Breadboard", "category": "tool", "qty": 40, "price": 60})
storage.save(items)             # เขียนกลับลงไฟล์ (จัดรูปแบบสวย ๆ ให้)
```

## data.sample.json = ข้อมูลตั้งต้นสำรอง
ทดสอบจนข้อมูลเละ? `python -c "import storage; storage.reset()"` หรือคัดลอก `data.sample.json` ทับ `data.json`
เมื่อออกแบบข้อมูลของกลุ่มเสร็จ **และรันเว็บบันทึกอะไรสักครั้ง** (`storage.save()` จัดรูปแบบไฟล์ใหม่) ให้คัดลอก data.json ไปเป็น data.sample.json (`check_project.py` ก็ใช้มันคืนค่าหลังทดสอบฟอร์ม)

## กติกาออกแบบ data.json (สัปดาห์ที่ 1)
- ทุกแถวมี field ชุดเดียวกัน 3–7 field
- มี field ตัวเลขอย่างน้อย 1 ตัว (ราคา, จำนวน, คะแนน, ประตู) — หน้า stats/ranking ต้องมีอะไรให้นับ
- มี field ข้อความอย่างน้อย 1 ตัว (ชื่อ) — หน้า search ต้องมีอะไรให้ค้น
- field สถานะ (`"picked": true`, `"status": "sold"`) ใช้เก็บสิ่งที่ผู้ใช้เลือกข้ามหน้า (ดู catalog/cart)
- รูป: `"image": "book.svg"` → ไฟล์ใน `static/img/` (มีไอคอนตัวอย่าง 13 ไฟล์)
- เริ่มด้วย 5–10 แถวที่พิมพ์เอง · ไม่มี id — ใช้ตำแหน่งใน list (`items[3]`) แล้วประทับ `item["no"]` ใน `build()` เมื่อต้องส่งกลับมาในฟอร์ม

## ผิดบ่อย
| อาการ | สาเหตุ |
|---|---|
| หน้าขึ้น `JSONDecodeError` | ลูกน้ำเกินท้ายแถวสุดท้าย, ลืมปิด `}` หรือ `]`, ใช้ `'` แทน `"` |
| `KeyError: 'price'` | บางแถวไม่มี field นี้ หรือสะกดต่างกัน (`Price` ≠ `price`) → `item.get("price", 0)` |
| `TypeError: ... str and int` | เก็บตัวเลขเป็นข้อความ `"850"` แทน `850` |
| ลบแถวแล้วแถวอื่นเลื่อน | ตำแหน่งใน list เปลี่ยน — ส่ง `item.no` ที่ประทับใน `build()` ไม่ใช่ `loop.index0` ของตารางที่ `|reverse` |
| ข้อมูลหาย | `storage.reset()` หรือ `git checkout data.json` |
