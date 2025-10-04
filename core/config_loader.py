"""Configuration loader for LinkedIn outreach automation"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from core.models import Config


class ConfigLoader:
    """Loads and validates application configuration"""
    
    def __init__(self, env_file: str = '.env', settings_file: str = 'config/settings.yaml'):
        self.env_file = env_file
        self.settings_file = settings_file
        self._config = None
    
    def load(self) -> Config:
        """Load configuration from environment and settings files"""
        # Load environment variables
        load_dotenv(self.env_file)
        
        # Load settings YAML
        settings = self._load_settings()
        
        # Create Config object
        self._config = Config(
            linkedin_email=os.getenv('LINKEDIN_EMAIL', ''),
            linkedin_password=os.getenv('LINKEDIN_PASSWORD', ''),
            message_templates=settings['messaging']['templates'],
            daily_limit=settings['linkedin']['limits']['daily_messages'],
            session_limit=settings['linkedin']['limits']['session_messages'],
            max_connections=settings['linkedin']['limits']['max_connections'],
            min_delay=settings['messaging']['delays']['min_seconds'],
            max_delay=settings['messaging']['delays']['max_seconds'],
            typing_speed=settings['messaging']['delays']['typing_speed_chars_per_second'],
            page_load_min=settings['messaging']['delays']['page_load_min'],
            page_load_max=settings['messaging']['delays']['page_load_max'],
            log_level=settings['logging']['level'],
            log_file=settings['logging']['log_file'],
            enable_circuit_breaker=settings['safety']['enable_circuit_breaker'],
            max_consecutive_failures=settings['safety']['max_consecutive_failures'],
            retry_attempts=settings['linkedin']['limits']['retry_attempts']
        )
        
        return self._config
    
    def _load_settings(self) -> dict:
        """Load settings from YAML file"""
        settings_path = Path(self.settings_file)
        
        if not settings_path.exists():
            raise FileNotFoundError(f"Settings file not found: {self.settings_file}")
        
        with open(settings_path, 'r') as f:
            settings = yaml.safe_load(f)
        
        # Validate required keys
        required_keys = ['linkedin', 'messaging', 'logging', 'safety']
        for key in required_keys:
            if key not in settings:
                raise ValueError(f"Missing required section in settings: {key}")
        
        return settings
    
    @property
    def config(self) -> Config:
        """Get loaded configuration"""
        if self._config is None:
            raise RuntimeError("Configuration not loaded. Call load() first.")
        return self._config