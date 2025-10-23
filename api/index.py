import re
import httpx
import urllib.parse
from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="HS Instagram Downloader", version="3.0")

DEVELOPER = "Haseeb Sahil"
POWERED_BY = "@hsmodzofc2"

@app.get("/")
async def download(request: Request, url: str = None):
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    # --- Fix encoding bug (don’t double-encode hashes or params) ---
    safe_url = urllib.parse.quote(url, safe=":/?&=#")
    target_url = f"https://snapdownloader.com/tools/instagram-reels-downloader/download?url={safe_url}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        async with httpx.AsyncClient(timeout=40.0, follow_redirects=True) as client:
            res = await client.get(target_url, headers=headers)
            html = res.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    if not html or "<html" not in html.lower():
        return {
            "status": "error",
            "message": "Failed to load target HTML. Source site may be blocking requests.",
            "developer": DEVELOPER,
            "powered_by": POWERED_BY
        }

    # --- Extract video URL (.mp4) ---
    video_match = re.search(r'href="([^"]+\.mp4[^"]*)"', html)
    video_url = video_match.group(1) if video_match else None

    # --- Extract thumbnail (.jpg) ---
    thumb_match = re.search(r'href="([^"]+\.jpg[^"]*)"', html)
    thumb_url = thumb_match.group(1) if thumb_match else None

    if video_url:
        return {
            "status": "success",
            "video": video_url,
            "thumbnail": thumb_url,
            "developer": DEVELOPER,
            "powered_by": POWERED_BY
        }
    else:
        return {
            "status": "error",
            "message": "Video not found or URL parsing failed (Bad URL hash or blocked request).",
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