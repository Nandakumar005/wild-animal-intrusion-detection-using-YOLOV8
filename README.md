# 🦁 Wildlife Detection and Alert System

A Flask-based web application that uses **YOLOv8** for real-time wildlife detection. It can monitor video streams from webcams, CCTV/IP cameras, or uploaded video files, and automatically send **email alerts** when wildlife is detected.

---

## ✨ Features

- 🔍 **Real-time detection** with YOLOv8 (fast & accurate)
- 🎚️ Configurable **confidence threshold** for detections
- 📧 **Email alerts** with images of detected wildlife
- 🌐 Interactive **web interface** to:
  - View live detections
  - Switch between video sources (Webcam, IP Camera, Video Upload)
  - Configure settings
- 💾 Saves detection clips/images for later review
- 🛠️ Easy integration with existing farm/security infrastructure

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Webcam or IP camera (optional)
- SMTP email account for notifications

### 1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create & activate a virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the application
Update `config.py` with:
- Email credentials for alerts
- YOLO model path (`best.pt`)
- Detection confidence thresholds

### 5. Run the app
```bash
python app.py
```

### 6. Access the web interface
Open your browser and navigate to `http://localhost:5000`

---

## ⚙️ Configuration

The application requires configuration of the following components:

- **📧 Email Settings**: SMTP server credentials for sending alerts
- **🤖 Model Path**: Location of the trained YOLOv8 model file (`best.pt`)
- **🎯 Detection Parameters**: Confidence thresholds and alert frequency settings

---

## 📂 Project Structure

```
├── app.py                # Flask app entry point
├── best.pt               # YOLOv8 trained model
├── config.py             # Configuration settings
├── templates/            # HTML templates for web interface
│   ├── base.html
│   ├── detections.html
│   └── settings.html
├── static/               # Saved detection images/videos
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

---

## 🎯 Usage

1. **🚀 Start the Application**: Run `python app.py` to launch the web server
2. **⚙️ Configure Settings**: Access the settings page to configure email alerts and detection parameters
3. **📹 Select Input Source**: Choose between webcam, IP camera, or video file upload
4. **👀 Monitor Detections**: View real-time detection results on the main dashboard
5. **📁 Review Archives**: Access saved detection images and videos in the static directory

---

## 🛠️ Technical Requirements

- **Python**: 3.8+
- **Framework**: Flask
- **Computer Vision**: YOLOv8 (Ultralytics)
- **Dependencies**: Listed in `requirements.txt`

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Nandakumar D**  
B.Tech Artificial Intelligence & Data Science  
Machine Learning & AI Enthusiast | Python Developer | Data-Driven Problem Solver

- 🔗 **GitHub**: [Nandakumar005](https://github.com/Nandakumar005)
- 💼 **LinkedIn**: [nanda-kumar-d-2325a5326](https://www.linkedin.com/in/nanda-kumar-d-2325a5326/)
- 📧 **Email**: nandakumardg8@gmail.com

---

