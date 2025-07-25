import os
from app import app, init_app

if __name__ == '__main__':
    init_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 