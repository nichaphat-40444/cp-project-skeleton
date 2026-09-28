"""หน้าเล่นเกม Hangman: เริ่มเกม รับตัวอักษร และบันทึกผลเมื่อจบเกม."""
import random
import time

import models
import storage

TITLE = "เล่นเกม Hangman"
WORD_TIME_LIMITS = {"ง่าย": 60, "กลาง": 90, "ยาก": 120}
ROUND_HINT_LIMIT = 3

CATEGORIES = {
    "สัตว์": "Animals",
    "สิ่งของ": "Tools",
    "ของใช้ในบ้าน": "Furniture",
    "ประเทศ": "Countries",
    "จังหวัดไทย": "Provinces of Thailand",
}
DIFFICULTIES = ["ง่าย", "กลาง", "ยาก"]
THAI_TRANSLATIONS = {
    "สัตว์": {
        "bear": "หมี", "bee": "ผึ้ง", "bird": "นก", "camel": "อูฐ",
        "cat": "แมว", "cow": "วัว", "deer": "กวาง", "dog": "สุนัข",
        "duck": "เป็ด", "eagle": "นกอินทรี", "fish": "ปลา", "fox": "สุนัขจิ้งจอก",
        "frog": "กบ", "goat": "แพะ", "hen": "แม่ไก่", "horse": "ม้า",
        "lion": "สิงโต", "mouse": "หนู", "owl": "นกฮูก", "pig": "หมู",
        "shark": "ฉลาม", "sheep": "แกะ", "snake": "งู", "tiger": "เสือ",
        "zebra": "ม้าลาย", "chicken": "ไก่", "dolphin": "โลมา", "hamster": "หนูแฮมสเตอร์",
        "leopard": "เสือดาว", "monkey": "ลิง", "parrot": "นกแก้ว", "rabbit": "กระต่าย",
        "turtle": "เต่า", "butterfly": "ผีเสื้อ", "crocodile": "จระเข้",
        "elephant": "ช้าง", "kangaroo": "จิงโจ้", "rhinoceros": "แรด",
    },
    "สิ่งของ": {
        "axe": "ขวาน", "file": "ตะไบ", "nail": "ตะปู", "saw": "เลื่อย",
        "bit": "ดอกสว่าน", "drill": "สว่าน", "jack": "แม่แรง", "level": "ระดับน้ำ",
        "plier": "คีม", "screw": "สกรู", "vice": "ปากกาจับชิ้นงาน", "vise": "ปากกาจับชิ้นงาน",
        "chisel": "สิ่ว", "hammer": "ค้อน", "mallet": "ค้อนไม้", "pulley": "รอก",
        "spanner": "ประแจ", "trowel": "เกรียง", "winch": "เครื่องกว้าน", "wrench": "ประแจ",
        "pliers": "คีม", "crowbar": "ชะแลง", "screwdriver": "ไขควง",
        "sledgehammer": "ค้อนปอนด์", "jackhammer": "เครื่องเจาะคอนกรีต",
        "wheelbarrow": "รถเข็นล้อเดียว", "visegrip": "คีมล็อก",
    },
    "ของใช้ในบ้าน": {
        "bed": "เตียง", "chair": "เก้าอี้", "desk": "โต๊ะเขียนหนังสือ", "lamp": "โคมไฟ",
        "rack": "ชั้นวางของ", "rug": "พรม", "sofa": "โซฟา", "stool": "เก้าอี้ไม่มีพนัก",
        "table": "โต๊ะ", "bench": "ม้านั่ง", "bookcase": "ตู้หนังสือ", "cabinet": "ตู้เก็บของ",
        "couch": "โซฟา", "dresser": "ตู้ลิ้นชัก", "shelf": "ชั้นวางของ",
        "wardrobe": "ตู้เสื้อผ้า", "armchair": "เก้าอี้มีที่วางแขน", "cupboard": "ตู้เก็บของ",
        "bookcase": "ตู้หนังสือ", "chiffonier": "ตู้ลิ้นชัก",
        "footstool": "ม้านั่งวางเท้า", "headboard": "หัวเตียง",
        "highchair": "เก้าอี้เด็ก", "sideboard": "ตู้เก็บของข้างผนัง",
    },
    "ประเทศ": {
        "chad": "ชาด", "chile": "ชิลี", "china": "จีน", "cuba": "คิวบา",
        "fiji": "ฟิจิ", "haiti": "เฮติ", "india": "อินเดีย", "iran": "อิหร่าน",
        "iraq": "อิรัก", "italy": "อิตาลี", "japan": "ญี่ปุ่น", "laos": "ลาว",
        "mali": "มาลี", "nepal": "เนปาล", "oman": "โอมาน", "peru": "เปรู",
        "spain": "สเปน", "togo": "โตโก", "brazil": "บราซิล", "canada": "แคนาดา",
        "france": "ฝรั่งเศส", "greece": "กรีซ", "israel": "อิสราเอล", "jordan": "จอร์แดน",
        "mexico": "เม็กซิโก", "norway": "นอร์เวย์", "poland": "โปแลนด์", "russia": "รัสเซีย",
        "sweden": "สวีเดน", "taiwan": "ไต้หวัน", "thailand": "ประเทศไทย", "turkey": "ตุรกี",
        "turky": "ตุรกี", "vietnam": "เวียดนาม", "argentina": "อาร์เจนตินา",
        "australia": "ออสเตรเลีย", "indonesia": "อินโดนีเซีย", "singapore": "สิงคโปร์",
        "switzerland": "สวิตเซอร์แลนด์", "netherlands": "เนเธอร์แลนด์",
        "philippines": "ฟิลิปปินส์", "madagascar": "มาดากัสการ์",
    },
    "จังหวัดไทย": {
        "nan": "น่าน", "tak": "ตาก", "trat": "ตราด", "yala": "ยะลา",
        "loei": "เลย", "krabi": "กระบี่", "satun": "สตูล", "surin": "สุรินทร์",
        "trang": "ตรัง", "phrae": "แพร่", "korat": "นครราชสีมา (โคราช)",
        "phuket": "ภูเก็ต", "phayao": "พะเยา", "rayong": "ระยอง", "ranong": "ระนอง",
        "lampang": "ลำปาง", "lamphun": "ลำพูน", "pattani": "ปัตตานี", "chainat": "ชัยนาท",
        "chonburi": "ชลบุรี", "mukdahan": "มุกดาหาร", "kanchanaburi": "กาญจนบุรี",
        "chiangmai": "เชียงใหม่", "phetchabun": "เพชรบูรณ์", "phetchaburi": "เพชรบุรี",
        "nakhonsawan": "นครสวรรค์", "ubonratchathani": "อุบลราชธานี",
        "sakonnakhon": "สกลนคร",
    },
}
WORD_HINTS = {
    "สัตว์": {
        "bear": "สัตว์เลี้ยงลูกด้วยนมตัวใหญ่ มีขนหนาและอุ้งเท้าแข็งแรง",
        "bee": "แมลงมีปีกที่ช่วยผสมเกสรและผลิตน้ำหวาน",
        "bird": "สัตว์มีขนและปีก ออกลูกเป็นไข่",
        "camel": "สัตว์ทะเลทรายที่มีโหนกและทนต่อการขาดน้ำ",
        "cat": "สัตว์เลี้ยงตระกูลแมว มีหนวดและเล็บแหลม",
        "cow": "สัตว์เลี้ยงขนาดใหญ่ที่ให้น้ำนมและมีเขา",
        "deer": "สัตว์กีบที่ตัวผู้หลายชนิดมีเขาแตกกิ่ง",
        "dog": "สัตว์เลี้ยงที่ขึ้นชื่อเรื่องความซื่อสัตย์และการดมกลิ่น",
        "duck": "นกน้ำที่มีปากแบนและเท้ามีพังผืด",
        "eagle": "นกล่าเหยื่อตัวใหญ่ มีสายตาคมและกรงเล็บแข็งแรง",
        "fish": "สัตว์น้ำที่ใช้เหงือกหายใจและใช้ครีบว่ายน้ำ",
        "fox": "สัตว์ตระกูลสุนัข มีหางเป็นพวงและมักออกหากินกลางคืน",
        "frog": "สัตว์สะเทินน้ำสะเทินบก กระโดดเก่งและมีผิวชื้น",
        "goat": "สัตว์เลี้ยงมีเขา ชอบปีนป่ายและกินพืช",
        "hen": "ไก่เพศเมียที่ออกไข่",
        "horse": "สัตว์กีบที่คนใช้ขี่หรือเทียมรถ มีแผงคอ",
        "lion": "แมวใหญ่ที่ตัวผู้มีแผงคอและมักถูกเรียกว่าเจ้าป่า",
        "mouse": "สัตว์ฟันแทะตัวเล็ก มีหางยาวและชอบแทะสิ่งของ",
        "owl": "นกล่าเหยื่อที่มักหากินกลางคืนและมีดวงตากลมโต",
        "pig": "สัตว์เลี้ยงจมูกแบน กินได้ทั้งพืชและอาหารหลายชนิด",
        "shark": "ปลาทะเลนักล่าที่มีกระดูกอ่อนและฟันหลายแถว",
        "sheep": "สัตว์เลี้ยงที่มีขนเป็นปุยและให้ขนสำหรับทำผ้า",
        "snake": "สัตว์เลื้อยคลานลำตัวยาว ไม่มีขาและเลื้อยไปกับพื้น",
        "tiger": "แมวใหญ่ลายพาดกลอน เป็นนักล่าที่ว่ายน้ำเก่ง",
        "zebra": "สัตว์คล้ายม้าที่มีลายขาวสลับดำทั่วตัว",
        "chicken": "สัตว์ปีกเลี้ยงในฟาร์ม มีทั้งเพศผู้และเพศเมีย",
        "dolphin": "สัตว์เลี้ยงลูกด้วยนมในทะเล ฉลาดและใช้เสียงสื่อสาร",
        "hamster": "สัตว์ฟันแทะตัวเล็กที่เก็บอาหารไว้ในกระพุ้งแก้ม",
        "leopard": "แมวใหญ่ลายจุด ว่องไวและปีนต้นไม้เก่ง",
        "monkey": "สัตว์เลี้ยงลูกด้วยนมที่ใช้มือจับสิ่งของและปีนต้นไม้",
        "parrot": "นกสีสันสดใสที่เลียนเสียงคนได้",
        "rabbit": "สัตว์หูยาว กินพืชและกระโดดด้วยขาหลัง",
        "turtle": "สัตว์เลื้อยคลานที่มีกระดองแข็งปกป้องลำตัว",
        "butterfly": "แมลงมีปีกสีสันสวยงามที่เติบโตจากหนอน",
        "crocodile": "สัตว์เลื้อยคลานนักล่าปากยาว อาศัยใกล้แหล่งน้ำ",
        "elephant": "สัตว์บกตัวใหญ่ มีงวงและใบหูขนาดใหญ่",
        "kangaroo": "สัตว์มีกระเป๋าหน้าท้อง กระโดดเก่งและพบในออสเตรเลีย",
        "rhinoceros": "สัตว์ตัวใหญ่ผิวหนา มีเขาบนจมูก",
    },
    "สิ่งของ": {
        "axe": "เครื่องมือมีคมติดด้ามยาว ใช้ฟันหรือตัดไม้",
        "file": "เครื่องมือผิวหยาบ ใช้ถูแต่งขอบโลหะหรือไม้",
        "nail": "หมุดโลหะปลายแหลม ใช้ตอกยึดวัสดุเข้าด้วยกัน",
        "saw": "เครื่องมือตัดที่มีฟันเรียงตามขอบใบ",
        "bit": "หัวปลายตัดที่ใส่กับสว่านเพื่อเจาะรู",
        "drill": "เครื่องมือหมุนหัวเจาะเพื่อทำรูบนวัสดุ",
        "jack": "อุปกรณ์ยกของหนัก เช่น รถยนต์ ให้พ้นจากพื้น",
        "level": "เครื่องมือมีหลอดฟองอากาศ ใช้ตรวจว่าพื้นผิวได้ระดับ",
        "plier": "เครื่องมือมีปากสองข้างและด้ามบีบ ใช้จับหรือดัดชิ้นงาน",
        "screw": "ตัวยึดเกลียวที่หมุนเข้าไปในวัสดุด้วยไขควง",
        "vice": "เครื่องมือมีปากเลื่อน ใช้หนีบชิ้นงานให้อยู่นิ่ง",
        "vise": "เครื่องมือมีปากเลื่อน ใช้หนีบชิ้นงานให้อยู่นิ่ง",
        "chisel": "เครื่องมือปลายคม ใช้สกัดหรือตกแต่งไม้และหิน",
        "hammer": "เครื่องมือหัวหนัก ใช้ตอกตะปูหรือกระแทกชิ้นงาน",
        "mallet": "ค้อนหัวนุ่ม มักทำจากไม้หรือยาง ใช้เคาะโดยไม่ทำผิวเป็นรอยง่าย",
        "pulley": "ล้อมีร่องสำหรับพาดเชือก ช่วยผ่อนแรงยกของ",
        "spanner": "เครื่องมือปากเปิดหรือปากแหวน ใช้หมุนนอต",
        "trowel": "เครื่องมือใบแบนมีด้าม ใช้ตักหรือเกลี่ยปูนและดิน",
        "winch": "อุปกรณ์มีดรัมและสาย ใช้ดึงหรือยกของหนัก",
        "wrench": "เครื่องมือปรับปากหรือมีปาก固定 ใช้ขันและคลายนอต",
        "pliers": "เครื่องมือด้ามบีบสองข้าง ใช้จับ ดัด หรือตัดลวด",
        "crowbar": "เหล็กแท่งปลายงัด ใช้แงะหรือถอนตะปู",
        "screwdriver": "เครื่องมือด้ามจับกับปลายแบนหรือแฉก ใช้หมุนสกรู",
        "sledgehammer": "ค้อนหัวใหญ่และด้ามยาว ใช้ทุบวัสดุแข็ง",
        "jackhammer": "เครื่องเจาะกระแทกขนาดใหญ่ ใช้ทุบพื้นคอนกรีต",
        "wheelbarrow": "รถเข็นมีล้อเดียวและด้ามจับ ใช้ขนดินหรือวัสดุ",
        "visegrip": "คีมที่ล็อกปากค้างไว้ได้ ใช้หนีบชิ้นงานแน่น",
    },
    "ของใช้ในบ้าน": {
        "bed": "เฟอร์นิเจอร์สำหรับนอน มีพื้นรองรับที่นอน",
        "chair": "ที่นั่งสำหรับหนึ่งคน โดยทั่วไปมีพนักพิงและขา",
        "desk": "โต๊ะพื้นเรียบที่ออกแบบไว้สำหรับเขียนหนังสือหรือทำงาน",
        "lamp": "อุปกรณ์ให้แสงสว่างจากหลอดไฟ มักตั้งหรือแขวนไว้ในห้อง",
        "rack": "โครงหรือชั้นสำหรับวางและจัดเก็บสิ่งของ",
        "rug": "ผ้าหนาใช้ปูพื้นเพื่อความนุ่มหรือประดับห้อง",
        "sofa": "ที่นั่งบุนวมขนาดใหญ่สำหรับหลายคน มักวางในห้องนั่งเล่น",
        "stool": "ที่นั่งขนาดเล็กที่มักไม่มีพนักพิง",
        "table": "เฟอร์นิเจอร์พื้นราบมีขา ใช้วางของหรือรับประทานอาหาร",
        "bench": "ที่นั่งยาวสำหรับหลายคน มักมีพนักพิงหรือไม่มีพนักก็ได้",
        "bookcase": "ตู้หรือชั้นแบ่งช่องสำหรับเก็บหนังสือ",
        "cabinet": "เฟอร์นิเจอร์มีช่องเก็บของ มักมีบานประตูหรือชั้นภายใน",
        "couch": "ที่นั่งบุนวมสำหรับพักผ่อน คล้ายโซฟา",
        "dresser": "ตู้เก็บเสื้อผ้าที่มีลิ้นชักหลายช่อง",
        "shelf": "แผ่นวางแนวนอนที่ติดผนังหรืออยู่ในตู้ ใช้วางของ",
        "wardrobe": "ตู้ทรงสูงมีบานเปิด ใช้แขวนและเก็บเสื้อผ้า",
        "armchair": "เก้าอี้บุเบาะที่มีที่วางแขนสองข้าง",
        "cupboard": "ตู้มีบานปิด ใช้เก็บจานหรือของใช้ในบ้าน",
        "chiffonier": "ตู้ลิ้นชักทรงสูง ใช้เก็บเสื้อผ้าหรือของชิ้นเล็ก",
        "footstool": "ม้านั่งเตี้ยสำหรับวางเท้าขณะนั่ง",
        "headboard": "แผ่นพนักที่ติดอยู่ตรงหัวเตียง",
        "highchair": "เก้าอี้ขาสูงพร้อมถาด สำหรับให้เด็กเล็กนั่งกินอาหาร",
        "sideboard": "ตู้เตี้ยยาวที่มักวางชิดผนัง ใช้เก็บภาชนะหรือผ้าปูโต๊ะ",
    },
    "ประเทศ": {
        "chad": "ประเทศในแอฟริกากลาง ไม่มีทางออกสู่ทะเล",
        "chile": "ประเทศยาวแคบทางชายฝั่งตะวันตกของอเมริกาใต้",
        "china": "ประเทศขนาดใหญ่ในเอเชียตะวันออก มีเมืองหลวงชื่อปักกิ่ง",
        "cuba": "ประเทศหมู่เกาะในทะเลแคริบเบียน",
        "fiji": "ประเทศหมู่เกาะในมหาสมุทรแปซิฟิกตอนใต้",
        "haiti": "ประเทศในทะเลแคริบเบียน ครองพื้นที่ด้านตะวันตกของเกาะฮิสปันโยลา",
        "india": "ประเทศในเอเชียใต้ มีเมืองหลวงชื่อนิวเดลี",
        "iran": "ประเทศในเอเชียตะวันตก มีเมืองหลวงชื่อเตหะราน",
        "iraq": "ประเทศในตะวันออกกลาง ระหว่างแม่น้ำไทกริสและยูเฟรทีส",
        "italy": "ประเทศยุโรปใต้ที่มีรูปร่างคล้ายรองเท้าบูต",
        "japan": "ประเทศหมู่เกาะในเอเชียตะวันออก มีเมืองหลวงชื่อโตเกียว",
        "laos": "ประเทศเพื่อนบ้านของไทยในเอเชียตะวันออกเฉียงใต้ ไม่มีทางออกสู่ทะเล",
        "mali": "ประเทศในแอฟริกาตะวันตก มีเมืองหลวงชื่อบามาโก",
        "nepal": "ประเทศเอเชียใต้ที่มีเทือกเขาหิมาลัยและยอดเขาเอเวอเรสต์",
        "oman": "ประเทศบนคาบสมุทรอาหรับ ติดทะเลอาหรับ",
        "peru": "ประเทศชายฝั่งแปซิฟิกในอเมริกาใต้ มีเทือกเขาแอนดีส",
        "spain": "ประเทศทางตะวันตกเฉียงใต้ของยุโรป มีเมืองหลวงชื่อมาดริด",
        "togo": "ประเทศแคบยาวริมอ่าวกินีในแอฟริกาตะวันตก",
        "brazil": "ประเทศใหญ่ที่สุดในอเมริกาใต้ มีป่าฝนอเมซอน",
        "canada": "ประเทศขนาดใหญ่ทางเหนือของสหรัฐอเมริกา",
        "france": "ประเทศในยุโรปตะวันตก มีเมืองหลวงชื่อปารีส",
        "greece": "ประเทศยุโรปใต้ มีเกาะจำนวนมากและเป็นแหล่งอารยธรรมโบราณ",
        "israel": "ประเทศในตะวันออกกลาง ติดชายฝั่งทะเลเมดิเตอร์เรเนียน",
        "jordan": "ประเทศในตะวันออกกลาง มีแหล่งโบราณคดีชื่อเพตรา",
        "mexico": "ประเทศในอเมริกาเหนือ อยู่ทางใต้ของสหรัฐอเมริกา",
        "norway": "ประเทศนอร์ดิก มีชายฝั่งเว้าแหว่งและฟยอร์ด",
        "poland": "ประเทศในยุโรปกลาง มีเมืองหลวงชื่อวอร์ซอ",
        "russia": "ประเทศขนาดใหญ่ที่ครอบคลุมพื้นที่ทั้งยุโรปและเอเชีย",
        "sweden": "ประเทศนอร์ดิกในยุโรปเหนือ มีเมืองหลวงชื่อสตอกโฮล์ม",
        "taiwan": "เกาะในเอเชียตะวันออก ทางตะวันออกของจีนแผ่นดินใหญ่",
        "thailand": "ประเทศในเอเชียตะวันออกเฉียงใต้ มีกรุงเทพมหานครเป็นเมืองหลวง",
        "turkey": "ประเทศที่มีพื้นที่เชื่อมต่อระหว่างยุโรปกับเอเชีย",
        "turky": "ประเทศที่มีพื้นที่เชื่อมต่อระหว่างยุโรปกับเอเชีย",
        "vietnam": "ประเทศยาวตามชายฝั่งทะเลจีนใต้ในเอเชียตะวันออกเฉียงใต้",
        "argentina": "ประเทศในอเมริกาใต้ มีเมืองหลวงชื่อบัวโนสไอเรส",
        "australia": "ประเทศและทวีปบนซีกโลกใต้ มีสัตว์อย่างจิงโจ้",
        "indonesia": "ประเทศหมู่เกาะขนาดใหญ่ในเอเชียตะวันออกเฉียงใต้",
        "singapore": "ประเทศเกาะขนาดเล็กทางใต้ของคาบสมุทรมลายู",
        "switzerland": "ประเทศในยุโรปกลางที่มีเทือกเขาแอลป์",
        "netherlands": "ประเทศในยุโรปตะวันตก มีพื้นที่ต่ำและคลองจำนวนมาก",
        "philippines": "ประเทศหมู่เกาะในเอเชียตะวันออกเฉียงใต้",
        "madagascar": "เกาะขนาดใหญ่ทางตะวันออกของชายฝั่งแอฟริกา",
    },
    "จังหวัดไทย": {
        "nan": "จังหวัดภาคเหนือ มีภูเขาและภาพจิตรกรรมฝาผนังวัดภูมินทร์",
        "tak": "จังหวัดภาคตะวันตกติดชายแดนเมียนมา มีน้ำตกทีลอซู",
        "trat": "จังหวัดภาคตะวันออกติดกัมพูชา เป็นทางไปเกาะช้าง",
        "yala": "จังหวัดชายแดนใต้สุดของประเทศไทย ไม่มีพื้นที่ติดทะเล",
        "loei": "จังหวัดภาคตะวันออกเฉียงเหนือ มีภูเขาและอากาศหนาวในบางฤดู",
        "krabi": "จังหวัดภาคใต้ฝั่งอันดามัน มีหน้าผาหินปูนและเกาะพีพี",
        "satun": "จังหวัดภาคใต้ฝั่งอันดามัน ติดชายแดนมาเลเซียและมีเกาะหลีเป๊ะ",
        "surin": "จังหวัดภาคตะวันออกเฉียงเหนือ มีชื่อเสียงเรื่องช้าง",
        "trang": "จังหวัดภาคใต้ฝั่งอันดามัน มีเกาะและถ้ำมรกต",
        "phrae": "จังหวัดภาคเหนือ มีบ้านไม้สักและวัดเก่าแก่",
        "korat": "ชื่อเรียกสั้นของจังหวัดภาคตะวันออกเฉียงเหนือที่มีพื้นที่กว้างใหญ่",
        "phuket": "จังหวัดเกาะทางภาคใต้ฝั่งอันดามัน เป็นแหล่งท่องเที่ยวชายทะเล",
        "phayao": "จังหวัดภาคเหนือ มีทะเลสาบกว๊านพะเยา",
        "rayong": "จังหวัดภาคตะวันออก มีชายหาดและเกาะเสม็ด",
        "ranong": "จังหวัดภาคใต้ฝั่งอันดามัน มีฝนตกชุกและบ่อน้ำพุร้อน",
        "lampang": "จังหวัดภาคเหนือ มีรถม้าและวัดพระธาตุลำปางหลวง",
        "lamphun": "จังหวัดภาคเหนือ เคยเป็นศูนย์กลางอาณาจักรหริภุญชัย",
        "pattani": "จังหวัดชายแดนใต้ ติดอ่าวไทยและมีแม่น้ำปัตตานี",
        "chainat": "จังหวัดภาคกลาง มีเขื่อนเจ้าพระยา",
        "chonburi": "จังหวัดภาคตะวันออก มีเมืองพัทยาและชายหาดบางแสน",
        "mukdahan": "จังหวัดภาคตะวันออกเฉียงเหนือ ริมแม่น้ำโขงตรงข้ามลาว",
        "kanchanaburi": "จังหวัดภาคตะวันตก มีสะพานข้ามแม่น้ำแควและน้ำตกเอราวัณ",
        "phetchabun": "จังหวัดภาคเหนือตอนล่าง มีภูเขาและอากาศเย็นที่เขาค้อ",
        "phetchaburi": "จังหวัดภาคตะวันตก มีพระนครคีรีและชายหาดชะอำ",
    },
}
EXCLUDED_WORDS = {
    "turky", "tyre", "diningtable", "rockingchair", "grandfatherclock",
    "chiangmai", "nakhonsawan", "ubonratchathani", "sakonnakhon",
}


def difficulty_for(word):
    if len(word) <= 5:
        return "ง่าย"
    if len(word) <= 8:
        return "กลาง"
    return "ยาก"


def translate_word(word, category=None):
    return THAI_TRANSLATIONS.get(category, {}).get(word.lower(), "ไม่พบคำแปลที่ยืนยันได้")


def thai_hint(word, category):
    clue = WORD_HINTS.get(category, {}).get(word.lower())
    if clue:
        return f"{clue} คำตอบขึ้นต้นด้วย {word[0].upper()} และมี {len(word)} ตัวอักษร"
    return f"คำตอบอยู่ในหมวด{category} ขึ้นต้นด้วย {word[0].upper()} และมี {len(word)} ตัวอักษร"


def dictionary_words(category, difficulty):
    return [
        {"word": word, "category": category, "difficulty": difficulty}
        for word in THAI_TRANSLATIONS.get(category, {})
        if word not in EXCLUDED_WORDS
        and len(word) >= 3
        and word.isalpha()
        and difficulty_for(word) == difficulty
        and word in WORD_HINTS.get(category, {})
    ]


def active_game(rows):
    for row in rows:
        if row.get("type") == "active":
            return row
    return None


def latest_game(rows):
    for row in reversed(rows):
        if row.get("type") == "game":
            return row
    return None


def choose_word(rows, category="ทั้งหมด", difficulty="ง่าย"):
    if category == "ทั้งหมด":
        category = random.choice(list(CATEGORIES))
    pool = dictionary_words(category, difficulty)
    if not pool:
        return None
    used_words = {row.get("word") for row in rows if row.get("word")}
    available = [item for item in pool if item["word"] not in used_words]
    if not available:
        last_word = latest_game(rows)
        available = [item for item in pool if not last_word or item["word"] != last_word.get("word")]
    available = available or pool
    selected = random.choice(available)
    selected["_remaining_words"] = [item["word"] for item in available if item["word"] != selected["word"]]
    selected["_word_pool"] = [item["word"] for item in available]
    selected["translation"] = translate_word(selected["word"], selected["category"])
    selected["thai_hint"] = thai_hint(selected["word"], selected["category"])
    return selected


def display_game(row):
    game = models.HangmanGame(row["word"], row["category"], row["difficulty"], row.get("player"))
    game.guessed = row.get("guessed", [])
    game.hint_letters = row.get("hint_letters", [])
    game.wrong = row.get("wrong", 0)
    game.status = row.get("status", "active")
    game.score = row.get("score", 0)
    return game


def archive_game(rows, row, game):
    row.update(game.to_dict())
    row["type"] = "game"
    rows.remove(row)
    rows.append(row)


def next_word(row, rows):
    used_words = set(row.get("round_words", []))
    if not used_words:
        used_words.update(set(row.get("word_pool", [])) - set(row.get("remaining_words", [])))
        used_words.add(row["word"])

    word_pool = row.get("word_pool", [])
    remaining = [word for word in row.get("remaining_words", []) if word not in used_words]
    if remaining:
        word = remaining.pop(random.randrange(len(remaining)))
    else:
        try:
            fresh_pool = dictionary_words(row["category"], row["difficulty"])
        except (OSError, TimeoutError, ValueError):
            fresh_pool = []
        fresh_pool = [item for item in fresh_pool if item["word"] not in used_words]
        if not fresh_pool:
            return None
        selected = random.choice(fresh_pool)
        word = selected["word"]
        word_pool = [item["word"] for item in fresh_pool]
        remaining = [item for item in word_pool if item != word]

    used_words.add(word)
    return {
        "word": word,
        "category": row["category"],
        "difficulty": row["difficulty"],
        "translation": translate_word(word, row["category"]),
        "thai_hint": thai_hint(word, row["category"]),
        "_remaining_words": remaining,
        "_word_pool": word_pool,
        "_round_words": sorted(used_words),
    }


def advance_after_win(rows, row, game):
    archive_game(rows, row, game)
    selected = next_word(row, rows)
    if selected is None:
        storage.save(rows)
        return "ชนะแล้ว แต่ไม่มีคำถัดไปในหมวดนี้ กรุณาเริ่มเกมใหม่"
    rows.append({
        "type": "active",
        "player": row.get("player", "ผู้เล่น"),
        **{key: value for key, value in selected.items() if not key.startswith("_")},
        "remaining_words": selected.get("_remaining_words", []),
        "word_pool": selected.get("_word_pool", []),
        "round_words": selected.get("_round_words", [selected["word"]]),
        "round_hints_used": row.get("round_hints_used", 0),
        "last_result": {
            "word": row["word"],
            "translation": row.get("translation", "ไม่พบคำแปล"),
            "status": "won",
            "hint_letters": row.get("last_hint_letters", []),
        },
        "guessed": [],
        "hint_letters": [],
        "wrong": 0,
        "status": "active",
        "score": 0,
        "deadline": time.time() + WORD_TIME_LIMITS.get(row["difficulty"], 60),
    })
    storage.save(rows)
    return "ชนะแล้ว! คำถัดไปเริ่มแล้ว"


def expire_game(rows, row):
    game = display_game(row)
    game.status = "lost"
    game.score = 0
    archive_game(rows, row, game)
    storage.save(rows)


def build():
    rows = storage.load()
    row = active_game(rows)
    if row and row.get("status", "active") == "active":
        if not row.get("deadline"):
            row["deadline"] = time.time() + WORD_TIME_LIMITS.get(row.get("difficulty"), 60)
            storage.save(rows)
        elif row["deadline"] <= time.time():
            expire_game(rows, row)
            row = None
    row = row or latest_game(rows)
    game = display_game(row) if row else None
    remaining_seconds = max(0, int(row["deadline"] - time.time() + 0.999)) if row and row.get("type") == "active" else 0
    if row and row.get("type") == "active":
        last_result = row.get("last_result")
        word_hint = row.get("thai_hint", thai_hint(row["word"], row["category"]))
        last_hint_letters = row.get("last_hint_letters", [])
    elif row:
        last_result = {
            "word": row["word"],
            "translation": row.get("translation", "ไม่พบคำแปล"),
            "status": row.get("status", "lost"),
            "hint_letters": row.get("last_hint_letters", []),
        }
        word_hint = ""
        last_hint_letters = row.get("last_hint_letters", [])
    else:
        last_result = None
        word_hint = ""
        last_hint_letters = []
    return {
        "game": game,
        "letters": list("abcdefghijklmnopqrstuvwxyz"),
        "max_wrong": 6,
        "categories": list(CATEGORIES),
        "difficulties": DIFFICULTIES,
        "can_hint": bool(game and set(game.word) - set(game.guessed) and row.get("round_hints_used", 0) < ROUND_HINT_LIMIT),
        "hint_limit": ROUND_HINT_LIMIT,
        "hints_used": row.get("round_hints_used", 0) if row else 0,
        "remaining_seconds": remaining_seconds,
        "deadline": row.get("deadline", 0) if row and row.get("type") == "active" else 0,
        "word_hint": word_hint,
        "last_result": last_result,
        "last_hint_letters": last_hint_letters,
    }


def handle(form):
    rows = storage.load()
    action = form.get("action", "")
    if action == "start":
        category = form.get("category", "ทั้งหมด")
        difficulty = form.get("difficulty", "ง่าย")
        if category not in CATEGORIES and category != "ทั้งหมด":
            return "กรุณาเลือกหมวดหมู่ที่มีให้"
        if difficulty not in DIFFICULTIES:
            return "กรุณาเลือกระดับความยากที่มีให้"
        try:
            selected = choose_word(rows, category, difficulty)
        except (OSError, TimeoutError, ValueError):
            return "ซิงค์คำศัพท์ไม่สำเร็จ กรุณาตรวจสอบอินเทอร์เน็ตแล้วลองอีกครั้ง"
        if selected is None:
            return "หมวดนี้ไม่มีคำระดับที่เลือก กรุณาเลือกระดับอื่น"
        rows = [row for row in rows if row.get("type") != "active"]
        rows.append({
            "type": "active",
            "player": form.get("player", "ผู้เล่น").strip() or "ผู้เล่น",
            **{key: value for key, value in selected.items() if not key.startswith("_")},
            "remaining_words": selected.get("_remaining_words", []),
            "word_pool": selected.get("_word_pool", []),
            "round_words": [selected["word"]],
            "round_hints_used": 0,
            "last_hint_letters": [],
            "guessed": [],
            "hint_letters": [],
            "wrong": 0,
            "status": "active",
            "score": 0,
            "deadline": time.time() + WORD_TIME_LIMITS.get(difficulty, 60),
        })
        storage.save(rows)
        return "เริ่มเกมใหม่แล้ว"
    if action in ("hint", "guess", "timeout"):
        row = active_game(rows)
        if row is None:
            return "กรุณาเริ่มเกมก่อน"
        if not row.get("deadline"):
            row["deadline"] = time.time() + WORD_TIME_LIMITS.get(row.get("difficulty"), 60)
        if row["deadline"] <= time.time():
            expire_game(rows, row)
            return "หมดเวลา เกมจบแล้ว"
        if action == "timeout":
            storage.save(rows)
            return "ยังมีเวลาเล่นอยู่"
    if action == "hint":
        if row.get("round_hints_used", 0) >= ROUND_HINT_LIMIT:
            return "ใช้คำใบ้ครบ 3 ครั้งของรอบนี้แล้ว"
        game = display_game(row)
        available = sorted(set(game.word) - set(game.guessed))
        if not available:
            return "ไม่มีตัวอักษรให้ใบ้แล้ว"
        letters_to_reveal = random.sample(available, random.randint(1, min(2, len(available))))
        row["round_hints_used"] = row.get("round_hints_used", 0) + 1
        row["last_hint_letters"] = letters_to_reveal
        for letter in letters_to_reveal:
            game.hint_letters.append(letter)
            game.guess(letter)
        if game.status == "won":
            return advance_after_win(rows, row, game)
        row.update(game.to_dict())
        row["type"] = "active"
        storage.save(rows)
        return "คำใบ้เปิดตัวอักษร " + ", ".join(letter.upper() for letter in letters_to_reveal)
    if action == "guess":
        game = display_game(row)
        result = game.guess(form.get("letter", ""))
        if result == "invalid":
            return "กรุณาเลือกตัวอักษรที่ยังไม่เคยทาย"
        if game.status == "won":
            return advance_after_win(rows, row, game)
        row.update(game.to_dict())
        if game.status == "lost":
            archive_game(rows, row, game)
            message = "เกมจบแล้ว ลองใหม่อีกครั้ง"
        else:
            row["type"] = "active"
            message = "ทายถูก" if result == "correct" else "ทายผิด"
        storage.save(rows)
        return message
    return "คำสั่งไม่ถูกต้อง"
