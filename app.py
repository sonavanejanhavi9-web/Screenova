"""
Screenova - Digital Wellness System
app.py - Main backend (register, login, usage, analytics, detox, chatbot)
"""

from flask import (Flask, render_template, request, redirect,
                   url_for, session, jsonify, send_from_directory)
import json, os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "screenova_secret_2026"

# ── JSON file paths ───────────────────────────────────────
USERS_FILE = "users.json"
USAGE_FILE = "usage.json"
DETOX_FILE = "detox_limits.json"

# ── Helpers ───────────────────────────────────────────────
def load_json(filepath):
    """Load data from a JSON file. Returns empty dict if file missing."""
    if not os.path.exists(filepath): return {}
    with open(filepath, "r") as f: return json.load(f)

def save_json(filepath, data):
    """Save data to a JSON file."""
    with open(filepath, "w") as f: json.dump(data, f, indent=4)

def get_addiction_level(mins):
    """Return addiction level, color and icon based on total minutes."""
    h = mins / 60
    if h < 2:   return "Healthy",  "#00c896", "🌿"
    elif h < 4: return "Moderate", "#f0a500", "⚠️"
    elif h < 6: return "High",     "#ff6b35", "🔥"
    else:       return "Severe",   "#e63946", "🚨"

def get_health_score(mins):
    """Return a health score out of 100. Lower screen time = higher score."""
    h = mins / 60
    if h <= 1:   return 100
    elif h <= 2: return 85
    elif h <= 3: return 70
    elif h <= 4: return 55
    elif h <= 5: return 40
    elif h <= 6: return 25
    else:        return max(0, 25 - int((h - 6) * 5))

# ── Routes: Home ──────────────────────────────────────────
@app.route("/")
def home():
    return render_template("home.html")

# ── Routes: Register ──────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users    = load_json(USERS_FILE)
        if username in users:
            return render_template("register.html", error="Username already exists.")
        users[username] = {
            "password": password,
            "created":  str(datetime.now().date())
        }
        save_json(USERS_FILE, users)
        return redirect(url_for("login"))
    return render_template("register.html")

# ── Routes: Login ─────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users    = load_json(USERS_FILE)
        if username in users and users[username].get("password") == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

# ── Routes: Logout ────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ── Routes: Dashboard ─────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect(url_for("login"))
    user       = session["user"]
    today      = str(datetime.now().date())
    usage_data = load_json(USAGE_FILE)
    detox_data = load_json(DETOX_FILE)

    entry     = usage_data.get(user, {}).get(today, {})
    instagram = entry.get("instagram", 0)
    youtube   = entry.get("youtube",   0)
    whatsapp  = entry.get("whatsapp",  0)
    other     = entry.get("other",     0)
    total     = instagram + youtube + whatsapp + other

    level, color, icon = get_addiction_level(total)
    score = get_health_score(total)
    limit = detox_data.get(user, {}).get("limit", 0)

    return render_template("dashboard.html",
        user=user, today=today, total=total,
        instagram=instagram, youtube=youtube,
        whatsapp=whatsapp,   other=other,
        level=level, color=color, icon=icon,
        score=score, limit=limit,
        detox_exceeded=limit > 0 and (total / 60) > limit)

# ── Routes: Usage Input ───────────────────────────────────
@app.route("/usage", methods=["GET", "POST"])
def usage():
    if "user" not in session: return redirect(url_for("login"))
    user = session["user"]; message = None

    if request.method == "POST":
        date      = request.form.get("date")
        instagram = int(request.form.get("instagram", 0))
        youtube   = int(request.form.get("youtube",   0))
        whatsapp  = int(request.form.get("whatsapp",  0))
        other     = int(request.form.get("other",     0))
        other_name = request.form.get("other_name", "Other Apps")
        total     = instagram + youtube + whatsapp + other

        usage_data = load_json(USAGE_FILE)
        if user not in usage_data: usage_data[user] = {}
        usage_data[user][date] = {
            "instagram": instagram, "youtube": youtube,
            "whatsapp":  whatsapp,  "other":   other,
            "other_name": other_name, "total":  total
        }
        save_json(USAGE_FILE, usage_data)
        message = "Usage saved successfully!"

    return render_template("usage.html", user=user, message=message,
                           today=str(datetime.now().date()))

# ── Routes: Analytics ─────────────────────────────────────
@app.route("/analytics")
def analytics():
    if "user" not in session: return redirect(url_for("login"))
    user  = session["user"]
    udata = load_json(USAGE_FILE).get(user, {})
    days  = [datetime.now().date() - timedelta(days=i) for i in range(6, -1, -1)]
    totals = [udata.get(str(d), {}).get("total", 0) for d in days]
    labels = [d.strftime("%a %d") for d in days]
    avg    = round(sum(totals) / 7, 1)

    at = {"Instagram": 0, "YouTube": 0, "WhatsApp": 0, "Other": 0}
    for d in days:
        e = udata.get(str(d), {})
        at["Instagram"] += e.get("instagram", 0)
        at["YouTube"]   += e.get("youtube",   0)
        at["WhatsApp"]  += e.get("whatsapp",  0)
        at["Other"]     += e.get("other",     0)

    most_used = max(at, key=at.get)
    first_half  = sum(totals[:3])
    second_half = sum(totals[4:])
    if second_half > first_half:   trend, tc = "📈 Increasing", "#e63946"
    elif second_half < first_half: trend, tc = "📉 Decreasing", "#00c896"
    else:                          trend, tc = "➡️ Stable",     "#f0a500"

    return render_template("analytics.html", user=user,
        labels=json.dumps(labels), daily_totals=json.dumps(totals),
        avg=avg, most_used=most_used, app_totals=at,
        trend=trend, trend_color=tc)

# ── Routes: Detox ─────────────────────────────────────────
@app.route("/detox", methods=["GET", "POST"])
def detox():
    if "user" not in session: return redirect(url_for("login"))
    user = session["user"]; ddata = load_json(DETOX_FILE); message = None

    if request.method == "POST":
        limit = float(request.form.get("limit", 2))
        if user not in ddata: ddata[user] = {}
        ddata[user]["limit"] = limit
        save_json(DETOX_FILE, ddata)
        message = f"Detox limit set to {limit} hours/day!"

    cl          = ddata.get(user, {}).get("limit", None)
    today       = str(datetime.now().date())
    total_today = load_json(USAGE_FILE).get(user, {}).get(today, {}).get("total", 0)
    hours_today = round(total_today / 60, 2)

    return render_template("detox.html", user=user, current_limit=cl,
        hours_today=hours_today, exceeded=cl and hours_today > cl,
        message=message)

# ── Routes: Chatbot ───────────────────────────────────────
@app.route("/chatbot")
def chatbot():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("chatbot.html", user=session["user"])

@app.route("/chat_api", methods=["POST"])
def chat_api():
    """Rule-based chatbot — reads live usage data and returns wellness tips."""
    if "user" not in session: return jsonify({"reply": "Please log in first."})
    user  = session["user"]
    msg   = request.json.get("message", "").lower().strip()
    udata = load_json(USAGE_FILE).get(user, {})
    today = str(datetime.now().date())
    total = udata.get(today, {}).get("total", 0)
    hrs   = round(total / 60, 2)
    level, _, _ = get_addiction_level(total)

    if any(k in msg for k in ["screen time", "usage", "how much", "today"]):
        reply = f"📊 Today you've spent <b>{total} minutes ({hrs} hrs)</b> on screen. Level: <b>{level}</b>."
    elif any(k in msg for k in ["stress", "stressed", "anxious", "anxiety"]):
        reply = "🧘 Try the 20-20-20 rule: every 20 min, look 20 feet away for 20 seconds. Take a 10-min walk!"
    elif any(k in msg for k in ["sad", "unhappy", "depressed", "lonely"]):
        reply = "💙 Connect with someone in person today. Limit social media to 30 mins and spend time outdoors."
    elif any(k in msg for k in ["reduce", "cut down", "less screen", "limit"]):
        reply = "✅ Tips:<br>1. Set a Detox limit.<br>2. No phone 1 hr before bed.<br>3. Delete one app for a week."
    elif any(k in msg for k in ["score", "health score"]):
        s = get_health_score(total)
        reply = f"💚 Health Score: <b>{s}/100</b>. {'Keep it up!' if s >= 70 else 'Try to reduce screen time!'}"
    elif any(k in msg for k in ["hello", "hi", "hey"]):
        reply = f"👋 Hello {user}! I'm your Screenova wellness assistant. Ask me anything!"
    elif any(k in msg for k in ["help", "what can you do"]):
        reply = "🤖 Ask me: 'my screen time', 'I feel stressed', 'how to reduce usage', 'my score'"
    elif any(k in msg for k in ["sleep", "insomnia", "can't sleep"]):
        reply = "😴 Avoid screens 1 hr before bed. Use Night Mode after 8 PM. Your sleep will improve!"
    elif any(k in msg for k in ["addiction", "addicted"]):
        reply = f"🔍 Current level: <b>{level}</b>. Awareness is step one. Use Detox Mode to set limits."
    else:
        reply = "🤔 Try: 'What is my screen time?', 'I feel stressed', 'How to reduce usage?'"
    return jsonify({"reply": reply})

# ── Routes: Push Notifications (browser only) ─────────────
@app.route("/sw.js")
def service_worker():
    return send_from_directory("static", "sw.js", mimetype="application/javascript")

@app.route("/push_status")
def push_status():
    """Returns today's addiction level for the browser push notification check."""
    if "user" not in session: return jsonify({"level": "unknown", "total": 0})
    user  = session["user"]
    today = str(datetime.now().date())
    total = load_json(USAGE_FILE).get(user, {}).get(today, {}).get("total", 0)
    level, color, icon = get_addiction_level(total)
    detox_limit = load_json(DETOX_FILE).get(user, {}).get("limit", 0)
    return jsonify({"level": level, "total": total, "icon": icon,
                    "detox_exceeded": detox_limit > 0 and (total / 60) > detox_limit,
                    "detox_limit": detox_limit})

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    for f in [USERS_FILE, USAGE_FILE, DETOX_FILE]:
        if not os.path.exists(f): save_json(f, {})
    app.run(debug=True)
