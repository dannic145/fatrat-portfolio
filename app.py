from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Calculate absolute paths for Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

@app.route('/')
def home():
    return render_template('index.html')

# Serve static files explicitly
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

# Vercel serverless handler
def vercel_handler(request):
    with app.app_context():
        # Create a test request context
        with app.test_request_context(path=request['path'], method=request['method']):
            # Dispatch the request
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.data.decode('utf-8')
            }

# Local development handler
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
