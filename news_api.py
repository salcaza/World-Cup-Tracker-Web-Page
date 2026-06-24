import os
import requests
import json

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_BASE_URL = "https://newsapi.org/v2/"


def save_news(team_name):
    x = (
        "('national team' OR squad OR lineup OR "
        "match OR injury OR coach OR 'World Cup')"
    )
    params = {
        'q': f'("{team_name}" AND {x})',
        "searchIn": "title",
        "from": "2026-05-30",
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    response = requests.get(f"{NEWS_BASE_URL}everything",
                            params=params,
                            headers=headers)

    data = response.json()

    with open("news_data.json", "w") as f:
        json.dump(data, f, indent=2)

    return data


def get_news(team):
    # Uncomment line if need data from API
    #save_news(team)
    with open("news_data.json", "r") as f:
        news_data = json.load(f)

    articles = []

    for article in news_data["articles"]:
        article = {
            "team_name": team,
            "title": article.get("title"),
            "author": article.get("author"),
            "description": article.get("description"),
            "url" : article.get("url")
        }
        
        articles.append(article)

    return articles


def print_news(team):
    print(f"RECENT HEADLINES FOR {team}")
    print()

    articles = get_news(team)
    
    for article in articles:
        print(f'Title: {article.get("title")}')
        print(f'By: {article.get("author")}')
        print(f'Description: {article.get("description")}')
        print(f'URL: {article.get("url")}')
        print()


if __name__ == "__main__":
    team = input("Enter team name: ")
    print_news(team)
