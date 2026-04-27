import streamlit as st
import imaplib
import email
from email.header import decode_header
import pandas as pd
import re
import plotly.express as px
import base64
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="MailSentry Insight™",
    layout="wide",
    page_icon="🛡️"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

.header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

.header img {
    width: 60px;
}

.header-title {
    font-size: 28px;
    font-weight: bold;
    color: #00FFA3;
}

.kpi-container {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
    flex-wrap: wrap;
}

.kpi-card {
    flex: 1 1 120px;
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    text-align: center;
}

.kpi-value {
    font-size: 34px;
    font-weight: bold;
    color: #00FFA3;
}

.kpi-label {
    color: #94a3b8;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

logo_base64 = get_base64_image("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_base64}">' if logo_base64 else ''

st.markdown(f"""
<div class="header">
    {logo_html}
    <div class="header-title">MailSentry Insight™ 2.0</div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("logo.png")
    st.title("Control Panel")

    email_user = st.text_input("Gmail")
    email_pass = st.text_input("App Password", type="password")
    fetch_limit = st.slider("Emails", 10, 500, 50)

    fetch_btn = st.button("Fetch Emails")

# ---------------- FUNCTIONS ----------------
def clean_text(text):
    text = re.sub('<.*?>', '', text)
    text = re.sub('[^a-zA-Z0-9 ]', '', text)
    return text.lower()

def classify(text):
    text = text.lower()

    if any(k in text for k in ["invoice", "payment", "bill"]):
        return "Invoice"
    elif any(k in text for k in ["error", "issue", "failed", "problem"]):
        return "Support"
    elif any(k in text for k in ["resume", "job", "application"]):
        return "HR"
    elif any(k in text for k in ["buy", "interested", "price", "quote"]):
        return "Sales Lead"
    elif any(k in text for k in ["meeting", "team", "update"]):
        return "Internal"
    else:
        return "Spam"
def extract_entities(text):
    emails = re.findall(r"\S+@\S+", text)
    phones = re.findall(r"\d{10}", text)
    return emails, phones

def fetch_emails(user, password, limit):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, password)
    mail.select("inbox")

    _, messages = mail.search(None, "ALL")
    ids = messages[0].split()[-limit:]

    data = []

    for i in ids:
        _, msg_data = mail.fetch(i, "(RFC822)")
        for res in msg_data:
            if isinstance(res, tuple):
                msg = email.message_from_bytes(res[1])

                subject, _ = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                sender = msg.get("From")
                date = msg.get("Date")

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                clean = clean_text(body)
                category = classify(clean)
                emails, phones = extract_entities(body)

                data.append({
                    "Sender": sender,
                    "Subject": subject,
                    "Date": date,
                    "Category": category,
                    "Emails": ", ".join(emails),
                    "Phones": ", ".join(phones),
                    "Preview": body[:200]
                })

    mail.logout()
    return pd.DataFrame(data)


# ---------------- MAIN ----------------
if fetch_btn:
    with st.spinner("Fetching Emails..."):
        df = fetch_emails(email_user, email_pass, fetch_limit)

    if not df.empty:

        df.columns = df.columns.str.strip()

        if 'Category' not in df.columns:
            st.error("Category column missing")
        else:
            df['Category'] = df['Category'].fillna("Spam")

            # ---------------- SUMMARY ----------------
            total = df.shape[0]

            summary_df = df['Category'].value_counts().reset_index()
            summary_df.columns = ["Category", "Count"]
            summary_df["Percentage (%)"] = (summary_df["Count"] / total * 100).round(2)

            st.markdown("### 📊 Category Summary Table")
            st.dataframe(summary_df, use_container_width=True)

            # ---------------- PROGRESS ----------------
            st.markdown("### 📈 Category Distribution Progress")
            for _, row in summary_df.iterrows():
                st.write(f"{row['Category']} ({row['Count']})")
                st.progress(int(row["Percentage (%)"]))

        # ---------------- CHARTS ----------------
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.pie(df, names="Category", title="Category Distribution")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.histogram(df, x="Category", title="Category Frequency")
            st.plotly_chart(fig2, use_container_width=True)

        # ---------------- TABLE ----------------
        st.markdown("### 📄 Email Data")
        st.dataframe(df, use_container_width=True)

        # ---------------- DOWNLOAD ----------------
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False),
            "emails.csv"
        )

    else:
        st.error("No emails found")