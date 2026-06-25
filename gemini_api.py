import os
from google import genai 
from google.genai import types, errors
from football_api import get_team_schedule
from news_api import get_news, save_news
from dotenv import load_dotenv

load_dotenv()

#Set environment variables

my_api_key = os.getenv('GENAI_KEY')
genai.api_key = my_api_key

# Creates a genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key
)

# Schedule context to feed gemini (re-used print schedule from football_api.py)
def build_schedule_context(team_name):
    schedule = get_team_schedule(team_name)

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
    schedule_context = build_schedule_context(team_name)
     

    user_prompt = f"Analyze {team_name}'s 2026 World Cup future matchups. Use {schedule_context} as context for team schedule." 

    try: 
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a professional football analyst for the 2026 World Cup and you are able to provide very brief, realistic future insights on teams."
            ), 
            contents=user_prompt
        )
        return print(response.text)
    
    # Error handling
    except errors.ServerError as e:
        print("Gemini is currently unavailable")
        print("Error: ", e)


def get_headlines_summary(team_name):

    # obtain articles
    articles = get_news(team_name)[0:1]

    # so we can save to database
    headline_list = []

    
    for article in articles:

        print(f'Title: {article["title"]}')
        print(f'By: {article["author"]}')
        print(f'Description: {article["description"]}')
        print(f'URL: {article["url"]}')    

        user_prompt = f"follow up with a summary of each article one by one about {team_name} using {article}"

        try: 
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction="You are a news reporter that gives clear, very brief summaries(1-2 sentences long on each article) on news articles on specific football teams."
                ), 
                contents=user_prompt
            )

            # including summary key-value pair within each article
            article["summary"] = response.text
            print(f'Summary: {article["summary"]}')
            print( "-" * 50)
            print()
            headline_list.append(article)
 
        # Error handling
        except errors.ServerError as e:
            print("Gemini is currently unavailable")
            print("Error: ", e)

    return headline_list




if __name__ == "__main__":

    insight = get_future_insight("Mexico")
    summary_test = get_summary("Mexico")

