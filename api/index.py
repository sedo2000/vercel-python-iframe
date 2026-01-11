from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import httpx

app = FastAPI()

SOURCE_URL = "https://can.yalla--shoots.live/bein-max1/"

@app.get("/", response_class=HTMLResponse)
def player():
    return """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>مشغل مخصص</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { margin:0; background:#000; }
#player-container { position:relative; width:100%; height:100vh; }
iframe { width:100%; height:100%; border:none; }
.controls {
    position:absolute;
    bottom:20px;
    left:50%;
    transform:translateX(-50%);
    display:flex;
    gap:10px;
}
button {
    padding:10px 16px;
    border:none;
    border-radius:8px;
    font-size:16px;
    cursor:pointer;
}
</style>
</head>
<body>

<div id="player-container">
    <iframe id="frame" src="/proxy"></iframe>

    <div class="controls">
        <button onclick="reload()">🔄 تحديث</button>
        <button onclick="fullscreen()">⛶ ملء الشاشة</button>
    </div>
</div>

<script>
function reload(){
    document.getElementById('frame').src = '/proxy?' + Date.now();
}
function fullscreen(){
    let el = document.getElementById('frame');
    if (el.requestFullscreen) el.requestFullscreen();
}
</script>

</body>
</html>
"""

@app.get("/proxy")
async def proxy(request: Request):
    headers = {
        "User-Agent": request.headers.get("user-agent", ""),
        "Referer": SOURCE_URL
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(SOURCE_URL, headers=headers, timeout=20)

    return HTMLResponse(
        content=r.text,
        status_code=r.status_code
    )
