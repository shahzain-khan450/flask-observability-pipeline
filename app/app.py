import random
import time
from flask import Flask, render_template_string
from prometheus_client import make_wsgi_app, Counter, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Core Golden Signals: Request tracking metrics
REQUEST_COUNT = Counter(
    'app_requests_total', 
    'Total HTTP Requests tracked by status and endpoint', 
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 
    'HTTP Request Latency tracking in seconds', 
    ['endpoint']
)

BASE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Production App</title></head>
<body style="font-family:sans-serif; text-align:center; margin-top:100px;">
    <h2>Application Status: Online</h2>
    <p>Refresh this page to simulate real production traffic.</p>
</body>
</html>
"""

@app.route('/')
def home():
    start_time = time.time()
    
    # Intentionally inject variable latency (100ms - 500ms)
    time.sleep(random.uniform(0.1, 0.5)) 
    
    # Intentionally inject a 10% error rate for dashboard visualization
    status = "200" if random.random() > 0.1 else "500"
    
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=status).inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
    
    if status == "500":
        return "Internal Server Error", 500
    return render_template_string(BASE_HTML), 200

# Mount Prometheus WSGI handler onto /metrics path
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
