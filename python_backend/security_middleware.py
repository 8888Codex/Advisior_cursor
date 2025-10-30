"""
Security Middleware for AdvisorIA Elite
Adds security headers and input sanitization
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import re
from typing import Callable


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to all responses
    
    Headers added:
    - X-Content-Type-Options: nosniff (prevent MIME sniffing)
    - X-Frame-Options: DENY (prevent clickjacking)
    - X-XSS-Protection: 1; mode=block (XSS protection for old browsers)
    - Strict-Transport-Security: HSTS for HTTPS
    - Content-Security-Policy: Basic CSP
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # HSTS - Only for HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Basic CSP - Allow same origin + common CDNs
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' http://localhost:5001 http://127.0.0.1:5001;"
        )
        response.headers["Content-Security-Policy"] = csp
        
        # Remove server header if present
        if "server" in response.headers:
            del response.headers["server"]
        
        return response


def sanitize_html(text: str) -> str:
    """
    Remove HTML tags from text to prevent XSS attacks
    
    Args:
        text: Input text that may contain HTML
        
    Returns:
        Text with HTML tags removed
        
    Examples:
        >>> sanitize_html("<script>alert('xss')</script>Hello")
        "Hello"
        >>> sanitize_html("Normal text")
        "Normal text"
    """
    if not text:
        return text
    
    # Remove all HTML tags
    clean_text = re.sub(r'<[^>]*>', '', text)
    
    # Remove potentially dangerous characters
    # Keep common punctuation and letters
    clean_text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)\[\]\{\}\'\"\/\@\#\$\%\&\+\=\*]', '', clean_text)
    
    return clean_text


def sanitize_dict(data: dict, fields_to_sanitize: list[str]) -> dict:
    """
    Sanitize specific fields in a dictionary
    
    Args:
        data: Dictionary with potentially unsafe data
        fields_to_sanitize: List of field names to sanitize
        
    Returns:
        Dictionary with sanitized fields
    """
    sanitized = data.copy()
    
    for field in fields_to_sanitize:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitize_html(sanitized[field])
    
    return sanitized


def validate_email(email: str) -> bool:
    """
    Simple email validation
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email format is valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL format is valid
    """
    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return bool(re.match(pattern, url))

