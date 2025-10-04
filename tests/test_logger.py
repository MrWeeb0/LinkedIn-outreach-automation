"""Unit tests for logging module"""

import pytest
import tempfile
import csv
from pathlib import Path
from core.logger import OutreachLogger
from core.models import Recipient


class TestOutreachLogger:
    """Test outreach logging functionality"""
    
    @pytest.fixture
    def temp_log_file(self):
        """Create temporary log file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
    
    @pytest.fixture
    def logger(self, temp_log_file):
        """Create logger instance with temp file"""
        return OutreachLogger(log_file=temp_log_file)
    
    @pytest.fixture
    def sample_recipient(self):
        """Create sample recipient for testing"""
        return Recipient(
            first_name="John",
            last_name="Doe",
            profile_url="https://www.linkedin.com/in/johndoe/",
            company="TechCorp"
        )
    
    def test_logger_initialization(self, temp_log_file):
        """Test logger creates log file with headers"""
        logger = OutreachLogger(log_file=temp_log_file)
        
        assert Path(temp_log_file).exists()
        
        # Check headers
        with open(temp_log_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert 'recipient_name' in headers
            assert 'status' in headers
    
    def test_log_message_sent(self, logger, sample_recipient, temp_log_file):
        """Test logging successful message"""
        message = "Hi John!"
        logger.log_message_sent(sample_recipient, message, template_used="template1")
        
        assert logger.get_message_count() == 1
        assert len(logger.logs) == 1
        assert logger.logs[0].status == 'sent'
        
        # Verify file content
        with open(temp_log_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]['status'] == 'sent'
            assert rows[0]['recipient_name'] == 'John Doe'
    
    def test_log_message_failed(self, logger, sample_recipient, temp_log_file):
        """Test logging failed message"""
        error = "Network timeout"
        logger.log_message_failed(sample_recipient, error, message_content="Test")
        
        assert logger.get_failed_count() == 1
        assert logger.logs[0].status == 'failed'
        assert logger.logs[0].error_message == error
    
    def test_log_message_skipped(self, logger, sample_recipient):
        """Test logging skipped message"""
        reason = "Duplicate recipient"
        logger.log_message_skipped(sample_recipient, reason)
        
        assert logger.get_skipped_count() == 1
        assert logger.logs[0].status == 'skipped'
        assert logger.logs[0].error_message == reason
    
    def test_multiple_logs(self, logger, sample_recipient):
        """Test logging multiple events"""
        logger.log_message_sent(sample_recipient, "Message 1")
        logger.log_message_failed(sample_recipient, "Error 1")
        logger.log_message_skipped(sample_recipient, "Reason 1")
        
        assert len(logger.logs) == 3
        assert logger.get_message_count() == 1
        assert logger.get_failed_count() == 1
        assert logger.get_skipped_count() == 1
    
    def test_export_logs(self, logger, sample_recipient, temp_log_file):
        """Test exporting logs"""
        logger.log_message_sent(sample_recipient, "Test message")
        
        export_path = logger.export_logs()
        assert export_path == str(temp_log_file)
        assert Path(export_path).exists()
    
    def test_message_count_accuracy(self, logger, sample_recipient):
        """Test that message count only counts sent messages"""
        logger.log_message_sent(sample_recipient, "Message 1")
        logger.log_message_sent(sample_recipient, "Message 2")
        logger.log_message_failed(sample_recipient, "Error")
        logger.log_message_skipped(sample_recipient, "Skipped")
        
        assert logger.get_message_count() == 2