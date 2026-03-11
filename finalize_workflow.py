import os
import pandas as pd
from dotenv import load_dotenv

# Standard imports
from stage_03_ai_engine.groq_engine import GroqEngine
from stage_03_ai_engine.gemini_engine import GeminiEngine
from stage_04_ui_actions.actions import WorkflowActions

def finalize():
    load_dotenv()
    if not os.path.exists(os.path.join("stage_02_processing", "reviews_cleaned.csv")):
        print("Dataset not found. Please run Stage 2 first.")
        return

    df = pd.read_csv(os.path.join("stage_02_processing", "reviews_cleaned.csv"))
    
    # Initialize Engines
    groq_engine = GroqEngine()
    gemini_engine = GeminiEngine()
    actions = WorkflowActions()
    
    print("\n--- FINALIZING: EXECUTING ACTIONS (Groq + Gemini V2) ---")
    
    # 1. Generate Pulse (Groq)
    pulse = groq_engine.analyze_reviews(df)
    
    # 2. Generate Fee Explainer (Gemini)
    fee = gemini_engine.generate_fee_explainer()
    
    # 3. Execute Gated Actions (User Approved)
    print("Appending to Master Notes...")
    actions.append_to_notes(pulse, fee)
    
    print("Creating Email Draft...")
    draft_path = actions.create_email_draft(pulse, fee)
    
    print("\n" + "="*50)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Notes Updated: outputs/MASTER_NOTES.md")
    print(f"Email Draft: {draft_path}")
    print("="*50)

if __name__ == "__main__":
    finalize()
