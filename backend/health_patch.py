from backend.main import app
from fastapi.responses import JSONResponse

@app.get("/health", status_code=200)
def health():
    return JSONResponse({"status": "ok"})
