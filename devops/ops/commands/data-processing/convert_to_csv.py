#!/usr/bin/env python3
"""
Convert Heavy Equipment Mechanics JSON to CSV with LinkedIn URL column
"""

import json
import csv
from pathlib import Path

def convert_json_to_csv():
    # Load the JSON data
    with open('heavy_equipment_mechanics_canada_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prepare CSV output
    output_file = 'heavy_equipment_mechanics_canada_all.csv'
    
    # Define CSV columns matching SignalHire export format
    fieldnames = [
        'Id',
        'First Name',
        'Last Name', 
        'Position',
        'Company',
        'Location',
        'Summary',
        'Personal Email1',
        'Personal Email2',
        'Years of Experience',
        'Skill',
        'Education Degree1',
        'Education Faculty1',
        'Education University1',
        'Education Started1',
        'Education Ended1',
        'LinkedIn Link',
        'Twitter Link', 
        'Facebook Link',
        'Instagram Link'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for profile in data.get('profiles', []):
            # Get current experience (first one is usually current)
            current_company = ""
            current_title = ""
            years_experience = ""
            if profile.get('experience'):
                current_exp = profile['experience'][0]
                current_company = current_exp.get('company', '')
                current_title = current_exp.get('title', '')
                years_experience = str(len(profile.get('experience', [])))
            
            # Split full name into first and last
            full_name = profile.get('fullName', '') or ''
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Join skills into comma-separated string (like SignalHire format)
            skills_str = ', '.join(profile.get('skills', []))
            
            # Get first education entry if available
            education = profile.get('education', [])
            education_degree = education[0].get('degree', '') if education else ''
            education_faculty = education[0].get('faculty', '') if education else ''
            education_university = education[0].get('university', '') if education else ''
            education_started = education[0].get('startedYear', '') if education else ''
            education_ended = education[0].get('endedYear', '') if education else ''
            
            row = {
                'Id': profile.get('uid', ''),
                'First Name': first_name,
                'Last Name': last_name,
                'Position': current_title,
                'Company': current_company,
                'Location': profile.get('location', ''),
                'Summary': '',  # Empty for now, would be filled from reveals
                'Personal Email1': '',  # Empty for now, will be filled during contact reveals
                'Personal Email2': '',  # Empty for now, will be filled during contact reveals
                'Years of Experience': years_experience,
                'Skill': skills_str,
                'Education Degree1': education_degree,
                'Education Faculty1': education_faculty,
                'Education University1': education_university,
                'Education Started1': education_started,
                'Education Ended1': education_ended,
                'LinkedIn Link': '',  # Empty for now, will be filled during contact reveals
                'Twitter Link': '',   # Empty for now, will be filled during contact reveals
                'Facebook Link': '',  # Empty for now, will be filled during contact reveals
                'Instagram Link': ''  # Empty for now, will be filled during contact reveals
            }
            
            writer.writerow(row)
    
    print(f"✅ Successfully converted {len(data.get('profiles', []))} profiles to {output_file}")
    print(f"📊 Total prospects found: {data.get('total', 0)}")
    print(f"🔍 Request ID: {data.get('requestId', 'N/A')}")
    
    return output_file

if __name__ == "__main__":
    convert_json_to_csv()