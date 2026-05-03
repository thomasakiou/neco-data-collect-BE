import csv
from collections import defaultdict

def update_csv():
    input_file = 'nigeria_lgas.csv'
    output_file = 'nigeria_lgas_updated.csv'
    
    # Read the data
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Group by state_code
    state_groups = defaultdict(list)
    for row in data:
        state_groups[row['state_code']].append(row)
    
    updated_data = []
    
    # Sort state_codes to keep some consistency
    sorted_state_codes = sorted(state_groups.keys())
    
    for state_code in sorted_state_codes:
        # Sort LGAs alphabetically within the state
        # The prompt says: "followed by 3 digit from 001 to the last lga in that state alphabetically"
        lgas = sorted(state_groups[state_code], key=lambda x: x['LGA'])
        
        for i, row in enumerate(lgas, 1):
            # Generate lga_code: state_code (3 digits) + sequence (3 digits)
            # Ensure state_code is padded to 3 digits just in case
            sc = str(row['state_code']).zfill(3)
            seq = str(i).zfill(3)
            row['lga_code'] = f"{sc}{seq}"
            updated_data.append(row)
    
    # Write the updated data back
    fieldnames = ['State', 'state_code', 'LGA', 'lga_code']
    with open(input_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_data)
    
    print(f"Updated {len(updated_data)} rows in {input_file}")

if __name__ == "__main__":
    update_csv()
