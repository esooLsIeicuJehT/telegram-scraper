"""
Telegram Member Scraper - Extract members from Telegram groups
"""

import csv
import sys
import time
import os
import datetime
import config
import utils
from telethon.sync import TelegramClient
from telethon.tl.types import (
    UserStatusRecently, UserStatusOnline, UserStatusLastWeek, 
    UserStatusLastMonth, UserStatusOffline, ChannelParticipantsAdmins
)
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError

# Use colors and symbols from utils
LG = utils.LG
RS = utils.RS
R = utils.R
W = utils.W
CY = utils.CY
info = utils.info
error = utils.error
success = utils.success
INPUT = utils.INPUT

def write_member(writer, group, member):
    """Write member data to CSV"""
    username = member.username if member.username else ''
    
    if isinstance(member.status, UserStatusOffline):
        writer.writerow([
            username, 
            member.id, 
            member.access_hash, 
            group.title, 
            group.id,
            member.status.was_online
        ])
    else:
        status_name = type(member.status).__name__
        writer.writerow([
            username, 
            member.id, 
            member.access_hash, 
            group.title, 
            group.id,
            status_name
        ])

def scrape_members():
    """Main scraping function"""
    utils.clear_screen()
    utils.banner()
    
    # Load accounts
    accs = utils.load_accounts()
    
    if not accs:
        print(f'{error} No accounts available! Please add accounts using manager.py.')
        sys.exit(1)
    
    print(f'{INPUT}{CY} Choose an account to scrape members\n')
    for i, acc in enumerate(accs):
        print(f'{LG}({W}{i}{LG}) {acc[2]}')
    
    try:
        ind = int(input(f'\n{INPUT}{CY} Enter choice: '))
        if ind < 0 or ind >= len(accs):
            print(f'{error} Invalid choice!')
            sys.exit(1)
    except ValueError:
        print(f'{error} Invalid input!')
        sys.exit(1)
    
    api_id = accs[ind][0]
    api_hash = accs[ind][1]
    phone = accs[ind][2]
    
    group_name = input(f"Enter the name of the group without the @: {R}")
    
    # Create client
    c = TelegramClient(f'{config.SESSIONS_DIR}/{phone}', api_id, api_hash)
    c.connect()
    
    if not c.is_user_authorized():
        try:
            c.send_code_request(phone)
            code = input(f'{INPUT}{LG} Enter the login code for {W}{phone}{R}: ')
            c.sign_in(phone, code)
        except PhoneNumberBannedError:
            print(f'{error}{W}{phone}{R} is banned!')
            print(f'{error}{LG} Run manager.py to filter them{RS}')
            sys.exit(1)
        except Exception as e:
            print(f'{error} Error during authentication: {e}')
            sys.exit(1)
    
    try:
        group = c.get_entity(group_name)
        target_grp = f"t.me/{group_name}"
    except Exception as e:
        print(f'{error} Error getting group: {e}')
        c.disconnect()
        sys.exit(1)
    
    # Display options
    print(f"\n{LG}How would you like to obtain the users?\n")
    print(f"{R}[{CY}0{R}]{LG} All users")
    print(f"{R}[{CY}1{R}]{LG} Active Users (online today and yesterday)")
    print(f"{R}[{CY}2{R}]{LG} Users active in the last week")
    print(f"{R}[{CY}3{R}]{LG} Users active in the last month")
    print(f"{R}[{CY}4{R}]{LG} Non-active users (not active in the last month)")

    try:
        choice = int(input(f"\nYour choice: "))
        if choice not in range(5):
            print(f'{error} Invalid choice!')
            c.disconnect()
            sys.exit(1)
    except ValueError:
        print(f'{error} Invalid input!')
        c.disconnect()
        sys.exit(1)
    
    members = c.iter_participants(group, aggressive=True)
    
    try:
        channel_full_info = c(GetFullChannelRequest(group))
        cont = channel_full_info.full_chat.participants_count
    except:
        cont = "Unknown"
    
    # Ensure members directory exists
    os.makedirs(config.MEMBERS_DIR, exist_ok=True)
    
    # Ask about admins
    admin_choice = input(f"{LG}Would you like to have admins on a separate CSV file? {RS}[y/n] {LG}")
    if admin_choice.lower() == 'y':
        print(f"{LG}Scraping admins...\n")
        with open(f"{config.MEMBERS_DIR}/admins.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id', 'status'])
            count = 0
            for member in c.iter_participants(group, filter=ChannelParticipantsAdmins):
                if not member.bot:
                    write_member(writer, group, member)
                    count += 1
            print(f"{success} Scraped {count} admins")
    
    print(f"\n{LG}Starting member scraping...{RS}\n")
    
    # Date calculations
    today = datetime.datetime.now()
    today_date = today.date()
    yesterday = today - datetime.timedelta(days=1)

    with open(f"{config.MEMBERS_DIR}/members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id', 'status'])
        
        count = 0
        try:
             # We iterate over the generator
             for index, member in enumerate(members):
                print(f"{index+1}/{cont}", end="\r")
                if index % 100 == 0 and index > 0:
                    time.sleep(config.SCRAPE_DELAY)
                
                if member.bot:
                    continue

                should_write = False

                if choice == 0:
                    should_write = True

                elif choice == 1: # Active today/yesterday
                    if isinstance(member.status, (UserStatusRecently, UserStatusOnline)):
                        should_write = True
                    elif isinstance(member.status, UserStatusOffline):
                        d = getattr(member.status, 'was_online', None)
                        if d:
                             # Compare dates
                             today_user = d.day == today.day and d.month == today.month and d.year == today.year
                             yesterday_user = d.day == yesterday.day and d.month == yesterday.month and d.year == yesterday.year
                             if today_user or yesterday_user:
                                 should_write = True

                elif choice == 2: # Last week
                    if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek)):
                        should_write = True
                    elif isinstance(member.status, UserStatusOffline):
                         d = getattr(member.status, 'was_online', None)
                         if d:
                             if (today_date - d.date()).days <= 7:
                                 should_write = True

                elif choice == 3: # Last month
                    if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek, UserStatusLastMonth)):
                         should_write = True
                    elif isinstance(member.status, UserStatusOffline):
                         d = getattr(member.status, 'was_online', None)
                         if d and (today_date - d.date()).days <= 30:
                             should_write = True

                elif choice == 4: # Non-active
                     is_active = False
                     if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek, UserStatusLastMonth)):
                         is_active = True
                     elif isinstance(member.status, UserStatusOffline):
                         d = getattr(member.status, 'was_online', None)
                         if d and (today_date - d.date()).days <= 30:
                             is_active = True

                     if not is_active:
                         should_write = True

                if should_write:
                    write_member(writer, group, member)
                    count += 1

        except Exception as e:
            print(f"\n{error} Error during scraping loop: {e}")

        print(f"\n{LG}Total members saved: {count}{RS}")

    print(f"\n{LG}Users saved in the CSV file.{RS}\n")
    
    # Save target group info
    os.makedirs(config.DATA_DIR, exist_ok=True)
    with open(config.TARGET_GROUP_FILE, 'w') as f:
        f.write(target_grp)
    
    c.disconnect()
    
    print(f"{success} Scraping complete!{RS}\n")

if __name__ == '__main__':
    scrape_members()
