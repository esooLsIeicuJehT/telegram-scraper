"""
Telegram Member Scraper - Extract members from Telegram groups
"""

from telethon.sync import TelegramClient
from telethon.tl.types import (
    UserStatusRecently, UserStatusOnline, UserStatusLastWeek, 
    UserStatusLastMonth, UserStatusOffline, ChannelParticipantsAdmins
)
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import sys
import pickle
import random
import os
import datetime
import config
from colorama import init, Fore
import pyfiglet

# Initialize colorama
init()

# Color constants
LG = Fore.LIGHTGREEN_EX
RS = Fore.RESET
R = Fore.RED
W = Fore.WHITE
CY = Fore.CYAN
G = Fore.GREEN
B = Fore.BLUE

# Date calculations
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

# Info messages
info = LG + '(' + W + 'i' + LG + ')' + RS
error = LG + '(' + R + '!' + LG + ')' + RS
success = W + '(' + LG + '+' + W + ')' + RS
INPUT = LG + '(' + CY + '~' + LG + ')' + RS

colors = [LG, W, R, CY]


def banner():
    """Display banner"""
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Telegram')
    print(random.choice(colors) + logo + RS)


def clear_screen():
    """Clear terminal screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


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
        writer.writerow([
            username, 
            member.id, 
            member.access_hash, 
            group.title, 
            group.id,
            type(member.status).__name__
        ])


def scrape_members():
    """Main scraping function"""
    import pyfiglet
    
    clear_screen()
    banner()
    print(f'  {R}Enhanced Version: 1.0 {R}| Author: Enhanced by SuperNinja{RS}\n')
    
    # Check if accounts file exists
    if not os.path.exists(config.DATA_FILE):
        print(f'{error}{R} No accounts found! Run manager.py first to add accounts.{RS}')
        sys.exit(1)
    
    # Load accounts
    accs = []
    try:
        f = open(config.DATA_FILE, 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
    except Exception as e:
        print(f'{error}{R} Error loading accounts: {e}{RS}')
        sys.exit(1)
    
    if len(accs) == 0:
        print(f'{error}{R} No accounts available! Please add accounts using manager.py.{RS}')
        sys.exit(1)
    
    print(f'{INPUT}{CY} Choose an account to scrape members\n')
    i = 0
    for acc in accs:
        print(f'{LG}({W}{i}{LG}) {acc[2]}')
        i += 1
    
    try:
        ind = int(input(f'\n{INPUT}{CY} Enter choice: '))
        if ind < 0 or ind >= len(accs):
            print(f'{error}{R} Invalid choice!{RS}')
            sys.exit(1)
    except ValueError:
        print(f'{error}{R} Invalid input!{RS}')
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
            print(f'{error}{W}{phone}{R} is banned!{RS}')
            print(f'{error}{LG} Run manager.py to filter them{RS}')
            sys.exit(1)
        except Exception as e:
            print(f'{error}{R} Error during authentication: {e}{RS}')
            sys.exit(1)
    
    try:
        group = c.get_entity(group_name)
        target_grp = f"t.me/{group_name}"
    except Exception as e:
        print(f'{error}{R} Error getting group: {e}{RS}')
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
        if choice < 0 or choice > 4:
            print(f'{error}{R} Invalid choice!{RS}')
            c.disconnect()
            sys.exit(1)
    except ValueError:
        print(f'{error}{R} Invalid input!{RS}')
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
            print(f"{success}{LG} Scraped {count} admins{RS}")
        f.close()
    
    print(f"\n{LG}Starting member scraping...{RS}\n")
    
    with open(f"{config.MEMBERS_DIR}/members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id', 'status'])
        
        if choice == 0:
            # All users
            try:
                count = 0
                for index, member in enumerate(members):
                    print(f"{index+1}/{cont}", end="\r")
                    if index % 100 == 0 and index > 0:
                        from time import sleep
                        sleep(config.SCRAPE_DELAY)
                    if not member.bot:
                        write_member(writer, group, member)
                        count += 1
            except Exception as e:
                print(f"\n{R}There was an error: {e}")
                print(f"{R}But check members.csv. Some members should already be added.{RS}")
        
        elif choice == 1:
            # Active users (today and yesterday)
            try:
                count = 0
                for index, member in enumerate(members):
                    print(f"{index+1}/{cont}", end="\r")
                    if index % 100 == 0 and index > 0:
                        from time import sleep
                        sleep(config.SCRAPE_DELAY)
                    if not member.bot:
                        if isinstance(member.status, (UserStatusRecently, UserStatusOnline)):
                            write_member(writer, group, member)
                            count += 1
                        elif isinstance(member.status, UserStatusOffline):
                            d = member.status.was_online
                            today_user = d.day == today.day and d.month == today.month and d.year == today.year
                            yesterday_user = d.day == yesterday.day and d.month == yesterday.month and d.year == yesterday.year
                            if today_user or yesterday_user:
                                write_member(writer, group, member)
                                count += 1
            except Exception as e:
                print(f"\n{R}There was an error: {e}")
        
        elif choice == 2:
            # Users active in last week
            try:
                count = 0
                for index, member in enumerate(members):
                    print(f"{index+1}/{cont}", end="\r")
                    if index % 100 == 0 and index > 0:
                        from time import sleep
                        sleep(config.SCRAPE_DELAY)
                    if not member.bot:
                        if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek)):
                            write_member(writer, group, member)
                            count += 1
                        elif isinstance(member.status, UserStatusOffline):
                            d = member.status.was_online
                            for i in range(0, 7):
                                current_day = today - datetime.timedelta(days=i)
                                correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                if correct_user:
                                    write_member(writer, group, member)
                                    count += 1
                                    break
            except Exception as e:
                print(f"\n{R}There was an error: {e}")
        
        elif choice == 3:
            # Users active in last month
            try:
                count = 0
                for index, member in enumerate(members):
                    print(f"{index+1}/{cont}", end="\r")
                    if index % 100 == 0 and index > 0:
                        from time import sleep
                        sleep(config.SCRAPE_DELAY)
                    if not member.bot:
                        if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek, UserStatusLastMonth)):
                            write_member(writer, group, member)
                            count += 1
                        elif isinstance(member.status, UserStatusOffline):
                            d = member.status.was_online
                            for i in range(0, 30):
                                current_day = today - datetime.timedelta(days=i)
                                correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                if correct_user:
                                    write_member(writer, group, member)
                                    count += 1
                                    break
            except Exception as e:
                print(f"\n{R}There was an error: {e}")
        
        elif choice == 4:
            # Non-active users
            try:
                all_users = []
                active_users = []
                for index, member in enumerate(members):
                    print(f"{index+1}/{cont}", end="\r")
                    all_users.append(member)
                    if index % 100 == 0 and index > 0:
                        from time import sleep
                        sleep(config.SCRAPE_DELAY)
                    if not member.bot:
                        if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek, UserStatusLastMonth)):
                            active_users.append(member)
                        elif isinstance(member.status, UserStatusOffline):
                            d = member.status.was_online
                            for i in range(0, 30):
                                current_day = today - datetime.timedelta(days=i)
                                correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                if correct_user:
                                    active_users.append(member)
                                    break
                
                count = 0
                for member in all_users:
                    if member not in active_users:
                        write_member(writer, group, member)
                        count += 1
            except Exception as e:
                print(f"\n{R}There was an error: {e}")
        
        print(f"\n{LG}Total members saved: {count}{RS}")
        f.close()
    
    print(f"\n{LG}Users saved in the CSV file.{RS}\n")
    
    # Save target group info
    os.makedirs(config.DATA_DIR, exist_ok=True)
    with open(config.TARGET_GROUP_FILE, 'w') as f:
        f.write(target_grp)
    f.close()
    
    c.disconnect()
    
    print(f"{success}{LG} Scraping complete!{RS}\n")


if __name__ == '__main__':
    scrape_members()