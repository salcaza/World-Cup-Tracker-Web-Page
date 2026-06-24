import database as db
from football_api import get_team_schedule, print_schedule
from news_api import get_news, print_news

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
            "View Saved Schedule (Enter: VS)\n"
            "View Saved Headlines (Enter: VH)\n"
            "View Saved Insights (Enter: VI)\n"
            "Change Team (Enter: C)\n"
            "Quit (Enter: Q)\n"
        )

        choice = input(menu).upper()

        if choice == "S":
            print()
            print_schedule(team)
            print()
            save = input("\nWould you like to save this info? (y/n)")
            if save.lower() == "y":
                sched = get_team_schedule(team)
                db.save_schedule(sched, team)

        elif choice == "H":
            print()
            print_news(team)
            print()
            save = input("\nWould you like to save this info? (y/n)")
            if save.lower() == "y":
                db.save_headlines(get_news(team))

        elif choice == "I":
            print("Not ready yet")

        elif choice == "VS":
            db.read_schedules_for_team(team)

        elif choice == "VH":
            db.read_saved_headlines_for_team(team)

        elif choice == "VI":
            print("Not ready yet")

        elif choice == "C":
            # Break out of the inner loop and choose another team
            break

        elif choice == "Q":
            exit()

        else:
            print("INVALID CHOICE")
