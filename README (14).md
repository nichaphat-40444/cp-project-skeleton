# list — ตารางทุกรายการ

**แสดง:** ทุกแถวใน data.json เป็นตาราง พร้อมเลขลำดับและจำนวนรวม
**พื้นฐานที่ได้ใช้:** loop (`for item in items`)

**ปรับให้เป็นของกลุ่ม**
- เปลี่ยน `TITLE`
- ใน `page.html` เปลี่ยนหัวตารางและ `item.name / item.category / item.qty / item.price` เป็น field ของกลุ่ม
- อยากซ่อนบางแถว? เพิ่ม `if` ใน loop ของ `build()` ก่อน `append`

**ไอเดียต่อยอด:** เพิ่มคอลัมน์ "มูลค่า" = qty × price คำนวณใน loop
