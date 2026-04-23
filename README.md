# PDF/Text Parser for Unstructured Company Reports

## What
A Python script that parses multi-line text reports with inconsistent formatting and extracts structured data (company name, address, phone, contact, city/state/zip, permits, expiration dates).

## Why
Demonstrates ability to:
- Extract data from unstructured text
- Handle irregular formatting (inconsistent spacing, page headers, line breaks)
- Convert messy reports into clean CSV for analysis
- Apply pattern matching and edge case handling

## How It Works
The script:
1. Reads a text file (exported from PDF or other source)
2. Identifies line patterns based on indentation and content
3. Splits fields using multi-space delimiters
4. Handles edge cases like missing data or varying field order
5. Outputs a structured CSV file

## Key Techniques
- Regex pattern matching (`re.split(r' {2,}', line)`)
- Line-by-line state tracking
- Indentation-based parsing (space detection)
- Date pattern detection

## Files
- `parser.py` — Main extraction script
- `sample_input.txt` — Example of the expected text format (synthetic data)
- `sample_output.csv` — Example of the structured output

## Sample Input Format
```
Company Name                123 Main St, City           (555) 123-4567
  Contact Person            City, State 12345          PERMIT123        04/15/2026
```

## Sample Output
| Company Name | Address | Phone | Contact | City/State/Zip | Permits | Exp Date |
|--------------|---------|-------|---------|----------------|---------|----------|
| Example Co   | 123 Main St | (555) 123-4567 | Contact Person | City, State 12345 | PERMIT123 | 04/15/2026 |

## How to Run
```bash
python parser.py
```

## Limitations
- Assumes consistent delimiter (2+ spaces)
- Requires text extraction from PDF before parsing
- Designed for specific report structure

## Real-World Application
This script was developed for a real-world data extraction task. The original data cannot be shared due to privacy and ethical considerations. The methodology is demonstrated using synthetic data.
