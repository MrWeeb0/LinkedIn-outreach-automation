"""Unit tests for utility modules"""

import pytest
from core.models import Recipient
from utils.placeholders import PlaceholderReplacer
from utils.throttling import Throttler


class TestPlaceholderReplacer:
    """Test placeholder replacement functionality"""
    
    def test_replace_all_placeholders(self):
        """Test replacing all supported placeholders"""
        template = "Hi {first_name} {last_name} from {company} working as {position} in {location}!"
        recipient = Recipient(
            first_name="John",
            last_name="Doe",
            profile_url="https://www.linkedin.com/in/johndoe/",
            company="TechCorp",
            position="Engineer",
            location="SF"
        )
        
        result = PlaceholderReplacer.replace_placeholders(template, recipient)
        assert result == "Hi John Doe from TechCorp working as Engineer in SF!"
    
    def test_replace_with_missing_optional_fields(self):
        """Test replacement when optional fields are missing"""
        template = "Hi {first_name} from {company}!"
        recipient = Recipient(
            first_name="John",
            last_name="Doe",
            profile_url="https://www.linkedin.com/in/johndoe/"
        )
        
        result = PlaceholderReplacer.replace_placeholders(template, recipient)
        assert result == "Hi John from your company!"
    
    def test_validate_valid_placeholders(self):
        """Test validation of valid placeholders"""
        template = "Hi {first_name}, working at {company}"
        invalid = PlaceholderReplacer.validate_placeholders(template)
        assert len(invalid) == 0
    
    def test_validate_invalid_placeholders(self):
        """Test validation catches invalid placeholders"""
        template = "Hi {first_name}, {invalid_field}!"
        invalid = PlaceholderReplacer.validate_placeholders(template)
        assert "invalid_field" in invalid
    
    def test_get_available_placeholders(self):
        """Test getting list of available placeholders"""
        placeholders = PlaceholderReplacer.get_available_placeholders()
        assert "first_name" in placeholders
        assert "company" in placeholders
        assert len(placeholders) == 5
    
    def test_get_missing_data(self):
        """Test identifying missing data for placeholders"""
        template = "Hi {first_name} from {company}"
        recipient = Recipient(
            first_name="John",
            last_name="Doe",
            profile_url="https://www.linkedin.com/in/johndoe/"
        )
        
        missing = PlaceholderReplacer.get_missing_data(template, recipient)
        assert "company" in missing


class TestThrottler:
    """Test throttling functionality"""
    
    def test_human_delay_range(self):
        """Test that human delay is within specified range"""
        throttler = Throttler(min_delay=30, max_delay=120)
        
        for _ in range(10):
            delay = throttler.human_delay()
            assert 30 <= delay <= 120
    
    def test_typing_delay_calculation(self):
        """Test typing delay calculation"""
        throttler = Throttler(typing_speed=5)
        message_length = 100
        
        delay = throttler.typing_delay(message_length)
        # Expected: 100/5 = 20 seconds, with ±20% variance
        assert 16 <= delay <= 24
    
    def test_page_load_delay_range(self):
        """Test page load delay range"""
        throttler = Throttler(page_load_range=(2, 5))
        
        for _ in range(10):
            delay = throttler.page_load_delay()
            assert 2 <= delay <= 5
    
    def test_exponential_backoff(self):
        """Test exponential backoff calculation"""
        # First attempt
        delay0 = Throttler.exponential_backoff(0, base_delay=5)
        assert 5 <= delay0 <= 6  # base + jitter
        
        # Second attempt
        delay1 = Throttler.exponential_backoff(1, base_delay=5)
        assert 10 <= delay1 <= 11  # base*2 + jitter
        
        # Third attempt
        delay2 = Throttler.exponential_backoff(2, base_delay=5)
        assert 20 <= delay2 <= 22  # base*4 + jitter
    
    def test_exponential_backoff_max_delay(self):
        """Test that exponential backoff respects max delay"""
        delay = Throttler.exponential_backoff(10, base_delay=5, max_delay=60)
        assert delay <= 66  # max_delay + jitter


class TestCSVHandler:
    """Test CSV handling functionality"""
    
    def test_parse_valid_row(self):
        """Test parsing valid CSV row"""
        from utils.csv_handler import CSVHandler
        
        handler = CSVHandler()
        row = {
            'first_name': 'John',
            'last_name': 'Doe',
            'profile_url': 'https://www.linkedin.com/in/johndoe/',
            'company': 'TechCorp',
            'position': 'Engineer',
            'location': 'SF'
        }
        
        recipient, error = handler._parse_row(row, 1)
        assert recipient is not None
        assert error is None
        assert recipient.first_name == 'John'
    
    def test_parse_invalid_url(self):
        """Test parsing row with invalid URL"""
        from utils.csv_handler import CSVHandler
        
        handler = CSVHandler()
        row = {
            'first_name': 'John',
            'last_name': 'Doe',
            'profile_url': 'invalid-url',
            'company': '',
            'position': '',
            'location': ''
        }
        
        recipient, error = handler._parse_row(row, 1)
        assert recipient is None
        assert error is not None
        assert 'Invalid LinkedIn profile URL' in error
    
    def test_parse_missing_required_field(self):
        """Test parsing row with missing required field"""
        from utils.csv_handler import CSVHandler
        
        handler = CSVHandler()
        row = {
            'first_name': '',
            'last_name': 'Doe',
            'profile_url': 'https://www.linkedin.com/in/johndoe/',
            'company': '',
            'position': '',
            'location': ''
        }
        
        recipient, error = handler._parse_row(row, 1)
        assert recipient is None
        assert error is not None