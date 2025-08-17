# Wildlife Detection and Alert System

## Description
This project is a Flask-based web application designed to detect wildlife using YOLO object detection models. It captures video streams from various sources such as webcams, CCTV IP cameras, or uploaded video files, processes the frames to detect wildlife, and sends email alerts with detection details and images.

## Features
- Real-time wildlife detection using YOLO models.
- Configurable confidence thresholds for detection.
- Email alerts with detected wildlife details and images.
- Web interface for viewing detections and configuring settings.
- Supports multiple video sources.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirement.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Configuration
Sensitive data such as email credentials and model paths are stored in `config.py`. Ensure this file is excluded from version control.

## License
This project is licensed under the MIT License.

## Author
Nandakumar D

## Note
Make sure to set up a virtual environment and exclude sensitive data before deploying or sharing the project.
