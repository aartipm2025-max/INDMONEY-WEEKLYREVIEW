import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class GroqEngine:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def scrub_pii(self, text):
        """Removes common PII like phone numbers and emails."""
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
        return text

    def analyze_reviews(self, df):
        print("Running Groq analysis for Weekly Pulse (Small Batch for Stability)...")
        # Sort by rating ascending to prioritize negative/critical feedback for analysis
        df_sorted = df.sort_values(by='Rating', ascending=True)
        reviews_list = df_sorted['Review'].apply(self.scrub_pii).tolist()
        
        # Reduced to 40 reviews to strictly stay under the 6,000 Tokens Per Minute (TPM) limit
        combined_text = "\n- ".join(reviews_list[:40]) 

        prompt = f"""
        Analyze these 40 critical product reviews for INDmoney:
        {combined_text}

        Your goal: Provide a concise Weekly Product Pulse focusing on resolving friction.
        Tasks:
        1. Identify exactly 3 core themes describing the current "Pulse" of the product based on these reviews.
        2. For each theme, provide a concise Topic and a 1-2 sentence Detailed Description that captures the summary of user complaints for that segment.
        3. Extract 3 detailed, representative user quotes (strictly no PII).
        4. Suggest 3 tactical action ideas.

        IMPORTANT: Do NOT use markdown formatting (like ** or #) inside the JSON values. The output must be PURE JSON.
        
        Format as a valid JSON object with these exact keys:
        {{
            "themes": [
                {{"topic": "Theme Topic 1", "description": "Pulse summary description"}},
                {{"topic": "Theme Topic 2", "description": "Pulse summary description"}},
                {{"topic": "Theme Topic 3", "description": "Pulse summary description"}}
            ],
            "top_themes": ["Theme Topic 1", "Theme Topic 2", "Theme Topic 3"],
            "quotes": ["quote1", "quote2", "quote3"],
            "action_ideas": ["action1", "action2", "action3"]
        }}
        """
        
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)

    def generate_fee_explainer(self, scenario="Exit Load"):
        print(f"Generating Fee Explainer for {scenario}...")
        prompt = f"""
        Provide a structured explanation for the following fee scenario in INDmoney: {scenario}.
        
        Requirements:
        1. Generate EXACTLY 6 bullet structured explanation.
        2. Include EXACTLY 2 official source links.
        3. Maintain a neutral, facts-only tone. 
        
        Format strictly as JSON:
        {{
            "scenario": "{scenario}",
            "explanation": ["bullet 1", "bullet 2", ...],
            "sources": ["url1", "url2"],
            "last_checked": "{datetime.now().strftime('%Y-%m-%d')}"
        }}
        """
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
