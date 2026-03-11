import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_sample_reviews():
    # Templates for good and bad reviews
    english_reviews = [
        "Love the app! SIP setup is so easy. Highly recommended.",
        "The login is so slow. It takes forever to authenticate with FaceID.",
        "Why is there a withdrawal charge? I wasn't informed. My number is 9876543210.",
        "Great interface, but US stock prices update very slowly.",
        "Kudos to Rahul from support for helping me with my KYC.",
        "Waiting for 2 weeks for KYC. Very frustrating experience so far.",
        "The interface is clean and dark mode looks premium.",
        "I need more mutual fund options from SBI and Nippon.",
        "Too many notifications. Stop spamming my email test@example.com.",
        "Brokerage for US stocks is higher than competitors.",
        "App crashes when I try to open the portfolio section.",
        "The wealth tracker is amazing. Combined view of all assets is a plus.",
        "Fees are confusing. Need a better explainer for brokerage.",
        "Simple and effective. Used it for 3 months now.",
        "Support is slow. No one responded to my ticket #12345."
    ]
    
    non_english_reviews = [
        "बहुत अच्छा ऐप है, इस्तेमाल करने में आसान।", # Hindi
        "Esta aplicación es excelente para invertir.", # Spanish
        "C'est une très bonne application." # French
    ]
    
    short_reviews = [
        "Good app.",
        "Bad UI.",
        "Nice!",
        "Poor service."
    ]

    data = []
    end_date = datetime.now()
    
    # Generate 200 reviews
    for i in range(200):
        # Mix in some non-English and short reviews
        rand_val = random.random()
        if rand_val < 0.1: # 10% non-English
            review_text = random.choice(non_english_reviews)
        elif rand_val < 0.2: # 10% short
            review_text = random.choice(short_reviews)
        else:
            review_text = random.choice(english_reviews)
            
        title = f"Review Title {i+1}"
        days_ago = random.randint(0, 84)
        date = (end_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        rating = random.randint(1, 5)
        data.append([date, title, rating, review_text])

    df = pd.DataFrame(data, columns=['Date', 'Title', 'Rating', 'Review'])
    output_path = os.path.join('stage_01_data', 'reviews_raw.csv')
    df.to_csv(output_path, index=False)
    print(f"Generated 200 reviews in {output_path}")

if __name__ == "__main__":
    generate_sample_reviews()
