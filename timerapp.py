import os
import csv
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
import webbrowser
from threading import Timer

app = Flask(__name__)

# --- CONFIGURATION ---
HIDE_NUMBERS = False # True: 3초 후 숫자를 숨김, False: 항상 숫자를 보여줌
CSV_FILE = 'records.csv'
# ---------------------

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'elapsed', 'diff'])

def get_records():
    records = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)

    # Sort by diff (absolute difference from 7.000)
    # We convert to float for proper sorting
    records.sort(key=lambda x: abs(float(x['diff'])))
    return records[:10] # Top 10

@app.route('/')
def index():
    records = get_records()

    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>7 SECONDS PERFECT CHALLENGE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        :root {{
            --bg-color: #050510;
            --panel-bg: rgba(255, 255, 255, 0.05);
            --accent-cyan: #00f2ff;
            --accent-pink: #ff2a6d;
            --accent-gold: #ffdf00;
            --text-color: #ffffff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Rajdhani', sans-serif;
            user-select: none;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: radial-gradient(circle at center, #1a1a3a 0%, #050510 100%);
        }}

        .main-wrapper {{
            display: flex;
            gap: 40px;
            align-items: stretch;
            max-width: 1000px;
            padding: 20px;
            animation: fadeIn 0.8s ease-out;
        }}

        .container {{
            width: 450px;
            padding: 40px;
            background: var(--panel-bg);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
            position: relative;
        }}

        .leaderboard-box {{
            width: 320px;
            padding: 30px;
            background: var(--panel-bg);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
            max-height: 600px;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            margin-bottom: 5px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
        }}

        .subtitle {{
            color: #888;
            font-size: 1.1rem;
            margin-bottom: 40px;
        }}

        .timer-box {{
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            padding: 50px 20px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(0, 242, 255, 0.2);
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        }}

        .timer-box::after {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            animation: sweep 3s infinite;
        }}

        @keyframes sweep {{
            0% {{ left: -100%; }}
            100% {{ left: 200%; }}
        }}

        #timer {{
            font-family: 'Orbitron', sans-serif;
            font-size: 5.5rem;
            font-weight: 700;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .hidden-timer {{
            color: #151525 !important;
            text-shadow: none !important;
        }}

        #feedback {{
            height: 30px;
            margin-bottom: 30px;
            font-size: 1.4rem;
            font-weight: 500;
            color: #aaa;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .main-btn {{
            width: 100%;
            padding: 22px;
            font-size: 1.6rem;
            font-weight: 700;
            border: none;
            border-radius: 18px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 3px;
        }}

        .btn-start {{
            background: var(--accent-cyan);
            color: #000;
            box-shadow: 0 10px 20px rgba(0, 242, 255, 0.3);
        }}

        .btn-stop {{
            background: var(--accent-pink);
            color: #fff;
            box-shadow: 0 10px 20px rgba(255, 42, 109, 0.3);
        }}

        .btn-retry {{
            background: #fff;
            color: #000;
            box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
        }}

        .main-btn:active {{
            transform: scale(0.96);
        }}

        .perfect {{
            color: var(--accent-gold) !important;
            text-shadow: 0 0 40px var(--accent-gold) !important;
            animation: pulse 0.5s infinite alternate;
        }}
        @keyframes pulse {{ from {{ transform: scale(1); }} to {{ transform: scale(1.03); }} }}

        .hint {{
            margin-top: 25px;
            font-size: 0.9rem;
            color: #555;
            letter-spacing: 1px;
        }}

        /* Leaderboard Styles */
        .lb-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.6rem;
            margin-bottom: 25px;
            color: var(--accent-cyan);
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 15px;
            letter-spacing: 2px;
        }}

        .lb-list {{
            list-style: none;
            overflow-y: auto;
            flex-grow: 1;
            padding-right: 5px;
        }}

        .lb-list::-webkit-scrollbar {{
            width: 4px;
        }}
        .lb-list::-webkit-scrollbar-thumb {{
            background: rgba(255,255,255,0.1);
            border-radius: 2px;
        }}

        .lb-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 1.2rem;
            transition: background 0.2s;
        }}

        .lb-rank {{ width: 35px; color: #666; font-weight: 700; font-size: 0.9rem; }}
        .lb-score {{ flex-grow: 1; text-align: center; font-family: 'Orbitron', sans-serif; }}
        .lb-diff {{ width: 80px; text-align: right; color: #888; font-size: 0.85rem; font-family: 'Rajdhani'; }}

        /* Highlight Rank 1, 2, 3 in Yellow/Gold */
        .lb-item.top-rank {{
            color: var(--accent-gold);
        }}
        .lb-item.top-rank .lb-rank {{ color: var(--accent-gold); }}
        .lb-item.top-rank .lb-score {{ font-weight: 700; text-shadow: 0 0 15px rgba(255, 223, 0, 0.4); }}
        .lb-item.top-rank .lb-diff {{ color: rgba(255, 223, 0, 0.7); }}

    </style>
</head>
<body>
    <div class="main-wrapper">
        <div class="container">
            <h1>7.000 SEC</h1>
            <p class="subtitle">HIT THE EXACT MOMENT</p>

            <div class="timer-box">
                <div id="timer">0.000</div>
            </div>

            <div id="feedback">READY TO START?</div>

            <button id="mainBtn" class="main-btn btn-start">START</button>

            <p class="hint">{f"TIP: TIMER HIDES AFTER 3 SECONDS" if HIDE_NUMBERS else "TIP: FOCUS ON THE TIMING"}</p>
        </div>

        <div class="leaderboard-box">
            <div class="lb-title">LEADERBOARD</div>
            <ul id="lbList" class="lb-list">
                <!-- Leaderboard items will be injected here -->
            </ul>
        </div>
    </div>

    <script>
        const timerEl = document.getElementById('timer');
        const feedbackEl = document.getElementById('feedback');
        const btnEl = document.getElementById('mainBtn');
        const lbListEl = document.getElementById('lbList');
        const hideNumbersEnabled = {str(HIDE_NUMBERS).lower()};

        let state = 'READY'; // READY, RUNNING, STOPPED
        let startTime = 0;
        let timerInterval = null;

        async function loadLeaderboard() {{
            try {{
                const res = await fetch('/records');
                const records = await res.json();
                lbListEl.innerHTML = '';

                if (records.length === 0) {{
                    lbListEl.innerHTML = '<li style="text-align:center; color:#444; margin-top:20px;">No records yet</li>';
                    return;
                }}

                records.forEach((rec, index) => {{
                    const li = document.createElement('li');
                    li.className = 'lb-item';
                    // Highlight rank 1, 2, 3
                    if (index < 3) li.classList.add('top-rank');

                    li.innerHTML = `
                        <span class="lb-rank">${{index + 1}}</span>
                        <span class="lb-score">${{parseFloat(rec.elapsed).toFixed(3)}}s</span>
                        <span class="lb-diff">±${{Math.abs(parseFloat(rec.diff)).toFixed(3)}}</span>
                    `;
                    lbListEl.appendChild(li);
                }});
            }} catch (e) {{
                console.error("Failed to load leaderboard", e);
            }}
        }}

        async function saveScore(elapsed, diff) {{
            await fetch('/save', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ elapsed, diff }})
            }});
            loadLeaderboard();
        }}

        function updateDisplay() {{
            const elapsed = (Date.now() - startTime) / 1000;

            if (hideNumbersEnabled && elapsed > 3.0) {{
                timerEl.textContent = '?.???';
                timerEl.classList.add('hidden-timer');
                feedbackEl.textContent = 'FEEL THE BEAT...';
                feedbackEl.style.color = 'var(--accent-pink)';
            }} else {{
                timerEl.textContent = elapsed.toFixed(3);
            }}
        }}

        function trigger() {{
            if (state === 'READY') {{
                state = 'RUNNING';
                startTime = Date.now();
                btnEl.textContent = 'STOP';
                btnEl.className = 'main-btn btn-stop';
                feedbackEl.textContent = 'CONCENTRATE...';
                feedbackEl.style.color = 'var(--accent-cyan)';
                timerEl.classList.remove('hidden-timer');
                timerEl.classList.remove('perfect');

                timerInterval = setInterval(updateDisplay, 10);
            }}
            else if (state === 'RUNNING') {{
                state = 'STOPPED';
                clearInterval(timerInterval);
                const endTime = Date.now();
                const elapsed = (endTime - startTime) / 1000;
                const diff = elapsed - 7.0;

                timerEl.textContent = elapsed.toFixed(3);
                timerEl.classList.remove('hidden-timer');

                const absDiff = Math.abs(diff);
                if (absDiff === 0) {{
                    feedbackEl.textContent = 'GOD-LIKE! PERFECT 0.000!';
                    feedbackEl.style.color = 'var(--accent-gold)';
                    timerEl.classList.add('perfect');
                }} else if (absDiff < 0.01) {{
                    feedbackEl.textContent = 'INSANE PRECISION!';
                    feedbackEl.style.color = 'var(--accent-cyan)';
                    timerEl.classList.add('perfect');
                }} else if (absDiff < 0.05) {{
                    feedbackEl.textContent = 'LEGENDARY!';
                    feedbackEl.style.color = '#fff';
                }} else if (absDiff < 0.2) {{
                    feedbackEl.textContent = 'GREAT JOB!';
                    feedbackEl.style.color = '#fff';
                }} else if (absDiff < 0.5) {{
                    feedbackEl.textContent = 'NOT BAD.';
                    feedbackEl.style.color = '#888';
                }} else {{
                    feedbackEl.textContent = 'TOO FAR! TRY AGAIN.';
                    feedbackEl.style.color = 'var(--accent-pink)';
                }}

                saveScore(elapsed, diff);

                btnEl.textContent = 'RETRY';
                btnEl.className = 'main-btn btn-retry';
            }}
            else if (state === 'STOPPED') {{
                state = 'READY';
                timerEl.textContent = '0.000';
                feedbackEl.textContent = 'READY TO START?';
                feedbackEl.style.color = '#aaa';
                btnEl.textContent = 'START';
                btnEl.className = 'main-btn btn-start';
            }}
        }}

        btnEl.addEventListener('click', trigger);
        window.addEventListener('keydown', (e) => {{
            if (e.code === 'Space') {{
                e.preventDefault();
                trigger();
            }}
        }});

        loadLeaderboard();
    </script>
</body>
</html>
"""
    return render_template_string(html_content)

@app.route('/records')
def records():
    return jsonify(get_records())

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    elapsed = data.get('elapsed')
    diff = data.get('diff')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, elapsed, diff])

    return jsonify(success=True)

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Use a timer to open the browser after the server starts
    Timer(1, open_browser).start()
    app.run(port=5000)

