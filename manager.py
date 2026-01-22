"""
Account Manager - Add, filter, and manage Telegram accounts
"""

import os
import time
import asyncio
from telethon.sync import TelegramClient
from telethon import TelegramClient as AsyncTelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import config
import utils

# Use colors and symbols from utils
LG = utils.LG
R = utils.R
W = utils.W
CY = utils.CY
info = utils.info
error = utils.error
success = utils.success

async def check_account_status(account):
    """Check single account status asynchronously"""
    api_id = int(account[0])
    api_hash = str(account[1])
    phone = str(account[2])
    session_path = f'{config.SESSIONS_DIR}/{phone}'

    client = AsyncTelegramClient(session_path, api_id, api_hash)

    status = "ERROR"
    try:
        await client.connect()
        if not await client.is_user_authorized():
            status = "UNAUTHORIZED"
        else:
            status = "ACTIVE"
    except PhoneNumberBannedError:
        status = "BANNED"
    except Exception as e:
        status = f"ERROR:{str(e)}"
    finally:
        await client.disconnect()

    return account, status

async def check_all_accounts_parallel(accounts):
    """Check all accounts in parallel"""
    tasks = [check_account_status(acc) for acc in accounts]
    return await asyncio.gather(*tasks)

def add_accounts():
    """Add new accounts"""
    accounts = utils.load_accounts()
    
    newly_added = []
    while True:
        try:
            a = int(input(f'\n{LG}Enter API ID: {R}'))
            b = str(input(f'{LG}Enter API Hash: {R}'))
            c = str(input(f'{LG}Enter Phone Number (with country code): {R}'))
            p = ''.join(c.split())

            # Check if account already exists
            exists = False
            for acc in accounts:
                if acc[2] == p:
                    print(f'{error} Account {p} already exists!')
                    exists = True
                    break

            if not exists:
                account = [a, b, p]
                accounts.append(account)
                utils.save_accounts(accounts)
                newly_added.append(account)
                print(f'{success} Account saved!')

            ab = input(f'\nDo you want to add more accounts? [y/n]: ')
            if 'y' not in ab.lower():
                print(f'\n{info} Saved all accounts')
                time.sleep(1)
                utils.clear_screen()
                print(f'{info} Logging in from new accounts...\n')

                os.makedirs(config.SESSIONS_DIR, exist_ok=True)

                # Check status of all new accounts in parallel
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    results = loop.run_until_complete(check_all_accounts_parallel(newly_added))
                finally:
                    loop.close()

                unauthorized_accs = []

                for account, status in results:
                    phone = account[2]
                    if status == "ACTIVE":
                        print(f'\n{success} Logged in - {phone}')
                        print('\n')
                    elif status == "BANNED":
                        print(f'{error} {phone} is banned! Filter it using option 2')
                        print('\n')
                    elif status == "UNAUTHORIZED":
                        unauthorized_accs.append(account)
                    else:
                        print(f'{error} Error logging in {phone}: {status}')
                        print('\n')

                # Process unauthorized accounts sequentially
                for added in unauthorized_accs:
                    c = TelegramClient(f'{config.SESSIONS_DIR}/{added[2]}', added[0], added[1])
                    try:
                        c.start()
                        print(f'\n{success} Logged in - {added[2]}')
                        c.disconnect()
                    except PhoneNumberBannedError:
                        print(f'{error} {added[2]} is banned! Filter it using option 2')
                        continue
                    except Exception as e:
                        print(f'{error} Error logging in {added[2]}: {e}')
                        continue
                    print('\n')

                input(f'\n{LG}Press enter to go to main menu...')
                break
        except ValueError:
            print(f'{error} Invalid input! Please enter a valid number for API ID.')
            continue

def filter_banned_accounts():
    """Filter and remove banned accounts"""
    accounts = utils.load_accounts()
    banned_accs = []
    
    if not accounts:
        print(f'{error} No accounts found! Please add accounts first.')
        time.sleep(3)
        return
    
    print(f'{info} Checking accounts status...')

    # Run async checks
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(check_all_accounts_parallel(accounts))
    finally:
        loop.close()

    unauthorized_accs = []

    for account, status in results:
        phone = account[2]
        if status == "ACTIVE":
             print(f'{success} {phone} is active')
        elif status == "BANNED":
             print(f'{error} {phone} is banned!')
             banned_accs.append(account)
        elif status == "UNAUTHORIZED":
             unauthorized_accs.append(account)
        else:
             print(f'{error} Error checking {phone}: {status}')

    # Handle unauthorized accounts sequentially (interactive)
    for account in unauthorized_accs:
        api_id = int(account[0])
        api_hash = str(account[1])
        phone = str(account[2])
        session_path = f'{config.SESSIONS_DIR}/{phone}'

        # Use sync client for interaction
        client = TelegramClient(session_path, api_id, api_hash)
        try:
            client.connect()
            
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    code = input(f'{utils.plus} Enter the code for {phone}: ')
                    client.sign_in(phone, code)
                except PhoneNumberBannedError:
                    print(f'{error} {phone} is banned!')
                    banned_accs.append(account)
                except Exception as e:
                    print(f'{error} Error checking {phone}: {e}')
            else:
                print(f'{success} {phone} is active')
        except Exception as e:
             print(f'{error} Error connecting {phone}: {e}')
        finally:
             client.disconnect()

    if not banned_accs:
        print(f'{success} Congrats! No banned accounts')
    else:
        for m in banned_accs:
            if m in accounts:
                accounts.remove(m)
        
        utils.save_accounts(accounts)
        print(f'{info} All banned accounts removed')

    input('\nPress enter to go to main menu')

def list_accounts():
    """List all accounts"""
    accounts = utils.load_accounts()
    
    if not accounts:
        print(f'{error} No accounts found! Please add accounts first.')
        time.sleep(3)
        return
    
    print(f'\n{LG}')
    print(f'{"API ID":<15} | {"API Hash":<35} | {"Phone Number"}')
    print('=' * 70)
    for z in accounts:
        print(f'{z[0]:<15} | {z[1]:<35} | {z[2]}')
    print('=' * 70)
    input('\nPress enter to go to main menu')

def delete_account():
    """Delete a specific account"""
    accounts = utils.load_accounts()
    
    if not accounts:
        print(f'{error} No accounts found! Please add accounts first.')
        time.sleep(3)
        return
    
    print(f'\n{info} Choose an account to delete\n')
    for i, acc in enumerate(accounts):
        print(f'{LG}[{i}] {acc[2]}')
    
    try:
        index = int(input(f'\n{utils.plus} Enter a choice: {utils.RS}'))
        if index < 0 or index >= len(accounts):
            print(f'{error} Invalid choice!')
            time.sleep(2)
            return
        
        phone = str(accounts[index][2])
        session_file = f'{config.SESSIONS_DIR}/{phone}.session'
        
        # Remove session file if it exists
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
            except OSError as e:
                print(f"{error} Could not delete session file: {e}")
        
        del accounts[index]
        
        utils.save_accounts(accounts)
        
        print(f'\n{success} Account Deleted')
        input(f'{LG}Press enter to go to main menu')
    except ValueError:
        print(f'{error} Invalid input!')
        time.sleep(2)

def main():
    """Main menu loop"""
    menu_options = {
        1: add_accounts,
        2: filter_banned_accounts,
        3: list_accounts,
        4: delete_account,
    }

    while True:
        utils.clear_screen()
        utils.banner()
        print(f'{LG}[1] Add new accounts{utils.RS}')
        print(f'{LG}[2] Filter all banned accounts{utils.RS}')
        print(f'{LG}[3] List out all the accounts{utils.RS}')
        print(f'{LG}[4] Delete specific accounts{utils.RS}')
        print(f'{LG}[5] Quit{utils.RS}')

        try:
            choice_str = input(f'\nEnter your choice: {R}')
            if not choice_str.isdigit():
                print(f'{error} Invalid choice! Please try again.')
                time.sleep(2)
                continue

            choice = int(choice_str)

            if choice == 5:
                utils.clear_screen()
                utils.banner()
                print(f'{LG}Goodbye!{utils.RS}')
                break

            action = menu_options.get(choice)
            if action:
                action()
            else:
                print(f'{error} Invalid choice! Please try again.')
                time.sleep(2)
        except ValueError:
            print(f'{error} Invalid input! Please enter a number.')
            time.sleep(2)


if __name__ == '__main__':
    main()
