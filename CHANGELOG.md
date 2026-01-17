# Changelog

All notable changes to the Telegram Scraper and Member Adder project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of enhanced Telegram Scraper and Member Adder
- Multi-account support for parallel operations
- Advanced member filtering options (all, active, weekly, monthly, inactive)
- Automated multi-account orchestrator (main_adder.py)
- Comprehensive documentation suite
- Cross-platform compatibility (Windows, Linux, macOS)
- Rate limiting and anti-spam measures
- Session management system
- Error handling for flood errors, privacy restrictions, and banned accounts
- CSV export functionality for member data

### Features
- Account manager with add, filter, list, and delete capabilities
- Member scraper with multiple filtering strategies
- Single-account and multi-account member adding
- Configurable delays and batch sizes
- Colored terminal output with banners
- Progress tracking and statistics
- Automatic account authentication
- Session persistence
- Admin-only scraping option

### Documentation
- README.md - Comprehensive main documentation
- QUICK_START.md - 5-minute quick start guide
- INSTALLATION.md - Detailed installation instructions
- USAGE_EXAMPLES.md - 24 practical usage examples
- CONTRIBUTING.md - Contribution guidelines
- LICENSE.txt - MIT License
- CHANGELOG.md - This file

### Technical
- Built with Telethon 1.42.0
- Python 3.7+ support
- Modular code structure
- Comprehensive error handling
- Cross-platform compatibility

## [1.0.0] - 2025-01-05

### Added
- Initial public release
- Based on DenizShabani/telegramscraper reference implementation
- Enhanced with improved error handling
- Better code organization and structure
- Comprehensive documentation
- Cross-platform support
- Multi-account orchestration

### Changed
- Improved user interface with colored output
- Enhanced error messages and user feedback
- Better session management
- Improved configuration system
- Added rate limiting defaults

### Fixed
- Session file handling issues
- Account authentication flow
- CSV export formatting
- Platform-specific path handling
- Import dependencies

## [0.9.0] - Development

### Added
- Basic scraper functionality
- Account management system
- Member adding capability
- CSV export

### Known Issues
- Limited error handling
- Platform-specific issues on macOS
- Session file corruption in some cases

---

**Note**: Version 1.0.0 is the first stable release suitable for production use.