# setup — ติดตั้งครั้งเดียว แล้วรันได้ทุกวัน

ต้องมี **Python 3.12 ขึ้นไป** ในเครื่อง (ตรวจ: `python --version`) และ VS Code

## ครั้งแรก (สร้าง virtual environment + ติดตั้ง Flask/pytest)
| ระบบ | ทำ |
|---|---|
| Windows | ดับเบิลคลิก `setup.bat` (หรือใน terminal: `setup.bat`) |
| macOS / Linux | `bash setup.sh` |

สคริปต์จะสร้างโฟลเดอร์ `.venv/` (Python ส่วนตัวของโปรเจกต์นี้) แล้วติดตั้งจาก `wheels/` ที่แนบมาในซิป — **ไม่ต้องต่ออินเทอร์เน็ต** (ถ้า wheels ใช้ไม่ได้จะลองดาวน์โหลดให้)
`.venv/` อยู่ใน `.gitignore` แล้ว — ไม่ต้อง commit สมาชิกแต่ละคนรัน setup เองในเครื่องตัวเอง

## ทุกวัน
| ทำอะไร | Windows | macOS / Linux |
|---|---|---|
| รันเว็บ | `run.bat` → เปิด http://localhost:5000 | `bash run.sh` |
| ดูคะแนน + pytest | `check.bat` | `bash check.sh` |
| ใช้คำสั่ง python เอง | `.venv\Scripts\activate` แล้ว `python app.py` | `source .venv/bin/activate` แล้ว `python app.py` |

VS Code: เปิดโฟลเดอร์โปรเจกต์ → มุมล่างขวาเลือก interpreter เป็น `.venv` (VS Code มักถามให้เอง) → terminal ใน VS Code จะ activate ให้อัตโนมัติ

## ถ้าพัง
| อาการ | ทำอย่างไร |
|---|---|
| `python` ไม่ใช่คำสั่ง | ติดตั้ง Python จาก python.org ติ๊ก "Add python.exe to PATH" · บน Mac ลอง `python3` |
| `No module named flask` | ยังไม่ได้ activate `.venv` หรือยังไม่ได้รัน setup |
| port 5000 ถูกใช้แล้ว | `python app.py 5001` (แล้วเปิด localhost:5001) |
| อยากเริ่มใหม่ | ลบโฟลเดอร์ `.venv/` แล้วรัน setup อีกครั้ง |
