# models — class 1 ตัวของกลุ่ม (9 คะแนน)

`models.py` มี class ตั้งต้นชื่อ `Item` — เปลี่ยนให้เป็นของกลุ่ม

```python
class Equipment:                                          # ชื่อตรงหัวข้อ: Book, Player, Expense ...
    def __init__(self, name, category, qty, price):       # field เดียวกับแถวใน data.json
        self.name = name
        self.category = category
        self.qty = qty
        self.price = price

    def total_value(self):                                # method 1 ตัวที่มีประโยชน์
        return self.qty * self.price

    def describe(self):                                   # จะมีมากกว่า 1 method ก็ได้
        if self.qty < 5:
            return self.name + " เหลือน้อย"
        return self.name + " มีพอ"
```

## ใช้ในหน้าเว็บ
```python
import models
for row in storage.load():
    e = models.Equipment(row["name"], row["category"], row["qty"], row["price"])
    total = total + e.total_value()
```
ดูตัวอย่างเต็มใน `catalog/detail/page.py` (สร้าง object 1 ตัว) — จะ loop สร้างทุกแถวแล้วรวมค่าก็ได้ (โค้ดข้างบน)

## เกณฑ์ที่ check_project.py ดู
- มี `class` ที่มี `__init__` + method อีกอย่างน้อย 1 ตัว
- **ไม่เหลือคำว่า TODO** ใน class (class ตั้งต้นมี TODO → 0/9 จนกว่าจะแก้)
- ควรมีอย่างน้อยหนึ่งหน้าที่ `import models` และใช้มันจริง (อาจารย์ดูตอนนำเสนอ)

## อย่าเพิ่ง
`@property`, `@staticmethod`, inheritance, dataclass, type hints — ยังไม่จำเป็น และ Copilot จะถูกบอกให้เลี่ยง
