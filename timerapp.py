import webbrowser
import os
import tempfile

html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>7 SECONDS PERFECT CHALLENGE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        :root {
            --bg-color: #050510;
            --panel-bg: rgba(255, 255, 255, 0.05);
            --accent-cyan: #00f2ff;
            --accent-pink: #ff2a6d;
            --accent-gold: #ffdf00;
            --text-color: #ffffff;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Rajdhani', sans-serif;
            user-select: none;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: radial-gradient(circle at center, #1a1a3a 0%, #050510 100%);
        }

        .container {
            width: 450px;
            padding: 40px;
            background: var(--panel-bg);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            margin-bottom: 5px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
        }

        .subtitle {
            color: #888;
            font-size: 1.1rem;
            margin-bottom: 40px;
        }

        .timer-box {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            padding: 40px 20px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(0, 242, 255, 0.2);
        }

        .timer-box::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            animation: sweep 3s infinite;
        }

        @keyframes sweep {
            0% { left: -100%; }
            100% { left: 200%; }
        }

        #timer {
            font-family: 'Orbitron', sans-serif;
            font-size: 5rem;
            font-weight: 700;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
            transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .hidden-timer {
            color: #222 !important;
            text-shadow: none !important;
        }

        #feedback {
            height: 30px;
            margin-bottom: 30px;
            font-size: 1.4rem;
            font-weight: 500;
            color: #aaa;
            transition: all 0.3s;
        }

        .main-btn {
            width: 100%;
            padding: 20px;
            font-size: 1.5rem;
            font-weight: 700;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .btn-start {
            background: var(--accent-cyan);
            color: #000;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
        }

        .btn-stop {
            background: var(--accent-pink);
            color: #fff;
            box-shadow: 0 0 20px rgba(255, 42, 109, 0.4);
        }

        .btn-retry {
            background: #fff;
            color: #000;
        }

        .main-btn:active {
            transform: scale(0.95);
        }

        .perfect { color: var(--accent-gold) !important; text-shadow: 0 0 30px var(--accent-gold) !important; animation: pulse 0.5s infinite alternate; }
        @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }

        .hint {
            margin-top: 20px;
            font-size: 0.9rem;
            color: #444;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>7.000 SEC</h1>
        <p class="subtitle">HIT THE EXACT MOMENT</p>

        <div class="timer-box">
            <div id="timer">0.00</div>
        </div>

        <div id="feedback">READY TO START?</div>

        <button id="mainBtn" class="main-btn btn-start">START</button>

        <p class="hint">TIP: TIMER HIDES AFTER 3 SECONDS</p>
    </div>

    <script>
        const timerEl = document.getElementById('timer');
        const feedbackEl = document.getElementById('feedback');
        const btnEl = document.getElementById('mainBtn');

        let state = 'READY'; // READY, RUNNING, STOPPED
        let startTime = 0;
        let timerInterval = null;

        function updateDisplay() {
            const elapsed = (Date.now() - startTime) / 1000;

            if (elapsed > 3.0) {
                timerEl.textContent = '?.???';
                timerEl.classList.add('hidden-timer');
                feedbackEl.textContent = 'FEEL THE BEAT...';
                feedbackEl.style.color = 'var(--accent-pink)';
            } else {
                timerEl.textContent = elapsed.toFixed(3);
            }
        }

        function trigger() {
            if (state === 'READY') {
                state = 'RUNNING';
                startTime = Date.now();
                btnEl.textContent = 'STOP';
                btnEl.className = 'main-btn btn-stop';
                feedbackEl.textContent = 'CONCENTRATE...';
                feedbackEl.style.color = 'var(--accent-cyan)';
                timerEl.classList.remove('hidden-timer');
                timerEl.classList.remove('perfect');

                timerInterval = setInterval(updateDisplay, 10);
            }
            else if (state === 'RUNNING') {
                state = 'STOPPED';
                clearInterval(timerInterval);
                const endTime = Date.now();
                const elapsed = (endTime - startTime) / 1000;
                const diff = Math.abs(7.0 - elapsed);

                timerEl.textContent = elapsed.toFixed(3);
                timerEl.classList.remove('hidden-timer');

                if (diff === 0) {
                    feedbackEl.textContent = 'GOD-LIKE! PERFECT 0.000!';
                    feedbackEl.style.color = 'var(--accent-gold)';
                    timerEl.classList.add('perfect');
                } else if (diff < 0.01) {
                    feedbackEl.textContent = 'INSANE PRECISION!';
                    feedbackEl.style.color = 'var(--accent-cyan)';
                    timerEl.classList.add('perfect');
                } else if (diff < 0.05) {
                    feedbackEl.textContent = 'LEGENDARY!';
                    feedbackEl.style.color = '#fff';
                } else if (diff < 0.2) {
                    feedbackEl.textContent = 'GREAT JOB!';
                    feedbackEl.style.color = '#fff';
                } else if (diff < 0.5) {
                    feedbackEl.textContent = 'NOT BAD.';
                    feedbackEl.style.color = '#888';
                } else {
                    feedbackEl.textContent = 'TOO FAR! TRY AGAIN.';
                    feedbackEl.style.color = 'var(--accent-pink)';
                }

                btnEl.textContent = 'RETRY';
                btnEl.className = 'main-btn btn-retry';
            }
            else if (state === 'STOPPED') {
                state = 'READY';
                timerEl.textContent = '0.000';
                feedbackEl.textContent = 'READY TO START?';
                feedbackEl.style.color = '#aaa';
                btnEl.textContent = 'START';
                btnEl.className = 'main-btn btn-start';
            }
        }

        btnEl.addEventListener('click', trigger);
        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                trigger();
            }
        });
    </script>
</body>
</html>
"""

# Create a temporary HTML file and open it
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    f.write(html_content)
    temp_path = f.name

print(f"Opening 7 Seconds Challenge...")
webbrowser.open('file://' + os.path.realpath(temp_path))
