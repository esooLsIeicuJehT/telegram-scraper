# Telegram Scraper and Member Adder

An enhanced Python tool for scraping Telegram group members and adding them to other groups using multiple accounts. Based on [DenizShabani/telegramscraper](https://github.com/DenizShabani/telegramscraper) with improvements and bug fixes.

## Features

- **Multi-Account Support**: Use multiple Telegram accounts simultaneously
- **Member Scraping**: Extract members from Telegram groups with various filters
- **Member Adding**: Add scraped members to target groups via username
- **Account Management**: Add, filter, and manage multiple accounts
- **Rate Limiting**: Built-in delays to prevent account bans
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **CSV Export**: Export member data to CSV format

## Requirements

- Python 3.7 or higher
- Telegram API credentials (api_id and api_hash)
- Telegram accounts (phone numbers)

## Installation

1. Clone or download this repository:
```bash
cd telegram_scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Getting Telegram API Credentials

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Sign in with your phone number
3. Navigate to "API development tools"
4. Fill in the form to create a new application
5. Save your `api_id` and `api_hash`

## Usage

### Step 1: Add Accounts

Run the account manager to add your Telegram accounts:

```bash
python manager.py
```

Choose option `[1] Add new accounts` and enter:
- API ID
- API Hash
- Phone Number (with country code, e.g., +1234567890)

You'll receive a verification code on Telegram for each account. Enter it when prompted.

**Note**: It's recommended to use multiple accounts to distribute the load and avoid rate limits.

### Step 2: Scrape Members

Run the scraper to extract members from a target group:

```bash
python scraper.py
```

You'll be prompted to:
1. Choose which account to use for scraping
2. Enter the group name (without @)
3. Select filtering options:
   - All users
   - Active users (online today/yesterday)
   - Users active in the last week
   - Users active in the last month
   - Non-active users (not active in the last month)

Scraped members will be saved to `members/members.csv`

### Step 3: Add Members

#### Option A: Automated Multi-Account Adding (Windows)

Run the main adder to automate the process across multiple accounts:

```bash
python main_adder.py
```

This will:
1. Join the target group from all accounts
2. Distribute scraped members among accounts
3. Automatically launch adder instances for each account (Windows only)

#### Option B: Manual Adding (Linux/Mac or Windows)

Run the adder manually for a specific account:

```bash
python adder.py <api_id> <api_hash> <phone> <csv_file> <target_group>
```

Example:
```bash
python adder.py 12345 abcdef1234567890 +1234567890 members/members0.csv mygroup
```

## Configuration

Edit `config.py` to customize settings:

```python
# Delay settings (in seconds)
ADD_MEMBER_DELAY = 30      # Delay between adding each member
BATCH_DELAY = 120          # Delay after adding a batch of 50 members
SCRAPE_DELAY = 3           # Delay during scraping

# Batch settings
MEMBERS_PER_ACCOUNT = 60   # Members to assign to each account
ADD_BATCH_SIZE = 50        # Batch size for adding members
```

## File Structure

```
telegram_scraper/
├── manager.py          # Account management
├── scraper.py          # Member scraping
├── adder.py            # Single account member adding
├── main_adder.py       # Multi-account orchestrator
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── sessions/           # Telegram session files (auto-created)
├── members/            # Scraped member data (auto-created)
│   ├── members.csv
│   └── admins.csv
└── data/               # Account data (auto-created)
    ├── vars.txt
    └── target_grp.txt
```

## Important Notes

### Rate Limiting
- Telegram has strict rate limits to prevent spam
- Default delays are configured to be safe, but you may need to adjust based on your situation
- Using multiple accounts helps distribute the load

### Account Safety
- Use accounts that you own or have permission to use
- Adding too many members quickly can result in temporary account restrictions
- Start with conservative settings and monitor results
- Consider using newer accounts with less activity history

### Filtering Options
- **All users**: Scrapes every member (may include inactive/bot accounts)
- **Active users**: Most likely to accept invitations and engage
- **Non-active users**: Less likely to join or be active

### Privacy Settings
- Some users have privacy settings that prevent being added to groups
- These users will be skipped during the adding process
- The scraper still collects their data, but they won't be added

### Platform Differences
- **Windows**: Full automation support with multiple command windows
- **Linux/Mac**: Manual execution required for each account
- Commands are provided for manual execution on all platforms

## Troubleshooting

### "No accounts found!"
- Run `python manager.py` and add accounts first

### "Account is banned!"
- Use option `[2] Filter all banned accounts` in manager.py
- Remove banned accounts and add new ones

### "Peer Flood Error"
- Account has hit Telegram's rate limits
- Wait 24-48 hours before trying again
- Increase delays in config.py
- Use different accounts

### "User Privacy Restriction"
- User has privacy settings preventing group additions
- These users are automatically skipped
- This is normal behavior

### Session Issues
- Delete the session file from `sessions/` directory
- Re-authenticate the account using manager.py

## Best Practices

1. **Start Small**: Test with a few members first
2. **Use Multiple Accounts**: Distribute load across accounts
3. **Monitor Progress**: Watch for errors and adjust settings
4. **Respect Privacy**: Only add users who would likely want to join
5. **Stay Within Limits**: Don't abuse the system or you'll get banned
6. **Backup Data**: Keep copies of your CSV files
7. **Update Regularly**: Keep dependencies updated

## Legal and Ethical Considerations

- Only use accounts you own or have explicit permission to use
- Respect Telegram's Terms of Service
- Be aware that aggressive adding can result in account bans
- Consider the privacy and consent of the users you're adding
- This tool is for educational purposes and legitimate use cases

## Credits

- Original project: [DenizShabani/telegramscraper](https://github.com/DenizShabani/telegramscraper)
- Enhanced and improved by SuperNinja
- Built with Telethon library

## License

This project is provided as-is for educational purposes. Use responsibly and at your own risk.

## Support

For issues, questions, or contributions:
- Check the troubleshooting section first
- Review the original repository for additional context
- Ensure you have valid API credentials and accounts

---

**DISCLAIMER**: This tool is for educational purposes only. Users are responsible for ensuring their use complies with Telegram's Terms of Service and applicable laws. The authors are not responsible for any misuse or account bans resulting from using this tool.