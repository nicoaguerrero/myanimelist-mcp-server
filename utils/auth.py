import httpx
import time
import secrets
import webbrowser
import http.server
import socketserver
import urllib.parse
import os
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

_access_token: Optional[str] = None
_refresh_token: Optional[str] = None
_expires_at: Optional[float] = None

REDIRECT_URI = "http://localhost:8080/callback"
CALLBACK_PORT = 8080
CALLBACK_CODE = None
CALLBACK_STATE = None

def get_new_code_verifier() -> str:
    return secrets.token_urlsafe(64)  # ~86 caracteres, dentro del rango

async def get_authorization_url() -> tuple[str, str, str]:
    code_verifier = get_new_code_verifier()
    code_challenge = code_verifier
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": os.getenv("MAL_CLIENT_ID"),
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "plain",
        "redirect_uri": REDIRECT_URI,
        "state": state
    }
    url = "https://myanimelist.net/v1/oauth2/authorize?" + urllib.parse.urlencode(params)
    return url, code_verifier, state

class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global CALLBACK_CODE, CALLBACK_STATE
        query = urllib.parse.urlparse(self.path).query
        query_components = urllib.parse.parse_qs(query)
        CALLBACK_CODE = query_components.get("code", [None])[0]
        CALLBACK_STATE = query_components.get("state", [None])[0]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Authorization code received. You can close this window.")

async def capture_authorization_code(expected_state: str) -> str:
    global CALLBACK_CODE, CALLBACK_STATE
    CALLBACK_CODE = None
    CALLBACK_STATE = None
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", CALLBACK_PORT), CallbackHandler) as httpd:
            print(f"HTTP server started on {REDIRECT_URI}. Waiting authorization_code...")
            httpd.handle_request()
    except OSError as e:
        raise ValueError(f"Error starting HTTP server: {e}")
    if not CALLBACK_CODE:
        raise ValueError("Authorization_code don't received")
    if CALLBACK_STATE != expected_state:
        raise ValueError(f"State mismatch: expected {expected_state}, received {CALLBACK_STATE}")
    return CALLBACK_CODE

async def exchange_code_for_token(code: str, code_verifier: str) -> Dict:
    url = "https://myanimelist.net/v1/oauth2/token"
    payload = {
        "client_id": os.getenv("MAL_CLIENT_ID"),
        "client_secret": os.getenv("MAL_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Full answer: {e.response.text}")
            raise httpx.HTTPStatusError(
                f"Error getting token: {e.response.status_code} - {e.response.text}",
                request=e.request,
                response=e.response
            )

async def refresh_access_token(refresh_token: str) -> Dict:
    url = "https://myanimelist.net/v1/oauth2/token"
    payload = {
        "client_id": os.getenv("MAL_CLIENT_ID"),
        "client_secret": os.getenv("MAL_CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                f"Error refreshing token: {e.response.status_code} - {e.response.text}",
                request=e.request,
                response=e.response
            )

async def get_mal_access_token() -> str:
    global _access_token, _refresh_token, _expires_at
    current_time = time.time()
    if _access_token and _expires_at and current_time < _expires_at - 60:
        return _access_token
    if _refresh_token:
        try:
            data = await refresh_access_token(_refresh_token)
            _access_token = data["access_token"]
            _refresh_token = data.get("refresh_token", _refresh_token)
            _expires_at = current_time + data["expires_in"]
            return _access_token
        except httpx.HTTPStatusError as e:
            print(f"Couldn't refresh the token: {e}. Getting a new one...")
    auth_url, code_verifier, state = await get_authorization_url()
    print(f"Please, open this URL in your browser to authorize:\n{auth_url}")
    webbrowser.open(auth_url)
    code = await capture_authorization_code(state)
    data = await exchange_code_for_token(code, code_verifier)
    _access_token = data["access_token"]
    _refresh_token = data.get("refresh_token")
    _expires_at = current_time + data["expires_in"]
    return _access_token