from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from settings import settings
from utils import require_params, colon_mac_to_lower

app = FastAPI(title="ALE External Captive Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"]
    , allow_headers=["*"]
)

# Serve built frontend (optional). If you build the React app into ../frontend/dist
# you can uncomment the next two lines to serve statics from FastAPI as well.
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/login/ale")
async def login_ale(request: Request):
    """Entry point called by AP redirect.
    Reads AP-provided query params and returns a small HTML page that boots the React app
    or a minimal fallback form if JS is disabled.
    Required params per spec: clientmac, clientip, switchmac, switchip, ssid, url
    """
    q = dict(request.query_params)
    missing = require_params(q, ["clientmac", "clientip", "switchmac", "switchip", "ssid", "url"])
    if missing:
        raise HTTPException(400, detail={"error": "missing params", "missing": missing})

    # Normalize for display/use
    q["clientmac"] = colon_mac_to_lower(q["clientmac"])  # tolerant on formats
    q["switchmac"] = colon_mac_to_lower(q["switchmac"])  # tolerant on formats

    # Render a tiny HTML that forwards params to the frontend via window.__CP__
    html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ALE Captive Portal</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <script>
    window.__CP__ = {q};
    window.__AP_LOGIN_URL__ = {repr(q.get('loginurl') or settings.AP_LOGIN_URL)};
  </script>
</head>
<body class="bg-light d-flex align-items-center" style="min-height:100vh;">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-12 col-sm-10 col-md-8 col-lg-6">
        <div class="card shadow-lg border-0 rounded-4">
          <div class="card-body p-4">
            <h4 class="card-title mb-2 text-center">Welcome to {q['ssid']}</h4>
            
            <form id="fallback" method="post" action="{q.get('loginurl') or settings.AP_LOGIN_URL}">
              <input type="hidden" name="url" value="{q['url']}">
              <input type="hidden" name="onerror" value="{q.get('onerror') or ""}">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" name="user" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">Continue</button>
              </div>
            </form>
            <p class="text-muted small mt-3 text-center">
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """
    return HTMLResponse(content=html)

