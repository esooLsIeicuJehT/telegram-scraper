"""
Account Manager - Add, filter, and manage Telegram accounts
"""

import pickle
import pyfiglet
from colorama import init, Fore
import os
import random
from time import sleep
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import config

# Initialize colorama
init()

# Color constants
LG = Fore.LIGHTGREEN_EX
W = Fore.WHITE
CY = Fore.CYAN
YE = Fore.YELLOW
R = Fore.RED
N = Fore.RESET

colors = [LG, R, W, CY, YE]


def banner():
    """Display banner"""
    f = pyfiglet.Figlet(font='slant')
    banner_text = f.renderText('Telegram')
    print(f'{random.choice(colors)}{banner_text}{N}')
    print(R + '  Enhanced Version: 1.0 | Based on DenizShabani/telegramscraper' + N + '\n')


def clear_screen():
    """Clear terminal screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def add_accounts():
    """Add new accounts to vars.txt"""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    with open(config.DATA_FILE, 'ab') as g:
        newly_added = []
        while True:
            try:
                a = int(input(f'\n{LG}Enter API ID: {R}'))
                b = str(input(f'{LG}Enter API Hash: {R}'))
                c = str(input(f'{LG}Enter Phone Number (with country code): {R}'))
                p = ''.join(c.split())
                pickle.dump([a, b, p], g)
                newly_added.append([a, b, p])
                ab = input(f'\nDo you want to add more accounts? [y/n]: ')
                if 'y' not in ab.lower():
                    print(f'\n{LG}[i] Saved all accounts in {config.DATA_FILE}{N}')
                    g.close()
                    sleep(3)
                    clear_screen()
                    print(f'{LG}[*] Logging in from new accounts...\n')
                    
                    for added in newly_added:
                        os.makedirs(config.SESSIONS_DIR, exist_ok=True)
                        c = TelegramClient(f'{config.SESSIONS_DIR}/{added[2]}', added[0], added[1])
                        try:
                            c.start()
                            print(f'\n{LG}[+] Logged in - {added[2]}')
                            c.disconnect()
                        except PhoneNumberBannedError:
                            print(f'{R}[!] {added[2]} is banned! Filter it using option 2')
                            continue
                        except Exception as e:
                            print(f'{R}[!] Error logging in {added[2]}: {e}')
                            continue
                        print('\n')
                    
                    input(f'\n{LG}Press enter to goto main menu...')
                    break
            except ValueError:
                print(f'{R}[!] Invalid input! Please enter a valid number for API ID.')
                continue


def filter_banned_accounts():
    """Filter and remove banned accounts"""
    accounts = []
    banned_accs = []
    
    if not os.path.exists(config.DATA_FILE):
        print(f'{R}[!] No accounts file found! Please add accounts first.{N}')
        sleep(3)
        return
    
    h = open(config.DATA_FILE, 'rb')
    while True:
        try:
            accounts.append(pickle.load(h))
        except EOFError:
            break
    h.close()
    
    if len(accounts) == 0:
        print(f'{R}[!] There are no accounts! Please add some and retry')
        sleep(3)
    else:
        for account in accounts:
            api_id = int(account[0])
            api_hash = str(account[1])
            phone = str(account[2])
            session_path = f'{config.SESSIONS_DIR}/{phone}'
            client = TelegramClient(session_path, api_id, api_hash)
            client.connect()
            
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    code = input(f'[+] Enter the code for {phone}: ')
                    client.sign_in(phone, code)
                except PhoneNumberBannedError:
                    print(f'{R}{phone} is banned!{N}')
                    banned_accs.append(account)
                except Exception as e:
                    print(f'{R}[!] Error checking {phone}: {e}{N}')
            else:
                print(f'{LG}[+] {phone} is active{N}')
            
            client.disconnect()
        
        if len(banned_accs) == 0:
            print(f'{LG}Congrats! No banned accounts')
            input('\nPress enter to goto main menu')
        else:
            for m in banned_accs:
                if m in accounts:
                    accounts.remove(m)
            
            with open(config.DATA_FILE, 'wb') as k:
                for a in accounts:
                    Id = a[0]
                    Hash = a[1]
                    Phone = a[2]
                    pickle.dump([Id, Hash, Phone], k)
            k.close()
            print(f'{LG}[i] All banned accounts removed{N}')
            input('\nPress enter to goto main menu')


def list_accounts():
    """List all accounts"""
    display = []
    
    if not os.path.exists(config.DATA_FILE):
        print(f'{R}[!] No accounts file found! Please add accounts first.{N}')
        sleep(3)
        return
    
    j = open(config.DATA_FILE, 'rb')
    while True:
        try:
            display.append(pickle.load(j))
        except EOFError:
            break
    j.close()
    
    print(f'\n{LG}')
    print(f'{"API ID":<15} | {"API Hash":<35} | {"Phone Number"}')
    print('=' * 70)
    for z in display:
        print(f'{z[0]:<15} | {z[1]:<35} | {z[2]}')
    print('=' * 70)
    input('\nPress enter to goto main menu')


def delete_account():
    """Delete a specific account"""
    if not os.path.exists(config.DATA_FILE):
        print(f'{R}[!] No accounts file found! Please add accounts first.{N}')
        sleep(3)
        return
    
    accs = []
    f = open(config.DATA_FILE, 'rb')
    while True:
        try:
            accs.append(pickle.load(f))
        except EOFError:
            break
    f.close()
    
    i = 0
    print(f'\n{LG}[i] Choose an account to delete\n')
    for acc in accs:
        print(f'{LG}[{i}] {acc[2]}{N}')
        i += 1
    
    try:
        index = int(input(f'\n{LG}[+] Enter a choice: {N}'))
        if index < 0 or index >= len(accs):
            print(f'{R}[!] Invalid choice!{N}')
            sleep(2)
            return
        
        phone = str(accs[index][2])
        session_file = f'{config.SESSIONS_DIR}/{phone}.session'
        
        # Remove session file if it exists
        if os.path.exists(session_file):
            os.remove(session_file)
        
        del accs[index]
        
        f = open(config.DATA_FILE, 'wb')
        for account in accs:
            pickle.dump(account, f)
        f.close()
        
        print(f'\n{LG}[+] Account Deleted{N}')
        input(f'{LG}Press enter to goto main menu{N}')
    except ValueError:
        print(f'{R}[!] Invalid input!{N}')
        sleep(2)


def main():
    """Main menu loop"""
    while True:
        clear_screen()
        banner()
        print(f'{LG}[1] Add new accounts{N}')
        print(f'{LG}[2] Filter all banned accounts{N}')
        print(f'{LG}[3] List out all the accounts{N}')
        print(f'{LG}[4] Delete specific accounts{N}')
        print(f'{LG}[5] Quit{N}')
        
        try:
            a = int(input(f'\nEnter your choice: {R}'))
            
            if a == 1:
                add_accounts()
            elif a == 2:
                filter_banned_accounts()
            elif a == 3:
                list_accounts()
            elif a == 4:
                delete_account()
            elif a == 5:
                clear_screen()
                banner()
                print(f'{LG}Goodbye!{N}')
                break
            else:
                print(f'{R}[!] Invalid choice! Please try again.{N}')
                sleep(2)
        except ValueError:
            print(f'{R}[!] Invalid input! Please enter a number.{N}')
            sleep(2)


if __name__ == '__main__':
    main()