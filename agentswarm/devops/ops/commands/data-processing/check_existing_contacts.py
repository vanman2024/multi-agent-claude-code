#!/usr/bin/env python3
"""
Check which prospects already have contact information vs need revealing
"""

import json

def analyze_contact_status():
    # Load search results
    with open('heavy_equipment_mechanics_canada_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    profiles = data.get('profiles', [])
    
    has_contacts = 0
    needs_reveal = 0
    has_contacts_list = []
    needs_reveal_list = []
    
    for profile in profiles:
        uid = profile.get('uid', '')
        name = profile.get('fullName', '')
        contacts_fetched = profile.get('contactsFetched')
        
        if contacts_fetched:
            has_contacts += 1
            has_contacts_list.append({
                'uid': uid,
                'name': name,
                'contactsFetched': contacts_fetched
            })
        else:
            needs_reveal += 1
            needs_reveal_list.append({
                'uid': uid,
                'name': name
            })
    
    print(f"📊 Contact Status Analysis")
    print(f"   Total prospects: {len(profiles)}")
    print(f"   ✅ Already have contacts: {has_contacts}")
    print(f"   🔍 Need revealing: {needs_reveal}")
    print(f"   💰 Credits needed: {needs_reveal}")
    print()
    
    if needs_reveal > 0:
        print(f"🎯 You need {needs_reveal} credits to reveal all remaining contacts")
        print(f"   You have 1333 credits, so you can reveal {min(1333, needs_reveal)} contacts")
        
        if needs_reveal > 1333:
            print(f"   ⚠️  You'll need {needs_reveal - 1333} more credits for complete coverage")
    
    # Save lists for processing
    with open('prospects_need_reveal.json', 'w', encoding='utf-8') as f:
        json.dump(needs_reveal_list, f, indent=2, ensure_ascii=False)
    
    with open('prospects_have_contacts.json', 'w', encoding='utf-8') as f:
        json.dump(has_contacts_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Saved files:")
    print(f"   - prospects_need_reveal.json ({needs_reveal} prospects)")
    print(f"   - prospects_have_contacts.json ({has_contacts} prospects)")
    
    return {
        'total': len(profiles),
        'has_contacts': has_contacts,
        'needs_reveal': needs_reveal,
        'can_afford': min(1333, needs_reveal)
    }

if __name__ == "__main__":
    analyze_contact_status()