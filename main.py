from football_api import get_team_schedule, print_schedule
from news_api import get_news
from database import save_headlines, save_schedule, save_team

print("WELCOME TO THE WORLD CUP TRACKER")

team = input("Enter a team you'd like to track: ")

menu = (
    "MENU OPTIONS:\n"
    "View Team Schedule (S)\n"
    "View Recent Headlines (H)\n"
    "View Future Insights (I)\n"
)

choice = input(menu)

if choice.upper() == "S":
    print_schedule(team)
    print()
    save = input("Would you like to save this info? (y/n)")
    if save.lower() == "y":
        save_schedule(get_team_schedule(team))
#if choice.upper() == "H":
