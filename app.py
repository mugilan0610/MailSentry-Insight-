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

# ---------------- STATE INITIALIZATION ----------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'email_user' not in st.session_state:
    st.session_state['email_user'] = ""
if 'email_pass' not in st.session_state:
    st.session_state['email_pass'] = ""
if 'email_data' not in st.session_state:
    st.session_state['email_data'] = pd.DataFrame()

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

@keyframes slideUpFade {
    0% { opacity: 0; transform: translateY(40px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

/* Animate the login form */
div[data-testid="stForm"] {
    animation: slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    padding: 40px !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    backdrop-filter: blur(20px);
}

.login-title {
    animation: fadeIn 1s ease-in;
    text-align: center;
    margin-bottom: 20px;
    font-size: 36px;
    background: -webkit-linear-gradient(#00FFA3, #0284c7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
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
    border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.2s, background 0.2s;
}

.kpi-card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.08);
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

def check_login(user, password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, password)
        mail.logout()
        return True
    except Exception as e:
        return False

def fetch_emails(user, password, limit):
    try:
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

                    subject_data = decode_header(msg.get("Subject", "No Subject"))[0]
                    subject = subject_data[0]
                    encoding = subject_data[1]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="replace")

                    sender_data = decode_header(msg.get("From", "Unknown"))[0]
                    sender = sender_data[0]
                    encoding = sender_data[1]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding if encoding else "utf-8", errors="replace")
                    
                    date = msg.get("Date", "Unknown")

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                except:
                                    pass
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                        except:
                            pass

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
    except Exception as e:
        st.error(f"Error fetching emails: {e}")
        return pd.DataFrame()


# ---------------- LOGIN SCREEN ----------------
if not st.session_state['logged_in']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='login-title'>Welcome to MailSentry</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Sign In</h3>", unsafe_allow_html=True)
            email_user = st.text_input("Gmail Address", placeholder="e.g. your_email@gmail.com")
            email_pass = st.text_input("App Password", type="password", placeholder="Enter your 16-character app password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Authenticate", use_container_width=True)
            
            if submitted:
                if email_user and email_pass:
                    with st.spinner("Establishing secure connection..."):
                        if check_login(email_user, email_pass):
                            st.session_state['logged_in'] = True
                            st.session_state['email_user'] = email_user
                            st.session_state['email_pass'] = email_pass
                            st.rerun()
                        else:
                            st.error("Authentication failed. Please check your credentials.")
                else:
                    st.warning("Please enter both email and password.")

# ---------------- MAIN DASHBOARD ----------------
else:
    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.image("logo.png")
        st.title("Control Panel")
        
        st.markdown(f"**Account:**<br><small>{st.session_state['email_user']}</small>", unsafe_allow_html=True)
        
        st.markdown("---")
        nav_selection = st.radio("Navigation", ["Dashboard Overview", "Detailed Analysis"])
        st.markdown("---")
        
        # We will render the Date Filter here dynamically if df is not empty
        filter_container = st.container()
        
        st.markdown("---")
        fetch_limit = st.slider("Emails to Fetch", 10, 500, 50)
        fetch_btn = st.button("Fetch New Emails", use_container_width=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['email_user'] = ""
            st.session_state['email_pass'] = ""
            st.session_state['email_data'] = pd.DataFrame()
            st.rerun()

    # ---------------- FETCH LOGIC ----------------
    if fetch_btn or st.session_state['email_data'].empty:
        with st.spinner("Fetching Emails..."):
            df = fetch_emails(st.session_state['email_user'], st.session_state['email_pass'], fetch_limit)
            if not df.empty:
                st.session_state['email_data'] = df
            else:
                st.warning("No emails found or failed to fetch.")

    df = st.session_state['email_data']

    if not df.empty:
        df = df.copy() # Avoid modifying the session state directly when filtering
        df.columns = df.columns.str.strip()
        if 'Category' not in df.columns:
            st.error("Category column missing")
        else:
            df['Category'] = df['Category'].fillna("Spam")
            
            # Extract Dates for Filtering
            df['Parsed_Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce', utc=True)
            df['Day'] = df['Parsed_Date'].dt.date
            
            # ---------------- DATE FILTER ----------------
            min_date = df['Day'].dropna().min()
            max_date = df['Day'].dropna().max()
            
            if pd.notnull(min_date) and pd.notnull(max_date):
                with filter_container:
                    st.markdown("**Filters**")
                    date_range = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
                    
                    if len(date_range) == 2:
                        start_date, end_date = date_range
                        df = df[(df['Day'] >= start_date) & (df['Day'] <= end_date)]

            # Recalculate metrics based on filtered df
            total = df.shape[0]
            summary_df = df['Category'].value_counts().reset_index()
            summary_df.columns = ["Category", "Count"]
            if total > 0:
                summary_df["Percentage (%)"] = (summary_df["Count"] / total * 100).round(2)
            else:
                summary_df["Percentage (%)"] = 0

            # ---------------- NAVIGATION VIEWS ----------------
            if nav_selection == "Dashboard Overview":
                st.markdown("### 📊 Dashboard Overview")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if total > 0:
                    # KPIs
                    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total}</div><div class="kpi-label">Total Emails</div></div>', unsafe_allow_html=True)
                    if 'Invoice' in summary_df['Category'].values:
                        inv_count = summary_df[summary_df['Category'] == 'Invoice']['Count'].values[0]
                        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{inv_count}</div><div class="kpi-label">Invoices</div></div>', unsafe_allow_html=True)
                    if 'Support' in summary_df['Category'].values:
                        sup_count = summary_df[summary_df['Category'] == 'Support']['Count'].values[0]
                        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{sup_count}</div><div class="kpi-label">Support Tickets</div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<hr style='opacity: 0.2; margin: 30px 0;'>", unsafe_allow_html=True)

                    col1, spacer, col2 = st.columns([1, 0.1, 1.5])
                    with col1:
                        st.markdown("#### Category Distribution Progress")
                        st.markdown("<br>", unsafe_allow_html=True)
                        for _, row in summary_df.iterrows():
                            st.write(f"{row['Category']} ({row['Count']})")
                            st.progress(int(row["Percentage (%)"]))
                            
                    with col2:
                        fig1 = px.pie(df, names="Category", title="Category Share", hole=0.4)
                        fig1.update_layout(margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig1, use_container_width=True)

                    st.markdown("<hr style='opacity: 0.2; margin: 30px 0;'>", unsafe_allow_html=True)

                    # Time Series
                    st.markdown("#### 📈 Emails Over Time")
                    daily_counts = df.groupby('Day').size().reset_index(name='Email Count')
                    
                    if not daily_counts.empty:
                        fig3 = px.line(daily_counts, x='Day', y='Email Count', markers=True)
                        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig3, use_container_width=True)
                    else:
                        st.info("Not enough valid date information to plot Emails Per Day.")
                else:
                    st.info("No emails found in the selected date range.")

            elif nav_selection == "Detailed Analysis":
                st.markdown("### 🔍 Detailed Analysis")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if total > 0:
                    col1, spacer, col2 = st.columns([1, 0.1, 1.5])
                    with col1:
                        st.markdown("#### Category Summary Table")
                        st.dataframe(summary_df, use_container_width=True, height=350)
                    with col2:
                        fig2 = px.histogram(df, x="Category", title="Category Frequency", color="Category")
                        fig2.update_layout(margin=dict(t=30, b=0, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig2, use_container_width=True)

                    st.markdown("<hr style='opacity: 0.2; margin: 30px 0;'>", unsafe_allow_html=True)
                    
                    st.markdown("#### 📄 Email Data Archive")
                    st.dataframe(df.drop(columns=['Parsed_Date', 'Day'], errors='ignore'), use_container_width=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        "⬇️ Download Filtered CSV",
                        df.to_csv(index=False).encode('utf-8'),
                        "filtered_emails.csv",
                        "text/csv",
                        type="primary"
                    )
                else:
                    st.info("No emails found in the selected date range.")