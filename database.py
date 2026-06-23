import sqlalchemy as db
import pandas as pd 
import datetime




#SQLite database engine
engine = db.create_engine('sqlite:///world_cup.db')

#Mock data for saved teams
mock_saved_teams = [
    {"team_name": "Mexico",
    "saved_at": "2026-06-23 2:00:00"},

    {"team_name": "Brazil",
    "saved_at": "2026-06-23 2:05:00"}
]

#Mock Data for Team Schedules
mock_schedule = [{
    "team_name": "Mexico",
    "opponent": "Belgium",
    "venue": "State Roi Baudouin",
    "date": "2026-06-28",
    "status": "Match Upcoming"},

    {"team_name": "Mexico",
    "opponent": "Brazil",
    "venue": "State Roi Baudouin",
    "date": "2026-06-20",
    "status": "Match Finished"}]

#Mock data for team information
mock_team_info = [
    {"team_name": "Argentina",
    "player_name" : "Lionel Messi",
    "position": "Forward",
    "coach": "Lionel Scaloni"
    }
]

#Mock data for news headlines on teams
mock_headlines = [{
    "team_name" : "Argentina",
    "title": "...",
    "author": "...",
    "description": "...",
    "url" : "..."

}]

# Function that takes in team, represents it as a dictionary of team name and time saved.
# Transforms team_data into a dataframe that will be saved in a database table. 
def save_team(team_name):
    team_data = {
        "team_name": team_name,
        "saved_at" : datetime.now().strftime("%I:%M%p on %B %d, %Y")
    }

    df = pd.DataFrame.from_dict(team_data)

    #if the table already exists append the new values
    df.tosql("saved_teams", con=engine, if_exists='append', index=False)

# Function that saves the schedule list of a particular team in the database
def save_schedule(schedule_list):

    #
    df = pd.DataFame.from_dict(schedule_list)

    df.tosql("saved_schedules", con=engine, if_exists='append', index=False)

def save_headlines(headline_list):


def save_team_info(team_info_list):


#Read functions will query the database and read the sql 

#Stores the mock database from the mock data 
def create_mock_database():


#Calls the mock database and tests outputs
if __name__ == __main__:










df_football = 

df_news = 

