# Troubleshooting Guide

Common issues and their solutions for LinkedIn Outreach Automation.

## Installation Issues

### Python Version Error

**Error:** `SyntaxError` or `requires Python 3.8+`

**Solution:**
```bash
# Check Python version
python --version

# If version < 3.8, install Python 3.8+
# Then use:
python3 -m venv venv
python3 main.py
```

### Package Installation Fails

**Error:** `pip install` fails with errors

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install packages one by one
pip install requests
pip install selenium
pip install python-dotenv
pip install pyyaml
# etc.

# Or use specific version
pip install -r requirements.txt --no-cache-dir
```

### ChromeDriver Issues

**Error:** `WebDriver not found` or browser doesn't open

**Solution:**
```bash
# Update webdriver-manager
pip install --upgrade webdriver-manager

# Update Chrome browser to latest version
# Restart terminal
# Try again
```

## Authentication Issues

### Login Fails Immediately

**Error:** "Authentication failed" immediately

**Checklist:**
1. Verify credentials in `.env` are correct
2. No extra spaces in email/password
3. Password doesn't contain special characters that need escaping

**Solution:**
```bash
# Test credentials manually
# Try logging into LinkedIn in regular browser first

# Check .env format
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=YourPassword

# NO quotes, NO spaces around =
```

### CAPTCHA Appears

**Error:** LinkedIn shows CAPTCHA during login

**Solution:**
1. **Complete CAPTCHA manually** in the browser window
2. Wait for it to continue
3. System will proceed after verification
4. This is normal for new IPs/devices

**Prevention:**
- Use the tool less frequently
- Login manually to LinkedIn periodically
- Don't run from VPN/proxy

### Two-Factor Authentication (2FA)

**Error:** 2FA code requested

**Solution:**

**Option 1 - Disable 2FA temporarily:**
1. Go to LinkedIn Settings
2. Turn off 2FA
3. Run automation
4. Re-enable 2FA after

**Option 2 - Use App Password:**
1. Generate app-specific password in LinkedIn
2. Use that in `.env` instead of regular password

### Session Expired

**Error:** "Session expired, logging in again..."

**Solution:**
- This is normal behavior
- System will re-authenticate automatically
- If keeps failing, delete `data/session.pkl`

```bash
rm data/session.pkl
python main.py
```

### "Check credentials or handle CAPTCHA manually"

**Error:** Login timeout after credentials entered

**Solution:**
1. Don't close browser window
2. Check for CAPTCHA or verification
3. Complete any verification manually
4. Wait for LinkedIn to fully load
5. System will detect success automatically

## Configuration Issues

### FileNotFoundError: .env not found

**Error:** `FileNotFoundError: .env`

**Solution:**
```bash
# Create .env from template
cp .env.template .env

# Or create manually
echo "LINKEDIN_EMAIL=your@email.com" > .env
echo "LINKEDIN_PASSWORD=yourpassword" >> .env

# Edit with your credentials
nano .env  # or use any text editor
```

### YAML Configuration Error

**Error:** `yaml.scanner.ScannerError` or invalid YAML

**Solution:**
```bash
# Check settings.yaml syntax
# Common issues:
# - Incorrect indentation (use spaces, not tabs)
# - Missing colons
# - Unquoted strings with special characters

# Validate YAML online: yamllint.com
# Or reinstall default:
cp config/settings.yaml.backup config/settings.yaml
```

### Missing Configuration Keys

**Error:** `KeyError` or "Missing required section"

**Solution:**
```bash
# Restore default settings.yaml
# Ensure all sections exist:
# - linkedin
# - messaging
# - logging
# - safety

# Or download fresh copy from repository
```

## CSV/Data Issues

### CSV File Not Found

**Error:** `FileNotFoundError: connections.csv`

**Solution:**
```bash
# Create sample CSV
python main.py --create-sample

# Verify location
ls data/connections.csv

# Or create manually
mkdir -p data
touch data/connections.csv
```

### Invalid CSV Format

**Error:** "Missing required section" or validation errors

**Solution:**
1. Check CSV has required headers:
   ```csv
   first_name,last_name,profile_url,company,position,location
   ```

2. Check for:
   - No extra commas
   - No missing commas
   - UTF-8 encoding
   - No empty rows between data

3. Use correct format:
   ```csv
   John,Doe,https://www.linkedin.com/in/johndoe/,TechCorp,Engineer,SF
   ```

### Invalid Profile URLs

**Error:** "Invalid LinkedIn profile URL"

**Valid formats:**
```
✅ https://www.linkedin.com/in/username/
✅ https://linkedin.com/in/username/
✅ http://www.linkedin.com/in/username/

❌ linkedin.com/in/username
❌ www.linkedin.com/in/username
❌ https://linkedin.com/profile/username
```

**Solution:**
- Must include `https://` or `http://`
- Must contain `/in/`
- Must end with `/` or username

### CSV Shows "Row X: Invalid"

**Error:** Specific rows failing validation

**Debugging:**
1. Check row in CSV (count from 2, after header)
2. Verify required fields not empty:
   - first_name
   - last_name
   - profile_url
3. Check for hidden characters/spaces
4. Re-type the problematic row

**Quick fix:**
```bash
# View specific row (replace X with row number)
sed -n 'Xp' data/connections.csv

# Check for invisible characters
cat -A data/connections.csv
```

## Messaging Issues

### Message Button Not Found

**Error:** "Could not find message button"

**Causes:**
- Not a 1st-degree connection
- Connection's messaging settings restrict you
- LinkedIn UI changed
- Page didn't load fully

**Solution:**
1. Verify recipient is 1st-degree connection
2. Check manually: Can you message them via LinkedIn?
3. Increase page load delays in settings.yaml:
   ```yaml
   page_load_min: 5
   page_load_max: 10
   ```

### Messages Not Sending

**Error:** "Failed to send message"

**Checklist:**
```bash
# 1. Check LinkedIn status
# Visit linkedin.com manually - is it working?

# 2. Check connection degree
# Only 1st-degree connections can receive messages

# 3. Check message limits
# Have you sent 50+ messages today?

# 4. Check logs
cat data/logs.csv | grep failed

# 5. Try manually
# Can you send message via LinkedIn interface?
```

**Solutions:**
- Wait 24 hours and retry
- Reduce message volume
- Check recipient's messaging settings
- Verify LinkedIn account in good standing

### Timeout Waiting for Message Box

**Error:** "Timeout waiting for message box"

**Solution:**
```yaml
# Increase timeouts in code if needed
# Or check:
# 1. Internet connection stable?
# 2. LinkedIn loading slowly?
# 3. Browser window visible?

# Try:
# - Close other programs
# - Restart computer
# - Check internet speed
```

## Browser/Selenium Issues

### Browser Opens Then Closes

**Error:** Chrome window flashes and closes

**Solution:**
```bash
# Update Chrome
# Check Chrome version matches ChromeDriver

# Update Selenium and webdriver-manager
pip install --upgrade selenium webdriver-manager

# Clear cached drivers
rm -rf ~/.wdm
pip cache purge
```

### "WebDriver not found"

**Error:** selenium.common.exceptions.WebDriverException

**Solution:**
```bash
# Let webdriver-manager auto-download
pip install --upgrade webdriver-manager

# Or manually download ChromeDriver
# 1. Check Chrome version (chrome://version)
# 2. Download matching ChromeDriver
# 3. Add to system PATH
```

### Browser Automation Detected

**Error:** "Looks like you're using automation software"

**Solution:**
- This is LinkedIn detecting automation
- Options:
  1. Stop and wait 24-48 hours
  2. Use tool less frequently
  3. Increase delays in settings
  4. Send fewer messages per session

**Prevention:**
```yaml
# Use longer, more random delays
messaging:
  delays:
    min_seconds: 90
    max_seconds: 180
```

## Runtime Errors

### KeyboardInterrupt / Ctrl+C

**Error:** Process stopped by user

**Recovery:**
```bash
# Logs are saved incrementally
# Check what was completed
cat data/logs.csv

# Can run again - won't duplicate sends
# (if you track sent recipients)
```

### Circuit Breaker Triggered

**Error:** "Circuit breaker triggered after X consecutive failures"

**Meaning:** System detected multiple failures and stopped for safety

**Solution:**
1. Check logs to see failure reason:
   ```bash
   tail -20 data/logs.csv
   ```

2. Address the underlying issue
3. Wait before retrying
4. Or disable circuit breaker (not recommended):
   ```yaml
   safety:
     enable_circuit_breaker: false
   ```

### Session Limit Reached

**Message:** "Session limit of 10 messages reached"

**Solution:**
- This is expected behavior
- Increase if needed in settings.yaml:
  ```yaml
  linkedin:
    limits:
      session_messages: 20  # Increase carefully
  ```
- Or run again later (logs prevent duplicates)

### Memory/Performance Issues

**Error:** System slow or frozen

**Solution:**
```bash
# Close other applications
# Increase system resources
# Run one session at a time

# Check memory usage
# Task Manager (Windows) or Activity Monitor (Mac)

# Restart computer if needed
```

## Log/Output Issues

### Can't Read Logs

**Error:** logs.csv corrupted or empty

**Solution:**
```bash
# Check if file exists
ls -lh data/logs.csv

# View with cat
cat data/logs.csv

# Open in Excel/Numbers/Google Sheets

# If corrupted, delete and start fresh
mv data/logs.csv data/logs.csv.backup
```

### No Output in Terminal

**Error:** Script runs but shows nothing

**Solution:**
```bash
# Check if running in background
# Ensure terminal is active

# Run with verbose output
python main.py 2>&1 | tee output.log

# Check for redirected output
```

## Testing Issues

### pytest Not Found

**Error:** `command not found: pytest`

**Solution:**
```bash
# Install pytest
pip install pytest pytest-cov pytest-mock

# Or install from requirements
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Tests Failing

**Error:** Tests fail with errors

**Solution:**
```bash
# Run specific test
pytest tests/test_models.py -v

# Run with more info
pytest tests/ -vv --tb=long

# Skip failing tests temporarily
pytest tests/ -k "not failing_test_name"
```

## Network Issues

### Connection Timeout

**Error:** Network request timeout

**Solution:**
```bash
# Check internet connection
ping google.com

# Check LinkedIn accessible
curl -I linkedin.com

# Try different network
# Disable VPN if using one
# Check firewall settings
```

### SSL Certificate Errors

**Error:** SSL verification failed

**Solution:**
```bash
# Update certificates
pip install --upgrade certifi

# Or temporarily disable SSL verification (not recommended)
# In requests calls, add: verify=False
```

## Getting More Help

### Enable Debug Logging

Add to `config/settings.yaml`:
```yaml
logging:
  level: "DEBUG"  # More detailed output
```

### Collect Diagnostic Info

```bash
# System info
python --version
pip list
google-chrome --version  # or chrome --version

# Check files
ls -R

# Check logs
tail -50 data/logs.csv

# Check environment
cat .env  # Remove before sharing!
```

### Before Reporting Issues

Collect:
1. Error message (full traceback)
2. Python version
3. OS and version
4. What you were trying to do
5. What happened instead
6. Relevant log entries

### Still Stuck?

1. Re-read [README.md](README.md)
2. Try [QUICKSTART.md](QUICKSTART.md) from beginning
3. Run `--dry-run` to isolate issue
4. Check LinkedIn's help center
5. Test manually via LinkedIn interface

---

**Most issues are due to:**
- Incorrect credentials
- Invalid CSV format
- Not 1st-degree connections
- LinkedIn rate limiting
- Network problems

**Always try:**
1. `--dry-run` mode first
2. Start with 1-2 recipients
3. Check logs after each run
4. Wait 24h between runs