"""Placeholder replacement utility for message templates"""

import re
from typing import Dict, List
from core.models import Recipient


class PlaceholderReplacer:
    """Handles dynamic variable replacement in message templates"""
    
    SUPPORTED_PLACEHOLDERS = [
        'first_name',
        'last_name',
        'company',
        'position',
        'location'
    ]
    
    @staticmethod
    def replace_placeholders(template: str, recipient: Recipient) -> str:
        """
        Replace all placeholders in template with recipient data
        
        Args:
            template: Message template with {placeholder} syntax
            recipient: Recipient object with data to insert
            
        Returns:
            Message with all placeholders replaced
        """
        message = template
        
        # Build replacement dictionary
        replacements = {
            'first_name': recipient.first_name,
            'last_name': recipient.last_name,
            'company': recipient.company or 'your company',
            'position': recipient.position or 'your field',
            'location': recipient.location or 'your area'
        }
        
        # Replace each placeholder
        for placeholder, value in replacements.items():
            pattern = f'{{{placeholder}}}'
            message = message.replace(pattern, value)
        
        return message
    
    @staticmethod
    def validate_placeholders(template: str) -> List[str]:
        """
        Validate placeholders in template and return list of invalid ones
        
        Args:
            template: Message template to validate
            
        Returns:
            List of invalid placeholder names (empty if all valid)
        """
        # Find all placeholders in template
        placeholders = re.findall(r'\{(\w+)\}', template)
        
        # Check which ones are not supported
        invalid = [p for p in placeholders 
                  if p not in PlaceholderReplacer.SUPPORTED_PLACEHOLDERS]
        
        return invalid
    
    @staticmethod
    def get_available_placeholders() -> List[str]:
        """
        Get list of all supported placeholder variables
        
        Returns:
            List of supported placeholder names
        """
        return PlaceholderReplacer.SUPPORTED_PLACEHOLDERS.copy()
    
    @staticmethod
    def get_missing_data(template: str, recipient: Recipient) -> List[str]:
        """
        Identify which required placeholders have missing data
        
        Args:
            template: Message template
            recipient: Recipient to check
            
        Returns:
            List of placeholder names with missing data
        """
        placeholders = re.findall(r'\{(\w+)\}', template)
        missing = []
        
        for placeholder in placeholders:
            value = getattr(recipient, placeholder, None)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing.append(placeholder)
        
        return missing