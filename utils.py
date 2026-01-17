import os
import sys
import json
import pickle
import random
import config
from colorama import init, Fore

# Initialize colorama
init()

# Colors
R = Fore.RED
G = Fore.GREEN
LG = Fore.LIGHTGREEN_EX
W = Fore.WHITE
CY = Fore.CYAN
YE = Fore.YELLOW
RS = Fore.RESET

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
        print(f'{R}   Multi-Account Tool Version: 1.1 {R}| Enhanced by SuperNinja{RS}')
    except ImportError:
        print(f'{LG}Multi-Account Tool V1.1{RS}\n')

def clear_screen():
    """Clear terminal screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_accounts():
    """Load accounts from JSON, migrating from pickle if necessary"""
    json_file = os.path.join(config.DATA_DIR, 'accounts.json')
    pickle_file = config.DATA_FILE # data/vars.txt

    # Ensure data directory exists
    os.makedirs(config.DATA_DIR, exist_ok=True)

    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{error} Error decoding {json_file}. Returning empty list.")
            return []

    # Migration path
    if os.path.exists(pickle_file):
        print(f"{info} Migrating accounts from {pickle_file} to {json_file}...")
        accounts = []
        try:
            with open(pickle_file, 'rb') as f:
                while True:
                    try:
                        accounts.append(pickle.load(f))
                    except EOFError:
                        break
        except Exception as e:
            print(f"{error} Error reading pickle file: {e}")
            return []

        # Save as JSON
        save_accounts(accounts)

        # Rename old file to .bak
        try:
            os.rename(pickle_file, pickle_file + '.bak')
            print(f"{success} Migration complete. Old file renamed to {pickle_file}.bak")
        except OSError as e:
            print(f"{error} Could not rename old file: {e}")

        return accounts

    return []

def save_accounts(accounts):
    """Save accounts to JSON"""
    json_file = os.path.join(config.DATA_DIR, 'accounts.json')
    os.makedirs(config.DATA_DIR, exist_ok=True)
    with open(json_file, 'w') as f:
        json.dump(accounts, f, indent=4)
