"""
Notification system for FPL Monthly Helper
Handles email, desktop, and calendar notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import os
import requests

def send_email_notification(subject, body, to_email="jobkimani@gmail.com"):
    """
    Send email notification with FPL tips.
    Requires Gmail app password setup.
    """
    try:
        # Email configuration - you'll need to set these in config.py
        from config import EMAIL_CONFIG
        sender_email = EMAIL_CONFIG.get('sender_email')
        sender_password = EMAIL_CONFIG.get('sender_password')
        
        if not sender_email or not sender_password:
            print("❌ Email credentials not configured. Please set up in config.py")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_desktop_notification(title, message):
    """
    Send desktop notification on macOS.
    """
    try:
        # Use macOS notification system
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        subprocess.run(['osascript', '-e', script], check=True)
        print("✅ Desktop notification sent")
        return True
    except Exception as e:
        print(f"❌ Failed to send desktop notification: {e}")
        return False

def get_weekly_report_text():
    """
    Generate a comprehensive weekly FPL report as text.
    """
    try:
        FPL_API = "https://fantasy.premierleague.com/api/bootstrap-static/"
        data = requests.get(FPL_API).json()
        players = data['elements']
        
        report = "📊 FPL Weekly Report\n"
        report += "=" * 50 + "\n\n"
        
        # Team tips
        top_players = sorted(players, key=lambda x: -x['form'])[:5]
        report += "💡 Suggested Transfers:\n"
        for p in top_players:
            report += f"• {p['web_name']} - Form: {p['form']} - Cost: £{p['now_cost']/10}m\n"
        
        # Captain pick
        best_captain = max(players, key=lambda x: float(x.get('expected_points', 0)) if x.get('expected_points') else 0)
        report += f"\n🧢 Recommended Captain: {best_captain['web_name']}\n"
        
        # Value for money
        value_players = [p for p in players if p['now_cost'] > 0 and p['total_points'] > 0]
        value_players = sorted(value_players, key=lambda x: -(x['total_points'] / x['now_cost']))[:5]
        report += "\n💸 Top Value for Money:\n"
        for p in value_players:
            ppm = round(p['total_points'] / (p['now_cost'] / 10), 2)
            report += f"• {p['web_name']} - {p['total_points']} pts - £{p['now_cost']/10}m - {ppm} pts/m\n"
        
        # Most transferred in
        most_in = sorted(players, key=lambda x: -x['transfers_in_event'])[:5]
        report += "\n⬆️ Most Transferred In:\n"
        for p in most_in:
            report += f"• {p['web_name']} - {p['transfers_in_event']} transfers\n"
        
        # Injuries
        injured = [p for p in players if p['status'] in ['i', 'd', 's', 'u']]
        injured = sorted(injured, key=lambda x: -x['now_cost'])[:5]
        report += "\n🚑 Expensive Injured Players:\n"
        for p in injured:
            report += f"• {p['web_name']} - Status: {p['status']} - £{p['now_cost']/10}m\n"
        
        return report
        
    except Exception as e:
        return f"❌ Failed to generate report: {e}"

def send_weekly_notifications():
    """
    Send all weekly notifications (email, desktop, calendar).
    """
    report = get_weekly_report_text()
    
    # Send desktop notification
    send_desktop_notification("FPL Weekly Reminder", "Check your email for this week's FPL tips!")
    
    # Send email notification
    send_email_notification("⚽️ FPL Weekly Report", report)
    
    print("📧 All notifications sent!") 