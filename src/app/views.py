from flask import jsonify, request, render_template
import os
from datetime import datetime
from app import app, logger
from app import models

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        messages = models.get_messages()
        return jsonify(messages)
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        return jsonify({"error": "Failed to retrieve messages"}), 500

@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({"error": "Message content is required"}), 400
    
    try:
        result = models.add_message(data['content'])
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error adding message: {e}")
        return jsonify({"error": "Failed to add message"}), 500 