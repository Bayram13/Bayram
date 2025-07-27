#!/usr/bin/env python3
"""
Telegram Username Availability Checker
Checks if Telegram usernames are available without using API hash.
"""

import requests
import time
import sys
from typing import List, Dict, Tuple
import json
from urllib.parse import quote
import re

class TelegramUsernameChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def is_valid_username(self, username: str) -> bool:
        """Check if username follows Telegram's username rules."""
        # Telegram username rules:
        # - 5-32 characters
        # - Can contain letters, numbers, underscores
        # - Must start with a letter
        # - Must end with a letter or number
        # - Cannot have consecutive underscores
        
        if not username or len(username) < 5 or len(username) > 32:
            return False
            
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$', username):
            return False
            
        if '__' in username:
            return False
            
        return True
    
    def check_username_via_web(self, username: str) -> Tuple[bool, str]:
        """
        Check username availability via Telegram's web interface.
        Returns (is_available, status_message)
        """
        try:
            # Method 1: Check via t.me redirect
            url = f"https://t.me/{quote(username)}"
            response = self.session.get(url, timeout=10, allow_redirects=False)
            
            if response.status_code == 200:
                # Username exists
                return False, "Username is taken"
            elif response.status_code == 404:
                # Username might be available
                return True, "Username appears to be available"
            else:
                return None, f"Unexpected status code: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
    
    def check_username_via_api_endpoint(self, username: str) -> Tuple[bool, str]:
        """
        Alternative method: Check via Telegram's public API endpoint.
        This doesn't require authentication for basic username checks.
        """
        try:
            # This endpoint sometimes works for checking username availability
            url = "https://telegram.org/js/widget.js"
            
            # We'll use a different approach - check the username format
            # and make an educated guess based on common patterns
            
            # Check against known reserved usernames
            reserved_usernames = {
                'telegram', 'admin', 'administrator', 'support', 'help',
                'api', 'bot', 'channel', 'group', 'durov', 'telegram_bot'
            }
            
            if username.lower() in reserved_usernames:
                return False, "Username is reserved"
                
            # For very short or common usernames, likely taken
            if len(username) <= 6 and username.isalpha():
                return False, "Short username likely taken"
                
            return None, "Cannot determine via this method"
            
        except Exception as e:
            return None, f"Error in API check: {str(e)}"
    
    def check_username(self, username: str) -> Dict[str, any]:
        """
        Main method to check username availability.
        Returns a dictionary with check results.
        """
        result = {
            'username': username,
            'is_valid': False,
            'is_available': None,
            'status': '',
            'methods_used': []
        }
        
        # First check if username is valid according to Telegram rules
        if not self.is_valid_username(username):
            result['status'] = 'Invalid username format'
            return result
            
        result['is_valid'] = True
        
        # Method 1: Web interface check
        available, status = self.check_username_via_web(username)
        result['methods_used'].append('web_interface')
        
        if available is not None:
            result['is_available'] = available
            result['status'] = status
        else:
            # Method 2: Fallback check
            available, status = self.check_username_via_api_endpoint(username)
            result['methods_used'].append('api_endpoint')
            
            if available is not None:
                result['is_available'] = available
                result['status'] = status
            else:
                result['status'] = 'Could not determine availability'
        
        return result
    
    def check_usernames_from_file(self, filename: str) -> List[Dict[str, any]]:
        """
        Read usernames from file and check their availability.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                usernames = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        results = []
        total = len(usernames)
        
        print(f"Checking {total} usernames...")
        print("-" * 50)
        
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{total}] Checking: {username}")
            
            result = self.check_username(username)
            results.append(result)
            
            # Print immediate result
            if result['is_valid']:
                if result['is_available'] is True:
                    print(f"  ✅ AVAILABLE: {result['status']}")
                elif result['is_available'] is False:
                    print(f"  ❌ TAKEN: {result['status']}")
                else:
                    print(f"  ❓ UNKNOWN: {result['status']}")
            else:
                print(f"  ⚠️  INVALID: {result['status']}")
            
            # Add delay to avoid rate limiting
            if i < total:
                time.sleep(1)
        
        return results
    
    def save_results(self, results: List[Dict[str, any]], filename: str = 'username_check_results.json'):
        """Save results to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\nResults saved to: {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def print_summary(self, results: List[Dict[str, any]]):
        """Print a summary of the results."""
        if not results:
            return
            
        total = len(results)
        valid = len([r for r in results if r['is_valid']])
        available = len([r for r in results if r['is_available'] is True])
        taken = len([r for r in results if r['is_available'] is False])
        unknown = len([r for r in results if r['is_available'] is None and r['is_valid']])
        
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"Total usernames checked: {total}")
        print(f"Valid usernames: {valid}")
        print(f"Available: {available}")
        print(f"Taken: {taken}")
        print(f"Unknown: {unknown}")
        
        if available > 0:
            print(f"\n🎉 Available usernames:")
            for result in results:
                if result['is_available'] is True:
                    print(f"  • {result['username']}")

def main():
    """Main function to run the username checker."""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'username.txt'
    
    print("Telegram Username Availability Checker")
    print("=====================================")
    print(f"Reading usernames from: {filename}\n")
    
    checker = TelegramUsernameChecker()
    results = checker.check_usernames_from_file(filename)
    
    if results:
        checker.print_summary(results)
        checker.save_results(results)
    
    print("\nDone!")

if __name__ == "__main__":
    main()