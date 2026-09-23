# detail — รายการเดียว ผ่าน class

**แสดง:** ข้อมูล 1 แถว เลือกด้วย `?i=0`, `?i=1`, … มีปุ่มก่อนหน้า/ถัดไป และประโยคจาก method ของ class
**พื้นฐานที่ได้ใช้:** class (`models.Item` → `.describe()`), if/else (ตรวจ index)

**กลไก:** `build(query)` — ถ้า `build` รับ parameter 1 ตัว app.py จะส่ง dict ของสิ่งที่อยู่หลัง `?` ใน URL มาให้

**ปรับให้เป็นของกลุ่ม**
- แก้ class ใน `models.py` ให้มี field ของกลุ่ม แล้วส่งค่าให้ครบตอน `models.Item(...)`
- ให้ `describe()` พูดอะไรที่มีประโยชน์ เช่น "Multimeter ราคา 850 บาท เหลือ 12 ชิ้น"

**ไอเดียต่อยอด:** ลิงก์จากหน้า list มาหน้านี้: `<a href="/page2?i={{ loop.index0 }}">`
