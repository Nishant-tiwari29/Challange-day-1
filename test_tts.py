#!/usr/bin/env python3
"""
Test script for the TTS API endpoint
This script demonstrates how to call the TTS endpoint programmatically
"""

import requests
import json
import os

def test_tts_endpoint():
    """Test the TTS endpoint with sample text"""
    
    # API endpoint URL (assuming server is running on localhost:8000)
    url = "http://localhost:8000/tts/generate"
    
    # Sample text to convert to speech
    sample_text = "Hello! This is a test of the text-to-speech API. Welcome to our demo!"
    
    # Request payload
    payload = {
        "text": sample_text,
        "voice_id": "en-US-Neural2-F",  # Default voice
        "speed": 0,  # Normal speed
        "pitch": 0   # Normal pitch
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Testing TTS Endpoint...")
        print(f"📝 Text: {sample_text}")
        print(f"🌐 URL: {url}")
        print("-" * 50)
        
        # Make the request
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        print("-" * 50)
        
        # Parse and display the response
        if response.status_code == 200:
            result = response.json()
            print("✅ Success Response:")
            print(json.dumps(result, indent=2))
            
            if result.get("success") and result.get("audio_url"):
                print(f"\n🎵 Audio URL: {result['audio_url']}")
                print("🔗 You can open this URL in a browser to play the audio!")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
        else:
            print("❌ Error Response:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(f"Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
        print("💡 Start the server with: python fastapi_app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_without_api_key():
    """Test the endpoint without setting the API key (should show error)"""
    
    url = "http://localhost:8000/tts/generate"
    payload = {
        "text": "This test should fail because no API key is set"
    }
    
    try:
        print("\n🔑 Testing without API key...")
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print("Response:", response.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("🎤 TTS API Test Script")
    print("=" * 50)
    
    # Test the main endpoint
    test_tts_endpoint()
    
    # Test without API key
    test_without_api_key()
    
    print("\n" + "=" * 50)
    print("📝 Instructions:")
    print("1. Set your Murf API key: export MURF_API_KEY='your_api_key_here'")
    print("2. Start the server: python fastapi_app.py")
    print("3. Run this test: python test_tts.py")
    print("4. Or use the interactive docs at: http://localhost:8000/docs") 