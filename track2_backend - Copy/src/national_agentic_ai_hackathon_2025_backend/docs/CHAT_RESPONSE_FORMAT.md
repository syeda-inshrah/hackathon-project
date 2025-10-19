# Chat API Response Format

## Overview

The chat API endpoints now return clean, focused responses that contain only the agent's answer to the current question, without including the entire chat history.

## Response Format

### General Chat Endpoint (`POST /api/v1/chat`)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -d "phone_number=+1234567890" \
  -d "message=I need help with my health"
```

**Response:**
```json
{
  "success": true,
  "message": "Message processed successfully",
  "data": {
    "phone_number": "+1234567890",
    "response": "I'd be happy to help you with your health concerns. Could you please tell me more about what specific health issues you're experiencing?",
    "total_messages": 2
  }
}
```

### Booking Chat Endpoint (`POST /api/v1/chat/booking`)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/booking" \
  -d "phone_number=+1234567890" \
  -d "message=I want to book an appointment for tomorrow at 2 PM"
```

**Response:**
```json
{
  "success": true,
  "message": "Booking message processed successfully",
  "data": {
    "phone_number": "+1234567890",
    "response": "I'd be happy to help you schedule an appointment. Let me check the availability for tomorrow at 2 PM. Could you please provide me with your name and the facility you'd like to visit?",
    "total_messages": 2
  }
}
```

## Key Changes

### Before (Old Format)
```json
{
  "success": true,
  "message": "Message processed successfully",
  "data": {
    "phone_number": "+1234567890",
    "user_message": {
      "content": "I need help with my health",
      "sender": "user",
      "type": "text",
      "timestamp": "2024-01-15T10:30:00"
    },
    "agent_response": {
      "content": "I'd be happy to help you...",
      "sender": "agent",
      "type": "text",
      "timestamp": "2024-01-15T10:30:05"
    },
    "total_messages": 2,
    "chat_history": [
      {
        "content": "I need help with my health",
        "sender": "user",
        "type": "text",
        "timestamp": "2024-01-15T10:30:00"
      },
      {
        "content": "I'd be happy to help you...",
        "sender": "agent",
        "type": "text",
        "timestamp": "2024-01-15T10:30:05"
      }
    ]
  }
}
```

### After (New Format)
```json
{
  "success": true,
  "message": "Message processed successfully",
  "data": {
    "phone_number": "+1234567890",
    "response": "I'd be happy to help you with your health concerns. Could you please tell me more about what specific health issues you're experiencing?",
    "total_messages": 2
  }
}
```

## Benefits

### ✅ **Cleaner Responses**
- Only returns the agent's answer to the current question
- No unnecessary chat history in the response
- Smaller payload size
- Easier to parse and display

### ✅ **Better Performance**
- Reduced response size
- Faster API responses
- Less bandwidth usage

### ✅ **Focused User Experience**
- Frontend can display just the agent's response
- No need to filter through chat history
- Cleaner UI implementation

### ✅ **Context Still Maintained**
- Chat history is still stored in the database
- AI agents still have access to conversation context
- Full conversation history available via `/chats/{phone_number}` endpoint

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Indicates if the request was successful |
| `message` | string | Status message |
| `data.phone_number` | string | User's phone number |
| `data.response` | string | Agent's response to the current question |
| `data.total_messages` | integer | Total number of messages in chat history |

## Error Responses

### User Not Found (404)
```json
{
  "detail": "User not found"
}
```

### Internal Server Error (500)
```json
{
  "detail": "Internal server error: [error message]"
}
```

## Accessing Chat History

If you need the full chat history, use the dedicated endpoint:

**GET** `/api/v1/chats/{phone_number}`

```json
{
  "success": true,
  "data": {
    "phone_number": "+1234567890",
    "messages": [
      {
        "content": "I need help with my health",
        "sender": "user",
        "type": "text",
        "timestamp": "2024-01-15T10:30:00"
      },
      {
        "content": "I'd be happy to help you...",
        "sender": "agent",
        "type": "text",
        "timestamp": "2024-01-15T10:30:05"
      }
    ],
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:05"
  }
}
```

## Frontend Integration

### Simple Display
```javascript
// Display just the agent's response
const response = await fetch('/api/v1/chat', {
  method: 'POST',
  body: new URLSearchParams({
    phone_number: '+1234567890',
    message: 'Hello'
  })
});

const data = await response.json();
if (data.success) {
  displayMessage(data.data.response);
}
```

### With Error Handling
```javascript
try {
  const response = await fetch('/api/v1/chat', {
    method: 'POST',
    body: new URLSearchParams({
      phone_number: '+1234567890',
      message: userInput
    })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Display agent response
    addMessageToChat(data.data.response, 'agent');
  } else {
    // Handle error
    showError(data.detail || 'An error occurred');
  }
} catch (error) {
  showError('Network error: ' + error.message);
}
```

## Testing

Run the test script to verify the new response format:

```bash
python src/national_agentic_ai_hackathon_2025_backend/scripts/test_clean_response.py
```

This will test both general chat and booking chat endpoints to ensure they return the clean response format.
