"""
Multi-Account Telegram Member Adder - Orchestrates adding members using multiple accounts
"""

import csv
import time
import os
import sys
import random
import asyncio
import config
import utils
from telethon.sync import TelegramClient
from telethon import TelegramClient as AsyncTelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError

# Use colors from utils
LG = utils.LG
R = utils.R
W = utils.W
CY = utils.CY
info = utils.info
error = utils.error
success = utils.success
plus = utils.plus
INPUT = utils.INPUT

def main():
    """Main orchestrator function"""
    utils.clear_screen()
    utils.banner()

    # Load accounts
    accounts = utils.load_accounts()
    
    if not accounts:
        print(f'{error}{R} No accounts found! Run manager.py first to add accounts.{utils.RS}')
        input('\nPress enter to exit...')
        sys.exit(1)
    
    # Check if members file exists
    if not os.path.exists(f'{config.MEMBERS_DIR}/members.csv'):
        print(f'{error}{R} No members file found! Run scraper.py first to scrape members.{utils.RS}')
        input('\nPress enter to exit...')
        sys.exit(1)
    
    # Load target group
    scraped_grp = ''
    if os.path.exists(config.TARGET_GROUP_FILE):
        with open(config.TARGET_GROUP_FILE, 'r') as f:
            scraped_grp = f.readline().strip()
    
    # Load users from CSV
    users = []
    input_file = f'{config.MEMBERS_DIR}/members.csv'
    try:
        with open(input_file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f, delimiter=',', lineterminator='\n')
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) < 5: continue
                user = {}
                user['username'] = row[0]
                user['user_id'] = row[1]
                user['access_hash'] = row[2]
                user['group'] = row[3]
                user['group_id'] = row[4]
                users.append(user)
    except Exception as e:
        print(f'{error} Error loading members: {e}')
        sys.exit(1)
    
    print(f'\n{info}{LG} Creating sessions for all accounts...{utils.RS}')
    
    # Verify accounts and remove banned ones
    banned = []
    valid_accounts = []

    for a in accounts:
        iD = int(a[0])
        Hash = str(a[1])
        phn = str(a[2])
        clnt = TelegramClient(f'{config.SESSIONS_DIR}/{phn}', iD, Hash)
        
        try:
            clnt.connect()

            if not clnt.is_user_authorized():
                try:
                    clnt.send_code_request(phn)
                    code = input(f'{INPUT}{LG} Enter code for {W}{phn}{CY}[s to skip]:{R}')
                    if 's' in code.lower():
                        # Skip this account - it won't be in valid_accounts
                        pass
                    else:
                        clnt.sign_in(phn, code)
                        valid_accounts.append(a)
                except PhoneNumberBannedError:
                    print(f'{error}{W}{phn} {R}is banned!{utils.RS}')
                    banned.append(a)
                except Exception as e:
                    print(f'{error}{R} Error with {phn}: {e}{utils.RS}')
            else:
                valid_accounts.append(a)

            clnt.disconnect()
        except Exception as e:
             print(f'{error} Error connecting {phn}: {e}')

    
    # Remove banned accounts from storage
    if banned:
        print(f"{info} Removing {len(banned)} banned accounts...")
        for b in banned:
            if b in accounts:
                accounts.remove(b)
        utils.save_accounts(accounts)

    accounts = valid_accounts
    print(f'{info}{LG} Sessions created!{utils.RS}')
    
    if len(accounts) == 0:
        print(f'{error}{R} No valid accounts available!{utils.RS}')
        input('\nPress enter to exit...')
        sys.exit(1)
    
    # Get target group
    time.sleep(1)
    print(f'{plus}{LG} Enter the exact username of the public group{W}[Without @]')
    g = input(f'{INPUT}{LG} Username [Eg: Techmedies_Hub]: {R}')
    group = f't.me/{g}'
    
    # Join target group from all accounts
    print(f'\n{info}{LG} Joining from all accounts...{utils.RS}')

    async def join_channel(account, group):
        api_id = int(account[0])
        api_hash = str(account[1])
        phone = str(account[2])
        client = AsyncTelegramClient(f'{config.SESSIONS_DIR}/{phone}', api_id, api_hash)
        try:
            await client.connect()
            username = await client.get_entity(group)
            await client(JoinChannelRequest(username))
            print(f'{success}{LG} Joined from {phone}')
        except Exception as e:
            print(f'{error}{R} Error in joining from {phone}: {e}')
        finally:
            await client.disconnect()

    async def join_all_accounts(accounts, group):
        tasks = []
        for account in accounts:
            tasks.append(join_channel(account, group))
        await asyncio.gather(*tasks)

    asyncio.run(join_all_accounts(accounts, group))
    
    time.sleep(1)
    utils.clear_screen()
    
    number = len(accounts)
    print(f'{info}{LG} Total accounts: {W}{number}')
    print(f'{info}{LG} If you have more than 10 accounts then it is recommended to use 10 at a time')
    
    try:
        a = int(input(f'{plus}{LG} Enter number of accounts to use: {R}'))
    except ValueError:
        a = number

    if a > number:
        a = number
    
    to_use = accounts[:a]
    
    # Distribute CSV files among accounts
    print(f'\n{info}{LG} Distributing CSV files...{utils.RS}')
    time.sleep(1)

    current_user_index = 0
    
    for i, acc in enumerate(to_use):
        file = f'{config.MEMBERS_DIR}/members{i}.csv'
        
        # Determine slice for this account
        start = current_user_index
        end = current_user_index + config.MEMBERS_PER_ACCOUNT
        members_for_account = users[start:end]
        current_user_index = end # Move pointer

        with open(file, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            
            for user in members_for_account:
                writer.writerow([
                    user['username'], 
                    user['user_id'], 
                    user['access_hash'], 
                    user['group'], 
                    user['group_id']
                ])
        
        if len(members_for_account) == 0:
            break

    # Save remaining users
    remaining_users = users[current_user_index:]
    if remaining_users:
        with open(f'{config.MEMBERS_DIR}/members.csv', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            for user in remaining_users:
                writer.writerow([
                    user['username'], 
                    user['user_id'], 
                    user['access_hash'], 
                    user['group'], 
                    user['group_id']
                ])
        print(f'{info}{LG} Remaining {len(remaining_users)} users stored in {W}members.csv')
    else:
         # Empty file if no users left
         with open(f'{config.MEMBERS_DIR}/members.csv', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
    
    # Rotate accounts
    rotated_accounts = accounts[a:] + accounts[:a]
    utils.save_accounts(rotated_accounts)
    
    print(f'{info}{LG} CSV file distribution complete{utils.RS}')
    time.sleep(1)
    utils.clear_screen()
    
    # Check platform for automation support
    if os.name != 'nt':
        print(f'{error}{R} Note: Full automation (launching multiple windows) supports only Windows systems')
        print(f'{info}{LG} On Linux/Mac, you will need to manually run adder.py for each account{utils.RS}')
        print(f'\n{info}{LG} Commands to run manually:{utils.RS}')
        for i, acc in enumerate(to_use):
            api_id = str(acc[0])
            api_hash = str(acc[1])
            phone = str(acc[2])
            file = f'{config.MEMBERS_DIR}/members{i}.csv'
            print(f'  python adder.py {api_id} {api_hash} {phone} {file} {group} {scraped_grp}')
        
        input(f'\n{plus}{LG} Press enter to exit...{utils.RS}')
        sys.exit(0)
    
    # Windows - automated launching
    program = 'adder.py'
    o = str(len(to_use))
    
    print(f'\n{info}{R} This will be fully automated.')
    print(f'{info}{R} Don\'t touch the keyboard until cmd window pop-up stops')
    input(f'\n{plus}{LG} Press enter to continue...{utils.RS}')
    
    print(f'\n{info}{LG} Launching from {o} accounts...{utils.RS}\n')
    
    try:
        import keyboard
        
        for i in range(5, 0, -1):
            print(random.choice(utils.colors) + str(i) + utils.RS)
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
        print(f'{error}{R} keyboard module not installed. Install it with: pip install keyboard{utils.RS}')
        print(f'\n{info}{LG} Commands to run manually:{utils.RS}')
        for i, account in enumerate(to_use):
            api_id = str(account[0])
            api_hash = str(account[1])
            phone = str(account[2])
            file = f'{config.MEMBERS_DIR}/members{i}.csv'
            print(f'  python adder.py {api_id} {api_hash} {phone} {file} {group} {scraped_grp}')
        
        input(f'\n{plus}{LG} Press enter to exit...{utils.RS}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\n{error}{R} Interrupted by user{utils.RS}')
        sys.exit(1)
    except Exception as e:
        print(f'\n\n{error}{R} Error: {e}{utils.RS}')
        import traceback
        traceback.print_exc()
        input('\nPress enter to exit...')
