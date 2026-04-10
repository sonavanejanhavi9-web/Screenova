# 🌿 Screenova — Social Media Addiction Analyzer/Digital Wellness System

> A web-based application to track social media usage, detect addiction levels, calculate digital health scores, and promote healthier screen habits.

---

## 👥 Team

| Name | Role |
|------|------|
| Janhavi Sonavane | Developer |
| Shreeharsha Rumade | Developer |
| Nikita Santra | Developer |
| Shravani Shirude | Developer |

**Academic Year:** 2025–2026  
**Institute:** Rajiv Gandhi Institute of Technology (RGIT), Mumbai  
**Class:** SE IT-B, Semester 4

---

## 📌 Project Overview

Screenova helps users — especially students — monitor and control their daily digital consumption. It tracks app-wise screen time, analyses addiction severity, generates a personalised health score, visualises weekly trends, enforces detox limits, and provides a wellness chatbot — all without any external database.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask |
| Frontend | HTML, CSS, JavaScript |
| Template Engine | Jinja2 |
| Charts | Chart.js 4.4.1 |
| Data Storage | JSON files |
| Push Notifications | Service Worker (sw.js) |

---

## 📁 Project Structure

```
screenova_project/
├── app.py                  # Main Flask backend — routes & business logic
├── users.json              # User account storage
├── usage.json              # Daily screen time records
├── detox_limits.json       # Per-user detox limits
├── static/
│   ├── style.css           # Global styles
│   ├── script.js           # Frontend interactivity
│   └── sw.js               # Service Worker for push notifications
└── templates/
    ├── home.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── usage.html
    ├── analytics.html
    ├── detox.html
    └── chatbot.html
```

---

## 🧩 Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | **Authentication** | Register, Login, Session management, Logout |
| 2 | **Usage Tracking** | Date picker, per-app minutes input, save to JSON |
| 3 | **Addiction Analysis** | Level detection algorithm + Health Score calculator |
| 4 | **Weekly Analytics** | 7-day Chart.js graphs + trend detection |
| 5 | **Digital Detox** | Daily limit slider, warning banners |
| 6 | **Chatbot** | Keyword matching with live JSON data replies |

---

## 🔢 Core Algorithms

### Addiction Level Detection

```
hours = total_minutes / 60

< 2 hours  → 🟢 Healthy
2–4 hours  → 🟡 Moderate
4–6 hours  → 🔴 High
> 6 hours  → 🚨 Severe
```

### Digital Health Score

```
≤ 1 hour  → 100
2 hours   → 85
3 hours   → 70
4 hours   → 55
5 hours   → 40
6 hours   → 25
> 6 hours → max(0, 25 − (hours − 6) × 5)
```

### Weekly Trend Detection

```
first_half  = sum of days 1–3
second_half = sum of days 5–7

second_half > first_half → 📈 Increasing
second_half < first_half → 📉 Decreasing
equal                    → ➡️ Stable
```

---

## ✨ Innovative Features

1. **Digital Health Score** — Original wellness scoring algorithm unique to Screenova
2. **Live Addiction Preview** — Addiction level updates in real-time as user types minutes
3. **Personalised Chatbot** — Reads live JSON data to give user-specific wellness advice
4. **Push Notifications** — Background alerts via Service Worker even when tab is inactive

---

## 🏗️ Architecture

Screenova follows a **3-Tier MVC Pattern**:

```
Presentation Layer   →   Browser (HTML, CSS, JS, Chart.js)
Application Layer    →   Flask app.py (Routes, Jinja2, Business Logic)
Data Layer           →   users.json, usage.json, detox_limits.json
```

| MVC Role | Files |
|----------|-------|
| Model | JSON files |
| View | HTML templates |
| Controller | app.py |

---

## 🧠 Programming Paradigms

| Paradigm | Implementation in Screenova |
|----------|-----------------------------|
| **Procedural** | `load_json()`, `save_json()`, `get_addiction_level()`, `get_health_score()` |
| **Object-Oriented** | `app = Flask(__name__)`, `@app.route` decorator, `session` dictionary |
| **Event-Driven** | `onclick`, `oninput`, `fetch()` AJAX calls, `setInterval()` |

---

## 🧹 Code Quality

- ✅ **Single Responsibility** — each function does exactly one thing
- ✅ **Meaningful Names** — `hours_today`, `detox_exceeded`, `total_minutes`
- ✅ **DRY Principle** — `load_json` / `save_json` reused across all routes
- ✅ **Consistent Error Handling** — unauthenticated access redirects to login
- ✅ **Docstrings** — every function documented
- ✅ **Separation of Concerns** — Python = Logic, HTML = Structure, CSS = Design, JS = Behaviour

---

## 🧪 Testing

| Category | Details |
|----------|---------|
| Total Test Cases | 15 |
| Pass Rate | 100% ✅ |
| Types | Valid input, Invalid input, Boundary value, Edge case |
| Boundary Values | 120 min (2 hrs), 240 min (4 hrs), 360 min (6 hrs) |

---

## 🗃️ Data Storage Format

**users.json**
```json
{ "username": "janhavi", "password": "hashed_password" }
```

**usage.json**
```json
{
  "janhavi": {
    "2025-04-01": {
      "Instagram": 45,
      "YouTube": 60,
      "total": 105
    }
  }
}
```

**detox_limits.json**
```json
{ "janhavi": 3 }
```

---

## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-repo/screenova.git
cd screenova_project

# 2. Install dependencies
pip install flask

# 3. Run the app
python app.py

# 4. Open in browser
http://127.0.0.1:5000
```



## 🔮 Future Scope

- Integration with real screen time APIs (Android/iOS)
- Machine learning-based personalised recommendations
- Social accountability features (friend groups)
- Export reports as PDF
- Dark mode and accessibility improvements

---

*Made with 💚 by Team Screenova — SE IT-B, RGIT Mumbai*