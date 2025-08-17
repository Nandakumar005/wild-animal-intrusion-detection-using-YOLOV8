import cv2
from ultralytics import YOLO
from flask import Flask, render_template, Response, request, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import os
import threading
import logging
from config import MODEL_PATH, DETECTION_DIR, EMAIL_CONFIG, current_config
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)
logging.basicConfig(level=logging.INFO)

# Configuration
os.makedirs(DETECTION_DIR, exist_ok=True)

# Global variables
camera = None
detections_list = []
lock = threading.Lock()

class WildlifeDetector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)
        self.confidence_threshold = current_config['confidence_threshold']

    def process_frame(self, frame):
        results = self.model(frame)[0]
        detections = []
        
        for box in results.boxes:
            conf = box.conf.item()
            if conf < self.confidence_threshold:
                continue
                
            cls = int(box.cls.item())
            class_name = results.names[cls]
            xyxy = box.xyxy[0].tolist()
            
            detections.append({
                'class': class_name,
                'confidence': conf,
                'bbox': tuple(map(int, xyxy))
            })
            
        return detections

    def send_email(self, image_path, animals):
        if time.time() - current_config['last_alert_time'] < EMAIL_CONFIG['cooldown']:
            return
            
        try:
            msg = MIMEMultipart()
            msg['Subject'] = 'Wildlife Detection Alert!'
            msg['From'] = EMAIL_CONFIG['sender']
            msg['To'] = EMAIL_CONFIG['recipient']
            
            body = f"Detected: {', '.join(animals)} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            msg.attach(MIMEText(body))
            
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read())
                msg.attach(img)
                
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
                server.send_message(msg)
                
            current_config['last_alert_time'] = time.time()
            logging.info("Alert email sent successfully")
            
        except Exception as e:
            logging.error(f"Email sending failed: {str(e)}")

detector = WildlifeDetector()

def generate_frames():
    global camera
    while camera is not None:
        success, frame = camera.read()
        if not success:
            break
            
        # Process frame for detections
        detections = detector.process_frame(frame)
        
        # Draw bounding boxes
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['class']} {det['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save detection and send email if needed
        with lock:
            if detections:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                img_name = f"detection_{timestamp}.jpg"
                img_path = os.path.join(DETECTION_DIR, img_name)
                cv2.imwrite(img_path, frame)
                
                # Update detection list
                detections_list.insert(0, {
                    'timestamp': timestamp,
                    'image': img_name,
                    'animals': list(set(d['class'] for d in detections))
                })
                
                # Send email in separate thread
                threading.Thread(target=detector.send_email, 
                                 args=(img_path, list(set(d['class'] for d in detections)))).start()

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', sources=['Webcam', 'CCTV IP', 'Video File'])

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detections')
def view_detections():
    with lock:
        detections = detections_list[:]  # Create a copy for thread safety
    return render_template('detections.html', detections=detections)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        EMAIL_CONFIG['recipient'] = request.form.get('email', EMAIL_CONFIG['recipient'])
        current_config['confidence_threshold'] = float(request.form.get('confidence', 0.5))
        detector.confidence_threshold = current_config['confidence_threshold']
        return redirect(url_for('settings'))
        
    return render_template('settings.html', 
                         current_email=EMAIL_CONFIG['recipient'],
                         current_confidence=current_config['confidence_threshold'])

@app.route('/start', methods=['POST'])
def start_detection():
    global camera
    
    # Release existing camera
    if camera is not None:
        camera.release()
        
    source_type = request.form['source']
    if source_type == 'Webcam':
        camera = cv2.VideoCapture(0)
    elif source_type == 'CCTV IP':
        camera = cv2.VideoCapture(request.form['cctv_url'])
    else:
        video_file = request.files['video_file']
        video_path = os.path.join(DETECTION_DIR, video_file.filename)
        video_file.save(video_path)
        camera = cv2.VideoCapture(video_path)
        
    return redirect(url_for('index'))

@app.route('/stop')
def stop_detection():
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')