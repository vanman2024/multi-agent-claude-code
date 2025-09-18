#!/usr/bin/env python3
"""
Create a small test sample of 10 prospects for reveal testing
"""

import json

def create_test_sample():
    # Load the full data
    with open('heavy_equipment_mechanics_canada_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Take first 10 prospects
    test_data = {
        'requestId': data['requestId'],
        'total': 10,
        'profiles': data['profiles'][:10]
    }
    
    # Save test sample
    with open('test_sample_10_prospects.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Created test sample with 10 prospects: test_sample_10_prospects.json")
    print("\n📋 Test prospects:")
    for i, profile in enumerate(test_data['profiles'], 1):
        print(f"  {i}. {profile['fullName']} - {profile['location']}")
        print(f"     UID: {profile['uid']}")

if __name__ == "__main__":
    create_test_sample()