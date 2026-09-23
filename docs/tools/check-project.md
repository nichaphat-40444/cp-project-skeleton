# check-project — ดูคะแนนอัตโนมัติของกลุ่มได้ตลอดเวลา

```
python check_project.py
```
```
check_project · Group 3
  pages running
    /page1    ✓                                                          10/10
    /page2    ✓                                                          10/10
    /page3    ✗  build() ยังเป็น TODO                                      0/10
                                                                         20/30
  Python foundations (pages/page*.py + models.py)
    if / else            ✓  pages/page2.py                                 7/7
    loop (for / while)   ✓  pages/page1.py, pages/page2.py                 7/7
    function (def)       ✓  6 found                                        7/7
    class + method       ✗  models.py Item still has a TODO — finish it    0/9
                                                                         21/30
  given files unchanged .. ✓  app.py, storage.py, check_project.py, test_pages.py, base.html, _not_built.html
  ----------------------------------------------------------------
  automated score: 41 / 60   (+ teamwork & presentation 40, from your teacher)
  warnings (no points lost here, but your teacher will see them)
    ! /page2: handle() crashes on an empty form (KeyError: 'name') — use form.get(...) and check values
```

## แต่ละบรรทัดหมายความว่า
| บรรทัด | ได้คะแนนเมื่อ |
|---|---|
| `/pageN` | เปิดหน้าแล้วได้ HTTP 200, ไม่ใช่หน้า "ยังไม่พร้อม", และไม่มีคำว่า `TODO` เหลือใน `pages/pageN.py` หรือ `templates/pageN.html` (ข้อมูลใน data.json มี TODO ได้ ไม่เป็นไร) |
| `if / else` | มี `if` ที่ไหนก็ได้ใน `pages/page*.py` หรือ `models.py` |
| `loop` | มี `for` หรือ `while` |
| `function (def)` | มี `def` (นอกจาก `__init__`) |
| `class + method` | มี class ที่มี `__init__` + method อีก 1 และไม่เหลือ TODO ใน class |
| `given files unchanged` | ไฟล์ห้ามแก้ยังเหมือนเดิม — ถ้า ✗ อาจารย์จะดู |

## warnings — ไม่หักคะแนนอัตโนมัติ แต่อาจารย์เห็น
| เตือนว่า | หมายความว่า |
|---|---|
| `no loop and no if in pages/pageN.py` | หน้านี้ไม่มีงาน Python → **อาจไม่นับเป็นหน้า 1–3** (เช่น หน้า text ล้วน) ใส่ loop หรือ if ที่ทำงานกับข้อมูลจริง |
| `handle() crashes on an empty form` | ส่งฟอร์มเปล่ามาแล้วพัง (มักเป็น `KeyError`) → ใช้ `form.get("x", "")` และตรวจค่าก่อนใช้ |
| `given files were edited` | คืนไฟล์จาก skeleton ต้นฉบับ |

หน้า 4 ขึ้นไปแสดงเป็น `bonus` ไม่นับคะแนนอัตโนมัติ (อาจารย์พิจารณาเอง)
`pytest` ทำสิ่งเดียวกับส่วน "pages running" ในรูปแบบ test 4 ตัว
