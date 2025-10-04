"""CSV handler for loading and validating connection data"""

import csv
from pathlib import Path
from typing import List, Tuple
from core.models import Recipient


class CSVHandler:
    """Handles loading and validating recipient data from CSV"""
    
    def __init__(self, csv_file: str = 'data/connections.csv', max_connections: int = 10):
        self.csv_file = Path(csv_file)
        self.max_connections = max_connections
    
    def load_connections(self) -> Tuple[List[Recipient], List[str]]:
        """
        Load connections from CSV file
        
        Returns:
            Tuple of (valid_recipients, error_messages)
        """
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
        recipients = []
        errors = []
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Validate headers
            required_headers = ['first_name', 'last_name', 'profile_url']
            if not all(header in reader.fieldnames for header in required_headers):
                raise ValueError(f"CSV must contain headers: {', '.join(required_headers)}")
            
            for idx, row in enumerate(reader, start=1):
                # Stop at max connections
                if len(recipients) >= self.max_connections:
                    print(f"⚠ Maximum of {self.max_connections} connections reached. Remaining entries skipped.")
                    break
                
                # Validate and create recipient
                recipient, error = self._parse_row(row, idx)
                
                if recipient:
                    recipients.append(recipient)
                else:
                    errors.append(error)
        
        return recipients, errors
    
    def _parse_row(self, row: dict, row_num: int) -> Tuple[Recipient, str]:
        """
        Parse a CSV row into a Recipient object
        
        Args:
            row: Dictionary from CSV row
            row_num: Row number for error reporting
            
        Returns:
            Tuple of (Recipient or None, error_message or None)
        """
        try:
            # Strip whitespace from all fields
            cleaned = {k: v.strip() if v else '' for k, v in row.items()}
            
            recipient = Recipient(
                first_name=cleaned.get('first_name', ''),
                last_name=cleaned.get('last_name', ''),
                profile_url=cleaned.get('profile_url', ''),
                company=cleaned.get('company') or None,
                position=cleaned.get('position') or None,
                location=cleaned.get('location') or None
            )
            
            return recipient, None
            
        except ValueError as e:
            error_msg = f"Row {row_num}: {str(e)}"
            return None, error_msg
        except Exception as e:
            error_msg = f"Row {row_num}: Unexpected error - {str(e)}"
            return None, error_msg
    
    def create_sample_csv(self) -> None:
        """Create a sample CSV file with example data"""
        self.csv_file.parent.mkdir(parents=True, exist_ok=True)
        
        sample_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'profile_url': 'https://www.linkedin.com/in/johndoe/',
                'company': 'TechCorp',
                'position': 'Software Engineer',
                'location': 'San Francisco, CA'
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'profile_url': 'https://www.linkedin.com/in/janesmith/',
                'company': 'DataCo',
                'position': 'Data Scientist',
                'location': 'New York, NY'
            }
        ]
        
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'first_name', 'last_name', 'profile_url', 
                'company', 'position', 'location'
            ])
            writer.writeheader()
            writer.writerows(sample_data)
        
        print(f"✓ Sample CSV created at: {self.csv_file}")
        print(f"  Add your connections and replace the sample data.")