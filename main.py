import database as db
from football_api import get_team_schedule, print_schedule
from news_api import get_news, print_news
from gemini_api import get_future_insight, get_headlines_summary

print("WELCOME TO THE WORLD CUP TRACKER")

while True:
    team = input("Enter a team you'd like to track (or 'quit' to exit): ")

    if team.lower() == "quit":
        break

    while True:

        menu = (
            "\nWhat would you like to do:\n"
            "View Team Schedule (Enter: S)\n"
            "View Recent Headlines (Enter: H)\n"
            "View Future Insights (Enter: I)\n"
            "View Saved Headlines (Enter: VH)\n"
            "Change Team (Enter: C)\n"
            "Quit (Enter: Q)\n\n"
        )

        choice = input(menu).upper()

        if choice == "S":
            print()
            print_schedule(team)
            print()

        elif choice == "H":
            print()
            print("Loading...")
            get_headlines_summary(team)
            print()
            save = input("\nWould you like to save this info? (y/n)")
            if save.lower() == "y":
                db.save_headlines(get_headlines_summary(team))

        elif choice == "I":
            print("Loading...")
            print()
            insight = get_future_insight(team)

        elif choice == "VH":
            db.read_saved_headlines_for_team(team)

        elif choice == "C":
            # Break out of the inner loop and choose another team
            break

        elif choice == "Q":
            exit()

        else:
            print("INVALID CHOICE")
