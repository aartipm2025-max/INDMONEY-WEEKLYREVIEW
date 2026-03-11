import os
import pandas as pd
from dotenv import load_dotenv
from stage_03_ai_engine.groq_engine import GroqEngine

def show_full_review():
    load_dotenv()
    if not os.path.exists(os.path.join("stage_02_processing", "reviews_cleaned.csv")):
        print("Dataset not found. Please run Stage 2 first.")
        return

    df = pd.read_csv(os.path.join("stage_02_processing", "reviews_cleaned.csv"))
    engine = GroqEngine()
    
    print("\n--- FETCHING FULL ANALYSIS FOR REVIEW ---")
    pulse = engine.analyze_reviews(df)
    fee = engine.generate_fee_explainer()
    
    print("\n" + "="*50)
    print("PART A: WEEKLY PRODUCT PULSE")
    print("="*50)
    print(f"PULSE NOTE:\n{pulse['pulse_note']}")
    print("\nTOP THEMES:")
    for t in pulse['top_themes']: print(f"- {t}")
    print("\nEXTRACTED QUOTES:")
    for q in pulse['quotes']: print(f"> {q}")
    print("\nACTION IDEAS:")
    for a in pulse['action_ideas']: print(f"- {a}")
    
    print("\n" + "="*50)
    print("PART B: FEE EXPLAINER (EXIT LOAD)")
    print("="*50)
    print(f"SCENARIO: {fee['scenario']}")
    print("\nEXPLANATION:")
    for e in fee['explanation']: print(f"- {e}")
    print("\nSOURCES:")
    for s in fee['sources']: print(f"- {s}")
    print(f"\nLAST CHECKED: {fee['last_checked']}")
    print("="*50)

if __name__ == "__main__":
    show_full_review()
