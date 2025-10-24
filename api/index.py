import httpx
from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="HS Instagram Downloader (Fixed)", version="4.0")

API_BASE = "https://socialdownloader2.anshapi.workers.dev/?url="

@app.get("/")
async def download(request: Request, url: str = None):
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.get(API_BASE + url)
            data = res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch: {str(e)}")

    if data.get("statusCode") == 200:
        return {
            "status": "success",
            "video": data.get("url"),
            "title": data.get("title"),
            "thumbnail": data.get("thumbnail"),
            "developer": "Haseeb Sahil",
            "powered_by": "@hsmodzofc2"
        }

    return {
        "status": "error",
        "message": "Download link not found or site error.",
        "developer": "Haseeb Sahil",
        "powered_by": "@hsmodzofc2"
    }