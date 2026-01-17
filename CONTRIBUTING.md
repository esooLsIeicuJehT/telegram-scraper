# Contributing to Telegram Scraper and Member Adder

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, please include:
- **Description**: A clear and concise description of what the bug is
- **Steps to Reproduce**: Steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Screenshots**: If applicable, add screenshots to help explain the problem
- **Environment**:
  - OS: [e.g., Windows 10, Ubuntu 20.04, macOS Big Sur]
  - Python version: [e.g., Python 3.9]
  - Telethon version: [e.g., 1.34.0]

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:
- **Description**: A clear and concise description of the enhancement
- **Motivation**: The motivation behind the enhancement (why should it be added?)
- **Use Cases**: Specific use cases where this enhancement would be helpful
- **Alternatives**: Any alternative solutions or features you've considered

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Write clean, readable code
   - Add comments for complex logic
   - Follow the existing code style
   - Update documentation if needed
4. **Test your changes** thoroughly
5. **Commit your changes**: `git commit -m 'Add some feature'`
6. **Push to the branch**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Example:

```python
def scrape_members(client: TelegramClient, group: str, filter_type: int) -> List[Dict]:
    """
    Scrape members from a Telegram group.
    
    Args:
        client: Telegram client instance
        group: Group username or ID
        filter_type: Filter type for members (0-4)
    
    Returns:
        List of member dictionaries
    
    Raises:
        ValueError: If group is not found
    """
    # Implementation here
    pass
```

### Comments
- Comment complex logic
- Explain "why" not "what"
- Keep comments up to date
- Use inline comments sparingly

## Testing

### Manual Testing Checklist
- [ ] Code runs without errors
- [ ] All existing features still work
- [ ] New features work as expected
- [ ] Edge cases are handled
- [ ] Error messages are clear
- [ ] Documentation is updated

### Test Environments
Test your changes on:
- At least one of: Windows, Linux, or macOS
- Python 3.7 or higher
- Fresh installation (virtual environment)

## Documentation

### When to Update Documentation
- Adding new features
- Changing existing functionality
- Fixing bugs that affect user behavior
- Updating dependencies
- Changing configuration options

### Documentation Files
- **README.md**: Main project documentation
- **QUICK_START.md**: Quick start guide
- **INSTALLATION.md**: Installation instructions
- **USAGE_EXAMPLES.md**: Usage examples
- **CONTRIBUTING.md**: This file

## Project Structure

```
telegram_scraper/
├── .gitignore              # Git ignore rules
├── LICENSE                 # License file
├── README.md               # Main documentation
├── QUICK_START.md          # Quick start guide
├── INSTALLATION.md         # Installation guide
├── USAGE_EXAMPLES.md       # Usage examples
├── CONTRIBUTING.md         # Contributing guidelines
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── manager.py             # Account management
├── scraper.py             # Member scraping
├── adder.py               # Single account adding
├── main_adder.py          # Multi-account orchestrator
├── sessions/              # Telegram sessions (not in git)
├── members/               # Scraped data (not in git)
└── data/                  # Account data (not in git)
```

## Development Workflow

### Setting Up Development Environment

1. **Fork and clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/telegram_scraper.git
cd telegram_scraper
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

### Making Changes

1. Write code following the style guidelines
2. Test thoroughly
3. Update documentation if needed
4. Commit with descriptive messages

### Commit Message Format

Use clear, descriptive commit messages:

```
Add feature: implement member filtering by activity level

- Added filter options in scraper.py
- Updated documentation in USAGE_EXAMPLES.md
- Added error handling for invalid filter types

Closes #123
```

## Types of Contributions

### Bug Fixes
- Always include a description of the bug
- Explain how the fix works
- Add tests if possible

### New Features
- Describe the feature and its use case
- Update documentation
- Provide usage examples

### Documentation
- Improve clarity
- Add examples
- Fix typos or errors
- Translate to other languages

### Code Refactoring
- Improve code structure
- Enhance readability
- Optimize performance
- Remove technical debt

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## Code Review Process

1. **Submit a Pull Request**
2. **Address Review Comments**: Make requested changes
3. **Keep PR Updated**: Respond to comments in a timely manner
4. **Maintain Clean History**: Squash commits if needed

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

If you have questions about contributing:
- Check existing issues and discussions
- Read the documentation
- Open a new discussion for questions

---

Thank you for contributing to the Telegram Scraper and Member Adder project!