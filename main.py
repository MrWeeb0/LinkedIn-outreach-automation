"""Main entry point for LinkedIn outreach automation"""

import sys
import argparse
from pathlib import Path
from core.auth import LinkedInAuth
from core.config_loader import ConfigLoader
from core.logger import OutreachLogger
from core.messenger import MessageSender, MessageTemplate
from utils.csv_handler import CSVHandler
from utils.throttling import Throttler


class OutreachOrchestrator:
    """Orchestrates the complete outreach workflow"""
    
    def __init__(self):
        self.config = None
        self.auth = None
        self.logger = None
        self.csv_handler = None
        self.throttler = None
        self.messenger = None
        self.consecutive_failures = 0
    
    def run(self, dry_run: bool = False) -> bool:
        """
        Execute the complete outreach workflow
        
        Args:
            dry_run: If True, load and validate data without sending messages
            
        Returns:
            True if workflow completed successfully
        """
        try:
            print("\n" + "="*60)
            print("LINKEDIN OUTREACH AUTOMATION")
            print("="*60 + "\n")
            
            # Step 1: Load configuration
            if not self._load_configuration():
                return False
            
            # Step 2: Initialize components
            self._initialize_components()
            
            # Step 3: Load recipients
            recipients, errors = self._load_recipients()
            if not recipients:
                print("✗ No valid recipients to process")
                return False
            
            # Step 4: Print dry run info
            if dry_run:
                self._print_dry_run_info(recipients)
                return True
            
            # Step 5: Authenticate
            if not self._authenticate():
                return False
            
            # Step 6: Send messages
            self._send_messages(recipients)
            
            # Step 7: Print summary
            self.logger.print_summary()
            self.logger.export_logs()
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠ Process interrupted by user")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error: {str(e)}")
            return False
        finally:
            self._cleanup()
    
    def _load_configuration(self) -> bool:
        """Load and validate configuration"""
        try:
            print("Loading configuration...")
            config_loader = ConfigLoader()
            self.config = config_loader.load()
            print("✓ Configuration loaded\n")
            return True
        except FileNotFoundError as e:
            print(f"✗ Configuration file not found: {str(e)}")
            return False
        except ValueError as e:
            print(f"✗ Configuration error: {str(e)}")
            return False
        except Exception as e:
            print(f"✗ Failed to load configuration: {str(e)}")
            return False
    
    def _initialize_components(self) -> None:
        """Initialize all components"""
        self.logger = OutreachLogger(self.config.log_file)
        self.csv_handler = CSVHandler(max_connections=self.config.max_connections)
        self.throttler = Throttler(
            min_delay=self.config.min_delay,
            max_delay=self.config.max_delay,
            typing_speed=self.config.typing_speed,
            page_load_range=(self.config.page_load_min, self.config.page_load_max)
        )
    
    def _load_recipients(self) -> tuple:
        """Load and validate recipients from CSV"""
        try:
            print("Loading recipients from CSV...")
            recipients, errors = self.csv_handler.load_connections()
            
            if errors:
                print(f"\n⚠ Found {len(errors)} invalid entries:")
                for error in errors:
                    print(f"  - {error}")
                print()
            
            print(f"✓ Loaded {len(recipients)} valid recipient(s)\n")
            return recipients, errors
            
        except FileNotFoundError:
            print("✗ CSV file not found. Creating sample file...")
            self.csv_handler.create_sample_csv()
            print("  Please edit data/connections.csv and run again.")
            return [], []
        except Exception as e:
            print(f"✗ Error loading recipients: {str(e)}")
            return [], []
    
    def _authenticate(self) -> bool:
        """Authenticate to LinkedIn"""
        try:
            print("Authenticating to LinkedIn...")
            print("(Browser will open - do not close it)\n")
            
            self.auth = LinkedInAuth(
                email=self.config.linkedin_email,
                password=self.config.linkedin_password
            )
            
            if not self.auth.authenticate():
                print("✗ Authentication failed")
                return False
            
            print("✓ Authentication successful\n")
            return True
            
        except Exception as e:
            print(f"✗ Authentication error: {str(e)}")
            return False
    
    def _send_messages(self, recipients: list) -> None:
        """Send messages to all recipients"""
        template_manager = MessageTemplate(self.config.message_templates)
        self.messenger = MessageSender(
            driver=self.auth.get_driver(),
            throttler=self.throttler,
            template_manager=template_manager
        )
        
        print(f"Starting to send messages to {len(recipients)} recipient(s)...\n")
        print("-" * 60)
        
        for idx, recipient in enumerate(recipients, start=1):
            # Check session limit
            if self.messenger.get_message_count() >= self.config.session_limit:
                print(f"\n⚠ Session limit of {self.config.session_limit} messages reached")
                break
            
            # Check circuit breaker
            if self._check_circuit_breaker():
                print(f"\n⚠ Circuit breaker triggered after {self.consecutive_failures} consecutive failures")
                break
            
            print(f"\n[{idx}/{len(recipients)}] Processing: {recipient.full_name}")
            
            # Send message
            success, message, error = self.messenger.send_message(recipient)
            
            # Log result
            if success:
                self.logger.log_message_sent(recipient, message)
                self.consecutive_failures = 0
            else:
                self.logger.log_message_failed(recipient, error or "Unknown error", message)
                self.consecutive_failures += 1
            
            # Wait before next message (except for last one)
            if idx < len(recipients) and success:
                self.throttler.wait_human_delay()
        
        print("\n" + "-" * 60)
    
    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker should trigger"""
        if not self.config.enable_circuit_breaker:
            return False
        
        return self.consecutive_failures >= self.config.max_consecutive_failures
    
    def _print_dry_run_info(self, recipients: list) -> None:
        """Print information for dry run"""
        print("DRY RUN MODE - No messages will be sent\n")
        print(f"Recipients to process: {len(recipients)}")
        print("\nRecipient list:")
        for idx, recipient in enumerate(recipients, start=1):
            print(f"  {idx}. {recipient.full_name}")
            print(f"     Company: {recipient.company or 'N/A'}")
            print(f"     Position: {recipient.position or 'N/A'}")
            print(f"     Profile: {recipient.profile_url}")
        
        print(f"\nMessage templates: {len(self.config.message_templates)}")
        print(f"Session limit: {self.config.session_limit} messages")
        print(f"Delay range: {self.config.min_delay}-{self.config.max_delay} seconds")
    
    def _cleanup(self) -> None:
        """Cleanup resources"""
        if self.auth:
            self.auth.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='LinkedIn Outreach Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate configuration and data without sending messages'
    )
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample connections.csv file'
    )
    
    args = parser.parse_args()
    
    # Handle create sample
    if args.create_sample:
        csv_handler = CSVHandler()
        csv_handler.create_sample_csv()
        return 0
    
    # Run orchestrator
    orchestrator = OutreachOrchestrator()
    success = orchestrator.run(dry_run=args.dry_run)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())