import os
import datetime
import smtplib
import markdown
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

class WorkflowActions:
    def __init__(self, notes_path=None, drafts_dir=None):
        # Explicitly reload to pick up any recent .env changes
        load_dotenv()
        
        self.notes_path = notes_path or os.getenv("NOTES_FILE_PATH", "outputs/MASTER_NOTES.md")
        self.drafts_dir = drafts_dir or os.getenv("EMAIL_DRAFTS_PATH", "outputs/email_drafts")
        
        # Email Config
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.recipient_email = os.getenv("EMAIL_RECIPIENT")

        # Debugging (visible in terminal logs)
        if self.sender_email and self.sender_password:
            print(f"DEBUG: SMTP Configured for {self.sender_email}")
        else:
            print("DEBUG: SMTP Credentials MISSING in environment.")

        # Ensure directories exist
        notes_dir = os.path.dirname(self.notes_path)
        if notes_dir and not os.path.exists(notes_dir):
            os.makedirs(notes_dir)
        if not os.path.exists(self.drafts_dir):
            os.makedirs(self.drafts_dir)

    def append_to_notes(self, pulse_data, fee_data):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        quotes_str = '\n- '.join(pulse_data['quotes'])
        actions_str = '\n- '.join(pulse_data['action_ideas'])
        explanation_str = '\n'.join(['- ' + b for b in fee_data['explanation']])
        
        # Handle theme structure
        themes_list = []
        for t in pulse_data.get('themes', []):
            if isinstance(t, dict):
                themes_list.append(f"**{t.get('topic')}**: {t.get('description')}")
            else:
                themes_list.append(f"**{t}**")
        themes_str = "\n- ".join(themes_list)

        content = f"""
## Report Date: {date_str}

### Weekly Product Pulse
{themes_str}

**Quotes:**
- {quotes_str}

**Action Items:**
- {actions_str}

### Fee Explainer ({fee_data['scenario']})
{explanation_str}

**Sources:** {' | '.join(fee_data['sources'])}
**Last checked:** {date_str}
---
"""
        with open(self.notes_path, "a", encoding="utf-8") as f:
            f.write(content)
        return True

    def create_email_draft(self, pulse_data, fee_data, send=False, recipient=None):
        """
        Phase 4: Email Delivery
        Produces a draft email (and optionally sends it) containing the weekly note.
        """
        date_obj = datetime.datetime.now()
        date_str = date_obj.strftime('%d %b %Y')
        subject = f"INDmoney Weekly Review Pulse --- Week of {date_str}"
        target_to = recipient or self.recipient_email or "team@indmoney.com"
        
        # Handle theme structure
        themes_list = []
        for t in pulse_data.get('themes', []):
            if isinstance(t, dict):
                themes_list.append(f"**{t.get('topic')}**: {t.get('description')}")
            else:
                themes_list.append(f"**{t}**")
        
        nl = '\n'
        # Construct Plain Text Body
        explanation_plain = '\n'.join(['- ' + b for b in fee_data['explanation']])
        body_plain = f"""
Hi Team,

INDmoney WEEKLY REVIEW PULSE --- Week of {date_str}

**Top 3 Themes / Weekly Pulse Summary:**
{nl.join(['- ' + t for t in themes_list])}

USER QUOTES:
{nl.join(['- ' + q for q in pulse_data['quotes']])}

TACTICAL ACTION IDEAS:
{nl.join(['- ' + a for a in pulse_data['action_ideas']])}

FEE EXPLANATION ({fee_data['scenario']}):
{explanation_plain}

Best,
AI Workflow Bot
"""
        # Construct HTML Body (using markdown + CSS)
        md_content = f"""
# INDmoney Weekly Review Pulse --- Week of {date_str}

### 📈 Top 3 Themes / Weekly Pulse Summary
{nl.join(['* ' + t for t in themes_list])}

### 💬 Detailed User Quotes
{nl.join(['* > ' + q for q in pulse_data['quotes']])}

### 💡 Tactical Action Ideas
{nl.join(['* ' + a for a in pulse_data['action_ideas']])}

---
### 💸 Fee Explanation: {fee_data['scenario']}
{nl.join(['* ' + b for b in fee_data['explanation']])}
"""
        # Convert to HTML and wrap in premium styling
        html_main = markdown.markdown(md_content)
        body_html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                    h1 {{ color: #007bff; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                    h3 {{ color: #007bff; margin-top: 25px; margin-bottom: 10px; }}
                    blockquote {{ background: #f9f9f9; border-left: 10px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px; font-style: italic; }}
                    ul {{ padding-left: 20px; }}
                    li {{ margin-bottom: 8px; }}
                    hr {{ border: 0; border-top: 1px solid #eee; margin: 30px 0; }}
                    .container {{ max-width: 700px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 10px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    {html_main}
                    <p style="color: #888; font-size: 12px; margin-top: 40px; border-top: 1px solid #eee; padding-top: 10px;">
                        This is an AI-generated report from the INDmoney Review Pulse Workflow.
                    </p>
                </div>
            </body>
        </html>
        """

        # Create Email Message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.sender_email or "bot@indmoney.com"
        msg["To"] = target_to

        msg.attach(MIMEText(body_plain, "plain"))
        msg.attach(MIMEText(body_html, "html"))

        # Save to file (Dry-run / Draft)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"pulse_{timestamp}.eml"
        file_path = os.path.join(self.drafts_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(msg.as_string())

        status_msg = f"Draft saved to {filename}"

        # Send if requested and credentials exist
        if send:
            if not (self.sender_email and self.sender_password and target_to):
                return f"Error: SMTP credentials missing or no recipient. {status_msg}"
            
            try:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                status_msg = f"Email sent successfully to {target_to} and {status_msg}"
            except Exception as e:
                status_msg = f"Failed to send email to {target_to}: {str(e)}. {status_msg}"

        return status_msg

    def clean_for_pdf(self, text):
        """FPDF v1 is extremely sensitive. Strip EVERYTHING non-printable ASCII."""
        if not text: return ""
        text_str = str(text)
        # Keep only standard printable characters (32-126) and newlines
        return "".join([c if (32 <= ord(c) <= 126 or c == '\n') else " " for c in text_str])

    def generate_pdf_one_pager(self, pulse_data, fee_data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="INDmoney Product Pulse One-Pager", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Weekly Product Pulse Summary", ln=True)
        pdf.set_font("Arial", size=10)
        
        # 1. Themes & Pulse
        for theme_obj in pulse_data.get('themes', []):
            if isinstance(theme_obj, dict):
                topic = self.clean_for_pdf(theme_obj.get('topic', 'Theme'))
                desc = self.clean_for_pdf(theme_obj.get('description', ''))
                pdf.set_font("Arial", 'B', 10)
                pdf.write(5, f"{topic}: ")
                pdf.set_font("Arial", size=10)
                pdf.write(5, f"{desc}\n")
            else:
                pdf.multi_cell(0, 5, txt=f"- {self.clean_for_pdf(theme_obj)}")
        
        # 2. User Quotes
        if 'quotes' in pulse_data and pulse_data['quotes']:
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt="Detailed User Quotes", ln=True)
            pdf.set_font("Arial", 'I', 10)
            for quote in pulse_data['quotes']:
                pdf.multi_cell(0, 5, txt=f"\"{self.clean_for_pdf(quote)}\"")
                pdf.ln(2)

        # 3. Action Ideas
        if 'action_ideas' in pulse_data and pulse_data['action_ideas']:
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt="Tactical Action Ideas", ln=True)
            pdf.set_font("Arial", size=10)
            for idea in pulse_data['action_ideas']:
                pdf.multi_cell(0, 5, txt=f"- {self.clean_for_pdf(idea)}")

        # 4. Fee Explainer
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"Fee Explainer: {self.clean_for_pdf(fee_data['scenario'])}", ln=True)
        pdf.set_font("Arial", size=10)
        for bullet in fee_data['explanation']:
            pdf.multi_cell(0, 5, txt=f"- {self.clean_for_pdf(bullet)}")
            
        return pdf.output(dest='S').encode('latin-1')
