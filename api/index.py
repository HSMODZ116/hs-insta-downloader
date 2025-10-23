import re
import urllib.parse
import httpx
from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="HS Instagram Downloader", version="2.0")

DEVELOPER = "Haseeb Sahil"
POWERED_BY = "@hsmodzofc2"

@app.get("/")
async def download(request: Request, url: str = None):
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    encoded_url = urllib.parse.quote(url, safe="")
    target_url = f"https://snapdownloader.com/tools/instagram-reels-downloader/download?url={encoded_url}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(target_url, headers=headers)
            html = response.text if response.status_code == 200 else ""
    except Exception as e:
        # Catch all HTTP or network-related errors
        return {
            "status": "error",
            "message": f"Failed to fetch page: {str(e)}",
            "developer": DEVELOPER,
            "powered_by": POWERED_BY
        }

    if not html or "<html" not in html.lower():
        return {
            "status": "error",
            "message": "Invalid or empty HTML response received.",
            "developer": DEVELOPER,
            "powered_by": POWERED_BY
        }

    # --- Extract video URL ---
    video_match = re.search(r'<a[^>]+href="([^"]+\.mp4[^"]*)"', html)
    video_url = urllib.parse.unquote(video_match.group(1)) if video_match else None

    # --- Extract thumbnail ---
    thumb_match = re.search(r'<a[^>]+href="([^"]+\.jpg[^"]*)"', html)
    thumb_url = urllib.parse.unquote(thumb_match.group(1)) if thumb_match else None

    if video_url:
        return {
            "status": "success",
            "video": video_url,
            "thumbnail": thumb_url,
            "developer": DEVELOPER,
            "powered_by": POWERED_BY
        }

    return {
        "status": "error",
        "message": "Unable to extract video link. The source page may have changed.",
        "developer": DEVELOPER,
        "powered_by": POWERED_BY
    }

@app.get("/ping")
async def ping():
    return {
        "status": "ok",
        "message": "HS Instagram Downloader API running perfectly",
        "developer": DEVELOPER
    }