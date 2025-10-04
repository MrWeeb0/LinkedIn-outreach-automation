LinkedIn Outreach Automation
A Python-based automation system for sending personalized LinkedIn messages to connections. Designed for test phase with 10 recipients maximum, following DRY and KISS principles.
⚠️ Important Disclaimer
Use this tool responsibly and at your own risk. Automated interactions with LinkedIn may violate their Terms of Service. This tool is for educational purposes and should be used sparingly to avoid account restrictions or bans.
Features

✅ Secure authentication with session persistence
✅ CSV-based recipient management (max 10 connections)
✅ Personalized message templates with dynamic variables
✅ Human-like delays to avoid detection
✅ Comprehensive activity logging
✅ Circuit breaker for safety
✅ Dry-run mode for testing
✅ Session limit enforcement

Prerequisites

Python 3.8 or higher
Google Chrome browser
LinkedIn account
Active LinkedIn connections

Installation
1. Clone or download the project
bash# Create project directory
mkdir linkedin-outreach
cd linkedin-outreach
2. Set up virtual environment
bash# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Create project structure
bashpython setup_project.py
5. Configure environment variables
bash# Copy template
cp .env.template .env

# Edit .env and add your credentials
# LINKEDIN_EMAIL=your_email@example.com
# LINKEDIN_PASSWORD=your_secure_password
6. Create sample CSV
bashpython main.py --create-sample
This creates data/connections.csv with sample data. Edit this file with your actual connections.
Configuration
Environment Variables (.env)
envLINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_secure_password
Application Settings (config/settings.yaml)
Customize message templates, delays, and limits:
yamllinkedin:
  limits:
    daily_messages: 50
    session_messages: 10
    
messaging:
  templates:
    - "Hi {first_name}, I hope you're doing well!..."
  delays:
    min_seconds: 30
    max_seconds: 120
Connections CSV (data/connections.csv)
Format your recipients file:
first_namelast_nameprofile_urlcompanypositionlocationJohnDoehttps://www.linkedin.com/in/johndoe/TechCorpEngineerSF, CA
Required fields: first_name, last_name, profile_url
Optional fields: company, position, location
Usage
Dry Run (Recommended First)
Test your configuration without sending messages:
bashpython main.py --dry-run
Send Messages
bashpython main.py
The browser will open automatically. Do not close it during the process.
Command-Line Options

--dry-run - Validate configuration without sending messages
--create-sample - Create sample connections.csv file

Message Templates
Use these placeholders in your templates:

{first_name} - Recipient's first name
{last_name} - Recipient's last name
{company} - Recipient's company
{position} - Recipient's position
{location} - Recipient's location

Example:
Hi {first_name}, I noticed you work at {company}. I'd love to connect and learn more about your experience in {position}!
Safety Features
Human-Like Delays

Random delays between 30-120 seconds between messages
Typing simulation based on message length
Page load delays

Circuit Breaker

Stops after 3 consecutive failures
Prevents account flagging from repeated errors

Session Limits

Maximum 10 messages per session (configurable)
Daily limit tracking

Activity Logging
All actions are logged to data/logs.csv:

Successful sends
Failed attempts with error details
Skipped recipients

Project Structure
linkedin-outreach/
├── core/
│   ├── auth.py              # Authentication & session
│   ├── config_loader.py     # Configuration management
│   ├── logger.py            # Activity logging
│   ├── messenger.py         # Message sending
│   └── models.py            # Data models
├── utils/
│   ├── csv_handler.py       # CSV processing
│   ├── placeholders.py      # Template variables
│   └── throttling.py        # Delay mechanisms
├── config/
│   └── settings.yaml        # Application settings
├── data/
│   ├── connections.csv      # Your recipients
│   └── logs.csv            # Activity logs
├── docs/                    # Documentation
├── tests/                   # Unit tests
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env                     # Credentials (create from template)
└── README.md               # This file
Troubleshooting
Authentication Issues
Problem: Login fails or times out
Solution:

Verify credentials in .env
Check for CAPTCHA (complete manually if appears)
Ensure 2FA is disabled or use app password

Message Not Sending
Problem: Messages fail to send
Solution:

Verify recipients are 1st-degree connections
Check LinkedIn's messaging restrictions
Ensure profile URLs are correct format
Wait and retry - may be temporary rate limit

Chrome Driver Issues
Problem: Browser won't open
Solution:

Update Chrome to latest version
Run: pip install --upgrade selenium webdriver-manager
Check system permissions

CSV Errors
Problem: Invalid recipient data
Solution:

Verify CSV has required headers: first_name, last_name, profile_url
Check profile URLs match format: https://www.linkedin.com/in/username/
Remove empty rows
Ensure UTF-8 encoding

Best Practices

Start Small: Test with 2-3 recipients first
Use Dry Run: Always validate before sending
Personalize Templates: Avoid generic messages
Respect Limits: Don't exceed 50 messages per day
Monitor Logs: Check data/logs.csv regularly
Vary Messages: Use multiple templates for variety
Be Patient: Let delays run - they protect your account

Security Considerations

Never commit .env to version control
Store credentials securely
Use strong, unique passwords
Consider LinkedIn's ToS implications
Monitor account for unusual activity warnings

Testing
Run unit tests:
bashpytest tests/
Run with coverage:
bashpytest --cov=core --cov=utils tests/
Limitations

Maximum 10 recipients per session (configurable)
Requires existing 1st-degree connections
Only sends text messages (no attachments)
Requires Chrome browser
Manual CAPTCHA handling may be needed

Contributing
This is a personal automation tool. Use and modify as needed for your purposes.
License
This project is provided as-is for educational purposes. Use responsibly and in accordance with LinkedIn's Terms of Service.
Support
For issues or questions:

Check the Troubleshooting section
Review logs in data/logs.csv
Verify configuration in config/settings.yaml
Test with --dry-run mode

Version History

v1.0.0 - Initial release

Basic messaging functionality
CSV recipient management
Template system with placeholders
Safety features and logging



Acknowledgments
Built following DRY and KISS principles with a distributed monolith architecture for easy maintenance and future scalability.