"""Messaging module for sending LinkedIn messages"""

import random
import time
from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from core.models import Recipient
from utils.placeholders import PlaceholderReplacer
from utils.throttling import Throttler


class MessageTemplate:
    """Manages message templates and selection"""
    
    def __init__(self, templates: List[str]):
        if not templates:
            raise ValueError("At least one template is required")
        self.templates = templates
        self.replacer = PlaceholderReplacer()
    
    def get_random_template(self) -> str:
        """Select a random template for variation"""
        return random.choice(self.templates)
    
    def apply_template(self, recipient: Recipient, template: Optional[str] = None) -> str:
        """
        Apply template with recipient data
        
        Args:
            recipient: Recipient data
            template: Specific template or None for random selection
            
        Returns:
            Personalized message
        """
        if template is None:
            template = self.get_random_template()
        
        return self.replacer.replace_placeholders(template, recipient)
    
    def validate_template(self, template: str) -> List[str]:
        """Validate template placeholders"""
        return self.replacer.validate_placeholders(template)


class MessageSender:
    """Core messaging functionality for LinkedIn"""
    
    def __init__(self, driver, throttler: Throttler, template_manager: MessageTemplate):
        self.driver = driver
        self.throttler = throttler
        self.template_manager = template_manager
        self.messages_sent = 0
    
    def send_message(self, recipient: Recipient) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Send personalized message to recipient
        
        Args:
            recipient: Recipient to message
            
        Returns:
            Tuple of (success, message_content, error_message)
        """
        try:
            # Validate recipient
            if not self.validate_recipient(recipient):
                return False, None, "Invalid recipient data"
            
            # Generate personalized message
            message = self.template_manager.apply_template(recipient)
            
            # Navigate to profile
            if not self._navigate_to_profile(recipient.profile_url):
                return False, message, "Failed to navigate to profile"
            
            # Click message button
            if not self._click_message_button():
                return False, message, "Could not find message button"
            
            # Type and send message
            if not self._type_and_send_message(message):
                return False, message, "Failed to send message"
            
            self.messages_sent += 1
            return True, message, None
            
        except Exception as e:
            return False, None, str(e)
    
    def validate_recipient(self, recipient: Recipient) -> bool:
        """
        Validate recipient has required data
        
        Args:
            recipient: Recipient to validate
            
        Returns:
            True if valid
        """
        try:
            # Recipient dataclass validates on init
            return True
        except Exception:
            return False
    
    def _navigate_to_profile(self, profile_url: str) -> bool:
        """Navigate to recipient's LinkedIn profile"""
        try:
            self.driver.get(profile_url)
            self.throttler.wait_page_load()
            
            # Verify we're on a profile page
            return '/in/' in self.driver.current_url
            
        except Exception as e:
            print(f"Navigation error: {str(e)}")
            return False
    
    def _click_message_button(self) -> bool:
        """Find and click the message button"""
        try:
            # Try multiple selectors as LinkedIn's UI varies
            selectors = [
                "//button[contains(@class, 'message-anywhere-button')]",
                "//button[contains(., 'Message')]",
                "//a[contains(@href, '/messaging/thread/')]"
            ]
            
            for selector in selectors:
                try:
                    message_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    message_btn.click()
                    time.sleep(2)
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Message button error: {str(e)}")
            return False
    
    def _type_and_send_message(self, message: str) -> bool:
        """Type message and send"""
        try:
            # Wait for message compose box
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.msg-form__contenteditable"))
            )
            
            # Click to focus
            message_box.click()
            time.sleep(1)
            
            # Simulate typing with human-like delays
            self._type_with_delays(message_box, message)
            
            # Wait a moment before sending
            time.sleep(1)
            
            # Find and click send button
            send_btn = self.driver.find_element(By.CSS_SELECTOR, "button.msg-form__send-button")
            send_btn.click()
            
            # Wait to confirm send
            time.sleep(2)
            
            return True
            
        except TimeoutException:
            print("Timeout waiting for message box")
            return False
        except NoSuchElementException:
            print("Could not find send button")
            return False
        except Exception as e:
            print(f"Messaging error: {str(e)}")
            return False
    
    def _type_with_delays(self, element, text: str) -> None:
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            # Small random delay between characters
            time.sleep(random.uniform(0.05, 0.15))
    
    def get_message_count(self) -> int:
        """Get count of messages sent"""
        return self.messages_sent