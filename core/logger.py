"""Logging module for tracking outreach activity"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from core.models import MessageLog, Recipient


class OutreachLogger:
    """Centralized logging for all messaging activity"""
    
    def __init__(self, log_file: str = 'data/logs.csv'):
        self.log_file = Path(log_file)
        self.logs: List[MessageLog] = []
        self._ensure_log_file()
    
    def _ensure_log_file(self) -> None:
        """Ensure log file and directory exist"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.log_file.exists():
            # Create with headers
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'recipient_name', 'profile_url', 'timestamp', 
                    'status', 'error_message', 'template_used', 'message_preview'
                ])
                writer.writeheader()
    
    def log_message_sent(self, recipient: Recipient, message_content: str, 
                        template_used: Optional[str] = None) -> None:
        """
        Log a successfully sent message
        
        Args:
            recipient: Recipient who received the message
            message_content: The actual message sent
            template_used: Template identifier if applicable
        """
        log = MessageLog(
            recipient_name=recipient.full_name,
            profile_url=recipient.profile_url,
            timestamp=datetime.now(),
            status='sent',
            template_used=template_used,
            message_content=message_content
        )
        self._add_log(log)
        print(f"✓ Message sent to {recipient.full_name}")
    
    def log_message_failed(self, recipient: Recipient, error: str, 
                          message_content: Optional[str] = None) -> None:
        """
        Log a failed message attempt
        
        Args:
            recipient: Recipient for whom the message failed
            error: Error message or reason for failure
            message_content: The message that failed to send
        """
        log = MessageLog(
            recipient_name=recipient.full_name,
            profile_url=recipient.profile_url,
            timestamp=datetime.now(),
            status='failed',
            error_message=error,
            message_content=message_content
        )
        self._add_log(log)
        print(f"✗ Message failed for {recipient.full_name}: {error}")
    
    def log_message_skipped(self, recipient: Recipient, reason: str) -> None:
        """
        Log a skipped message
        
        Args:
            recipient: Recipient who was skipped
            reason: Reason for skipping
        """
        log = MessageLog(
            recipient_name=recipient.full_name,
            profile_url=recipient.profile_url,
            timestamp=datetime.now(),
            status='skipped',
            error_message=reason
        )
        self._add_log(log)
        print(f"⊘ Message skipped for {recipient.full_name}: {reason}")
    
    def _add_log(self, log: MessageLog) -> None:
        """Add log to memory and persist to file"""
        self.logs.append(log)
        self._write_log_to_file(log)
    
    def _write_log_to_file(self, log: MessageLog) -> None:
        """Write a single log entry to CSV file"""
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'recipient_name', 'profile_url', 'timestamp', 
                'status', 'error_message', 'template_used', 'message_preview'
            ])
            writer.writerow(log.to_dict())
    
    def get_message_count(self) -> int:
        """
        Get count of messages sent in current session
        
        Returns:
            Number of successfully sent messages
        """
        return sum(1 for log in self.logs if log.status == 'sent')
    
    def get_failed_count(self) -> int:
        """Get count of failed messages"""
        return sum(1 for log in self.logs if log.status == 'failed')
    
    def get_skipped_count(self) -> int:
        """Get count of skipped messages"""
        return sum(1 for log in self.logs if log.status == 'skipped')
    
    def export_logs(self, output_file: Optional[str] = None) -> str:
        """
        Export all logs to file (already done incrementally, but can create summary)
        
        Args:
            output_file: Optional different output file path
            
        Returns:
            Path to exported log file
        """
        export_path = output_file or str(self.log_file)
        print(f"\nLogs exported to: {export_path}")
        return export_path
    
    def print_summary(self) -> None:
        """Print summary statistics of the outreach session"""
        sent = self.get_message_count()
        failed = self.get_failed_count()
        skipped = self.get_skipped_count()
        total = len(self.logs)
        
        print("\n" + "="*50)
        print("OUTREACH SESSION SUMMARY")
        print("="*50)
        print(f"Total recipients processed: {total}")
        print(f"✓ Messages sent: {sent}")
        print(f"✗ Messages failed: {failed}")
        print(f"⊘ Messages skipped: {skipped}")
        print("="*50)