# stats — นับ / รวม / เฉลี่ย / มากสุด / น้อยสุด + กราฟแท่ง

**แสดง:** การ์ดตัวเลข 4 ใบ, กราฟแท่งแนวนอนตามหมวด, ตารางแพงสุด-ถูกสุด
**พื้นฐานที่ได้ใช้:** loop + การสะสมค่า (`total = total + ...`), if/else (หา max/min, กันหารศูนย์), dict

**กราฟแท่งทำอย่างไร**
1. หาค่าที่มากที่สุด (`biggest`) ด้วย loop
2. แต่ละแถว: `percent = value * 100 / biggest`
3. ใน html: `<div class="bar-fill" style="width: {{ b.percent }}%">` — ใช้ class `.bar-row / .bar-track / .bar-fill` ที่มีให้ใน style.css
อย่าใช้ pixel จากค่าจริง (`width: {{ value }}px`) — เงิน 50,000 บาทจะได้แท่งยาว 50,000 px
กราฟแท่งแนวตั้ง: class `.chart / .col` (สูง = percent) — ดู `docs/tools/jinja.md`

**ปรับให้เป็นของกลุ่ม**
- เปลี่ยน field ตัวเลขที่รวม (`qty`, `price`) เป็นของกลุ่ม เช่น `goals`, `amount`, `score`
- เปลี่ยน field ที่จัดกลุ่ม (`category`) เป็นของกลุ่ม
- ไม่มี field ตัวเลข? เพิ่มใน data.json ก่อน — หน้าสถิติต้องมีอะไรให้นับ
