# Quick Start Guide

Get started with LinkedIn Outreach Automation in 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Google Chrome browser installed
- [ ] LinkedIn account with active connections
- [ ] Terminal/Command Prompt access

## Installation (5 Steps)

### Step 1: Set Up Project

```bash
# Create and navigate to project directory
mkdir linkedin-outreach
cd linkedin-outreach

# Download all project files here
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Project Structure

```bash
python setup_project.py
```

### Step 5: Configure Credentials

```bash
# Copy template
cp .env.template .env

# Edit .env with your editor
# Add your LinkedIn credentials
```

Example `.env`:
```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=YourSecurePassword123
```

## First Run (Test Mode)

### 1. Create Sample CSV

```bash
python main.py --create-sample
```

This creates `data/connections.csv` with example data.

### 2. Edit Connections File

Open `data/connections.csv` and add your real LinkedIn connections:

```csv
first_name,last_name,profile_url,company,position,location
John,Doe,https://www.linkedin.com/in/johndoe/,TechCorp,Engineer,SF
```

**Important:** 
- Use exact LinkedIn profile URLs
- Include only 1st-degree connections
- Maximum 10 connections per run

### 3. Run Dry Run

Test without sending messages:

```bash
python main.py --dry-run
```

This will:
- ✅ Load configuration
- ✅ Validate credentials
- ✅ Load and validate recipients
- ✅ Show what would happen
- ❌ NOT send any messages

### 4. Send Messages

When ready, run for real:

```bash
python main.py
```

**What happens:**
1. Chrome browser opens (don't close it!)
2. Logs into LinkedIn
3. Sends personalized messages
4. Logs all activity to `data/logs.csv`

## Customizing Messages

Edit `config/settings.yaml` to customize your message templates:

```yaml
messaging:
  templates:
    - "Hi {first_name}, I hope you're doing well! I came across your profile and was impressed by your work at {company}. Would love to connect!"
    - "Hello {first_name}, I noticed we share some common interests. I'd be interested in connecting and exchanging ideas."
```

**Available placeholders:**
- `{first_name}` - Recipient's first name
- `{last_name}` - Recipient's last name  
- `{company}` - Company name
- `{position}` - Job title
- `{location}` - Location

## Safety Settings

Adjust delays in `config/settings.yaml`:

```yaml
messaging:
  delays:
    min_seconds: 30      # Minimum wait between messages
    max_seconds: 120     # Maximum wait between messages
```

**Recommended settings:**
- Development/Testing: 30-60 seconds
- Production: 60-120 seconds
- Conservative: 90-180 seconds

## Viewing Results

Check your logs:

```bash
# View logs file
cat data/logs.csv

# Or open in Excel/Numbers/Google Sheets
```

Log format:
```csv
recipient_name,profile_url,timestamp,status,error_message,template_used,message_preview
John Doe,https://...,2025-10-04...,sent,,template1,"Hi John, I hope..."
```

## Common Issues & Solutions

### Issue: "Authentication failed"

**Solutions:**
1. Check credentials in `.env`
2. Try logging in manually to LinkedIn first
3. Disable 2FA temporarily or use app password
4. Complete any CAPTCHA that appears

### Issue: "CSV file not found"

**Solution:**
```bash
python main.py --create-sample
# Then edit data/connections.csv
```

### Issue: "Message failed to send"

**Possible causes:**
- Recipient is not a 1st-degree connection
- LinkedIn rate limit hit
- Network issue

**Solution:** Check logs for specific error, wait 15 minutes, retry

### Issue: Browser closes immediately

**Solution:**
- Update Chrome to latest version
- Run: `pip install --upgrade selenium webdriver-manager`

## Best Practices

### Before Your First Real Run

1. ✅ Test with `--dry-run`
2. ✅ Start with just 2-3 recipients
3. ✅ Use personalized templates
4. ✅ Check recipients are 1st-degree connections
5. ✅ Review LinkedIn's messaging guidelines

### During Operation

1. ✅ Let it run - don't interrupt
2. ✅ Monitor the browser window
3. ✅ Check logs after completion
4. ✅ Respect the delays (they protect you)

### After Completion

1. ✅ Review `data/logs.csv`
2. ✅ Check LinkedIn for responses
3. ✅ Wait at least 24 hours before next run
4. ✅ Don't exceed 50 messages per day

## Daily Workflow

```bash
# Morning routine
python main.py --dry-run              # Validate setup
python main.py                        # Send messages (if validation passed)

# Check results
cat data/logs.csv                     # Review what happened
```

## Limits & Restrictions

| Limit Type | Value | Why |
|-----------|-------|-----|
| Max connections per run | 10 | Test phase, avoid detection |
| Messages per session | 10 | Configurable, matches test phase |
| Daily messages | 50 | LinkedIn soft limit |
| Delay between messages | 30-120s | Mimic human behavior |

## Next Steps

Once comfortable with basics:

1. **Customize templates** - Add your personal touch
2. **Adjust delays** - Find your comfort level
3. **Monitor account** - Watch for LinkedIn warnings
4. **Scale carefully** - Increase slowly over time
5. **Track responses** - Measure effectiveness

## Getting Help

1. Check error in `data/logs.csv`
2. Review [README.md](README.md) troubleshooting section
3. Run with `--dry-run` to diagnose
4. Check LinkedIn's messaging policies

## Important Reminders

⚠️ **This tool automates LinkedIn - use responsibly**
- Start small (2-3 messages)
- Personalize your templates
- Don't spam connections
- Monitor your account
- Respect LinkedIn's ToS

🔒 **Security**
- Never commit `.env` to Git
- Use strong passwords
- Keep credentials private

✅ **Success Tips**
- Quality over quantity
- Personalize messages
- Be patient with delays
- Monitor and adjust

---

**Ready to start?** Run `python main.py --dry-run` to test your setup!