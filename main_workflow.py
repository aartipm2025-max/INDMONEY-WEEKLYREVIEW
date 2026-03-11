import os
import pandas as pd
from dotenv import load_dotenv

# Standard imports now that folders are correctly named
import stage_01_data.generate_data as generate_data
import stage_02_processing.preprocessor as preprocessor
from stage_03_ai_engine.groq_engine import GroqEngine
from stage_04_ui_actions.actions import WorkflowActions

def run_pipeline():
    load_dotenv()
    
    # 1. Data Generation (200 reviews)
    print("\n--- STAGE 1: Generating Data ---")
    generate_data.generate_sample_reviews()
    
    # 2. Preprocessing & Filtering
    print("\n--- STAGE 2: Cleaning & Filtering ---")
    preprocessor.clean_and_filter()
    
    # 3. AI Analysis
    print("\n--- STAGE 3: AI Analysis ---")
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in environment.")
        return
        
    df = pd.read_csv(os.path.join("stage_02_processing", "reviews_cleaned.csv"))
    engine = GroqEngine()
    pulse = engine.analyze_reviews(df)
    fee = engine.generate_fee_explainer()
    
    print("\n--- RESULTS ---")
    print(f"PULSE: {pulse['pulse_note'][:100]}...")
    
    # 4. Actions (Simulated Approval)
    print("\n--- STAGE 4: Actions ---")
    actions = WorkflowActions()
    
    confirm = input("Approve and execute actions? (y/n): ")
    if confirm.lower() == 'y':
        actions.append_to_notes(pulse, fee)
        actions.create_email_draft(pulse, fee)
        print("Actions completed. Check 'outputs/' directory.")

if __name__ == "__main__":
    run_pipeline()
