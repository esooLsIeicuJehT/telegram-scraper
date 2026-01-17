# Usage Examples - Telegram Scraper and Member Adder

This document provides detailed examples of common use cases for the Telegram Scraper and Member Adder.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Scraping Examples](#scraping-examples)
3. [Adding Members Examples](#adding-members-examples)
4. [Multi-Account Scenarios](#multi-account-scenarios)
5. [Advanced Usage](#advanced-usage)

## Basic Setup

### Example 1: Adding Your First Account

```bash
python manager.py
```

**Output:**
```
Enter your choice: 1

Enter API ID: 1234567
Enter API Hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Enter Phone Number: +1234567890

Do you want to add more accounts?[y/n]: n

[*] Logging in from new accounts...

[+] Logged in - +1234567890

Press enter to goto main menu...
```

### Example 2: Adding Multiple Accounts at Once

```bash
python manager.py
```

Follow the prompts to add accounts one by one:

```
Enter API ID: 1234567
Enter API Hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Enter Phone Number: +1234567890

Do you want to add more accounts?[y/n]: y

Enter API ID: 2345678
Enter API Hash: b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7
Enter Phone Number: +1987654321

Do you want to add more accounts?[y/n]: n
```

## Scraping Examples

### Example 3: Scraping All Members from a Group

```bash
python scraper.py
```

**Output:**
```
Choose an account to scrape members

(0) +1234567890
(1) +1987654321

Enter choice: 0

Enter the name of the group without the @: TechCommunity

How would you like to obtain the users?

[0] All users
[1] Active Users(online today and yesterday)
[2] Users active in the last week
[3] Users active in the last month
[4] Non-active users(not active in the last month)

Your choice: 0

Starting member scraping...

5000/5000
Total members saved: 4850

Users saved in the CSV file.

[+] Scraping complete!
```

### Example 4: Scraping Only Active Users

```bash
python scraper.py
```

Select option `[1] Active Users(online today and yesterday)`:

```
Your choice: 1

Starting member scraping...

5000/5000
Total members saved: 1250

Users saved in the CSV file.

[+] Scraping complete!
```

This is useful because active users are more likely to join your group.

### Example 5: Scraping Non-Active Users

```bash
python scraper.py
```

Select option `[4] Non-active users(not active in the last month)`:

```
Your choice: 4

Starting member scraping...

5000/5000
Total members saved: 3600

Users saved in the CSV file.

[+] Scraping complete!
```

### Example 6: Scraping Admins Separately

```bash
python scraper.py
```

When prompted:

```
Would you like to have admins on a separate CSV file? [y/n] y

Scraping admins...

[+] Scraped 5 admins

Starting member scraping...
```

This creates two files:
- `members/admins.csv` - Contains only admins
- `members/members.csv` - Contains all other members

## Adding Members Examples

### Example 7: Adding Members with Single Account (Manual)

```bash
python adder.py 1234567 a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 +1234567890 members/members.csv MyGroup
```

**Output:**
```
[+] Adding members to My Group

[i] Total users to add: 5000

[+] Added 123456 (1/5000)
[*] Sleep 30s
[+] Added 234567 (2/5000)
[*] Sleep 30s
...

[+] Addition complete!
[i] Successfully added: 4850
[i] Failed: 150
```

### Example 8: Automated Multi-Account Adding (Windows)

```bash
python main_adder.py
```

**Output:**
```
Total accounts: 5
If you have more than 10 accounts then it is recommended to use 10 at a time

Enter number of accounts to use: 3

Distributing CSV files...
[+] CSV file distribution complete

This will be fully automated.
Don't touch the keyboard until cmd window pop-up stops

Press enter to continue...

Launching from 3 accounts...

5
4
3
2
1

[+] Launched from +1234567890
[+] Launched from +1987654321
[+] Launched from +1555555555
```

This automatically opens 3 command windows, each running the adder with a different account.

### Example 9: Manual Multi-Account Adding (Linux/Mac)

First, run the distributor:

```bash
python main_adder.py
```

After distribution (before pressing enter), you'll see manual commands:

```
Note: Full automation supports only Windows systems
On Linux/Mac, you will need to manually run adder.py for each account

Commands to run manually:
  python adder.py 1234567 a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 +1234567890 members/members0.csv MyGroup
  python adder.py 2345678 b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7 +1987654321 members/members1.csv MyGroup
  python adder.py 3456789 c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8 +1555555555 members/members2.csv MyGroup
```

Open multiple terminal windows and run each command in a separate window.

## Multi-Account Scenarios

### Example 10: Scraping from One Group, Adding to Multiple Groups

```bash
# Step 1: Scrape members once
python scraper.py
# Select: TechCommunity -> Option 1 (Active Users)

# Step 2: Add to first group
python main_adder.py
# Enter: MyGroup1

# Step 3: Add to second group (repeat with remaining users)
python main_adder.py
# Enter: MyGroup2
```

### Example 11: Scraping from Multiple Groups, Adding to One Group

```bash
# Step 1: Scrape from first group
python scraper.py
# Select: GroupA -> Option 1
# Rename output file:
mv members/members.csv members/members_groupA.csv

# Step 2: Scrape from second group
python scraper.py
# Select: GroupB -> Option 1
# Rename output file:
mv members/members.csv members/members_groupB.csv

# Step 3: Combine files
cat members/members_groupA.csv members/members_groupB.csv > members/members_combined.csv
# Remove duplicate headers (you'll have one extra header line)

# Step 4: Add combined members
python main_adder.py
```

### Example 12: Rotating Accounts to Avoid Flood Errors

```bash
# Day 1: Use accounts 1-3
python manager.py
# Choose [4] Delete specific accounts
# Temporarily remove accounts 4-5

python main_adder.py
# Use 3 accounts

# Day 2: Use accounts 4-5
python manager.py
# Choose [4] Delete specific accounts
# Temporarily remove accounts 1-3

python main_adder.py
# Use 2 accounts
```

## Advanced Usage

### Example 13: Customizing Delays in config.py

Edit `config.py`:

```python
# For faster adding (higher risk)
ADD_MEMBER_DELAY = 15      # Reduced from 30
BATCH_DELAY = 60           # Reduced from 120

# For safer adding (lower risk)
ADD_MEMBER_DELAY = 45      # Increased from 30
BATCH_DELAY = 180          # Increased from 120

# For scraping large groups
SCRAPE_DELAY = 5           # Increased from 3
```

### Example 14: Filtering and Removing Banned Accounts

```bash
python manager.py
```

Choose `[2] Filter all banned accounts`:

```
[i] Choose an account to delete

[0] +1234567890
[1] +1987654321
[2] +1555555555

Enter a choice: 2

[+] Account Deleted
Press enter to goto main menu
```

### Example 15: Listing All Accounts

```bash
python manager.py
```

Choose `[3] List out all the accounts`:

```
API ID          |            API Hash              |    Phone Number
======================================================================
1234567         | a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6  | +1234567890
2345678         | b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7  | +1987654321
3456789         | c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8  | +1555555555
======================================================================

Press enter to goto main menu
```

### Example 16: Handling Errors During Adding

**Peer Flood Error:**
```
[!] Peer Flood Error - Account may be temporarily blocked
[i] Logging remaining users to file
[i] Remaining 2500 users saved to members/members0.csv
```

**Solution:** Wait 24-48 hours, then continue with the remaining file.

**User Privacy Restriction:**
```
[!] User Privacy Restriction - username_xyz
```

**Solution:** These users are automatically skipped. Continue running.

### Example 17: Checking Scraped Data

View the CSV file:

```bash
# On Linux/Mac
cat members/members.csv | head -10

# On Windows
type members\members.csv | more
```

**Output format:**
```csv
username,user id,access hash,group,group id,status
johndoe,123456789,987654321,TechCommunity,1234567890,UserStatusOnline
janedoe,234567890,876543210,TechCommunity,1234567890,UserStatusOffline
```

### Example 18: Resuming Interrupted Adding

If the adder was interrupted:

```bash
# Check remaining users in the CSV file
python main_adder.py
# The script will show remaining users and continue from where it left off
```

### Example 19: Using Different Filtering Strategies

**Strategy 1: Quality over Quantity**
```bash
python scraper.py
# Choose: Option 1 (Active Users)
# Result: Fewer members, but higher join rate
```

**Strategy 2: Quantity over Quality**
```bash
python scraper.py
# Choose: Option 0 (All Users)
# Result: More members, but lower join rate
```

**Strategy 3: Balanced Approach**
```bash
python scraper.py
# Choose: Option 2 (Last Week) or Option 3 (Last Month)
# Result: Balance between active and inactive users
```

## Troubleshooting Examples

### Example 20: Fixing Session Issues

If you get authentication errors:

```bash
# Delete session files
rm sessions/*.session
# On Windows: del sessions\*.session

# Re-authenticate
python manager.py
# Choose [2] Filter all banned accounts
# Enter codes for each account
```

### Example 21: Dealing with Flood Waits

If you hit flood limits repeatedly:

1. **Increase delays in config.py:**
```python
ADD_MEMBER_DELAY = 60      # Double the delay
BATCH_DELAY = 300          # 5 minutes instead of 2
```

2. **Use more accounts:**
```bash
python manager.py
# Add 5-10 accounts instead of 2-3
```

3. **Space out operations:**
```bash
# Run in morning
python main_adder.py

# Run again in evening
python main_adder.py
```

## Best Practices Examples

### Example 22: Daily Routine for Safe Adding

```bash
# Morning: Add 100 members with 3 accounts
python main_adder.py
# Select: 3 accounts

# Afternoon: Check results
# Review any errors or flood messages

# Evening: Add another 100 members
python main_adder.py
# Select: 3 accounts
```

### Example 23: Weekly Account Rotation

```bash
# Week 1: Use accounts 1-3
python manager.py
# Only use accounts 1, 2, 3

# Week 2: Use accounts 4-6
python manager.py
# Only use accounts 4, 5, 6

# Week 3: Use accounts 1-3 again
# This gives accounts time to recover from any rate limits
```

### Example 24: Monitoring Progress

```bash
# Terminal 1: Run adder
python adder.py 1234567 hash +1234567890 members/members0.csv MyGroup

# Terminal 2: Monitor progress
watch -n 10 'wc -l members/members0.csv'
```

---

**Note:** These examples assume you have valid API credentials and Telegram accounts. Always start with small batches to test your setup before scaling up.