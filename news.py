import os
import json
import requests
from newspaper import Article
from utils.config import read_config

# Load the configuration
config = read_config()

def fetch_blockchain_news(api_key):
    url = f"https://newsapi.org/v2/everything?q=blockchain&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

def fetch_full_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error fetching full article content from {url}: {e}")
        return None

def save_news_to_file(news_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, article in enumerate(news_data["articles"]):
        content = fetch_full_article_content(article["url"])
        if content is not None:
            article["content"] = content

        file_name = os.path.join(output_dir, f"blockchain_news_{i + 1}.json")
        with open(file_name, 'w') as f:
            json.dump(article, f, indent=4)
        print(f"Saved news article {i + 1} to {file_name}")

def main():
    api_key = config["news_api_key"]
    output_dir = "output_news"

    news_data = fetch_blockchain_news(api_key)

    if news_data is not None:
        save_news_to_file(news_data, output_dir)
    else:
        print("No news data to save.")

if __name__ == "__main__":
    main()
