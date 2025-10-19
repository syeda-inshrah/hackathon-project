#!/usr/bin/env python3
"""
Test script to verify the chat route fix
"""

import asyncio
import aiohttp
import json

async def test_chat_fix():
    """Test the fixed chat endpoint"""
    print("🧪 Testing Chat Route Fix")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    test_phone = "+923092328094"
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Create user first
        print("\n1. Creating test user...")
        user_data = {
            "phone_number": test_phone,
            "username": "test_user",
            "platform": "website"
        }
        
        try:
            async with session.post(f"{base_url}/users", json=user_data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ User created: {result['message']}")
                elif response.status == 400:
                    print("ℹ️ User already exists (expected)")
                else:
                    print(f"❌ Failed to create user: {response.status}")
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return
        
        # Test 2: Test general chat endpoint
        print("\n2. Testing general chat endpoint...")
        test_messages = [
            "Hello, I need help",
            "I want to book an appointment",
            "Can you help me with my health?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n   Test {i}: {message}")
            try:
                async with session.post(
                    f"{base_url}/chat",
                    params={"phone_number": test_phone, "message": message}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"   ✅ Success! Agent response: {result['data']['agent_response']['content'][:100]}...")
                    else:
                        error_text = await response.text()
                        print(f"   ❌ Error {response.status}: {error_text}")
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        # Test 3: Test booking chat endpoint
        print("\n3. Testing booking chat endpoint...")
        booking_messages = [
            "I want to schedule an appointment",
            "What times are available tomorrow?",
            "Can you help me book a consultation?"
        ]
        
        for i, message in enumerate(booking_messages, 1):
            print(f"\n   Booking Test {i}: {message}")
            try:
                async with session.post(
                    f"{base_url}/chat/booking",
                    params={"phone_number": test_phone, "message": message}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"   ✅ Success! Booking response: {result['data']['agent_response']['content'][:100]}...")
                    else:
                        error_text = await response.text()
                        print(f"   ❌ Error {response.status}: {error_text}")
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        # Test 4: Get chat history
        print("\n4. Testing chat history retrieval...")
        try:
            async with session.get(f"{base_url}/chats/{test_phone}") as response:
                if response.status == 200:
                    result = await response.json()
                    messages = result['data']['messages']
                    print(f"   ✅ Retrieved {len(messages)} messages from chat history")
                    for msg in messages[-2:]:  # Show last 2 messages
                        print(f"   - {msg['sender']}: {msg['content'][:50]}...")
                else:
                    error_text = await response.text()
                    print(f"   ❌ Error: {response.status} - {error_text}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Chat route fix testing completed!")

if __name__ == "__main__":
    print("🚀 Testing Chat Route Fix")
    print("=" * 60)
    print("Note: Make sure the FastAPI server is running on localhost:8000")
    print("=" * 60)
    
    asyncio.run(test_chat_fix())
    
    print("\n🎉 Test completed!")
