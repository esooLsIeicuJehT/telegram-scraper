# Installation Guide - Telegram Scraper and Member Adder

## Prerequisites

Before installing this tool, ensure you have:

- **Python 3.7 or higher** installed
- **pip** (Python package manager)
- **Telegram accounts** (phone numbers)
- **Telegram API credentials** (api_id and api_hash)

## Step 1: Verify Python Installation

Open your terminal or command prompt and check your Python version:

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from [python.org](https://python.org/downloads/)

## Step 2: Get Telegram API Credentials

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Sign in with your phone number
3. Navigate to "API development tools"
4. Fill in the application form:
   - App title: Any name you like (e.g., "Telegram Scraper")
   - Short name: A short version (e.g., "tgscraper")
   - Platform: Desktop
   - Description: Optional
5. Click "Create application"
6. Save your **api_id** (a number) and **api_hash** (a long string)

You'll need these credentials for each account you want to use.

## Step 3: Download or Clone the Project

### Option A: If you have the files
```bash
cd telegram_scraper
```

### Option B: Clone from repository (if available)
```bash
git clone <repository-url>
cd telegram_scraper
```

## Step 4: Create Virtual Environment (Recommended)

This keeps your project dependencies isolated:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

## Step 5: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `telethon` - Telegram client library
- `pyfiglet` - ASCII art banners
- `colorama` - Colored terminal output
- `pandas` - Data processing (optional, for future features)

**Note:** On Linux, if you encounter errors, you may need to install system dependencies first:

**Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install python3-dev libffi-dev libssl-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-devel libffi-devel openssl-devel
```

## Step 6: Verify Installation

Test that everything is installed correctly:

```bash
python -c "import telethon; import pyfiglet; import colorama; print('All dependencies installed!')"
```

If you see "All dependencies installed!" without errors, you're ready to go.

## Step 7: Add Your First Account

Run the account manager:

```bash
python manager.py
```

1. Choose `[1] Add new accounts`
2. Enter your API ID (the number from step 2)
3. Enter your API Hash (the long string from step 2)
4. Enter your phone number (with country code, e.g., +1234567890)
5. Check your Telegram app for the verification code
6. Enter the code when prompted

The script will create a session file for your account.

## Step 8: Test the Setup

Try running the scraper to verify everything works:

```bash
python scraper.py
```

You should see the banner and account selection menu. This confirms the installation is successful.

## Troubleshooting Installation

### "python: command not found"
- Install Python from [python.org](https://python.org/downloads/)
- Or use `python3` instead of `python`

### "pip: command not found"
- Ensure Python is installed correctly
- Try: `python -m pip install -r requirements.txt`

### Permission denied errors
**Linux/Mac:**
```bash
sudo pip install -r requirements.txt
```

**Windows:**
Run Command Prompt as Administrator

### ModuleNotFoundError after installation
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Telethon installation errors
```bash
pip install --upgrade pip setuptools wheel
pip install telethon
```

### PyFiglet not working
```bash
pip install pyfiglet --force-reinstall
```

### Virtual environment issues
If you have problems with virtual environment, you can install globally (not recommended but works):

```bash
pip install -r requirements.txt --user
```

## Directory Structure After Installation

```
telegram_scraper/
├── venv/                    # Virtual environment (if created)
├── sessions/                # Telegram session files (auto-created)
├── members/                 # Scraped member data (auto-created)
├── data/                    # Account data (auto-created)
├── manager.py               # Account management
├── scraper.py               # Member scraping
├── adder.py                 # Single account adding
├── main_adder.py            # Multi-account orchestrator
├── config.py                # Configuration settings
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
├── QUICK_START.md           # Quick start guide
└── INSTALLATION.md          # This file
```

## Next Steps

After successful installation:

1. Read the [QUICK_START.md](QUICK_START.md) for basic usage
2. Read the [README.md](README.md) for detailed documentation
3. Add multiple accounts for better performance
4. Test with small batches first

## Security Best Practices

1. **Don't share your API credentials** - Keep api_id and api_hash private
2. **Use separate accounts** - Don't use your main personal account
3. **Backup session files** - Keep copies of `sessions/` directory
4. **Use strong passwords** - For your Telegram accounts
5. **Enable 2FA** - Two-factor authentication on your accounts

## Uninstallation

To remove the tool:

```bash
# Deactivate virtual environment (if active)
deactivate

# Remove the directory
rm -rf telegram_scraper

# Remove dependencies (optional)
pip uninstall telethon pyfiglet colorama pandas
```

## Getting Help

If you encounter issues:

1. Check this installation guide's troubleshooting section
2. Review the README.md for common issues
3. Ensure you have the correct Python version (3.7+)
4. Verify all dependencies are installed
5. Check that you have valid API credentials

## System Requirements

**Minimum:**
- Python 3.7
- 100MB free disk space
- Internet connection
- 1GB RAM

**Recommended:**
- Python 3.9 or higher
- 500MB free disk space
- Stable internet connection
- 2GB RAM
- Multiple Telegram accounts

---

**Installation Complete!** You're now ready to use the Telegram Scraper and Member Adder. Refer to QUICK_START.md to get started.