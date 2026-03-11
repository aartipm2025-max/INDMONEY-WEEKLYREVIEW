from google_play_scraper import Sort, reviews
import pandas as pd
import os
from datetime import datetime, timedelta

def scrape_indmoney_reviews(app_id='in.indwealth', count=1000):
    print(f"Scraping {count} reviews for {app_id}...")
    
    # Get reviews
    result, continuation_token = reviews(
        app_id,
        lang='en', # Language focus as per Phase 2 requirement
        country='in',
        sort=Sort.NEWEST, # Latest reviews first
        count=count
    )
    
    # Convert to DataFrame
    data = []
    for r in result:
        # Columns: review date, title (if any), score (rating), content (review text)
        data.append([
            r['at'].strftime('%Y-%m-%d'),
            r['userName'], # Use userName since titled reviews aren't explicit in Play Store
            r['score'],
            r['content']
        ])
        
    df = pd.DataFrame(data, columns=['Date', 'Title', 'Rating', 'Review'])
    
    # Save to raw location
    os.makedirs('stage_01_data', exist_ok=True)
    output_path = os.path.join('stage_01_data', 'reviews_raw.csv')
    df.to_csv(output_path, index=False)
    print(f"Success: Scraped {len(df)} reviews to {output_path}")
    return df

if __name__ == "__main__":
    scrape_indmoney_reviews()
