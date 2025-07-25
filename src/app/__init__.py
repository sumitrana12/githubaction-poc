# Flask Message Board Application
from flask import Flask
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Import views after app is created to avoid circular imports
from app import views, models

# Initialize database
def init_app():
    models.init_db()
    logger.info("Application initialized") 