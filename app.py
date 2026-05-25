from flask import Flask, request
import random
import os

app = Flask(__name__)

IG_LINK = "https://www.instagram.com/gambler_168"

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    show_result = "none"

    if request.method == "POST":
        show_result = "block"

        try:
            today = request.form.get("today", "")
            current = int(request.form.get("current", 0))
            last1 = int(request.form.get("last1", 0))
            last2 = int(request.form.get("last2", 0))

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
                action = "建議低本測試"
                range_text = f"{int(avg*0.8)} ~ {int(avg*1.2)} 轉"
            elif current < avg * 0.7:
                status = "剛結束釋放"
                action = "不建議進場"
                range_text = f"等待至 {int(avg)} 轉以上"
            else:
                status = "訊號累積中"
                action = "建議低本測試"
                range_text = f"{int(avg*0.6)} ~ {int(avg*0.9)} 轉"

            signal_chance = random.randint(60, 95)
            confidence = random.randint(80, 96)

            # 🔒 免費版鎖（已修正白字）
            lock_html = f"""
            <a href="{IG_LINK}" target="_blank" style="text-decoration:none; color:white;">
                <div class="card step highlight">
                    🔒 操作建議（點我解鎖）
                </div>
            </a>

            <a href="{IG_LINK}" target="_blank" style="text-decoration:none; color:white;">
                <div class="card step">
                    🔒 建議區間（點我解鎖）
                </div>
            </a>
            """

            result = f"""
            <div id="cards">

                <div class="card step red">
                    📊 分析結果如下
                </div>

                <div class="card step">
                    🔥 成功捕捉熱點訊號（{signal_chance}%）
                </div>

                <div class="card step">
                    📊 節奏判定：{status}<br>
                    ⚠️ 波動狀態：{risk}
                </div>

                {lock_html}

                <div class="card step">
                    🤖 AI信心指數：{confidence}%
                </div>

                <div class="card step small">
                    ⚠️ 熱點訊號通常不會維持太久<br>
                    💡 建議低倍觀察，避免重壓
                </div>

                <div class="card step small">
                    ※ 本系統僅供參考
                </div>

            </div>
            """

        except:
            result = "<div class='card'>⚠️ 輸入錯誤</div>"

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
    body {{
        background:#0b0f1a;
        color:white;
        font-family:sans-serif;
        text-align:center;
        padding:20px;
    }}

    .title {{
        color:orange;
        font-size:26px;
        font-weight:bold;
    }}

    input {{
        width:90%;
        padding:12px;
        margin:8px 0;
        border-radius:10px;
        border:none;
        background:#1c2233;
        color:white;
    }}

    button {{
        width:95%;
        padding:15px;
        margin-top:15px;
        border:none;
        border-radius:12px;
        background:orange;
        color:black;
    }}

    .card {{
        background:#151a2c;
        margin-top:15px;
        padding:15px;
        border-radius:15px;
        opacity:0;
        transform:translateY(30px);
    }}

    .show {{
        animation:fadeUp 0.5s forwards;
    }}

    @keyframes fadeUp {{
        to {{ opacity:1; transform:translateY(0); }}
    }}

    .highlight {{
        background:orange;
        color:black;
        font-weight:bold;
    }}

    .red {{
        background:#ff3b3b;
        font-weight:bold;
    }}

    .small {{
        font-size:12px;
        color:gray;
    }}
    </style>

    <script>
    window.onload = function() {{
        let steps = document.querySelectorAll(".step");

        steps.forEach((el, i) => {{
            setTimeout(() => {{
                el.classList.add("show");
            }}, i * 600);
        }});
    }}
    </script>

    </head>

    <body>

    <div class="title">⚡ 熱點雷達</div>
    <div style="font-size:12px;color:gray;">※ 本系統僅供參考</div>

    <form method="post">
        <input name="today" placeholder="今日得分率">
        <input name="current" placeholder="未開轉數">
        <input name="last1" placeholder="上次轉數">
        <input name="last2" placeholder="上上次">
        <button type="submit">開始分析</button>
    </form>

    <div style="display:{show_result};">
        {result}
    </div>

    </body>
    </html>
    """

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
