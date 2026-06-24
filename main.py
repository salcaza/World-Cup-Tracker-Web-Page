from football_api import get_team_schedule, print_schedule
from news_api import get_news, print_news
from database import save_headlines, save_schedule, save_team

print("WELCOME TO THE WORLD CUP TRACKER")

while true:
    team = input("Enter a team you'd like to track (or 'quit' to exit): ")

    if team.lower() == "quit":
        break

    while true:

        menu = (
            "\nMENU OPTIONS:\n"
            "View Team Schedule (S)\n"
            "View Recent Headlines (H)\n"
            "View Future Insights (I)\n"
            "Change Team(C)\n"
            "Quit(Q)\n"
        )

        choice = input(menu).upper()

        if choice == "S":
            print_schedule(team)
            print()
            save = input("Would you like to save this info? (y/n)")
            if save.lower() == "y":
                save_schedule(get_team_schedule(team))
        elif choice == "H":
            print_news(team)
            print()
            save = input("Would you like to save this info? (y/n)")
            if save.lower() == "y":
                save_headlines(get_news)
        elif choice == "I":
            pass
        else:
            print("INVALID CHOICE")
