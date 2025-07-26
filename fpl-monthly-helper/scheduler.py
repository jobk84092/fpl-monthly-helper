"""
Weekly reminder scheduler
"""

import schedule
import time
from utils import (
    get_team_tips, get_captain_pick, get_value_for_money_players,
    get_most_transferred_in, get_most_transferred_out, get_injury_report
)
from notifications import send_weekly_notifications

def weekly_job():
    print("🗓️ Weekly FPL Reminder:")
    # Print to terminal (for immediate feedback)
    get_team_tips()
    get_captain_pick()
    get_value_for_money_players()
    get_most_transferred_in()
    get_most_transferred_out()
    get_injury_report()
    
    # Send notifications
    send_weekly_notifications()

def setup_weekly_reminder():
    schedule.every().friday.at("09:00").do(weekly_job)
    print("🔔 Reminder set for every Friday 9AM.")
    print("📧 Will send email to jobkimani@gmail.com")
    print("🖥️ Will show desktop notification")
    while True:
        schedule.run_pending()
        time.sleep(60)
