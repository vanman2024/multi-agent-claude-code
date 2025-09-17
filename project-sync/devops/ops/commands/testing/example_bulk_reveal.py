#!/usr/bin/env python3
"""
Example: How to do bulk contact reveals through the SignalHire CLI

This shows the complete workflow for bulk contact revelation:
1. Search for prospects
2. Extract UIDs from search results
3. Use Person API to reveal contacts in bulk
4. Handle callback results

This example demonstrates the CLI interface for bulk operations.
"""

import asyncio
import json
from src.services.signalhire_client import SignalHireClient
from src.lib.config import get_config

async def bulk_reveal_example():
    """Example of bulk contact reveal workflow using CLI-compatible methods."""
    print("🚀 SignalHire Bulk Contact Reveal Example")
    print("=" * 50)

    config = get_config()
    api_key = config.signalhire.api_key

    if not api_key:
        print("❌ No API key found! Set SIGNALHIRE_API_KEY environment variable.")
        return

    client = SignalHireClient(api_key=api_key)

    try:
        # Step 1: Search for prospects (like CLI search command)
        print("\n🔍 Step 1: Search for prospects...")
        search_criteria = {
            "currentTitle": "Heavy Equipment Mechanic",
            "location": "Canada",
            "keywords": "machinery OR equipment OR hydraulic"
        }

        search_response = await client.search_prospects(search_criteria, size=10)

        if not search_response.success:
            print(f"❌ Search failed: {search_response.error}")
            return

        profiles = search_response.data.get('profiles', [])
        print(f"✅ Found {len(profiles)} prospects to reveal")

        # Step 2: Extract UIDs for bulk reveal (like CLI would do)
        print("\n📋 Step 2: Extract prospect UIDs...")
        prospect_uids = []
        for profile in profiles:
            uid = profile.get('uid')
            name = profile.get('fullName', 'Unknown')
            title = profile.get('experience', [{}])[0].get('title', 'Unknown') if profile.get('experience') else 'Unknown'
            location = profile.get('location', 'Unknown')

            if uid:
                prospect_uids.append(uid)
                print(f"   • {name} - {title} - {location} [{uid}]")

        print(f"\n📊 Ready to reveal {len(prospect_uids)} contacts")

        # Step 3: Bulk reveal contacts (this is what CLI reveal bulk would do)
        print("\n📞 Step 3: Bulk reveal contacts via Person API...")

        # In real CLI usage, you would need a callback server running
        # For this example, we'll show the API call structure
        callback_url = "http://localhost:8000/callback"  # Your callback server

        reveal_requests = []
        for i, uid in enumerate(prospect_uids[:3]):  # Limit to 3 for example
            print(f"   📤 Sending reveal request {i+1} for UID: {uid}")

            # This is the Person API call the CLI would make
            response = await client.reveal_contact_by_identifier(uid, callback_url)

            if response.success:
                request_id = response.data.get('requestId')
                print(f"   ✅ Request {i+1} submitted successfully (ID: {request_id})")
                reveal_requests.append({
                    'uid': uid,
                    'request_id': request_id,
                    'status': 'submitted'
                })
            else:
                print(f"   ❌ Request {i+1} failed: {response.error}")

        # Step 4: Show what happens next (CLI would handle this automatically)
        print(f"\n🔄 Step 4: What happens next...")
        print(f"   1. SignalHire processes your {len(reveal_requests)} requests")
        print(f"   2. Results will be sent to: {callback_url}")
        print(f"   3. CLI callback server receives and saves contacts")
        print(f"   4. Final CSV/JSON export created automatically")

        print(f"\n📋 Request Summary:")
        for req in reveal_requests:
            print(f"   • UID {req['uid']} → Request {req['request_id']} ({req['status']})")

        # Show CLI commands that would achieve this
        print(f"\n💻 Equivalent CLI Commands:")
        print(f"   # Search")
        print(f'   signalhire search --title "Heavy Equipment Mechanic" --location "Canada" --output prospects.json')
        print(f"   ")
        print(f"   # Start callback server (separate terminal)")
        print(f"   signalhire callback-server start --port 8000")
        print(f"   ")
        print(f"   # Bulk reveal")
        print(f"   signalhire reveal bulk --search-file prospects.json --callback-url http://localhost:8000/callback --output contacts.csv")

    except Exception as e:
        print(f"💥 Error: {e}")
    finally:
        if client.session:
            await client.close_session()

if __name__ == "__main__":
    asyncio.run(bulk_reveal_example())
