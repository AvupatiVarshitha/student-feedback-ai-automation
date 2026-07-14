# 🤖 AI-Powered Student Feedback Automation & Analytics System

An end-to-end AI-powered automation platform that streamlines the complete student feedback process—from collecting feedback through Google Forms to generating AI-driven analytics reports and automatically emailing professional PDF reports.

---

## 🚀 Features

- 📢 Automatically sends Google Form links to Telegram groups
- 📋 Collects student feedback from Google Forms
- 📊 Reads responses directly from Google Sheets
- 🧹 Cleans and processes raw feedback data
- 🤖 Uses Ollama (Gemma 3) for AI-powered feedback analysis
- 📈 Generates visual analytics using Matplotlib
- 📄 Creates executive-style PDF reports using ReportLab
- 📧 Automatically emails the generated report
- ⏰ Supports scheduled automation using APScheduler

---

# 🛠 Tech Stack

- Python
- Ollama (Gemma 3)
- Google Forms
- Google Sheets API
- Telegram Bot API
- APScheduler
- Matplotlib
- ReportLab
- SMTP Email
- REST APIs

---

# 📂 Project Structure

```
student-feedback-ai-automation/

backend/
│
├── scheduler.py
├── config.py
│
├── services/
│   ├── data_processor.py
│   ├── report_builder.py
│   ├── charts_service.py
│   ├── pdf_service.py
│   ├── email_service.py
│   ├── telegram_service.py
│   ├── sheets_service.py
│   └── ollama_service.py
│
├── prompts/
│
├── reports/
│
└── tests/

dashboard/
```

---

# ⚙️ Workflow

```
Scheduler
     │
     ▼
Telegram Bot
     │
     ▼
Google Form
     │
Students Submit Feedback
     │
     ▼
Google Sheets
     │
     ▼
Data Processing
     │
     ▼
AI Analysis (Gemma 3)
     │
     ▼
Charts
     │
     ▼
Professional PDF
     │
     ▼
Automatic Email
```

---

# 📊 Generated Analytics

The system generates:

- Course Satisfaction Score
- Trainer Rating
- Program Team Rating
- Concept Clarity Analysis
- Course Pace Analysis
- Assignment Helpfulness
- Top Learning Topics
- Common Challenges
- Improvement Suggestions
- AI-generated Action Items
- Overall Quality Score

---

# 🤖 AI Capabilities

The system automatically generates:

- Overall Sentiment
- Key Strengths
- Major Concerns
- Learning Trends
- Actionable Recommendations
- Overall Quality Score

using **Gemma 3 (Ollama)**.

---

# 📧 Automation

The complete workflow is automated.

At the scheduled time:

✅ Sends Google Form to Telegram

After feedback collection:

✅ Reads Google Sheet

✅ Generates Analytics

✅ Generates Charts

✅ Generates Professional PDF

✅ Emails Report Automatically

---

# 📷 Screenshots

Add screenshots here.

- Telegram Notification
- Google Form
- Charts
- PDF Report
- Email Report

---

# 🚀 Future Enhancements

- Multi-course support
- Dashboard with Streamlit
- Trend analysis across weeks
- WhatsApp integration
- SMS notifications
- Cloud deployment
- Admin login
- Real-time analytics dashboard

---

# 👩‍💻 Author

**Varshitha**

B.Tech Computer Science (Data Science)

AI | Python | Automation | Backend Development



# 📷 Screenshots

## Telegram Notification

![Telegram](assets/telegram.png)

---

## Google Form

![Google Form](assets/google form.png)

---

## Analytics Charts

![Charts](assets/charts.png)

---

## Generated PDF Report

![PDF](assets/pdf.png)

---

## Email Report

![Email](assets/mail.png)