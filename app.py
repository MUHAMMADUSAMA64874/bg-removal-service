from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import io
from rembg import new_session, remove
from PIL import Image
import time
import os

app = FastAPI(title="Background Removal Service", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the default model session once
SESSION = new_session("u2net")

# Basic protections
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp", "image/tiff"}
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "your-secret-token")  # Use env var

@app.post("/remove-bg")
async def remove_background(
    file: UploadFile = File(...),
    token: str = None,
    authorization: str = Header(None)
):
    # Auth check
    if token is None and authorization is not None:
        if authorization.lower().startswith("bearer "):
            token = authorization[7:]
        else:
            token = authorization

    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # Check mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        # Process with rembg using a shared u2net session
        start_time = time.time()
        output = remove(file_content, session=SESSION)
        processing_time = time.time() - start_time

        # Convert to PIL Image to ensure PNG format
        output_image = Image.open(io.BytesIO(output))

        # Save as PNG
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return StreamingResponse(
            io.BytesIO(output_buffer.getvalue()),
            media_type="image/png",
            headers={"Processing-Time": f"{processing_time:.2f}s"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)