import csv
import re
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Clean up the lines and remove empty ones at the end
lines = [line.rstrip('\n') for line in lines if line.strip()]

data = []
i = 0

while i < len(lines):
    line = lines[i].strip()
    
    # Skip headers and page markers
    if (line.startswith('Company Summary') or 
        line.startswith('=====') or 
        line.startswith('Page') or 
        line.startswith('Total OPVH') or
        line.startswith('Monday, March 30, 2026') or
        line == 'Company Name' or
        'Contact Name' in line or
        'Address' in line):
        i += 1
        continue
    
    # Check if this looks like a company line (doesn't start with space AND has content)
    # Use the original line (with spaces preserved) to check indentation
    original_line = lines[i]
    
    # Company line: first character is NOT a space
    if len(original_line) > 0 and original_line[0] != ' ':
        # This is line 1 - Company, Address, Phone
        # Split by 2 or more spaces
        parts = re.split(r' {2,}', original_line)
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) >= 3:
            company = parts[0]
            address = parts[1]
            phone = parts[2]
            
            # Look ahead to line 2 (should start with spaces)
            if i + 1 < len(lines):
                next_original = lines[i + 1]
                
                # Check if next line starts with space (contact line)
                if len(next_original) > 0 and next_original[0] == ' ':
                    # Split line 2 by 2 or more spaces
                    parts2 = re.split(r' {2,}', next_original)
                    parts2 = [p.strip() for p in parts2 if p.strip()]
                    
                    contact = parts2[0] if len(parts2) > 0 else ''
                    city_state_zip = parts2[1] if len(parts2) > 1 else ''
                    
                    permits = ''
                    exp_date = ''
                    
                    # Handle permits and expiration date (could be in positions 2 and 3)
                    if len(parts2) > 2:
                        # Check if it looks like a date
                        if re.search(r'\d{1,2}/\d{1,2}/\d{4}', parts2[2]):
                            exp_date = parts2[2]
                        else:
                            permits = parts2[2]
                    if len(parts2) > 3:
                        if re.search(r'\d{1,2}/\d{1,2}/\d{4}', parts2[3]):
                            exp_date = parts2[3]
                        elif not permits and re.search(r'\d', parts2[3]):
                            permits = parts2[3]
                    
                    data.append([company, address, phone, contact, city_state_zip, permits, exp_date])
                    i += 2  # Skip the next line since we used it
                    continue
    i += 1

print(f"Found {len(data)} companies")

if data:
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Company Name', 'Address', 'Phone Number', 'Contact Name', 'City / State / Zip', 'Permits', 'Exp. Date'])
        writer.writerows(data)
    print("Saved opvh_export.csv")
    
    # Show first 5 rows as preview
    print("\nFirst 5 rows preview:")
    for row in data[:5]:
        print(f"  Company: {row[0][:40]}...")
        print(f"    Address: {row[1]}")
        print(f"    Phone: {row[2]}")
        print(f"    Contact: {row[3]}")
        print(f"    City: {row[4]}")
        print(f"    Expires: {row[6]}")
        print()
else:
    print("No data found - checking file structure...")
    # Debug: show first 10 lines with visible spaces
    print("\nFirst 10 lines of file (showing spaces as dots):")
    for idx in range(min(10, len(lines))):
        visible = lines[idx].replace(' ', '·')
        print(f"{idx}: '{visible}'")
