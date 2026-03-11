import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sample_reviews():
    themes = [
        "Login issues and biological authentication",
        "Slow portfolio updates",
        "High brokerage on US stocks",
        "Excellent customer support response",
        "Ease of use for SIP set up",
        "Requests for more AMC funds",
        "KYC processing delays",
        "Hidden charges in withdrawal"
    ]
    
    reviews = [
        "Love the app! SIP setup is so easy. Highly recommended.",
        "The login is so slow. It takes forever to authenticate with FaceID.",
        "Why is there a withdrawal charge? I wasn't informed about this. My number is 9876543210 - call me.",
        "Great interface, but US stock prices update very slowly.",
        "Kudos to Rahul from support for helping me with my KYC. Rahul was the best.",
        "Waiting for 2 weeks for KYC. Very frustrating.",
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

    data = []
    end_date = datetime.now()
    for i in range(50):
        review_text = random.choice(reviews)
        # Adding some randomness to simulate a real CSV
        days_ago = random.randint(0, 84) # Up to 12 weeks
        date = (end_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        rating = random.randint(1, 5)
        data.append([date, rating, review_text])

    df = pd.DataFrame(data, columns=['Date', 'Rating', 'Review'])
    df.to_csv('c:/M2 INDM REVIEWS/reviews_sample.csv', index=False)
    print("Generated reviews_sample.csv with 50 entries.")

if __name__ == "__main__":
    generate_sample_reviews()
