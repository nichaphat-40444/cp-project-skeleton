"""catalog/text — a plain content page (about us, rules, how-to).   Foundation: none

Good as a 4th page. It does NOT count as one of pages 1–3, because it has no Python work.
"""

TITLE = "เกี่ยวกับเรา"


def build():
    return {
        "updated": "2569-09-09",
        "sections": [
            {"heading": "เว็บนี้ทำอะไร", "body": "เขียนอธิบายสั้น ๆ ว่าเว็บของกลุ่มช่วยใคร ทำอะไร"},
            {"heading": "ข้อมูลมาจากไหน", "body": "เช่น พิมพ์เองจากรายการอุปกรณ์ในห้องแล็บ"},
            {"heading": "ทำต่อได้อย่างไร", "body": "ไอเดียหน้าถัดไปที่อยากทำ"},
        ],
    }
