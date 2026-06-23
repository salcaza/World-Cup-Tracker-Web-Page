import os
import requests
import json

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_BASE_URL = "https://newsapi.org/v2/"

def save_news(team_name):
    params = {
        'q': f'("{team_name}" AND ("national team" OR squad OR lineup OR match OR injury OR coach OR "World Cup"))',
        "searchin": "title,description",
        "from": "2026-05-23",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    response = requests.get(f"{NEWS_BASE_URL}everything", params=params, headers=headers)

    data = response.json()

    with open("news_data.json", "w") as f:
        json.dump(data, f, indent=2)

    return data

def get_news():
    with open("news_data.json", "r") as f:
        articles = json.load(f)

    return articles.get("articles", [])

if __name__ == "__main__":
    team = input("Enter team name:")
    #save_news(team)
    print(get_news())
