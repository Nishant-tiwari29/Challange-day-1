from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import os
from typing import Optional

app = FastAPI(
    title="TTS API Server",
    description="A FastAPI server that integrates with Murf's TTS API",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = "en-US-Neural2-F"  # Default voice
    speed: Optional[int] = 0  # Speed adjustment (-10 to 10)
    pitch: Optional[int] = 0  # Pitch adjustment (-20 to 20)

class TTSResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    error: Optional[str] = None
    message: str

@app.get("/")
async def root():
    """Root endpoint - returns basic info about the API"""
    return {
        "message": "TTS API Server is running!",
        "endpoints": {
            "POST /tts/generate": "Generate audio from text using Murf TTS",
            "GET /docs": "Interactive API documentation"
        }
    }

@app.post("/tts/generate", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    Generate audio from text using Murf's TTS API
    
    This endpoint accepts text input and returns a URL to the generated audio file.
    You'll need to set your Murf API key as an environment variable: MURF_API_KEY
    """
    
    # Get API key from environment variable
    api_key = os.getenv("MURF_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="MURF_API_KEY environment variable not set. Please set your Murf API key."
        )
    
    # Validate text input
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:  # Reasonable limit
        raise HTTPException(status_code=400, detail="Text too long. Maximum 5000 characters.")
    
    try:
        # Prepare the request payload for Murf API
        payload = {
            "text": request.text,
            "voice_id": request.voice_id,
            "speed": request.speed,
            "pitch": request.pitch
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make request to Murf's TTS API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.murf.ai/v1/tts/generate",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the audio URL from Murf's response
                # Note: The exact response structure may vary based on Murf's API
                audio_url = result.get("audio_url") or result.get("url") or result.get("download_url")
                
                if audio_url:
                    return TTSResponse(
                        success=True,
                        audio_url=audio_url,
                        message="Audio generated successfully"
                    )
                else:
                    return TTSResponse(
                        success=False,
                        error="No audio URL found in response",
                        message="Failed to extract audio URL from Murf response"
                    )
            else:
                error_detail = f"Murf API error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", error_detail)
                except:
                    pass
                
                return TTSResponse(
                    success=False,
                    error=error_detail,
                    message=f"Failed to generate audio. Status: {response.status_code}"
                )
                
    except httpx.TimeoutException:
        return TTSResponse(
            success=False,
            error="Request timeout",
            message="Request to Murf API timed out"
        )
    except httpx.RequestError as e:
        return TTSResponse(
            success=False,
            error=str(e),
            message="Network error occurred while calling Murf API"
        )
    except Exception as e:
        return TTSResponse(
            success=False,
            error=str(e),
            message="Unexpected error occurred"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "TTS API Server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 