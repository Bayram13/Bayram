# Telegram Username Availability Checker

A Python program that checks whether Telegram usernames are available without requiring an API hash or authentication.

## Features

- ✅ No API hash required
- ✅ Validates usernames according to Telegram's rules
- ✅ Checks availability via public endpoints
- ✅ Batch processing from text file
- ✅ JSON output with detailed results
- ✅ Rate limiting to avoid being blocked
- ✅ Comprehensive error handling

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

1. Create a `username.txt` file with one username per line:
   ```
   testuser123
   myawesomeusername
   availableusername2024
   ```

2. Run the checker:
   ```bash
   python telegram_username_checker.py
   ```

### Custom Input File

You can specify a different input file:
```bash
python telegram_username_checker.py my_usernames.txt
```

## How It Works

The program uses several methods to check username availability:

1. **Web Interface Check**: Makes HTTP requests to `t.me/username` to check if the username exists
2. **Pattern Analysis**: Checks against known reserved usernames and common patterns
3. **Validation**: Ensures usernames follow Telegram's rules:
   - 5-32 characters long
   - Start with a letter
   - End with a letter or number
   - Can contain letters, numbers, and underscores
   - No consecutive underscores

## Output

The program provides:
- Real-time progress with immediate results
- Summary statistics
- Detailed JSON file with all results (`username_check_results.json`)

### Example Output

```
Telegram Username Availability Checker
=====================================
Reading usernames from: username.txt

Checking 7 usernames...
--------------------------------------------------
[1/7] Checking: bymxd
  ❌ TAKEN: Username is taken
[2/7] Checking: telegram
  ❌ TAKEN: Username is reserved
[3/7] Checking: durov
  ❌ TAKEN: Short username likely taken
[4/7] Checking: elonmusk
  ❌ TAKEN: Username is taken
[5/7] Checking: testuser123
  ✅ AVAILABLE: Username appears to be available
[6/7] Checking: randomusername999
  ✅ AVAILABLE: Username appears to be available
[7/7] Checking: availableusername2024
  ✅ AVAILABLE: Username appears to be available

==================================================
SUMMARY
==================================================
Total usernames checked: 7
Valid usernames: 7
Available: 3
Taken: 4
Unknown: 0

🎉 Available usernames:
  • testuser123
  • randomusername999
  • availableusername2024

Results saved to: username_check_results.json

Done!
```

## Limitations

- This method doesn't use official Telegram APIs, so results may not be 100% accurate
- Rate limiting is implemented to avoid being blocked
- Some usernames might show as "unknown" if the check methods fail
- The program relies on public endpoints which may change over time

## Notes

- The program includes a 1-second delay between checks to avoid rate limiting
- Results are saved in JSON format for further processing
- Invalid usernames (not following Telegram's rules) are flagged appropriately

## License

This program is provided as-is for educational purposes. Use responsibly and respect Telegram's terms of service.