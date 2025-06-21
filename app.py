from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Calculate absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

# Vercel requires a handler named 'app'
def app_handler(request):
    with app.test_request_context(path=request['path'], method=request['method']):
        try:
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.data.decode('utf-8')
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Server error: {str(e)}'
            }

# This is required for Vercel
def app(request):
    return app_handler(request)

# Local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
