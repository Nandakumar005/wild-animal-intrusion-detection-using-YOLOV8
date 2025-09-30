# Path to the trained YOLOv8 model
MODEL_PATH = "best.pt"

# Directory to save detection images and videos
DETECTION_DIR = "static"

# Email configuration (DO NOT include passwords here)
EMAIL_CONFIG = {
    "sender": "your_email@example.com",     # Enter sender email
    "recipient": "recipient@example.com",   # Enter default recipient email
    "password": "",                         # Leave blank or load from environment variable
    "cooldown": 60                          # Cooldown in seconds between alerts
}

# Detection and application settings
current_config = {
    "confidence_threshold": 0.5,            # Default detection confidence threshold
    "last_alert_time": 0
}
