# GitHub Setup Guide

This guide will help you set up your GitHub repository for the Telegram Scraper and Member Adder project.

## Step 1: Initialize Git Repository

```bash
cd telegram_scraper
git init
```

## Step 2: Add All Files

```bash
git add .
```

This will add all files except those ignored by `.gitignore` (sessions, data files, etc.)

## Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Telegram Scraper and Member Adder v1.0.0"
```

## Step 4: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

If you have GitHub CLI installed:

```bash
gh repo create telegram-scraper --public --description "Enhanced Telegram Scraper and Member Adder with multi-account support and advanced filtering" --source=. --remote=origin --push
```

### Option B: Using GitHub Website

1. Go to [https://github.com/new](https://github.com/new)
2. Repository name: `telegram-scraper` (or your preferred name)
3. Description: `Enhanced Telegram Scraper and Member Adder with multi-account support and advanced filtering`
4. Choose **Public** or **Private**
5. Don't initialize with README, .gitignore, or license (we already have them)
6. Click **Create repository**

## Step 5: Connect Local Repository to GitHub

### If you chose Option B (Website):

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/telegram-scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 6: Verify Repository

Visit your GitHub repository:
```
https://github.com/YOUR_USERNAME/telegram-scraper
```

You should see all your files there.

## Step 7: Configure Repository Settings

### Enable Issues
1. Go to repository **Settings** tab
2. Click **General** on the left
3. Scroll down to **Features**
4. Check **Issues**
5. Click **Save changes**

### Enable Discussions (Optional)
1. Go to repository **Settings** tab
2. Click **General** on the left
3. Scroll down to **Features**
4. Check **Discussions**
5. Click **Save changes**

### Set Repository Topics
1. Go to repository **Settings** tab
2. Click **General** on the left
3. Scroll to **Topics**
4. Add these tags:
   - `telegram`
   - `telegram-bot`
   - `scraper`
   - `python`
   - `telethon`
   - `automation`
   - `telegram-api`
5. Click **Save changes**

### Add Repository Description
1. Go to repository **Settings** tab
2. Click **General** on the left
3. Edit the description:
   ```
   Enhanced Telegram Scraper and Member Adder with multi-account support, advanced filtering, and comprehensive documentation
   ```
4. Click **Save changes**

## Step 8: Create GitHub Pages (Optional)

If you want a documentation website:

1. Go to repository **Settings** tab
2. Click **Pages** on the left
3. Under **Source**, select **main** branch
4. Click **Save**

Your documentation will be available at:
```
https://YOUR_USERNAME.github.io/telegram-scraper/
```

## Step 9: Add a README Badge

Add badges to your README.md to show build status, license, etc.

Edit `README.md` and add at the top:

```markdown
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Telethon](https://img.shields.io/badge/telethon-1.34%2B-green.svg)
```

## Step 10: Create First Release

1. Go to repository
2. Click **Releases** on the right
3. Click **Create a new release**
4. Tag version: `v1.0.0`
5. Release title: `Version 1.0.0 - Initial Release`
6. Description: Copy from CHANGELOG.md
7. Click **Publish release**

## Step 11: Create Issues Template (Optional)

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment (please complete the following information):**
 - OS: [e.g. Windows 10, Ubuntu 20.04]
 - Python version: [e.g. Python 3.9]
 - Telethon version: [e.g. 1.34.0]

**Additional context**
Add any other context about the problem here.
```

## Step 12: Create Pull Request Template (Optional)

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
Please include a summary of the changes and the related issue. Please also include relevant motivation and context.

Fixes #(issue)

## Type of change
Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Please describe the tests that you ran to verify your changes.

- [ ] Test A
- [ ] Test B

**Test Configuration**:
- OS: 
- Python version:
- Telethon version:

## Checklist:
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
```

## Step 13: Add Security Policy (Optional)

Create `SECURITY.md`:

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to security@example.com. All security vulnerabilities will be promptly addressed.

Please do not open public issues for security vulnerabilities.
```

## Step 14: Add Code of Conduct (Optional)

Create `CODE_OF_CONDUCT.md`:

```markdown
# Contributor Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone.

## Our Standards

Examples of behavior that contributes to a positive environment:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

## Scope

This Code of Conduct applies within all community spaces.

## Enforcement

Project maintainers who do not follow the Code of Conduct may be removed from
the project team.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.0, available at
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html.

[homepage]: https://www.contributor-covenant.org
```

## Step 15: Final Verification

Checklist:
- [ ] Repository is public (or private as desired)
- [ ] All files are pushed to GitHub
- [ ] README.md displays correctly
- [ ] License is set to MIT
- [ ] Topics are added
- [ ] First release is created
- [ ] Issues are enabled
- [ ] Discussions are enabled (optional)

## Common Git Commands

```bash
# Check status
git status

# View changes
git diff

# Add specific file
git add filename.py

# Commit changes
git commit -m "Description of changes"

# Push changes
git push

# Pull changes from GitHub
git pull

# Create new branch
git branch feature-name
git checkout feature-name

# Merge branch to main
git checkout main
git merge feature-name

# Delete branch
git branch -d feature-name
```

## Next Steps

After setting up your repository:

1. **Share it**: Post about it in relevant communities
2. **Watch for issues**: Monitor and respond to issues
3. **Accept pull requests**: Review and merge contributions
4. **Update documentation**: Keep docs current with changes
5. **Make releases**: Tag releases for stable versions
6. **Engage with community**: Respond to discussions and issues

## Repository URL

Your repository will be available at:
```
https://github.com/YOUR_USERNAME/telegram-scraper
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

Need help? Check out [GitHub's documentation](https://docs.github.com/) for more detailed information.
