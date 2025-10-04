LinkedIn Outreach Automation

Automate personalized LinkedIn outreach to optimize networking, investor connections, and strategic communication. Designed for startups and professionals who want to efficiently manage outreach campaigns.

🔹 Features

Automated LinkedIn login and connection messaging

Personalized message templates with placeholders

CSV-based recipient management

Logging of messages and statuses

Throttling to avoid LinkedIn restrictions

Fully configurable via .env and YAML configuration files

🔹 Goal

Outreach 10 connections for testing purposes — with minimal setup and clear logging of sent messages.

🔹 Requirements

Python 3.12 (64-bit recommended)

Packages: selenium, webdriver-manager, python-dotenv, pandas, PyYAML

Chrome browser installed (matching ChromeDriver version)

Install dependencies:

pip install -r requirements.txt

🔹 Installation

Clone the repository:

git clone https://github.com/MrWeeb0/LinkedIn-outreach-automation.git
cd LinkedIn-outreach-automation


Create a virtual environment:

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Configure .env with your LinkedIn credentials and any necessary settings.

🔹 Usage

Prepare a CSV file with recipients (recipients.csv).

Update config.yaml if needed.

Run the automation:

python main.py


The browser will open and execute the outreach flow.

Logs and message statuses will be saved automatically.

🔹 Message Template

You can customize messages in templates/message_template.md:

Hi [First Name],

I’m [Your Name] from [Your Company]. We help startups create strategic intelligence briefs for investor conversations.

Could we spend 15 minutes reviewing our methodology? Here’s my Calendly: [Insert Link]

Best regards,
[Your Name]

🔹 Project Structure
linkedin-outreach/
├─ core/             # Core modules (auth, messenger, models, logger)
├─ utils/            # Utilities (CSV handling, placeholders, throttling)
├─ tests/            # Unit tests
├─ templates/        # Message templates
├─ main.py           # Entry point
├─ requirements.txt  # Python dependencies
└─ config.yaml       # Config file

🔹 Testing

Run tests with pytest:

pytest --cov=.

🔹 License

MIT License © [Your Name]