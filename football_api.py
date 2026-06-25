import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()   

API_KEY = os.environ.get("FOOTBALL_API_KEY")
BASE_URL = 'https://worldcup26.ir'


def save_schedule_json():
    response = requests.get(f'{BASE_URL}/get/games')

    if response.status_code != 200:
        print("Error:", response.status_code)
        return

    data = response.json()

    with open("schedule_data.json", "w") as f:
        json.dump(data, f, indent=2)

    return data

def save_stadium_json():
    response  = requests.get(f'{BASE_URL}/get/stadiums')

    if response.status_code != 200:
        print("Error:", response.status_code)
        return

    data = response.json()

    with open("stadium_data.json", "w") as f:
        json.dump(data, f, indent=2)

    return data


def find_stadium(s_id):
    # Uncomment line if need to get stadiums from API
    # save_stadium_json()
    with open("stadium_data.json", "r") as file:
        data = json.load(file)
    stadiums = data["stadiums"]

    for stadium in stadiums:
        if stadium["id"] == s_id:
            return (stadium["name_en"], stadium["city_en"])


def get_team_schedule(team_name):
    # Uncomment line if need to get schedule from API
    # save_schedule_json()
    with open("schedule_data.json", "r") as file:
        data = json.load(file)
    games = data["games"]
    team_name = team_name.strip().lower()

    matches = []

    for game in games:
        home = game.get("home_team_name_en", "").lower()
        away= game.get("away_team_name_en", "").lower()

        if team_name == home or team_name == away:
            match = {
                "group": game.get("group"),
                "local_date": game.get("local_date"),
                "finished": game.get("finished"),
                "type": game.get("type")
            }

            if team_name == home:
                match["team_name"] = game.get("home_team_name_en")
                match["opponent"] = game.get("away_team_name_en")
                if match["finished"] == 'TRUE':
                    match["team_score"] = game.get("home_score")
                    match["opponent_score"] = game.get("away_score")

            if team_name == away:
                match["opponent"] = game.get("home_team_name_en")
                match["team_name"] = game.get("away_team_name_en")
                if match["finished"] == 'TRUE':
                    match["opponent_score"] = game.get("home_score")
                    match["team_score"] = game.get("away_score")

            match["stadium"], match["city"] = find_stadium(game.get("stadium_id"))
            matches.append(match)

    matches.sort(key=lambda game: game["local_date"])
    return matches


def print_schedule(team_name):
    schedule = get_team_schedule(team_name)
    print()
    print(f"World Cup Schedule for {team_name}:\n")

    for game in schedule:
        date = game.get("local_date", "Date TBD")
        home = game.get("team_name", "TBD")
        away = game.get("opponent", "TBD")
        group = game.get("group", "")
        game_type = game.get("type","")
        team_score = game.get("team_score", "")
        opponent_score = game.get("opponent_score", "")
        stadium = game.get("stadium", "")
        city = game.get("city", "")

        if game_type == "group":
            print(f"{date} | {home} {team_score} vs {away} {opponent_score} | Group {group}")
            print(f"Played in {city} at {stadium}")
            print()
        else:
            print(f"{date} | {home} {team_score} vs {away} {opponent_score} | {game_type}")
            print(f"Played in {city} at {stadium}")
            print()

if __name__ == "__main__":
    team = input("Enter team name: ")
    print()
    get_team_schedule(team)
