"""
Multi-Account Telegram Member Adder - Orchestrates adding members using multiple accounts
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import time
import os
import pickle
import random
import config
from colorama import init, Fore

# Initialize colorama
init()

# Color constants
R = Fore.RED
LG = Fore.GREEN
RS = Fore.RESET
W = Fore.WHITE
CY = Fore.CYAN
YE = Fore.YELLOW

colors = [R, LG, W, YE, CY]

# Info messages
info = LG + '(' + W + 'i' + LG + ')' + RS
error = LG + '(' + R + '!' + LG + ')' + RS
success = W + '(' + LG + '*' + W + ')' + RS
INPUT = LG + '(' + CY + '~' + LG + ')' + RS
plus = LG + '(' + W + '+' + LG + ')' + RS


def banner():
    """Display banner"""
    try:
        import pyfiglet
        f = pyfiglet.Figlet(font='slant')
        logo = f.renderText('Telegram')
        print(random.choice(colors) + logo + RS)
        print(f'{R}   Multi-Account Adder Version: 1.0 {R}| Enhanced by SuperNinja{RS}')
    except ImportError:
        print(f'{LG}Multi-Account Adder V1.0{RS}\n')


def clear_screen():
    """Clear terminal screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def main():
    """Main orchestrator function"""
    clear_screen()
    banner()
    
    # Check if data file exists
    if not os.path.exists(config.DATA_FILE):
        print(f'{error}{R} No accounts found! Run manager.py first to add accounts.{RS}')
        input('\nPress enter to exit...')
        sys.exit(1)
    
    # Check if members file exists
    if not os.path.exists(f'{config.MEMBERS_DIR}/members.csv'):
        print(f'{error}{R} No members file found! Run scraper.py first to scrape members.{RS}')
        input('\nPress enter to exit...')
        sys.exit(1)
    
    # Load accounts
    accounts = []
    f = open(config.DATA_FILE, 'rb')
    while True:
        try:
            accounts.append(pickle.load(f))
        except EOFError:
            break
    f.close()
    
    # Load target group
    scraped_grp = ''
    if os.path.exists(config.TARGET_GROUP_FILE):
        with open(config.TARGET_GROUP_FILE, 'r') as f:
            scraped_grp = f.readline().strip()
    f.close()
    
    # Load users from CSV
    users = []
    input_file = f'{config.MEMBERS_DIR}/members.csv'
    with open(input_file, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=',', lineterminator='\n')
        next(reader, None)  # Skip header
        for row in reader:
            user = {}
            user['username'] = row[0]
            user['user_id'] = row[1]
            user['access_hash'] = row[2]
            user['group'] = row[3]
            user['group_id'] = row[4]
            users.append(user)
    
    print(f'\n{info}{LG} Creating sessions for all accounts...{RS}')
    
    # Verify accounts and remove banned ones
    banned = []
    for a in accounts:
        iD = int(a[0])
        Hash = str(a[1])
        phn = str(a[2])
        clnt = TelegramClient(f'{config.SESSIONS_DIR}/{phn}', iD, Hash)
        clnt.connect()
        
        if not clnt.is_user_authorized():
            try:
                clnt.send_code_request(phn)
                code = input(f'{INPUT}{LG} Enter code for {W}{phn}{CY}[s to skip]:{R}')
                if 's' in code.lower():
                    accounts.remove(a)
                else:
                    clnt.sign_in(phn, code)
            except PhoneNumberBannedError:
                print(f'{error}{W}{phn} {R}is banned!{RS}')
                banned.append(a)
            except Exception as e:
                print(f'{error}{R} Error with {phn}: {e}{RS}')
        
        for z in banned:
            if z in accounts:
                accounts.remove(z)
        
        time.sleep(0.5)
        clnt.disconnect()
    
    print(f'{info}{LG} Sessions created!{RS}')
    
    if len(accounts) == 0:
        print(f'{error}{R} No valid accounts available!{RS}')
        input('\nPress enter to exit...')
        sys.exit(1)
    
    # Get target group
    time.sleep(2)
    print(f'{plus}{LG} Enter the exact username of the public group{W}[Without @]')
    g = input(f'{INPUT}{LG} Username [Eg: Techmedies_Hub]: {R}')
    group = f't.me/{g}'
    
    # Join target group from all accounts
    print(f'\n{info}{LG} Joining from all accounts...{RS}')
    for account in accounts:
        api_id = int(account[0])
        api_hash = str(account[1])
        phone = str(account[2])
        client = TelegramClient(f'{config.SESSIONS_DIR}/{phone}', api_id, api_hash)
        client.connect()
        try:
            username = client.get_entity(group)
            client(JoinChannelRequest(username))
            print(f'{success}{LG} Joined from {phone}')
        except Exception as e:
            print(f'{error}{R} Error in joining from {phone}: {e}')
            if account in accounts:
                accounts.remove(account)
        client.disconnect()
    
    time.sleep(2)
    clear_screen()
    
    number = len(accounts)
    print(f'{info}{LG} Total accounts: {W}{number}')
    print(f'{info}{LG} If you have more than 10 accounts then it is recommended to use 10 at a time')
    
    a = int(input(f'{plus}{LG} Enter number of accounts to use: {R}'))
    if a > number:
        a = number
    
    to_use = accounts[:a]
    
    # Distribute CSV files among accounts
    print(f'\n{info}{LG} Distributing CSV files...{RS}')
    time.sleep(2)
    
    for i, acc in enumerate(to_use):
        done = []
        file = f'{config.MEMBERS_DIR}/members{i}.csv'
        
        with open(file, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            
            # Distribute members to this account
            members_for_account = users[:config.MEMBERS_PER_ACCOUNT]
            for user in members_for_account:
                writer.writerow([
                    user['username'], 
                    user['user_id'], 
                    user['access_hash'], 
                    user['group'], 
                    user['group_id']
                ])
                done.append(user)
        f.close()
        
        # Remove processed users from main list
        del_count = 0
        while del_count != len(done):
            del users[0]
            del_count += 1
        
        if len(users) == 0:
            break
    
    # Save remaining users
    if not len(users) == 0:
        with open(f'{config.MEMBERS_DIR}/members.csv', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            for user in users:
                writer.writerow([
                    user['username'], 
                    user['user_id'], 
                    user['access_hash'], 
                    user['group'], 
                    user['group_id']
                ])
        f.close()
        m = str(len(users))
        print(f'{info}{LG} Remaining {m} users stored in {W}members.csv')
    
    # Update vars.txt
    remaining_accounts = [acc for acc in accounts if acc not in to_use]
    with open(config.DATA_FILE, 'wb') as f:
        for acc in remaining_accounts:
            pickle.dump(acc, f)
        for k in to_use:
            pickle.dump(k, f)
    f.close()
    
    print(f'{info}{LG} CSV file distribution complete{RS}')
    time.sleep(2)
    clear_screen()
    
    # Check platform for automation support
    if os.name != 'nt':
        print(f'{error}{R} Note: Full automation (launching multiple windows) supports only Windows systems')
        print(f'{info}{LG} On Linux/Mac, you will need to manually run adder.py for each account{RS}')
        print(f'\n{info}{LG} Commands to run manually:{RS}')
        for i, acc in enumerate(to_use):
            api_id = str(acc[0])
            api_hash = str(acc[1])
            phone = str(acc[2])
            file = f'{config.MEMBERS_DIR}/members{i}.csv'
            print(f'  python adder.py {api_id} {api_hash} {phone} {file} {group} {scraped_grp}')
        
        input(f'\n{plus}{LG} Press enter to exit...{RS}')
        sys.exit(0)
    
    # Windows - automated launching
    program = 'adder.py'
    o = str(len(to_use))
    
    print(f'\n{info}{R} This will be fully automated.')
    print(f'{info}{R} Don\'t touch the keyboard until cmd window pop-up stops')
    input(f'\n{plus}{LG} Press enter to continue...{RS}')
    
    print(f'\n{info}{LG} Launching from {o} accounts...{RS}\n')
    
    try:
        import keyboard
        
        for i in range(5, 0, -1):
            print(random.choice(colors) + str(i) + RS)
            time.sleep(1)
        
        for i, account in enumerate(to_use):
            api_id = str(account[0])
            api_hash = str(account[1])
            phone = str(account[2])
            file = f'{config.MEMBERS_DIR}/members{i}.csv'
            
            os.system('start cmd')
            time.sleep(1.5)
            
            # Write command
            keyboard.write(f'python {program} {api_id} {api_hash} {phone} {file} {group} {scraped_grp}')
            keyboard.press_and_release('Enter')
            
            print(f'{plus}{LG} Launched from {phone}')
    
    except ImportError:
        print(f'{error}{R} keyboard module not installed. Install it with: pip install keyboard{RS}')
        print(f'\n{info}{LG} Commands to run manually:{RS}')
        for i, account in enumerate(to_use):
            api_id = str(account[0])
            api_hash = str(account[1])
            phone = str(account[2])
            file = f'{config.MEMBERS_DIR}/members{i}.csv'
            print(f'  python adder.py {api_id} {api_hash} {phone} {file} {group} {scraped_grp}')
        
        input(f'\n{plus}{LG} Press enter to exit...{RS}')


if __name__ == '__main__':
    try:
        import sys
        main()
    except KeyboardInterrupt:
        print(f'\n\n{error}{R} Interrupted by user{RS}')
        sys.exit(1)
    except Exception as e:
        print(f'\n\n{error}{R} Error: {e}{RS}')
        import traceback
        traceback.print_exc()
        input('\nPress enter to exit...')