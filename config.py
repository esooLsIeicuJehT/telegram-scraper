"""
Configuration file for Telegram Scraper and Adder
"""

# Delay settings (in seconds)
ADD_MEMBER_DELAY = 30
BATCH_DELAY = 120
SCRAPE_DELAY = 3

# Batch settings
MEMBERS_PER_ACCOUNT = 60
ADD_BATCH_SIZE = 50

# File paths
SESSIONS_DIR = "sessions"
MEMBERS_DIR = "members"
DATA_DIR = "data"
DATA_FILE = "data/vars.txt"
TARGET_GROUP_FILE = "data/target_grp.txt"

# Telegram API limits
MAX_RETRIES = 3
TIMEOUT = 30