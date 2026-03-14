from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import mediapipe as mp
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

# ================== MediaPipe Setup - للإصدار 0.10.32 ==================
# استخدام tasks API بدلاً من solutions
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# إعدادات Pose
BaseOptions = python.BaseOptions
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode = vision.RunningMode

pose_options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='pose_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_poses=1
)

# إعدادات Hands
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions

hand_options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2
)

# ================== Angle Calculation ==================
def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def draw_landmarks(frame, landmarks, connections, color=(0, 255, 0), thickness=2):
    """رسم النقاط والخطوط على الصورة"""
    h, w, _ = frame.shape
    
    # رسم الخطوط
    for connection in connections:
        start_idx, end_idx = connection
        start = landmarks[start_idx]
        end = landmarks[end_idx]
        
        x1, y1 = int(start.x * w), int(start.y * h)
        x2, y2 = int(end.x * w), int(end.y * h)
        
        cv2.line(frame, (x1, y1), (x2, y2), color, thickness)
    
    # رسم النقاط
    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)

# ================== API Endpoints ==================
@app.route('/api/process-video', methods=['POST'])
def process_video():
    """Process video frame and return annotated image"""
    try:
        # Receive frame
        data = request.json
        frame_data = data.get('frame')
        injured_hand = data.get('injured_hand', 'right')
        
        # Convert base64 to image
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        h, w, _ = frame.shape
        
        # Initialize variables
        shoulder_angle = 0
        elbow_angle = 0
        grip_percent = 0
        
        # ================== POSE DETECTION ==================
        with PoseLandmarker.create_from_options(pose_options) as landmarker:
            pose_result = landmarker.detect(mp_image)
            
            if pose_result.pose_landmarks:
                landmarks = pose_result.pose_landmarks[0]
                
                # رسم نقاط الجسم
                pose_connections = [
                    (11, 12), (11, 13), (13, 15),  # الذراع اليسرى
                    (12, 14), (14, 16),             # الذراع اليمنى
                    (11, 23), (12, 24)              # الاتصال بالجسم
                ]
                draw_landmarks(frame, landmarks, pose_connections, (0, 255, 255))
                
                # Calculate angles for injured side
                if injured_hand == 'left':
                    shoulder_angle = calculate_angle(
                        landmarks[23], landmarks[11], landmarks[13]
                    )
                    elbow_angle = calculate_angle(
                        landmarks[11], landmarks[13], landmarks[15]
                    )
                    cv2.putText(frame, f"L Shoulder: {int(shoulder_angle)}°",
                              (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    cv2.putText(frame, f"L Elbow: {int(elbow_angle)}°",
                              (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                else:  # right
                    shoulder_angle = calculate_angle(
                        landmarks[24], landmarks[12], landmarks[14]
                    )
                    elbow_angle = calculate_angle(
                        landmarks[12], landmarks[14], landmarks[16]
                    )
                    cv2.putText(frame, f"R Shoulder: {int(shoulder_angle)}°",
                              (w - 200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    cv2.putText(frame, f"R Elbow: {int(elbow_angle)}°",
                              (w - 200, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # ================== HAND DETECTION ==================
        with HandLandmarker.create_from_options(hand_options) as landmarker:
            hand_result = landmarker.detect(mp_image)
            
            if hand_result.hand_landmarks:
                for hand_landmarks, handedness in zip(hand_result.hand_landmarks, 
                                                      hand_result.handedness):
                    
                    # رسم نقاط اليد
                    hand_connections = [
                        (0,1),(1,2),(2,3),(3,4),      # الإبهام
                        (0,5),(5,6),(6,7),(7,8),      # السبابة
                        (0,9),(9,10),(10,11),(11,12), # الوسطى
                        (0,13),(13,14),(14,15),(15,16), # البنصر
                        (0,17),(17,18),(18,19),(19,20) # الخنصر
                    ]
                    draw_landmarks(frame, hand_landmarks, hand_connections, (0, 255, 0))
                    
                    # Calculate grip percentage
                    hand_label = handedness[0].category_name.lower()
                    
                    # Average finger angles for grip
                    angles = []
                    for tip, base in [(8,5), (12,9), (16,13), (20,17)]:
                        a = hand_landmarks[0]   # wrist
                        b = hand_landmarks[base]
                        c = hand_landmarks[tip]
                        angle = calculate_angle(a, b, c)
                        angles.append(angle)
                    
                    avg_angle = np.mean(angles) if angles else 90
                    grip_percent = int((avg_angle - 60) / (180 - 60) * 100)
                    grip_percent = max(0, min(100, grip_percent))
                    
                    # Display grip percentage
                    pos_x = 20 if hand_label == 'left' else w - 200
                    cv2.putText(frame, f"Grip: {grip_percent}%",
                              (pos_x, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Convert processed image to base64
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'processed_frame': f'data:image/jpeg;base64,{frame_base64}',
            'shoulder_angle': int(shoulder_angle),
            'elbow_angle': int(elbow_angle),
            'grip_percent': int(grip_percent)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'AI Service is running'})

if __name__ == '__main__':
    print("✅ Starting MediaPipe API Server on port 5001...")
    print("✅ Using MediaPipe Tasks API (compatible with v0.10.32)")
    print("✅ Available endpoints:")
    print("   - POST /api/process-video")
    print("   - GET  /api/health")
    app.run(port=5001, debug=True)