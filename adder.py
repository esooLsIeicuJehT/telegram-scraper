"""
Telegram Member Adder - Add members to Telegram groups using multiple accounts
"""

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import csv
import sys
import time
import random
import os
import pickle
import config
from colorama import init, Fore

# Initialize colorama
init()

# Color constants
R = Fore.RED
G = Fore.GREEN
RS = Fore.RESET
W = Fore.WHITE
CY = Fore.CYAN
YE = Fore.YELLOW
LG = Fore.LIGHTGREEN_EX

colors = [R, G, W, YE, CY]

# Info messages
info = G + '[' + W + 'i' + G + ']' + RS
attempt = G + '[' + W + '+' + G + ']' + RS
sleep_msg = G + '[' + W + '*' + G + ']' + RS
error = G + '[' + R + '!' + G + ']' + RS


def banner():
    """Display banner"""
    try:
        import pyfiglet
        f = pyfiglet.Figlet(font='slant')
        logo = f.renderText('Telegram')
        print(random.choice(colors) + logo + RS)
        print(f'{info}{G} Telegram Adder [USERNAME] V1.0{RS}')
        print(f'{info}{G} Enhanced by SuperNinja{RS}\n')
    except ImportError:
        print(f'{G}Telegram Adder V1.0{RS}\n')


def clear_screen():
    """Clear terminal screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Relog:
    """Handle relogging of remaining users"""
    def __init__(self, lst, filename):
        self.lst = lst
        self.filename = filename
    
    def start(self):
        with open(self.filename, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            for user in self.lst:
                writer.writerow([
                    user['username'], 
                    user['user_id'], 
                    user['access_hash'], 
                    user['group'], 
                    user['group_id']
                ])
            f.close()


def update_list(lst, temp_lst):
    """Update list by removing processed items"""
    count = 0
    while count != len(temp_lst):
        del lst[0]
        count += 1
    return lst


def add_members():
    """Main function to add members to group"""
    # Check arguments
    if len(sys.argv) < 6:
        print(f"{error}{R} Usage: python adder.py <api_id> <api_hash> <phone> <csv_file> <group> [scraped_group]{RS}")
        print(f"{info}{G} Or run main_adder.py for automated multi-account adding{RS}")
        sys.exit(1)
    
    clear_screen()
    banner()
    
    # Parse arguments
    api_id = int(sys.argv[1])
    api_hash = str(sys.argv[2])
    phone = str(sys.argv[3])
    file = str(sys.argv[4])
    group = str(sys.argv[5])
    
    # Check if file exists
    if not os.path.exists(file):
        print(f"{error}{R} CSV file not found: {file}{RS}")
        sys.exit(1)
    
    # Load users from CSV
    users = []
    try:
        with open(file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=',', lineterminator='\n')
            next(rows, None)  # Skip header
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['user_id'] = row[1]
                user['access_hash'] = row[2]
                user['group'] = row[3]
                user['group_id'] = row[4]
                users.append(user)
    except Exception as e:
        print(f"{error}{R} Error loading users: {e}{RS}")
        sys.exit(1)
    
    if len(users) == 0:
        print(f"{error}{R} No users found in CSV file{RS}")
        sys.exit(1)
    
    # Create client
    client = TelegramClient(f'{config.SESSIONS_DIR}/{phone}', api_id, api_hash)
    
    try:
        client.connect()
        time.sleep(1.5)
        
        # Get target group
        target_group = client.get_entity(group)
        entity = InputPeerChannel(target_group.id, target_group.access_hash)
        group_name = target_group.title
        
        print(f'{info}{G} Adding members to {group_name}{RS}\n')
        print(f'{info}{G} Total users to add: {len(users)}{RS}\n')
        
        n = 0
        added_users = []
        success_count = 0
        failed_count = 0
        
        for user in users:
            n += 1
            added_users.append(user)
            
            # Batch delay
            if n % config.ADD_BATCH_SIZE == 0:
                print(f'{sleep_msg}{G} Sleep {config.BATCH_DELAY}s to prevent possible account ban{RS}')
                time.sleep(config.BATCH_DELAY)
            
            try:
                # Skip users without username
                if user['username'] == "":
                    print(f'{info}{G} Skipped user {user["user_id"]} (no username){RS}')
                    continue
                
                # Get user entity
                user_to_add = client.get_input_entity(user['username'])
                
                # Add to group
                client(InviteToChannelRequest(entity, [user_to_add]))
                
                usr_id = user['user_id']
                print(f'{attempt}{G} Added {usr_id} ({n}/{len(users)}){RS}')
                success_count += 1
                
                print(f'{sleep_msg}{G} Sleep {config.ADD_MEMBER_DELAY}s{RS}')
                time.sleep(config.ADD_MEMBER_DELAY)
                
            except PeerFloodError:
                print(f'\n{error}{R} Peer Flood Error - Account may be temporarily blocked{RS}')
                print(f'{info}{G} Logging remaining users to file{RS}')
                update_list(users, added_users)
                if not len(users) == 0:
                    logger = Relog(users, file)
                    logger.start()
                    print(f'{info}{G} Remaining {len(users)} users saved to {file}{RS}')
                client.disconnect()
                sys.exit(1)
                
            except UserPrivacyRestrictedError:
                print(f'{error}{R} User Privacy Restriction - {user["username"]}{RS}')
                failed_count += 1
                continue
                
            except Exception as e:
                print(f'{error}{R} Error adding user: {e}{RS}')
                failed_count += 1
                continue
        
        # Summary
        print(f'\n{success}{G} Addition complete!{RS}')
        print(f'{info}{G} Successfully added: {success_count}{RS}')
        print(f'{info}{G} Failed: {failed_count}{RS}')
        
        client.disconnect()
        
        input(f'\n{info}{G}Press enter to exit...{RS}')
        
    except Exception as e:
        print(f'\n{error}{R} Fatal error: {e}{RS}')
        if 'client' in locals():
            client.disconnect()
        sys.exit(1)


if __name__ == '__main__':
    add_members()