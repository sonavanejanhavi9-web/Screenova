# Screenova – New Features Setup Guide

## Step 1 — Install Dependencies

```cmd
pip install flask authlib requests
```

---

## ✉️ Feature 1 — Gmail Email Alerts

### How to get a Gmail App Password

1. Go to your Google Account → **Security**
2. Make sure **2-Step Verification** is ON
3. Go to: https://myaccount.google.com/apppasswords
4. Click **"Select app"** → choose **Mail**
5. Click **"Select device"** → choose **Windows Computer** (or any)
6. Click **Generate** → copy the 16-character password

### In app.py — fill in these two lines:

```python
GMAIL_ADDRESS      = "yourname@gmail.com"      # your actual Gmail
GMAIL_APP_PASSWORD = "abcd efgh ijkl mnop"      # 16-char App Password (spaces OK)
```

### When are emails sent?

| Trigger | Email Type |
|---|---|
| User logs usage with High/Severe level | Automatic addiction alert |
| User clicks "📧 Daily Summary" on Dashboard | Daily wellness summary |
| User clicks "📊 Email Weekly Report" on Analytics | Weekly report |

### Adding your email address

- During **Register**, fill in the Email field
- OR on the **Dashboard** or **Analytics** page, type your email and click Save

---

## 🔑 Feature 2 — Google OAuth Login

### Step-by-step setup on Google Cloud Console

1. Go to: https://console.cloud.google.com/
2. Click **"Select a project"** → **"New Project"** → name it `Screenova`
3. Go to **APIs & Services** → **OAuth consent screen**
   - User Type: **External** → Click Create
   - App name: `Screenova`  |  Support email: your Gmail
   - Scroll down → Save and Continue (skip scopes) → Save and Continue
   - Add yourself as a **Test User** → Save
4. Go to **APIs & Services** → **Credentials**
   - Click **"+ Create Credentials"** → **OAuth 2.0 Client IDs**
   - Application type: **Web application**
   - Name: `Screenova Web`
   - Under **Authorised redirect URIs** → click **Add URI**:
     ```
     http://127.0.0.1:5000/google/callback
     ```
   - Click **Create**
5. Copy the **Client ID** and **Client Secret**

### In app.py — fill in:

```python
GOOGLE_CLIENT_ID     = "123456789-abc.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-your-secret-here"
```

### How it works

- User clicks **"Continue with Google"** on Login or Register
- They authenticate with their Google account
- Screenova auto-creates their account using their Google name
- Their Google profile picture appears in the navbar

---

## 🔔 Feature 3 — Browser Push Notifications

### No setup required!

Push notifications work automatically in the browser. Just:

1. Open the Dashboard
2. Click **"🔔 Enable Push"**
3. Click **"Allow"** in the browser popup

### When do push notifications appear?

| Condition | Notification |
|---|---|
| Addiction level is High or Severe | Warning notification every 5 minutes |
| Detox limit exceeded | Alert notification |

### Notes
- Push notifications only work while the browser tab is open (or service worker is active)
- Chrome, Edge, Firefox, and Brave all support this
- Safari on Mac requires macOS Ventura+ with web push enabled

---

## 🚀 Running the Full Project

```cmd
cd D:\janhavi\MPPP\project
pip install flask authlib requests
python app.py
```

Open: http://127.0.0.1:5000

---

## Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: authlib` | Run `pip install authlib` |
| Email not sending | Check App Password — it must be from myaccount.google.com/apppasswords, NOT your normal Gmail password |
| Google login redirect error | Make sure `http://127.0.0.1:5000/google/callback` is added in Google Console exactly as shown |
| Push notification not showing | Make sure you clicked "Allow" when the browser asked for permission |
| `TemplateNotFound` | Run `python app.py` from the folder that contains `templates/` |
