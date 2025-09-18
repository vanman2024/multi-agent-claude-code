#!/usr/bin/env python3
"""
Simple callback server to capture reveal webhook data
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI(title="Simple Reveal Callback Server")

@app.post("/callback")
async def receive_callback(request: Request):
    """Receive and save callback data"""
    
    # Get the raw JSON data
    try:
        data = await request.json()
    except Exception as e:
        data = {"error": f"Failed to parse JSON: {e}", "raw": await request.body()}
    
    # Save the callback data with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"callback_data_{timestamp}.json"
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📥 Received callback data - saved to: {filename}")
    print(f"🔍 Data preview:")
    print(json.dumps(data, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, indent=2))
    print()
    
    return {"status": "received", "timestamp": timestamp, "file": filename}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Simple callback server for SignalHire reveals",
        "endpoint": "/callback"
    }

if __name__ == "__main__":
    print("🚀 Starting simple callback server...")
    print("📡 Callback endpoint: http://localhost:8001/callback")
    print("💡 Use this URL in your reveal tests")
    print("📁 Callback data will be saved as JSON files")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8001)