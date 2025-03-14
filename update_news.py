import sys
import os
import json
import feedparser
import re
import html
import urllib.request
import ssl
from datetime import datetime

# Add parent directory to path to import from fetch_news_5.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fetch_news_5 import RSS_FEEDS, PREDEFINED_KEYWORDS, clean_text, extract_relevant_keywords

def fetch_news():
    """Fetch news from multiple RSS feeds and process them."""
    print("Starting news fetch...")
    articles = []
    
    # Create an SSL context that does not verify certificates
    context = ssl._create_unverified_context()
    
    for category, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            try:
                print(f"Attempting to fetch: {feed_url}")
                req = urllib.request.Request(feed_url)
                with urllib.request.urlopen(req, context=context) as response:
                    data = response.read()
                
                feed = feedparser.parse(data)
                if hasattr(feed, 'bozo_exception'):
                    print(f"Feed parsing error: {feed.bozo_exception}")
                    continue
                if not feed.entries:
                    print("No entries found in feed")
                    continue
                print(f"Successfully found {len(feed.entries)} articles in {feed_url}")
                
                # Limit to 5 articles per feed (adjust if needed)
                for entry in feed.entries[:5]:
                    title = html.unescape(entry.title)
                    description = html.unescape(entry.get('description', ''))
                    link = entry.link
                    clean_description = clean_text(description)
                    combined_text = f"{title} {clean_description}"
                    relevant_keywords = extract_relevant_keywords(category, combined_text)
                    articles.append({
                        'title': title,
                        'description': clean_description,
                        'link': link,
                        'category': category,
                        'keywords': relevant_keywords,
                        'source': feed.feed.get('title', '')
                    })
            except Exception as e:
                print(f"Error fetching news from {feed_url}: {str(e)}")
    
    return articles

def update_news_json():
    """Update the news.json file with fresh data."""
    try:
        # Fetch news
        articles = fetch_news()
        
        if not articles:
            print("No articles were fetched. Using sample data.")
            # If no articles were fetched, use the existing data
            try:
                with open('api/news.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                print("Could not read existing news.json. Using empty array.")
                return []
        
        # Save to JSON file
        api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api')
        os.makedirs(api_dir, exist_ok=True)
        
        json_path = os.path.join(api_dir, 'news.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        print(f"Updated news.json with {len(articles)} articles at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return articles
    except Exception as e:
        print(f"Error updating news: {str(e)}")
        return []

if __name__ == "__main__":
    update_news_json()
