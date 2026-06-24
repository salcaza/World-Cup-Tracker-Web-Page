import json
import os
import requests

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
                "id": game.get("id"),
                "group": game.get("group"),
                "local_date": game.get("local_date"),
                "finished": game.get("finished"),
                "team_name": game.get("home_team_name_en"),
                "opponent": game.get("away_team_name_en"),
                "type": game.get("type")
            }

            if game.get("finished") == "True":
                match["home_score"] = game.get("home_score")
                match["away_score"] = game.get("away_score")
            
            matches.append(match)

    return matches


def print_schedule(team_name):
    schedule = get_team_schedule(team_name)

    print(f"World Cup Schedule for {team_name}:\n")

    for game in schedule:
        date = game.get("local_date", "Date TBD")
        home = game.get("team_name", "TBD")
        away = game.get("opponent", "TBD")
        group = game.get("group", "")
        game_type = game.get("type","")

        if game_type == "group":
            print(f"{date} | {home} vs {away} | Group {group}")
        else:
            print(f"{date} | {home} vs {away} | {game_type}")

if __name__ == "__main__":
    team = input("Enter team name: ")
    print()
    print_schedule(team)
