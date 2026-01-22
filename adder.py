"""
Telegram Member Adder - Add members to Telegram groups using multiple accounts
"""

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import csv
import sys
import time
import os
import config
import utils

# Use colors from utils
LG = utils.LG
R = utils.R
W = utils.W
CY = utils.CY
G = utils.G
RS = utils.RS

# Info messages
info = G + '[' + W + 'i' + G + ']' + RS
attempt = G + '[' + W + '+' + G + ']' + RS
sleep_msg = G + '[' + W + '*' + G + ']' + RS
error = G + '[' + R + '!' + G + ']' + RS

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

def update_list(lst, temp_lst):
    """Update list by removing processed items"""
    count = len(temp_lst)
    del lst[:count]
    return lst

def add_members():
    """Main function to add members to group"""
    # Check arguments
    if len(sys.argv) < 6:
        print(f"{error}{R} Usage: python adder.py <api_id> <api_hash> <phone> <csv_file> <group>{RS}")
        print(f"{info}{G} Or run main_adder.py for automated multi-account adding{RS}")
        sys.exit(1)
    
    utils.clear_screen()
    utils.banner()
    
    # Parse arguments
    try:
        api_id = int(sys.argv[1])
        api_hash = str(sys.argv[2])
        phone = str(sys.argv[3])
        file = str(sys.argv[4])
        group = str(sys.argv[5])
    except ValueError:
        print(f"{error}{R} Invalid arguments provided.{RS}")
        sys.exit(1)
    
    # Check if file exists
    if not os.path.exists(file):
        print(f"{error}{R} CSV file not found: {file}{RS}")
        sys.exit(1)
    
    # Load users from CSV
    users = []
    try:
        with open(file, 'r', encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=',', lineterminator='\n')
            next(rows, None)  # Skip header
            for row in rows:
                if len(row) < 5: continue
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
        if not client.is_user_authorized():
             print(f'{error}{R} Client {phone} is not authorized. Run manager.py to authorize.{RS}')
             sys.exit(1)

        time.sleep(1.5)
        
        # Get target group
        try:
            target_group = client.get_entity(group)
            entity = InputPeerChannel(target_group.id, target_group.access_hash)
            group_name = target_group.title
        except Exception as e:
            print(f'{error}{R} Could not get target group: {e}{RS}')
            sys.exit(1)
        
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
                    # print(f'{info}{G} Skipped user {user["user_id"]} (no username){RS}')
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
                if len(users) > 0:
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
        print(f'\n{utils.success}{G} Addition complete!{RS}')
        print(f'{info}{G} Successfully added: {success_count}{RS}')
        print(f'{info}{G} Failed: {failed_count}{RS}')
        
        client.disconnect()
        
        time.sleep(2)
        
    except Exception as e:
        print(f'\n{error}{R} Fatal error: {e}{RS}')
        if 'client' in locals():
            client.disconnect()
        sys.exit(1)


if __name__ == '__main__':
    add_members()
