import os
from google import genai 
from google.genai import types, errors
import football_api
import news_api

#Set environment variables

my_api_key = os.getenv('GENAI_KEY')
genai.api_key = my_api_key

# Creates a genAI client using the key from our environment variable
client = genai.Client(
    api_key = my_api_key
)

# Schedule context to feed gemini (re-used print schedule from football_api.py)
def build_schedule_context(team_name):
    schedule = football_api.get_team_schedule(team_name)

    context = f"World Cup Schedule for {team_name}:\n"

    for game in schedule:
        # skip games that are finished
        finished = str(game.get("finished")).lower()
        if finished == "true":
            continue
        date = game.get("local_date", "Date TBD")
        home = game.get("home_team_name_en", "TBD")
        away = game.get("away_team_name_en", "TBD")
        group = game.get("group", "")
        game_type = game.get("type","")

        if game_type == "group":
            context += f"{date} | {home} vs {away} | Group {group}"
        else:
            context += f"{date} | {home} vs {away} | {game_type}"

    return context



# get future insights based on team
def get_future_insight(team_name):

    # Build the context needed by calling function on team name
    schedule_conext = build_schedule_context(team_name)

    user_prompt = f"Analyze {team_name}'s 2026 World Cup future matchups. Use {schedule_conext} as context for team schedule." 

    try: 
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a professional football analyst for the 2026 World Cup and you are able to provide brief, realistic future insights on teams."
            ), 
            contents=user_prompt
        )
        return print(response.text)
    
    # Error handling
    except errors.ServerError as e:
        print("Gemini is currently unavailable")
        print("Error: ", e)


if __name__ == "__main__":

    insight = get_future_insight("Mexico")

