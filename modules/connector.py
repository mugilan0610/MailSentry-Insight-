import imaplib
import email
import logging
from email.header import decode_header

def connect_and_fetch(email_user: str, app_password: str, limit: int = 10) -> list:
    """
    Connects to Gmail IMAP, fetches recent emails.
    Silently handles exceptions.
    Returns list of dicts: [{'subject': ..., 'sender': ..., 'date': ..., 'body': ...}]
    """
    emails = []
    try:
        if not email_user or not app_password:
            return emails
            
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, app_password)
        mail.select("inbox")
        
        # Search for all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return emails
            
        # Get list of email IDs
        email_ids = messages[0].split()
        
        # Fetch latest 'limit' emails and reverse to show most recent first
        latest_ids = email_ids[-limit:][::-1]
        
        for e_id in latest_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue
                
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Parse subject
                    subject, encoding = decode_header(msg.get("Subject", "No Subject"))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="replace")
                    elif subject is None:
                        subject = ""
                    else:
                        subject = str(subject)
                    
                    
                    sender, encoding = decode_header(msg.get("From", "Unknown"))[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding if encoding else "utf-8", errors="replace")
                    elif sender is None:
                        sender = "Unknown"
                    else:
                        sender = str(sender)
                        
                    date = msg.get("Date", "Unknown")
                    
                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            try:
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                    break
                                elif content_type == "text/html" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                    # Fallback to HTML if plain text not found
                            except:
                                pass
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except:
                            pass
                            
                    emails.append({
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "body": body
                    })
                    
        mail.logout()
        
    except Exception as e:
        logging.error(f"IMAP Connection error: {e}")
        
    return emails
