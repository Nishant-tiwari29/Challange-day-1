# 🎤 TTS API Server with Murf Integration

A FastAPI server that provides a REST endpoint for text-to-speech conversion using Murf's TTS API.

## 🚀 Features

- **Text-to-Speech Conversion**: Convert text to audio using Murf's AI voices
- **RESTful API**: Clean, documented API endpoints
- **Interactive Documentation**: Auto-generated Swagger UI at `/docs`
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Ready for frontend integration
- **Async Processing**: Fast, non-blocking API calls

## 📁 Project Structure

```
├── fastapi_app.py          # Main FastAPI server
├── test_tts.py            # Test script for the API
├── requirements_fastapi.txt # Python dependencies
├── README_TTS.md          # This documentation
└── app.py                 # Original Flask app (unchanged)
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements_fastapi.txt
```

### 2. Get Murf API Key

1. Sign up at [Murf.ai](https://murf.ai)
2. Navigate to your account settings
3. Generate an API key
4. Set it as an environment variable:

**Windows:**
```cmd
set MURF_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export MURF_API_KEY=your_api_key_here
```

### 3. Start the Server

```bash
python fastapi_app.py
```

The server will start on `http://localhost:8000`

## 📚 API Documentation

### Interactive Docs
Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

### Endpoints

#### `GET /`
Returns basic server information.

**Response:**
```json
{
  "message": "TTS API Server is running!",
  "endpoints": {
    "POST /tts/generate": "Generate audio from text using Murf TTS",
    "GET /docs": "Interactive API documentation"
  }
}
```

#### `POST /tts/generate`
Converts text to speech using Murf's TTS API.

**Request Body:**
```json
{
  "text": "Hello, this is a test message!",
  "voice_id": "en-US-Neural2-F",
  "speed": 0,
  "pitch": 0
}
```

**Parameters:**
- `text` (required): Text to convert to speech (max 5000 characters)
- `voice_id` (optional): Voice ID for the TTS (default: "en-US-Neural2-F")
- `speed` (optional): Speed adjustment (-10 to 10, default: 0)
- `pitch` (optional): Pitch adjustment (-20 to 20, default: 0)

**Success Response:**
```json
{
  "success": true,
  "audio_url": "https://api.murf.ai/audio/abc123.mp3",
  "message": "Audio generated successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here",
  "message": "Failed to generate audio"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "TTS API Server"
}
```

## 🧪 Testing

### Using the Test Script

```bash
python test_tts.py
```

### Using cURL

```bash
curl -X POST "http://localhost:8000/tts/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, this is a test!",
       "voice_id": "en-US-Neural2-F"
     }'
```

### Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:8000/tts/generate`
3. Set Content-Type header to `application/json`
4. Add request body:
```json
{
  "text": "Hello, this is a test message!",
  "voice_id": "en-US-Neural2-F"
}
```
5. Send the request

### Using the Interactive Docs

1. Open `http://localhost:8000/docs` in your browser
2. Click on the `POST /tts/generate` endpoint
3. Click "Try it out"
4. Enter your test data
5. Click "Execute"

## 🔧 Configuration

### Environment Variables

- `MURF_API_KEY`: Your Murf API key (required)

### Server Configuration

The server runs on:
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `8000`
- **Debug**: Enabled for development

To change these settings, modify the last lines in `fastapi_app.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

## 🎯 Use Cases

- **Content Creation**: Generate audio for videos, podcasts, presentations
- **Accessibility**: Convert text content to audio for visually impaired users
- **Language Learning**: Create pronunciation guides and language lessons
- **E-learning**: Generate audio narration for educational content
- **Customer Service**: Create automated voice responses

## 🔒 Security Considerations

- **API Key Protection**: Never commit your API key to version control
- **Input Validation**: Text length is limited to 5000 characters
- **Rate Limiting**: Consider implementing rate limiting for production use
- **CORS**: Configure CORS origins for production deployment

## 🚨 Error Handling

The API handles various error scenarios:

- **Missing API Key**: Returns 500 error with clear message
- **Invalid Input**: Returns 400 error for empty or too-long text
- **Network Errors**: Handles timeouts and connection issues
- **Murf API Errors**: Forwards error messages from Murf's API

## 📈 Production Deployment

For production deployment:

1. **Use a production ASGI server** like Gunicorn with Uvicorn workers
2. **Set up proper logging**
3. **Configure environment variables** securely
4. **Implement rate limiting**
5. **Set up monitoring and health checks**
6. **Use HTTPS** for secure communication

Example production command:
```bash
gunicorn fastapi_app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check that your Murf API key is set correctly
2. Verify the server is running on the correct port
3. Check the server logs for error messages
4. Ensure you have the required dependencies installed

For Murf API issues, refer to their [official documentation](https://docs.murf.ai). 