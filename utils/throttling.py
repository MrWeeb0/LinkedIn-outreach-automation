"""Throttling utilities for human-like delays"""

import time
import random
from typing import Tuple


class Throttler:
    """Implements human-like delays to avoid detection"""
    
    def __init__(self, min_delay: int = 30, max_delay: int = 120, 
                 typing_speed: int = 5, page_load_range: Tuple[int, int] = (2, 5)):
        """
        Initialize throttler with delay parameters
        
        Args:
            min_delay: Minimum seconds between messages
            max_delay: Maximum seconds between messages
            typing_speed: Characters typed per second
            page_load_range: Min and max seconds for page load delays
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.typing_speed = typing_speed
        self.page_load_min, self.page_load_max = page_load_range
    
    def human_delay(self) -> float:
        """
        Generate random delay between min and max to mimic human behavior
        
        Returns:
            Delay in seconds
        """
        delay = random.uniform(self.min_delay, self.max_delay)
        return delay
    
    def typing_delay(self, message_length: int) -> float:
        """
        Calculate delay based on message length to simulate typing
        
        Args:
            message_length: Number of characters in message
            
        Returns:
            Delay in seconds
        """
        base_delay = message_length / self.typing_speed
        # Add random variance (±20%)
        variance = base_delay * random.uniform(-0.2, 0.2)
        return base_delay + variance
    
    def page_load_delay(self) -> float:
        """
        Generate random delay for page loading
        
        Returns:
            Delay in seconds
        """
        return random.uniform(self.page_load_min, self.page_load_max)
    
    def wait_human_delay(self) -> None:
        """Execute human-like delay (blocking)"""
        delay = self.human_delay()
        print(f"Waiting {delay:.1f} seconds before next action...")
        time.sleep(delay)
    
    def wait_typing_delay(self, message_length: int) -> None:
        """Execute typing delay (blocking)"""
        delay = self.typing_delay(message_length)
        print(f"Simulating typing for {delay:.1f} seconds...")
        time.sleep(delay)
    
    def wait_page_load(self) -> None:
        """Execute page load delay (blocking)"""
        delay = self.page_load_delay()
        time.sleep(delay)
    
    @staticmethod
    def exponential_backoff(attempt: int, base_delay: int = 5, max_delay: int = 300) -> float:
        """
        Calculate exponential backoff delay for retries
        
        Args:
            attempt: Retry attempt number (0-indexed)
            base_delay: Base delay in seconds
            max_delay: Maximum delay cap
            
        Returns:
            Delay in seconds
        """
        delay = min(base_delay * (2 ** attempt), max_delay)
        # Add jitter
        jitter = delay * random.uniform(0, 0.1)
        return delay + jitter