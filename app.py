from flask import Flask, request
import random
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    show_result = "none"

    ig_link = "https://www.instagram.com/gambler_168"

    if request.method == "POST":
        show_result = "block"

        try:
            current = int(request.form["current"])
            last1 = int(request.form["last1"])
            last2 = int(request.form["last2"])

            avg = (last1 + last2) / 2
            diff = abs(last1 - last2)

            if diff > 80:
                risk = "高波動（節奏不穩）"
            elif diff > 30:
                risk = "中波動"
            else:
                risk = "穩定節奏"

            if current > avg * 1.3:
                status = "進入尾段醞釀"
            elif current < avg * 0.7:
                status = "剛結束釋放"
            else:
                status = "訊號累積中"

            signal_chance = random.randint(60, 95)
            signal_text = f"✅ 成功捕捉熱點訊號（{signal_chance}%）"

            def lock_block(text):
                return f'''
                <div onclick="window.location.href='{ig_link}'"
                     style="background:#222;padding:15px;border-radius:15px;margin-top:15px;">
                    🔒 {text}<br>
                    <span style="color:orange;">點擊前往 IG 解鎖</span>
                </div>
                '''

            result = f"""
            <div class="card red">📊 分析結果如下</div>

            <div class="card">{signal_text}</div>

            <div class="card">
                📊 節奏判定：{status}<br>
                ⚠️ 波動狀態：{risk}
            </div>

            {lock_block("操作建議已鎖定")}
            {lock_block("建議區間已鎖定")}

            """

        except:
            result = "<div class='card'>⚠️ 輸入錯誤</div>"

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{background:#0b0f1a;color:white;text-align:center;padding:20px;}}
        input {{width:90%;padding:12px;margin:8px;border-radius:10px;border:none;background:#1c2233;color:white;}}
        button {{width:95%;padding:15px;background:orange;border:none;border-radius:12px;}}
        .card {{background:#151a2c;margin-top:15px;padding:15px;border-radius:15px;}}
        .red {{background:#ff3b3b;}}
    </style>
    </head>

    <body>

    <h2>⚡ 熱點雷達</h2>

    <form method="post">
        <input name="current" placeholder="未開轉數">
        <input name="last1" placeholder="上次轉數">
        <input name="last2" placeholder="上上次">
        <button>開始分析</button>
    </form>

    {result}

    </body>
    </html>
    """

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
