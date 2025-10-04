"""Unit tests for data models"""

import pytest
from datetime import datetime
from core.models import Recipient, MessageLog, Config


class TestRecipient:
    """Test Recipient data model"""
    
    def test_valid_recipient(self):
        """Test creating valid recipient"""
        recipient = Recipient(
            first_name="John",
            last_name="Doe",
            profile_url="https://www.linkedin.com/in/johndoe/"
        )
        assert recipient.first_name == "John"
        assert recipient.full_name == "John Doe"
    
    def test_recipient_with_optional_fields(self):
        """Test recipient with all fields"""
        recipient = Recipient(
            first_name="Jane",
            last_name="Smith",
            profile_url="https://www.linkedin.com/in/janesmith/",
            company="TechCorp",
            position="Engineer",
            location="SF"
        )
        assert recipient.company == "TechCorp"
        assert recipient.position == "Engineer"
    
    def test_missing_first_name(self):
        """Test that missing first name raises error"""
        with pytest.raises(ValueError, match="First name is required"):
            Recipient(
                first_name="",
                last_name="Doe",
                profile_url="https://www.linkedin.com/in/test/"
            )
    
    def test_missing_last_name(self):
        """Test that missing last name raises error"""
        with pytest.raises(ValueError, match="Last name is required"):
            Recipient(
                first_name="John",
                last_name="",
                profile_url="https://www.linkedin.com/in/test/"
            )
    
    def test_invalid_profile_url(self):
        """Test that invalid URL raises error"""
        with pytest.raises(ValueError, match="Invalid LinkedIn profile URL"):
            Recipient(
                first_name="John",
                last_name="Doe",
                profile_url="https://invalid.com/profile"
            )
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        recipient = Recipient(
            first_name="John",
            last_name="Doe",
            profile_url="https://www.linkedin.com/in/johndoe/",
            company="TechCorp"
        )
        data = recipient.to_dict()
        assert data['first_name'] == "John"
        assert data['company'] == "TechCorp"


class TestMessageLog:
    """Test MessageLog data model"""
    
    def test_valid_message_log(self):
        """Test creating valid message log"""
        log = MessageLog(
            recipient_name="John Doe",
            profile_url="https://www.linkedin.com/in/johndoe/",
            timestamp=datetime.now(),
            status="sent"
        )
        assert log.status == "sent"
        assert log.recipient_name == "John Doe"
    
    def test_failed_message_log(self):
        """Test failed message log with error"""
        log = MessageLog(
            recipient_name="Jane Smith",
            profile_url="https://www.linkedin.com/in/janesmith/",
            timestamp=datetime.now(),
            status="failed",
            error_message="Network error"
        )
        assert log.status == "failed"
        assert log.error_message == "Network error"
    
    def test_invalid_status(self):
        """Test that invalid status raises error"""
        with pytest.raises(ValueError, match="Status must be one of"):
            MessageLog(
                recipient_name="Test",
                profile_url="https://www.linkedin.com/in/test/",
                timestamp=datetime.now(),
                status="invalid_status"
            )
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        timestamp = datetime.now()
        log = MessageLog(
            recipient_name="John Doe",
            profile_url="https://www.linkedin.com/in/johndoe/",
            timestamp=timestamp,
            status="sent",
            message_content="Hello John!"
        )
        data = log.to_dict()
        assert data['recipient_name'] == "John Doe"
        assert data['status'] == "sent"
        assert 'timestamp' in data


class TestConfig:
    """Test Config data model"""
    
    def test_valid_config(self):
        """Test creating valid configuration"""
        config = Config(
            linkedin_email="test@example.com",
            linkedin_password="password123",
            message_templates=["Template 1"],
            daily_limit=50,
            session_limit=10,
            max_connections=10,
            min_delay=30,
            max_delay=120,
            typing_speed=5,
            page_load_min=2,
            page_load_max=5,
            log_level="INFO",
            log_file="logs.csv",
            enable_circuit_breaker=True,
            max_consecutive_failures=3,
            retry_attempts=3
        )
        assert config.linkedin_email == "test@example.com"
        assert config.daily_limit == 50
    
    def test_invalid_email(self):
        """Test that invalid email raises error"""
        with pytest.raises(ValueError, match="Valid LinkedIn email is required"):
            Config(
                linkedin_email="invalid_email",
                linkedin_password="password",
                message_templates=["Template"],
                daily_limit=50,
                session_limit=10,
                max_connections=10,
                min_delay=30,
                max_delay=120,
                typing_speed=5,
                page_load_min=2,
                page_load_max=5,
                log_level="INFO",
                log_file="logs.csv",
                enable_circuit_breaker=True,
                max_consecutive_failures=3,
                retry_attempts=3
            )
    
    def test_empty_templates(self):
        """Test that empty templates raises error"""
        with pytest.raises(ValueError, match="At least one message template is required"):
            Config(
                linkedin_email="test@example.com",
                linkedin_password="password",
                message_templates=[],
                daily_limit=50,
                session_limit=10,
                max_connections=10,
                min_delay=30,
                max_delay=120,
                typing_speed=5,
                page_load_min=2,
                page_load_max=5,
                log_level="INFO",
                log_file="logs.csv",
                enable_circuit_breaker=True,
                max_consecutive_failures=3,
                retry_attempts=3
            )