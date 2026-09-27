# git — 4 คำสั่งที่ใช้ตลอดโครงงาน

```
git pull                              # 1 · ดึงงานเพื่อนมาก่อนเริ่มทำ (ทุกครั้ง!)
git add -A                            # 2 · เลือกทุกไฟล์ที่แก้
git commit -m "page1: รายการอุปกรณ์"   # 3 · บันทึกพร้อมข้อความ
git push                              # 4 · ส่งขึ้น GitHub
```
ไม่มี branch ไม่มี merge — ทำงานคนละหน้า คนละไฟล์ จะไม่ชนกัน
`.venv/` ไม่ถูก commit (อยู่ใน .gitignore) — เพื่อนที่ clone ไปต้องรัน `setup.bat` เองครั้งเดียว

## ข้อความ commit
| ทำอะไร | เขียนว่า |
|---|---|
| หน้า | `page1: รายการอุปกรณ์` · `page2: ฟอร์มเพิ่ม` |
| class | `models: Equipment class` |
| ทีม/ข้อมูล | `team: members filled` · `data: 10 rows` |
| แก้บั๊ก | `fix: page3 average when empty` |

## กติกา
- **1 หน้า = 1 คน = อย่างน้อย 1 commit** — อาจารย์ดู `git log` ว่าใครทำอะไร
- ตั้งชื่อผู้ใช้ให้ถูกก่อน commit ครั้งแรกบนเครื่องนั้น:
  `git config --global user.name "ชื่อจริง"` · `git config --global user.email "อีเมล ม."`
- commit ทันทีที่หน้าเปิดได้ ไม่ต้องรอสวย

## ผิดบ่อย
| อาการ | ทำอย่างไร |
|---|---|
| `push` ถูกปฏิเสธ (rejected) | เพื่อน push ก่อน → `git pull` แล้ว `git push` ใหม่ |
| แก้ data.json ชนกัน (CONFLICT) | เปิดไฟล์ ลบบรรทัด `<<<<<<<` `=======` `>>>>>>>` ให้เหลือข้อมูลที่ถูก → `git add -A` → `git commit` |
| อยากย้อนไฟล์เดียวกลับ | `git checkout -- data.json` |
| ดูว่าใคร commit อะไร | `git log --oneline` |
