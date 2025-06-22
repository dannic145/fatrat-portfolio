from flask import Flask, render_template, send_from_directory
import os

from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Security headers implementation - applied to all responses
@app.after_request
def add_security_headers(response):
    """
    Implements critical security headers for enhanced protection
    """
    # Content Security Policy (CSP)
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self' https://unpkg.com https://cdnjs.cloudflare.com 'unsafe-inline'; "
        "style-src 'self' https://fonts.googleapis.com https://cdnjs.cloudflare.com 'unsafe-inline'; "
        "img-src 'self' https://media.giphy.com data:; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "frame-src 'none'; "
        "object-src 'none';"
    )
    response.headers['Content-Security-Policy'] = csp_policy
    
    # HTTP Strict Transport Security (HSTS)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # X-Frame-Options (clickjacking protection)
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Additional security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response

# Serve static files with security considerations
@app.route('/static/<path:path>')
def serve_static(path):
    """Securely serves static files with proper headers"""
    return send_from_directory('static', path)

# ... rest of the application code ...

app = Flask(__name__)

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Main route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return 'OK', 200

# Run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
