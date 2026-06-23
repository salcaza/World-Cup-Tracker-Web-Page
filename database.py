import sqlalchemy as db
import pandas as pd 
from datetime import datetime, timezone




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
        "saved_at" : datetime.now(timezone.utc).strftime("%I:%M%p on %B %d, %Y")
    }

    #wrap team_data around a list since it is one dictionary (not a list of dictionaries)
    df = pd.DataFrame([team_data])

    #if the table already exists append the new values
    df.to_sql("saved_teams", con=engine, if_exists='append', index=False)


# Function that saves the schedule list of a particular team in the database
def save_schedule(schedule_list):
    if len(schedule_list) == 0:
        return

    #load data into dataframe
    df = pd.DataFrame(schedule_list)

    #Create sql table for schedules
    df.to_sql("schedules", con=engine, if_exists='append', index=False)


def save_headlines(headline_list):
    if len(headline_list) == 0:
        return
    
    #load data into dataframe
    df = pd.DataFrame(headline_list)

    #Create sql table for headlines
    df.to_sql("headlines", con=engine, if_exists='append', index=False)





#Read functions will query the database and read the sql 

#Writes a query to saved teams table and returns saved teams
def read_saved_teams():

    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM saved_teams;")).fetchall()
        return query_result

#Writes a query to saved schedules table and returns schedule for chosen team
def read_schedules_for_team(team_name):
    with engine.connect() as connection:
        #Filter by team name
        query_result = connection.execute(db.text("SELECT * FROM schedules WHERE team_name = :team_name;"), 
        {"team_name" : team_name}).fetchall()
        return query_result

#Writes a query to saved headlines table and returns saved headlines
def read_saved_headlines_for_team():
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM headlines WHERE team_name= :team_name;"),
        {"team_name" : team_name}).fetchall()
        return query_result
    



#Tests the databases using the same save/read functions that main will use 
def test_mock_database():
    reset_database()

    #initialize the save_team table
    for team in mock_saved_teams:
        save_team(team["team_name"])

    save_schedule(mock_schedule)
    save_headlines(mock_headlines)

    print("\n Saved Teams:")
    print(read_saved_teams())

    print("\nMexico Schedule:")

    print(read_schedules_for_team("Mexico"))

    print("\n Headlines for Mexico: ")
    print(read_saved_headlines_for_team("Mexico"))






#resets the database for testing purposes

def reset_database():
    with engine.connect() as connection:
        connection.execute(db.text("DROP TABLE IF EXISTS saved_teams"))
        connection.execute(db.text("DROP TABLE IF EXISTS schedules"))
        connection.execute(db.text("DROP TABLE IF EXISTS headlines"))


if __name__ == "__main__":
    test_mock_database()



