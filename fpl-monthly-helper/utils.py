"""
FPL API helper functions
"""

import requests
from tabulate import tabulate

FPL_API = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_fpl_data(fpl_id):
    """Fetch FPL data for the given user ID (placeholder)."""
    # TODO: Implement FPL API fetching logic
    return {}

def get_team_tips():
    data = requests.get(FPL_API).json()
    top_players = sorted(data['elements'], key=lambda x: -x['form'])[:5]
    print("💡 Suggested Transfers:")
    for p in top_players:
        print(f"{p['web_name']} - Form: {p['form']} - Cost: {p['now_cost'] / 10}")

def get_captain_pick():
    data = requests.get(FPL_API).json()
    best_captain = max(data['elements'], key=lambda x: float(x['expected_points']) if 'expected_points' in x else 0)
    print(f"🧢 Recommended Captain: {best_captain['web_name']}")

def get_template_team_by_ownership(top_n=15):
    data = requests.get(FPL_API).json()
    players = data['elements']
    # Sort by selected_by_percent (as float), descending
    template = sorted(players, key=lambda x: -float(x['selected_by_percent']))[:top_n]
    print(f"🏆 Template Team (Top {top_n} by Ownership):")
    for p in template:
        print(f"{p['web_name']} - Owned by {p['selected_by_percent']}% - Cost: {p['now_cost'] / 10}")

def get_top10k_template():
    """
    Fetches and prints the top 10K template team using the LiveFPL API.
    """
    url = "https://api.livefpl.net/api/template/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return

    print("\n📊 Top 10K Template Team:")
    for position in ['gk', 'def', 'mid', 'fwd']:
        players = data['top_10k'][position]
        table = [
            [
                p['element_name'],
                p['element_team_short'],
                p['element_type'],
                f"{p['ownership']:.2f}%"
            ]
            for p in players
        ]
        print(f"\n🔹 {position.upper()}s:")
        print(tabulate(table, headers=["Player", "Team", "Pos", "Ownership"], tablefmt="github"))

def get_my_team(player_ids):
    """
    Accepts a list of player element IDs and returns their names and teams.
    """
    try:
        elements = requests.get(FPL_API).json()['elements']
    except Exception as e:
        print(f"❌ Failed to fetch element data: {e}")
        return []

    my_players = [e for e in elements if e['id'] in player_ids]
    return [f"{p['web_name']} ({p['team_code']})" for p in my_players]

def get_value_for_money_players(top_n=10):
    """
    Prints the top N players with the highest points per million value.
    """
    data = requests.get(FPL_API).json()
    players = data['elements']
    # Avoid division by zero and filter out players with 0 cost
    value_players = [p for p in players if p['now_cost'] > 0 and p['total_points'] > 0]
    value_players = sorted(value_players, key=lambda x: -(x['total_points'] / x['now_cost']))[:top_n]
    print(f"\n💸 Top {top_n} Value for Money Players (Points per Million):")
    for p in value_players:
        ppm = round(p['total_points'] / (p['now_cost'] / 10), 2)
        print(f"{p['web_name']} - {p['total_points']} pts - £{p['now_cost']/10}m - {ppm} pts/m")

def get_most_transferred_in(top_n=10):
    """
    Prints the top N most transferred-in players this gameweek.
    """
    data = requests.get(FPL_API).json()
    players = data['elements']
    most_in = sorted(players, key=lambda x: -x['transfers_in_event'])[:top_n]
    print(f"\n⬆️ Top {top_n} Most Transferred In (This GW):")
    for p in most_in:
        print(f"{p['web_name']} - {p['transfers_in_event']} transfers in")

def get_most_transferred_out(top_n=10):
    """
    Prints the top N most transferred-out players this gameweek.
    """
    data = requests.get(FPL_API).json()
    players = data['elements']
    most_out = sorted(players, key=lambda x: -x['transfers_out_event'])[:top_n]
    print(f"\n⬇️ Top {top_n} Most Transferred Out (This GW):")
    for p in most_out:
        print(f"{p['web_name']} - {p['transfers_out_event']} transfers out")

def get_injury_report(top_n=10):
    """
    Prints a list of players flagged as injured or unavailable.
    """
    data = requests.get(FPL_API).json()
    players = data['elements']
    injured = [p for p in players if p['status'] in ['i', 'd', 's', 'u']]
    injured = sorted(injured, key=lambda x: -x['now_cost'])[:top_n]
    print(f"\n🚑 Top {top_n} Expensive Injured/Unavailable Players:")
    for p in injured:
        print(f"{p['web_name']} - Status: {p['status']} - £{p['now_cost']/10}m")
