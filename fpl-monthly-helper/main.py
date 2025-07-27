"""
Main script for FPL Monthly Helper
"""

from config import USER_CONFIG
from utils import (
    fetch_fpl_data, get_team_tips, get_captain_pick, get_template_team_by_ownership, get_top10k_template,
    get_value_for_money_players, get_most_transferred_in, get_most_transferred_out, get_injury_report
)
from scheduler import setup_weekly_reminder

def main():
    while True:
        print("\n==== FPL Monthly Helper ====")
        print("1. Get FPL tips for the week")
        print("2. Show template team by ownership")
        print("3. Show top 10K template team (LiveFPL)")
        print("4. Set up weekly reminder")
        print("5. Show value for money players")
        print("6. Show most transferred in players")
        print("7. Show most transferred out players")
        print("8. Show injury/unavailable report")
        print("0. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            print("\n📊 Fetching your FPL tips for the week...")
            get_team_tips()
            get_captain_pick()
        elif choice == "2":
            get_template_team_by_ownership()
        elif choice == "3":
            get_top10k_template()
        elif choice == "4":
            setup_weekly_reminder()
        elif choice == "5":
            get_value_for_money_players()
        elif choice == "6":
            get_most_transferred_in()
        elif choice == "7":
            get_most_transferred_out()
        elif choice == "8":
            get_injury_report()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
