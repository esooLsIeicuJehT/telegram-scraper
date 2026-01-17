# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: Yes |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

**Do not open a public issue** for security vulnerabilities.

Instead, please send an email to: security@example.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### What Happens Next

1. We will acknowledge receipt of your report within 48 hours
2. We will investigate the issue
3. We will work with you to understand and fix the vulnerability
4. We will release a fix as soon as possible
5. We will publicly disclose the vulnerability after the fix is released

### Security Best Practices for Users

1. **Never commit session files**: Session files contain sensitive authentication data
2. **Never share API credentials**: Keep your api_id and api_hash private
3. **Use separate accounts**: Don't use your main personal Telegram account
4. **Keep dependencies updated**: Regularly update to the latest versions
5. **Review code before running**: Understand what the code does before executing
6. **Use virtual environments**: Isolate project dependencies

### Known Security Considerations

#### Session Files
- Session files in the `sessions/` directory contain authentication tokens
- These files are excluded from git by `.gitignore`
- Never commit or share session files

#### API Credentials
- API credentials are stored in `data/vars.txt`
- This file is excluded from git by `.gitignore`
- Never commit or share this file

#### Telegram Rate Limits
- The tool includes built-in rate limiting to prevent account bans
- Modifying delays in `config.py` can increase security risks
- Aggressive scraping may trigger Telegram's anti-spam measures

#### Privacy Considerations
- Scraped member data may include personal information
- Handle scraped data responsibly and in compliance with privacy laws
- Respect user privacy settings (users who restrict group additions are skipped)

## License

This project is licensed under the MIT License. See LICENSE.txt for details.

---

Thank you for helping keep this project and its users safe!
