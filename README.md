 🛡️ MailSentry Insight™  
### Enterprise Email Intelligence & Analytics Engine

MailSentry Insight™ is a powerful email intelligence system that connects to a live Gmail inbox, processes emails, classifies them into business categories, extracts structured data, and generates actionable analytics dashboards.

---

## 🚀 Features

- 🔐 Secure Gmail Integration (IMAP + App Password)
- 📥 Bulk Email Processing (Scalable for 500+ emails)
- 🧠 Smart Email Classification
  - Sales Lead
  - Support
  - Invoice
  - HR
  - Internal
  - Spam
- 🔎 Structured Data Extraction (Regex-based)
  - Email addresses
  - Phone numbers
  - Invoice IDs (INV-XXXX)
  - Ticket IDs (TCK-XXXX)
  - Currency values (₹, $)
  - Order IDs
- 📊 Interactive Analytics Dashboard
  - Category Distribution (Pie Chart)
  - Email Frequency (Bar Chart)
  - Summary Table
- 📁 CSV Export for Reporting
- 🎨 Modern UI Dashboard (Glassmorphism Design)










---

## 🏗️ System Architecture


Gmail (IMAP)
↓
Email Fetching Engine
↓
Text Preprocessing
↓
Classification Engine
↓
Entity Extraction (Regex)
↓
Data Storage (DataFrame)
↓
Analytics Dashboard (Streamlit)


---

## ⚙️ Tech Stack

- Python 3.x
- Streamlit (UI Dashboard)
- Pandas (Data Processing)
- Plotly (Visualization)
- IMAPLIB (Email Retrieval)
- Regex (Data Extraction)

---
## 📊 Output
* Dashboard with analytics

---
<img width="1366" height="649" alt="1st " src="https://github.com/user-attachments/assets/07bb6d34-4a99-48bd-9447-930f4446efe6" />

---
<img width="1366" height="768" alt="Screenshot 2026-04-28 023810" src="https://github.com/user-attachments/assets/5b68fd17-73ca-47e1-92aa-b4a9f190a01c" />

---
* Email classification results
* Structured extracted data
* Downloadable CSV report

https://github.com/user-attachments/assets/bc5ef641-6c2f-4145-91bc-8d8c3df41f6e

---

## 📦 Installation

```bash
pip install streamlit pandas plotly
▶️ Run the Application
streamlit run app.py

If error:

python -m streamlit run app.py
🔐 Gmail Setup
Enable 2-Step Verification
Generate App Password
Use:
Email: your Gmail
Password: App Password

📁 Project Structure
MailSentry-Insight/
│
├── app.py
├── logo.png
├── modules/
│   ├── connector.py
│   ├── preprocessing.py
│   ├── classification_engine.py
│   ├── extraction_engine.py
│
└── README.md

⚠️ Security Note
Never upload real credentials
Use .gitignore to exclude:
config.json
.env


📈 Future Enhancements
AI-based classification (ML models)
Real-time email monitoring
Multi-account support
Cloud deployment (Streamlit Cloud)
Advanced anomaly detection


👨‍💻 Author
Mugilan M 
B.Tech Information Technology
Full Stack Developer | ML Enthusiast


