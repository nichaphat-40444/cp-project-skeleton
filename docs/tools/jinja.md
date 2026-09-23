# jinja — เขียนหน้า HTML ให้แสดงข้อมูลจาก Python

ไฟล์ใน `templates/` เป็น HTML ที่มี "ช่อง" ให้ Python เติมค่า เรียกว่า Jinja template

## โครงทุกหน้า
```html
{% extends "base.html" %}          ← ใช้หัว/เมนู/ท้ายจาก base.html (ห้ามแก้ base)
{% block content %}
  ... เนื้อหาหน้าของเรา ...
{% endblock %}
{% block scripts %}                ← (ถ้าจำเป็น) <script> ของหน้านี้
{% endblock %}
```

## 3 อย่างที่ต้องรู้
| เขียน | ทำอะไร |
|---|---|
| `{{ title }}` | แสดงค่าตัวแปร (key จาก dict ที่ `build()` return) |
| `{% for item in items %} … {% endfor %}` | วนแสดงทีละแถว |
| `{% if count == 0 %} … {% else %} … {% endif %}` | แสดงตามเงื่อนไข |

## เข้าถึงข้อมูล
```html
{% for item in items %}                      {# list ของ dict #}
  <tr><td>{{ item.name }}</td><td>{{ item.price }}</td></tr>
{% endfor %}

{% for cat, total in per_category.items() %} {# dict: key, value #}
  <tr><td>{{ cat }}</td><td>{{ total }}</td></tr>
{% endfor %}

{% for item in items %} … {% else %} <div class="empty">ไม่มีข้อมูล</div> {% endfor %}   {# list ว่าง #}
```

## ของแถมที่ใช้บ่อย
- `{{ items|length }}` = จำนวนแถว · `{{ loop.index }}` = เลขรอบ (เริ่ม 1) · `{{ loop.index0 }}` (เริ่ม 0) · `{{ items|reverse }}`
- `{{ "{:,.2f}".format(price) }}` = ทศนิยม 2 ตำแหน่งมีลูกน้ำ · `{{ "{:,.0f}".format(total) }}` = ไม่มีทศนิยม
- `{{ name|replace("นาย", "") }}` · `{{ text|upper }}` · `{{ text[:10] }}`
- รูป: `<img src="{{ url_for('static', filename='img/' + item.image) }}">`
- ลิงก์ไปหน้าอื่น: `<a href="/page2?i={{ loop.index0 }}">`

## class CSS ที่มีให้แล้วใน style.css
| ใช้ทำ | class |
|---|---|
| ตาราง | `table` · `td.num` (ชิดขวา) |
| การ์ดตัวเลข | `.stat-grid` > `.stat` (`.good` `.bad` `.gold`) > `.label` `.value` `.unit` |
| กล่อง / 2 คอลัมน์ | `.panel` · `.two-col` · `.hero-box` |
| การ์ดสินค้า | `.card-grid` > `.item-card` > `img` + `.body` + `.price` |
| ป้าย | `.badge` (`.good` `.bad` `.gold`) · `.pills` > `a.active` |
| กราฟแท่งแนวนอน | `.bar-row` > `span` + `.bar-track` > `.bar-fill` (`style="width: N%"`) + `span.num` |
| กราฟแท่งแนวตั้ง | `.chart` > `.col` > `div` (`style="height: N%"`) · ซ้อนหลายสี: `.col` > `.seg` `.seg.gold` · `.chart-labels` |
| โดนัท (สัดส่วน) | `.donut` (`style="--p: 42"`) > `span` (ตัวเลขตรงกลาง) |
| แถบความคืบหน้า | `.progress` > `div` (`style="width: N%"`) |
| ปุ่ม / ฟอร์ม | `.btn` (`.ghost` `.small` `.full` `.danger`) · `.field` > `label` + `input` · `.field-row` (ช่องเรียงแนวนอน) · `form.inline` |
| สรุปราคา / รูปย่อ / เกม | `.sum-row` (`.total`) · `.thumb` · `.game-board` (canvas) · `.hud` |
| อื่น ๆ | `.empty` · `.lead` · `.muted` · `.note` · `.kbd` (ปุ่มคีย์บอร์ด) · `.gallery` · `.member-grid` |

เปอร์เซ็นต์ของกราฟให้คำนวณใน Python (percent = value × 100 / ค่ามากสุด) — ดู catalog/stats
อยากเพิ่ม CSS เอง → เขียนท้ายไฟล์ `static/style.css` ใต้ "your own styles"
