"""Data models for LinkedIn outreach automation"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import re


@dataclass
class Recipient:
    """Represents a LinkedIn connection recipient"""
    first_name: str
    last_name: str
    profile_url: str
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    
    def __post_init__(self):
        """Validate recipient data after initialization"""
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name is required")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name is required")
        if not self.profile_url or not self.profile_url.strip():
            raise ValueError("Profile URL is required")
        if not self._is_valid_url(self.profile_url):
            raise ValueError(f"Invalid LinkedIn profile URL: {self.profile_url}")
    
    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Check if URL is a valid LinkedIn profile URL"""
        pattern = r'^https?://(www\.)?linkedin\.com/in/[\w-]+/?$'
        return bool(re.match(pattern, url))
    
    @property
    def full_name(self) -> str:
        """Return full name of recipient"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> dict:
        """Convert recipient to dictionary"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_url': self.profile_url,
            'company': self.company or '',
            'position': self.position or '',
            'location': self.location or ''
        }


@dataclass
class MessageLog:
    """Represents a log entry for a sent message"""
    recipient_name: str
    profile_url: str
    timestamp: datetime
    status: str  # 'sent', 'failed', 'skipped'
    error_message: Optional[str] = None
    template_used: Optional[str] = None
    message_content: Optional[str] = None
    
    def __post_init__(self):
        """Validate message log data"""
        valid_statuses = ['sent', 'failed', 'skipped']
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
    
    def to_dict(self) -> dict:
        """Convert message log to dictionary for CSV export"""
        return {
            'recipient_name': self.recipient_name,
            'profile_url': self.profile_url,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'error_message': self.error_message or '',
            'template_used': self.template_used or '',
            'message_preview': self.message_content[:50] + '...' if self.message_content else ''
        }


@dataclass
class Config:
    """Application configuration"""
    linkedin_email: str
    linkedin_password: str
    message_templates: List[str]
    daily_limit: int
    session_limit: int
    max_connections: int
    min_delay: int
    max_delay: int
    typing_speed: int
    page_load_min: int
    page_load_max: int
    log_level: str
    log_file: str
    enable_circuit_breaker: bool
    max_consecutive_failures: int
    retry_attempts: int
    
    def __post_init__(self):
        """Validate configuration values"""
        if not self.linkedin_email or '@' not in self.linkedin_email:
            raise ValueError("Valid LinkedIn email is required")
        if not self.linkedin_password:
            raise ValueError("LinkedIn password is required")
        if not self.message_templates:
            raise ValueError("At least one message template is required")
        if self.daily_limit <= 0:
            raise ValueError("Daily limit must be positive")
        if self.min_delay < 0 or self.max_delay < self.min_delay:
            raise ValueError("Invalid delay configuration")