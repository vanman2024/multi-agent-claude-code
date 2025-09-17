#!/usr/bin/env python3
"""
Test reveal API directly to see actual data structure
"""

import asyncio
import json
import os
from src.services.signalhire_client import SignalHireClient
from src.lib.config import load_config

async def test_reveal_api():
    """Test the reveal API with a few UIDs to see actual data structure"""
    
    # Load configuration
    config = load_config(validate_credentials=False)
    
    # Get API key from environment
    api_key = os.getenv('SIGNALHIRE_API_KEY')
    if not api_key:
        print("❌ No SIGNALHIRE_API_KEY found in environment")
        print("   Set your API key: export SIGNALHIRE_API_KEY='your_key'")
        return
    
    # Initialize client
    client = SignalHireClient(api_key=api_key)
    
    # Test UIDs from our search results
    test_uids = [
        "e17660b36f354dbda6ca2d85a4116c14",  # Frederick Valbuena
        "73759185058e4966aa642b4a95cc9497",  # Nilsson Gonsalves 
        "1c32a3647d84493c9daddc047d24eae4"   # Karthikeyan Jayasuriyakumar
    ]
    
    print(f"🧪 Testing reveal API with {len(test_uids)} prospects...")
    print("📋 Test prospects:")
    print("  1. Frederick Valbuena - Montreal, Quebec, Canada")
    print("  2. Nilsson Gonsalves - Mississauga, Ontario, Canada") 
    print("  3. Karthikeyan Jayasuriyakumar - North York, Ontario, Canada")
    print()
    
    # Set up callback URL (you can use a test service like webhook.site)
    callback_url = "https://webhook.site/unique-id-here"  # Replace with actual URL
    
    try:
        for i, uid in enumerate(test_uids, 1):
            print(f"🔍 Revealing contact {i}: {uid}")
            
            # Use the Person API endpoint
            response = await client.reveal_contact_by_identifier(uid, callback_url)
            
            if response.success:
                print(f"✅ Request successful!")
                print(f"   Request ID: {response.data}")
                print(f"   Credits used: {response.credits_used}")
                print(f"   Credits remaining: {response.credits_remaining}")
            else:
                print(f"❌ Request failed: {response.error}")
                print(f"   Status code: {response.status_code}")
            
            print()
            
            # Small delay to respect rate limits
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("💡 Note: Results will be sent to your callback URL asynchronously")
    print("   Check your webhook.site or callback server for the actual contact data")

if __name__ == "__main__":
    asyncio.run(test_reveal_api())