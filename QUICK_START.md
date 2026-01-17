# Quick Start Guide - Telegram Scraper and Member Adder

## Prerequisites
- Python 3.7+ installed
- Telegram API credentials (get from https://my.telegram.org)
- At least one Telegram account

## Setup (5 minutes)

### 1. Install Dependencies
```bash
cd telegram_scraper
pip install -r requirements.txt
```

### 2. Add Your First Account
```bash
python manager.py
```
- Choose `[1] Add new accounts`
- Enter API ID, API Hash, and phone number
- Enter verification code from Telegram

### 3. Scrape Members
```bash
python scraper.py
```
- Select your account
- Enter target group name (without @)
- Choose filtering option (e.g., `1` for active users)
- Members saved to `members/members.csv`

### 4. Add Members

#### Windows (Automated):
```bash
python main_adder.py
```
- Enter target group name
- Select number of accounts to use
- Watch the automation run

#### Linux/Mac (Manual):
```bash
python adder.py <api_id> <api_hash> <phone> members/members.csv <target_group>
```

## Common Commands

```bash
# Add more accounts
python manager.py

# Check account status
python manager.py
# Choose [3] List out all accounts

# Remove banned accounts
python manager.py
# Choose [2] Filter all banned accounts

# Scrape from different group
python scraper.py

# Add to different group
python main_adder.py
```

## Tips

1. **Use Multiple Accounts**: Add 3-5 accounts to distribute load
2. **Start Small**: Test with 10-20 members first
3. **Be Patient**: The scraper and adder have built-in delays to prevent bans
4. **Monitor Progress**: Watch the console output for any errors
5. **Adjust Settings**: Edit `config.py` if you need to change delays

## Example Workflow

```bash
# Day 1: Setup and test
python manager.py           # Add 2 accounts
python scraper.py           # Scrape from a large group
python main_adder.py        # Add 50 members to test group

# Day 2: Scale up (if no issues)
python scraper.py           # Scrape more members
python main_adder.py        # Add more members

# Day 3: Add more accounts
python manager.py           # Add 3 more accounts
python main_adder.py        # Use all 5 accounts
```

## Troubleshooting Quick Fixes

**"Account is banned!"**
```bash
python manager.py
# Choose [2] Filter all banned accounts
```

**"Peer Flood Error"**
- Wait 24-48 hours
- Increase `ADD_MEMBER_DELAY` in `config.py`

**"No members file found"**
```bash
python scraper.py
# Scrape members first
```

**Session issues:**
```bash
# Delete session files
rm sessions/*.session
# Re-authenticate with manager.py
python manager.py
```

## Safety Checklist

- [ ] Have valid API credentials
- [ ] Added at least 2-3 accounts
- [ ] Tested with small batch first
- [ ] Understand rate limiting delays
- [ ] Ready to monitor progress
- [ ] Have target group ready

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Adjust settings in [config.py](config.py)
- Review account management options
- Understand filtering options for scraping

---

**Need Help?** Check the full README.md for detailed documentation and troubleshooting.