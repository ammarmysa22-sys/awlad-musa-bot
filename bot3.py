import os
from flask import Flask, request
import requests
app = Flask(__name__)
TOKEN = os.environ.get("TOKEN") or os.environ.get("PAGE_ACCESS_TOKEN") or os.environ.get("ACCESS_TOKEN") or os.environ.get("PAGE_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN","awlad_musa_2024")
daftar = {}

def my_send(id, txt):
    try:
        url = f"https://graph.facebook.com/v19.0/me/messages?access_token={TOKEN}"
        r = requests.post(url, json={"recipient":{"id":id},"message":{"text":txt}}, timeout=15)
        print(f"SEND {r.status_code}: {r.text}")
    except Exception as e:
        print(f"SEND ERROR: {e}")

@app.route('/')
def home():
    return "بوت اولاد موسى شغال"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "غلط",403
    data = request.get_json()
    if not data: return "ok",200
    try:
        for entry in data.get('entry', []):
            for s in entry.get('messaging', []):
                if 'message' not in s: continue
                sender = s['sender']['id']
                if 'text' not in s['message']: continue
                txt = s['message']['text'].strip()
                state = daftar.get(sender,"start")
                if txt == "السلام عليكم" or state == "start":
                    daftar[sender]="main"
                    my_send(sender,"وعليكم السلام ورحمة الله \nمرحبا بيك في خدمات اولاد موسى 💳⚡🏦\n1️⃣ بيع رصيد 💳\n2️⃣ شراء كهرباء ⚡\n3️⃣ فتح حساب بنكك 🏦\n4️⃣ خدمات جاهزه 📶\n5️⃣ التكلم مع التاجر 👨‍💼")
                    continue
                if state=="main":
                    if txt=="1":
                        daftar[sender]="raseed"
                        my_send(sender,"💳 بيع رصيد خصم 200 على كل 1000 ⚠️\n1️⃣ زاين 💛\n2️⃣ سوداني 💙\n3️⃣ MTN 💛")
                    elif txt=="2":
                        my_send(sender,"⚡كهرباء ✅\nخصم 300 على كل 1000\nالتاجر +249968342013\n🔢 رسل رقم العداد والمبلغ")
                        daftar[sender]="start"
                    elif txt=="3":
                        daftar[sender]="bankak"
                        my_send(sender,"🏦فتح حساب بنكك ✅\n📍 العزيز غرب السكر\n1️⃣ قريب 🚶‍♂️\n2️⃣ بعيد ✈️")
                    elif txt=="4":
                        daftar[sender]="services"
                        my_send(sender,"📶 خدمات جاهزه\n1️⃣ زاين 💛\n2️⃣ سوداني 💙\n3️⃣ MTN 💛")
                    else:
                        my_send(sender,"👨‍💼 التاجر\n📱 واتساب +249968342013 💚")
                        daftar[sender]="start"
                    continue
                if state=="raseed":
                    daftar[sender]=f"raseed_{txt}"
                    my_send(sender,"1️⃣ كاش 💵\n2️⃣ بنكك 🏦")
                    continue
                if state.startswith("raseed_"):
                    my_send(sender,"✅ رسل رقم الشريحة والاشعار\n💳 حساب: 6859973 موسى يعقوب\n📍 شجرة اولاد حامد علي ")
                    daftar[sender]="start"
                    continue
                if state=="bankak":
                    if txt=="1": daftar[sender]="bankak_close"
                    else: daftar[sender]="bankak_far"
                    my_send(sender,"اختار نوع المستند 📄\n1️⃣ جواز سفر\n2️⃣ رقم وطني")
                    continue
                if state=="bankak_close":
                    my_send(sender,"📍 شجرة اولاد حامد علي \nتعال المحل ومعاك المستند")
                    daftar[sender]="start"
                    continue
                if state=="bankak_far":
                    my_send(sender,"📱 واتساب +249968342013 💚\n🌐 لازم تكون منشط نت")
                    daftar[sender]="start"
                    continue
                if state=="services":
                    if txt=="1": daftar[sender]="srv_zain"
                    elif txt=="2": daftar[sender]="srv_sudani"
                    else: daftar[sender]="srv_mtn"
                    my_send(sender,"اختار الخدمة\n1️⃣ يوم\n2️⃣ اسبوع\n3️⃣ شهر")
                    continue
                if state=="srv_zain":
                    my_send(sender,"💛 زين - 1,500 يوم - 5,500 اسبوع - 17,000 شهر\n💳 حول 6859973 موسى يعقوب")
                    daftar[sender]="start"
                    continue
                if state=="srv_sudani":
                    my_send(sender,"💙 سوداني - 2,500 يوم - 9000 اسبوع - 30,000 شهر\n💳 حول 6859973 موسى يعقوب")
                    daftar[sender]="start"
                    continue
                if state=="srv_mtn":
                    my_send(sender,"💛 MTN\n⚠️ لا تتوفر خدمة جاهزه\n✅ يتوفر رصيد فقط")
                    daftar[sender]="start"
                    continue
    except Exception as e:
        print(f"WEBHOOK ERROR: {e} - DATA: {data}")
    return "ok",200

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
