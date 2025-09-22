# 📚 CompanionAI API Reference

## 🔗 Base URL
```
http://localhost:8000
```

## 📋 Table of Contents
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## 🔐 Authentication
Currently, no authentication is required for API access in the development environment.

## 🎯 Endpoints

### 1. Main Troubleshooting Endpoint

#### `POST /answer`
Get AI-powered troubleshooting assistance for appliance issues.

**Request Body:**
```json
{
  "question": "string",
  "brand": "string (optional)",
  "model": "string (optional)"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/answer" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "My washing machine won't drain water",
       "brand": "Samsung",
       "model": "WF42H5200"
     }'
```

**Response:**
```json
{
  "answer": "string",
  "safety_flag": "boolean",
  "safety_level": "safe|caution|danger|emergency",
  "safety_message": "string (optional)",
  "sources": [
    {
      "filename": "string",
      "page": "integer",
      "relevance_score": "float",
      "content": "string"
    }
  ],
  "processing_time": "float",
  "error_code_info": {
    "code": "string",
    "brand": "string",
    "appliance_type": "string",
    "description": "string",
    "immediate_actions": ["string"],
    "troubleshooting_steps": ["string"],
    "estimated_repair_cost": "string"
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error

### 2. Health Check Endpoint

#### `GET /health`
Check the health status of the API server.

**Example Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-19T23:15:30.123456",
  "version": "1.0.0",
  "components": {
    "companion_ai": "ready",
    "safety_checker": "ready",
    "vector_database": "ready"
  }
}
```

### 3. API Documentation

#### `GET /docs`
Interactive Swagger UI documentation.

#### `GET /redoc`
Alternative ReDoc documentation.

## 📊 Data Models

### Question Request
```python
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    brand: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=100)
```

### Answer Response
```python
class AnswerResponse(BaseModel):
    answer: str
    safety_flag: bool = False
    safety_level: str = "safe"
    safety_message: Optional[str] = None
    sources: List[Source] = []
    processing_time: float
    error_code_info: Optional[ErrorCodeInfo] = None
```

### Source Information
```python
class Source(BaseModel):
    filename: str
    page: Optional[int] = None
    relevance_score: float
    content: str
```

### Error Code Information
```python
class ErrorCodeInfo(BaseModel):
    code: str
    brand: str
    appliance_type: str
    description: str
    safety_level: str
    immediate_actions: List[str]
    troubleshooting_steps: List[str]
    common_causes: List[str]
    prevention_tips: List[str]
    when_to_call_professional: List[str]
    estimated_repair_cost: Optional[str] = None
    difficulty_level: str = "beginner"
```

## ⚠️ Error Handling

### Error Response Format
```json
{
  "detail": "string",
  "error_code": "string",
  "timestamp": "string",
  "path": "string"
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `INVALID_INPUT` | Invalid or missing required fields |
| 400 | `QUESTION_TOO_LONG` | Question exceeds maximum length |
| 400 | `EMPTY_QUESTION` | Question field is empty |
| 500 | `AI_SERVICE_ERROR` | CompanionAI service unavailable |
| 500 | `VECTOR_SEARCH_ERROR` | Vector database error |
| 500 | `SAFETY_CHECK_ERROR` | Safety checker service error |

### Error Examples

**400 Bad Request:**
```json
{
  "detail": "Question field cannot be empty",
  "error_code": "EMPTY_QUESTION",
  "timestamp": "2025-09-19T23:15:30.123456",
  "path": "/answer"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "CompanionAI service temporarily unavailable",
  "error_code": "AI_SERVICE_ERROR", 
  "timestamp": "2025-09-19T23:15:30.123456",
  "path": "/answer"
}
```

## 🚦 Rate Limiting

### Current Limits
- **Requests per minute**: 60
- **Requests per hour**: 1000
- **Concurrent requests**: 10

### Rate Limit Headers
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995200
```

### Rate Limit Exceeded Response
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds.",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

## 💡 Usage Examples

### Basic Troubleshooting
```python
import requests

response = requests.post(
    "http://localhost:8000/answer",
    json={
        "question": "My dishwasher is not cleaning dishes properly",
        "brand": "Bosch",
        "model": "SHPM65W55N"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Answer: {data['answer']}")
    print(f"Safety Level: {data['safety_level']}")
else:
    print(f"Error: {response.status_code}")
```

### Error Code Lookup
```python
import requests

response = requests.post(
    "http://localhost:8000/answer",
    json={
        "question": "E3 error code on my Samsung washing machine",
        "brand": "Samsung"
    }
)

data = response.json()
if data.get('error_code_info'):
    error_info = data['error_code_info']
    print(f"Error Code: {error_info['code']}")
    print(f"Description: {error_info['description']}")
    print("Immediate Actions:")
    for action in error_info['immediate_actions']:
        print(f"  - {action}")
```

### Safety-Critical Query
```python
import requests

response = requests.post(
    "http://localhost:8000/answer",
    json={
        "question": "I smell gas from my oven and hear clicking sounds"
    }
)

data = response.json()
if data['safety_flag']:
    print(f"⚠️ SAFETY ALERT: {data['safety_level'].upper()}")
    print(f"Message: {data['safety_message']}")
    print(f"Answer: {data['answer']}")
```

### Health Check
```python
import requests

response = requests.get("http://localhost:8000/health")
data = response.json()

print(f"API Status: {data['status']}")
print("Component Status:")
for component, status in data['components'].items():
    print(f"  {component}: {status}")
```

## 🔧 SDK Examples

### Python SDK
```python
class CompanionAIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def ask_question(self, question, brand=None, model=None):
        """Ask a troubleshooting question"""
        payload = {"question": question}
        if brand:
            payload["brand"] = brand
        if model:
            payload["model"] = model
            
        response = requests.post(
            f"{self.base_url}/answer",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

# Usage
client = CompanionAIClient()
result = client.ask_question(
    "My microwave turntable is not rotating",
    brand="LG",
    model="MS2595DIS"
)
```

### JavaScript SDK
```javascript
class CompanionAIClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async askQuestion(question, brand = null, model = null) {
        const payload = { question };
        if (brand) payload.brand = brand;
        if (model) payload.model = model;
        
        const response = await fetch(`${this.baseUrl}/answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/health`);
        return await response.json();
    }
}

// Usage
const client = new CompanionAIClient();
const result = await client.askQuestion(
    'My vacuum cleaner has lost suction power',
    'Bosch',
    'BGL72294'
);
```

## 📈 Response Time Guidelines

### Expected Response Times
- **Simple queries**: < 1 second
- **Complex troubleshooting**: 1-3 seconds
- **Error code lookup**: < 2 seconds
- **Safety-critical queries**: < 1 second (priority)

### Performance Optimization Tips
1. **Specify brand/model** for faster, more accurate results
2. **Be specific** in your questions for better relevance
3. **Use error codes** when available for instant lookup
4. **Avoid very long questions** (> 500 characters)

## 🛡️ Safety Considerations

### Safety Response Handling
Always check the `safety_flag` and `safety_level` in responses:

```python
def handle_response(response_data):
    if response_data['safety_flag']:
        safety_level = response_data['safety_level']
        
        if safety_level == 'emergency':
            # Handle emergency - show immediate warning
            show_emergency_alert(response_data['safety_message'])
        elif safety_level == 'danger':
            # Show danger warning
            show_danger_warning(response_data['safety_message'])
        elif safety_level == 'caution':
            # Show caution notice
            show_caution_notice(response_data['safety_message'])
    
    # Display the answer
    display_answer(response_data['answer'])
```

---

**Next**: See [USER-GUIDE.md](./USER-GUIDE.md) for end-user documentation.