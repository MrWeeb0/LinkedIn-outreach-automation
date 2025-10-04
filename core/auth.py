"""Authentication module for LinkedIn session management"""

import pickle
import time
from pathlib import Path
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent


class LinkedInAuth:
    """Manages LinkedIn authentication and session persistence"""
    
    def __init__(self, email: str, password: str, session_file: str = 'data/session.pkl'):
        self.email = email
        self.password = password
        self.session_file = Path(session_file)
        self.driver: Optional[webdriver.Chrome] = None
        self._authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate to LinkedIn using credentials or saved session
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Initialize Chrome driver
            self._init_driver()
            
            # Try to load existing session first
            if self._load_session():
                print("✓ Loaded existing session")
                if self._verify_session():
                    self._authenticated = True
                    return True
                else:
                    print("Session expired, logging in again...")
            
            # Perform fresh login
            success = self._login()
            if success:
                self._save_session()
                self._authenticated = True
                print("✓ Authentication successful")
            
            return success
            
        except Exception as e:
            print(f"✗ Authentication failed: {str(e)}")
            return False
    
    def _init_driver(self) -> None:
        """Initialize Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set random user agent
        ua = UserAgent()
        options.add_argument(f'user-agent={ua.random}')
        
        # Uncomment to run headless
        # options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def _login(self) -> bool:
        """
        Perform LinkedIn login
        
        Returns:
            True if login successful
        """
        try:
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            # Wait for redirect to feed (indicates successful login)
            WebDriverWait(self.driver, 15).until(
                EC.url_contains('/feed')
            )
            
            return True
            
        except TimeoutException:
            print("Login timeout - check credentials or handle CAPTCHA manually")
            return False
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False
    
    def _verify_session(self) -> bool:
        """
        Verify that current session is still valid
        
        Returns:
            True if session is valid
        """
        try:
            self.driver.get('https://www.linkedin.com/feed')
            time.sleep(3)
            
            # Check if we're still logged in
            return '/feed' in self.driver.current_url
            
        except Exception:
            return False
    
    def _save_session(self) -> None:
        """Save cookies to file for session persistence"""
        try:
            self.session_file.parent.mkdir(parents=True, exist_ok=True)
            cookies = self.driver.get_cookies()
            with open(self.session_file, 'wb') as f:
                pickle.dump(cookies, f)
            print("✓ Session saved")
        except Exception as e:
            print(f"Warning: Could not save session: {str(e)}")
    
    def _load_session(self) -> bool:
        """
        Load cookies from file
        
        Returns:
            True if session loaded successfully
        """
        try:
            if not self.session_file.exists():
                return False
            
            self.driver.get('https://www.linkedin.com')
            time.sleep(2)
            
            with open(self.session_file, 'rb') as f:
                cookies = pickle.load(f)
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            return True
            
        except Exception as e:
            print(f"Could not load session: {str(e)}")
            return False
    
    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated
        
        Returns:
            True if authenticated
        """
        return self._authenticated and self.driver is not None
    
    def get_driver(self) -> webdriver.Chrome:
        """
        Get the Chrome WebDriver instance
        
        Returns:
            Chrome WebDriver
        """
        if not self.is_authenticated():
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self.driver
    
    def close(self) -> None:
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            self._authenticated = False
            print("✓ Browser closed")