# 🎓 Class Performance Dashboard

A Streamlit web app for analysing student performance — with role-based login.

## 📦 Setup

```bash
pip install -r requirements.txt
streamlit run class_performance_app.py
```

Open http://localhost:8501 in your browser.

## 🔐 Login Credentials

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |
| Staff | staff1   | staff123  |
| Staff | staff2   | staff456  |
| Staff | staff3   | staff789  |

**Admin** sees all 5 dashboard tabs + the 🛡️ Admin Panel tab.  
**Staff** sees all 5 dashboard tabs only.

## ➕ Adding New Staff Accounts

1. Log in as admin → go to the **Admin Panel** tab
2. Fill in the "Add New Staff Account" form and click **Generate Account Entry**
3. Copy the generated Python dict entry into the `USERS` dict in `class_performance_app.py`

## 📁 Files

| File | Description |
|------|-------------|
| `class_performance_app.py` | Main Streamlit app with login |
| `requirements.txt`         | Python dependencies |
| `README.md`                | This file |

## 🖥️ Requirements
Python 3.8+
