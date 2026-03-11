import os
import time
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import stages
import stage_01_data.scraper as scraper
import stage_02_processing.preprocessor as preprocessor
from stage_03_ai_engine.groq_engine import GroqEngine
from stage_04_ui_actions.actions import WorkflowActions

def run_automated_workflow():
    load_dotenv()
    start_time = datetime.now()
    log_file = "outputs/scheduler_logs.csv"
    os.makedirs("outputs", exist_ok=True)
    
    print(f"\n[{start_time}] Starting Automated Weekly Pulse...")
    
    try:
        # 1. Scrape actual data 
        scraper.scrape_indmoney_reviews(count=1000)
        
        # 2. Clean and Filter
        preprocessor.clean_and_filter()
        
        # 3. AI Analysis (Consolidated)
        df_cleaned = pd.read_csv("stage_02_processing/reviews_cleaned.csv")
        # Filter for last 8 weeks
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])
        cutoff_date = datetime.now() - timedelta(weeks=8)
        df_final = df_cleaned[df_cleaned['Date'] >= cutoff_date]
        
        # Initialize the AI engine (using the consolidated Groq/Llama structure)
        ai_engine = GroqEngine()
        
        pulse = ai_engine.analyze_reviews(df_final)
        fee = ai_engine.generate_fee_explainer("Exit Load")
        
        # 4. Final Actions (Auto-append and Email Draft)
        actions = WorkflowActions()
        actions.append_to_notes(pulse, fee)
        # Note: recipient can be customized per call
        recipient = os.getenv("EMAIL_RECIPIENT", "codeflex16@gmail.com")
        draft_path = actions.create_email_draft(pulse, fee, recipient=recipient)
        
        print(f"Workflow Complete. Draft saved for {recipient}.")
        
        status = "SUCCESS"
        error_msg = ""
    except Exception as e:
        status = "FAILED"
        error_msg = str(e)
        print(f"Error in Scheduler: {error_msg}")
        # Initialize df_final to 0 for log consistency if it fails early
        df_final = []

    # Log execution
    log_data = [{
        "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "reviews_processed": len(df_final) if status == "SUCCESS" else 0,
        "error": error_msg
    }]
    
    log_df = pd.DataFrame(log_data)
    if not os.path.exists(log_file):
        log_df.to_csv(log_file, index=False)
    else:
        log_df.to_csv(log_file, mode='a', header=False, index=False)

if __name__ == "__main__":
    # If run directly, run once and finish.
    # In a real scenario, this would be cron-triggered or run in a while loop.
    run_automated_workflow()
