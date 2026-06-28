"""mcp-billing — Client library for pay-per-use MCP servers"""
import os, json, time
from pathlib import Path
from functools import wraps
import urllib.request
import urllib.error

DEFAULT_API_URL = "https://mcp-billing-api.onrender.com"
CACHE = {}
CACHE_TTL = 60  # seconds

class BillingClient:
    def __init__(self, api_url=None):
        self.api_url = api_url or os.getenv("MCP_BILLING_API", DEFAULT_API_URL)
    
    def _get_license_key(self):
        key = os.environ.get("MCP_LICENSE_KEY", "")
        if key:
            return key
        key_file = Path.home() / ".mcp_license"
        if key_file.exists():
            return key_file.read_text().strip()
        if Path(".mcp_license").exists():
            return Path(".mcp_license").read_text().strip()
        return ""
    
    def _api_call(self, endpoint, data):
        """Make a POST request to the billing API"""
        payload = json.dumps(data).encode()
        req = urllib.request.Request(
            f"{self.api_url}{endpoint}",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try:
                return json.loads(body)
            except:
                return {"error": body, "remaining": 0}
        except Exception as e:
            # Offline mode — allow requests (fail open)
            return {"valid": True, "remaining": 999999, "tier": "offline", "error": str(e)}
    
    def verify(self, product="web-search"):
        """Check if current license has credits"""
        key = self._get_license_key()
        cache_key = f"{key}:{product}"
        
        now = time.time()
        if cache_key in CACHE:
            cached_at, result = CACHE[cache_key]
            if now - cached_at < CACHE_TTL:
                return result
        
        if not key:
            result = self._api_call("/verify", {"key": "anonymous-free", "product": product})
        else:
            result = self._api_call("/verify", {"key": key, "product": product})
        
        CACHE[cache_key] = (now, result)
        return result
    
    def use_credit(self, product="web-search", tool="unknown"):
        """Deduct 1 credit and log usage"""
        key = self._get_license_key()
        if not key:
            key = "anonymous-free"
        return self._api_call("/use", {"key": key, "product": product, "tool": tool})
    
    def check_and_deduct(self, product="web-search", tool="unknown"):
        """Combined check + deduct. Returns (allowed: bool, message: str, remaining: int)"""
        verify_result = self.verify(product)
        
        if not verify_result.get("valid", False):
            remaining = verify_result.get("remaining", 0)
            daily = verify_result.get("daily_used", 0)
            limit = verify_result.get("daily_limit", "N/A")
            return False, f"Out of credits. Get more: https://stinkmaster37.gumroad.com/l/mcp-credits", remaining
        
        result = self.use_credit(product, tool)
        remaining = result.get("remaining", 0)
        
        if result.get("success"):
            return True, f"Credit used. {remaining} remaining", remaining
        else:
            return False, result.get("error", "Payment required"), remaining

def require_credit(product="web-search"):
    """Decorator for MCP tools that require credit"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = BillingClient()
            allowed, msg, remaining = client.check_and_deduct(product, func.__name__)
            if not allowed:
                return {"error": msg, "payment_required": True, "remaining": remaining}
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                result["_credits_remaining"] = remaining
            return result
        return wrapper
    return decorator

# Singleton
billing = BillingClient()
