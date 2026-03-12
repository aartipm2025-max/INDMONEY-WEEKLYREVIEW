import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from stage_03_ai_engine.groq_engine import GroqEngine
from stage_04_ui_actions.actions import WorkflowActions
import stage_01_data.scraper as scraper
import stage_02_processing.preprocessor as preprocessor

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="INDmoney AI Product Pulse", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@600;700&display=swap');

    /* Global Professional Dark Theme */
    .main { 
        background-color: #020c1b; 
        font-family: 'Inter', sans-serif; 
        color: #ccd6f6;
    }
    
    /* Elegant Headings */
    h1 { 
        font-family: 'Outfit', sans-serif; 
        color: #ffffff !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 5px !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    h2, h3 { 
        font-family: 'Outfit', sans-serif; 
        color: #64ffda !important; 
        font-weight: 600 !important;
        text-align: center;
        margin-top: 2rem !important;
    }
    
    .centered-text { 
        text-align: center; 
        color: #8892b0; 
        font-size: 1.2rem; 
        margin-bottom: 40px; 
    }

    /* Professional Feedback Cards */
    .report-card { 
        padding: 40px; 
        border-radius: 12px; 
        background-color: #0a192f; 
        border: 1px solid #112240; 
        box-shadow: 0 10px 30px -15px rgba(2, 12, 27, 0.7);
        margin-bottom: 30px; 
        text-align: left !important;
        transition: all 0.25s cubic-bezier(0.645, 0.045, 0.355, 1);
    }
    .report-card:hover {
        border-color: #64ffda;
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -15px rgba(2, 12, 27, 0.7);
    }
    
    /* Maximum Visibility Intelligence Segments */
    .report-card h3 { 
        color: #ffffff !important; 
        text-align: left !important;
        font-size: 1.5rem !important;
        margin-top: 10px !important;
        border-bottom: 1px solid #112240;
        padding-bottom: 15px;
        margin-bottom: 20px !important;
    }
    .report-card .stMarkdown, .report-card p, .report-card span { 
        color: #a8b2d1 !important;
        font-size: 1.05rem !important;
        line-height: 1.6;
        text-align: left !important;
    }
    .report-card b, .report-card strong { 
        color: #64ffda !important; 
        font-weight: 600;
    }
    
    /* CodeNova Style Action Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        padding: 1rem 2rem;
        height: 3.5rem;
        background-color: transparent; 
        color: #64ffda; 
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border: 1.5px solid #64ffda;
        transition: all 0.25s cubic-bezier(0.645, 0.045, 0.355, 1);
        text-transform: none;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover { 
        background-color: rgba(100, 255, 218, 0.1);
        color: #64ffda;
        border-color: #64ffda;
    }
    
    /* White Gradient Primary Action (Stage 3) override */
    [data-testid="stVerticalBlock"] > div:nth-child(7) .stButton>button {
        background-color: #ffffff;
        color: #020c1b;
        border: none;
    }
    [data-testid="stVerticalBlock"] > div:nth-child(7) .stButton>button:hover {
        background-color: #e6e6e6;
        box-shadow: 0 5px 15px rgba(255,255,255,0.2);
    }
    
    /* Divider & Layout Cleanups */
    hr { border-top: 1px solid #112240; margin: 50px 0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid='stSidebar'] {display: none;}
    
    /* Quote Styling */
    blockquote, blockquote p, blockquote em {
        color: #ffffff !important;
    }
    blockquote {
        border-left: 3px solid #64ffda;
        padding: 15px 25px;
        font-style: italic;
        background: rgba(10, 25, 47, 0.5);
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Use columns to center the entire content
    _, center_col, _ = st.columns([1, 4, 1])

    with center_col:
        st.title("INDmoney AI Product Pulse Dashboard")
        st.markdown("<div class='centered-text'>AI-powered weekly review analysis for INDmoney product teams.</div>", unsafe_allow_html=True)

        # Get Keys from Environment
        groq_key = os.getenv("GROQ_API_KEY")

        # Initialize Engine & Actions
        if not groq_key:
            st.error("AI API key missing! Please configure secrets in settings.")
            return

        groq_engine = GroqEngine()
        actions = WorkflowActions()

        # --- MAIN INTERFACE STAGES (VERTICAL STACK) ---
        st.divider()
        st.subheader("STAGE 1")
        _, s1_col, _ = st.columns([1, 2, 1])
        with s1_col:
            if st.button("🔍 Scrape Actual Reviews", use_container_width=True):
                with st.spinner("Scraping Play Store..."):
                    scraper.scrape_indmoney_reviews(count=1000)
                    st.success("Scraped 1000 reviews")

        st.divider()
        st.subheader("STAGE 2")
        _, s2_col, _ = st.columns([1, 2, 1])
        with s2_col:
            if st.button("🧼 Clean Dataset", use_container_width=True):
                preprocessor.clean_and_filter()
                st.success("Cleaned dataset saved")

        st.divider()
        st.subheader("STAGE 3")
        cleaned_path = os.path.join("stage_02_processing", "reviews_cleaned.csv")
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
            st.info(f"Loaded {len(df)} filtered English reviews (> 5 words).")

            _, s3_col, _ = st.columns([1, 2, 1])
            with s3_col:
                if st.button("Run AI Analysis", use_container_width=True):
                    with st.spinner("Analyzing high-quality feedback..."):
                        pulse_results = groq_engine.analyze_reviews(df)
                        fee_results = groq_engine.generate_fee_explainer()
                        
                        st.session_state['pulse'] = pulse_results
                        st.session_state['fee'] = fee_results
                        st.session_state['ready'] = True

            if st.session_state.get('ready'):
                pulse = st.session_state['pulse']
                fee = st.session_state['fee']

                # Weekly Pulse - Full Width
                st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                st.subheader("📝 Weekly Product Pulse")
                st.markdown("### **Top 3 Themes**")
                
                # Consolidate: themes + their descriptions as the core "pulse"
                for i, theme_obj in enumerate(pulse.get('themes', []), 1):
                    if isinstance(theme_obj, dict):
                        st.markdown(f"**{i}. {theme_obj.get('topic', 'Theme')}**: {theme_obj.get('description', '')}")
                    else:
                        st.markdown(f"**{i}. {theme_obj}**")

                if 'quotes' in pulse:
                    st.markdown("### **💬 Detailed User Quotes**")
                    for quote in pulse['quotes']:
                        st.markdown(f"> *\"{quote}\"*")
                
                if 'action_ideas' in pulse:
                    st.markdown("### **💡 Action Ideas**")
                    ideas_html = "<ul style='text-align: left !important;'>"
                    for idea in pulse['action_ideas']:
                        ideas_html += f"<li style='text-align: left !important;'>{idea}</li>"
                    ideas_html += "</ul>"
                    st.markdown(ideas_html, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Fee Explainer - Followed below
                st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                st.subheader("💸 Fee Explainer")
                fee_html = "<ul style='text-align: left !important;'>"
                for b in fee['explanation']:
                    fee_html += f"<li style='text-align: left !important;'>{b}</li>"
                fee_html += "</ul>"
                st.markdown(fee_html, unsafe_allow_html=True)
                
                st.markdown(f"<p style='text-align: left !important;'><i>Last checked: {fee['last_checked']}</i></p>", unsafe_allow_html=True)
                with st.expander("Sources"):
                    for s in fee.get('sources', []):
                        st.write(s)
                st.markdown("</div>", unsafe_allow_html=True)

                st.divider()
                st.subheader("STAGE 4")
                
                # Recipient Input for flexibility
                recipient = st.text_input("📬 Recipient Email", value="", placeholder="Enter recipient email address...")
                
                c1, c2, c3 = st.columns(3)

                with c1:
                    if st.button("📁 Append to Notes"):
                        actions.append_to_notes(pulse, fee)
                        st.success(f"Appended to {os.path.basename(actions.notes_path)}")

                with c2:
                    if st.button("✉️ Create Email Draft"):
                        status = actions.create_email_draft(pulse, fee, send=False, recipient=recipient)
                        st.success(status)

                with c3:
                    if st.button("📧 Send Email via SMTP"):
                        status = actions.create_email_draft(pulse, fee, send=True, recipient=recipient)
                        if "Error" in status:
                            st.warning(status)
                        else:
                            st.info(status)
                
                # Download link at the bottom
                pdf_bytes = actions.generate_pdf_one_pager(pulse, fee)
                st.download_button(
                    label="📄 Download One-Pager PDF",
                    data=pdf_bytes,
                    file_name=f"INDmoney_Pulse_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Click 'Clean Dataset' above to prepare the data.")

if __name__ == "__main__":
    if 'ready' not in st.session_state:
        st.session_state['ready'] = False
    main()
