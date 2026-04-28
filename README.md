 🛡️ MailSentry Insight™  
### Enterprise Email Intelligence & Analytics Engine

MailSentry Insight™ is a powerful email intelligence system that connects to a live Gmail inbox, processes emails, classifies them into business categories, extracts structured data, and generates actionable analytics dashboards.

---

## 🚀 Features

- **[NEW]** 🔐 Secure Login & Session Management (IMAP Authentication)
- **[NEW]** 📅 Dynamic Date Range Filtering
- **[NEW]** 🧭 Tabbed Navigation (Dashboard Overview vs Detailed Analysis)
- **[NEW]** ✨ Interactive UI Animations
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
  - Email Frequency (Histogram)
  - Emails Over Time (Line Graph)
  - Summary Table
- 📁 CSV Export for Reporting
- 🎨 Modern UI Dashboard (Glassmorphism Design with Transparent Charts)










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
<img width="1366" height="2040" alt="Dashbord" src="https://github.com/user-attachments/assets/e49ad7b3-2131-45e4-8ae8-76e78970ff39" />


---
<img width="1366" height="1538" alt="detiled view" src="https://github.com/user-attachments/assets/2a81d5da-d156-4506-ac1d-3f998a7c6bb6" />


---
* Email classification results
* Structured extracted data
* Downloadable CSV report



https://github.com/user-attachments/assets/e90cde2f-0899-4388-9a82-4ca77c32c43e



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


