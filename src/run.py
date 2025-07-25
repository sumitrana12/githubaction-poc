import os
from app import app, init_app

if __name__ == '__main__':
    init_app()
    port = int(os.environ.get('PORT', 5000))
    # Use environment variable for host, default to localhost for security
    host = os.environ.get('HOST', '127.0.0.1')
    app.run(host=host, port=port) 