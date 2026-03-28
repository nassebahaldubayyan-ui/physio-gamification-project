# web_/consumers.py
import json
import base64
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from channels.generic.websocket import AsyncWebsocketConsumer
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
import os

# ================== MODEL PATHS ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'pose_landmarker_full.task')
HAND_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'hand_landmarker.task')

BaseOptions = python.BaseOptions
VisionRunningMode = vision.RunningMode

# ================== HAND CONNECTIONS ==================
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20)
]

class PoseDetectionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # MediaPipe models
        self.pose_landmarker = None
        self.hand_landmarker = None
        
        # Max values tracking
        self.max_shoulder = 0
        self.max_elbow = 0
        self.max_grip = 0
        
        # Angle smoothing variables
        self.prev_left_elbow = None
        self.prev_right_elbow = None
        self.prev_left_shoulder = None
        self.prev_right_shoulder = None
        self.SMOOTHING = 0.7
        
        self.start_time = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.injured_hand = 'left'
        self.patient_id = 25
        
    async def connect(self):
        try:
            # Initialize Pose Landmarker
            pose_options = vision.PoseLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=POSE_MODEL_PATH),
                running_mode=VisionRunningMode.VIDEO,
                num_poses=1
            )
            self.pose_landmarker = vision.PoseLandmarker.create_from_options(pose_options)
            
            # Initialize Hand Landmarker
            hand_options = vision.HandLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=HAND_MODEL_PATH),
                running_mode=VisionRunningMode.VIDEO,
                num_hands=2
            )
            self.hand_landmarker = vision.HandLandmarker.create_from_options(hand_options)
            
            self.start_time = time.time()
            
            await self.accept()
            print("✅ WebSocket connected - MediaPipe models loaded")
            
        except Exception as e:
            print(f"❌ Error initializing MediaPipe: {e}")
            await self.close()
    
    async def disconnect(self, close_code):
        if self.pose_landmarker:
            self.pose_landmarker.close()
        if self.hand_landmarker:
            self.hand_landmarker.close()
        print("WebSocket disconnected")
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            
            if 'frame' in data:
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.process_frame,
                    data['frame']
                )
                
                if result:
                    processed_frame, angles, feedback, max_values = result
                    await self.send(text_data=json.dumps({
                        'type': 'pose_data',
                        'angles': angles,
                        'feedback': feedback,
                        'frame': processed_frame,
                        'max_values': max_values
                    }))
            
            elif 'injured_hand' in data:
                self.injured_hand = data['injured_hand']
                print(f"🎯 Injured hand set to: {self.injured_hand}")
                
            elif 'patient_id' in data:
                self.patient_id = data['patient_id']
                
        except Exception as e:
            print(f"❌ Error receiving frame: {e}")
    
    def process_frame(self, frame_data):
        try:
            # Decode base64 image
            if ',' in frame_data:
                frame_data = frame_data.split(',')[1]
            
            image_data = base64.b64decode(frame_data)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return None, None, None, None
            
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int((time.time() - self.start_time) * 1000)
            
            # Process hand detection
            hand_result = self.hand_landmarker.detect_for_video(mp_image, timestamp_ms)
            self.process_hand(frame, hand_result, w, h)
            
            # Process pose detection
            pose_result = self.pose_landmarker.detect_for_video(mp_image, timestamp_ms)
            
            angles = {
                'left_shoulder': 0,
                'left_elbow': 0,
                'right_shoulder': 0,
                'right_elbow': 0
            }
            feedback = "Position yourself in front of the camera"
            
            if pose_result.pose_landmarks:
                landmarks = pose_result.pose_landmarks[0]
                
                if self.injured_hand == 'left':
                    angles = self.process_left_side(frame, landmarks, w, h)
                else:
                    angles = self.process_right_side(frame, landmarks, w, h)
                
                feedback = self.generate_feedback(angles)
            
            # Draw max values
            cv2.putText(frame, f"Max Shoulder: {int(self.max_shoulder)}", (20, h - 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Max Elbow: {int(self.max_elbow)}", (20, h - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Max Grip: {int(self.max_grip)}%", (20, h - 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Encode back to base64
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            processed_frame = base64.b64encode(buffer).decode('utf-8')
            
            max_values = {
                'shoulder': self.max_shoulder,
                'elbow': self.max_elbow,
                'grip': self.max_grip
            }
            
            return processed_frame, angles, feedback, max_values
            
        except Exception as e:
            print(f"❌ Process error: {e}")
            return None, None, None, None
    
    def smooth_angle(self, previous, current):
        """Smooth angle values"""
        if previous is None:
            return current
        return 0.7 * previous + 0.3 * current
    
    def calculate_angle(self, a, b, c, w, h):
        """Angle calculation from your original code"""
        a = np.array([a.x * w, a.y * h])
        b = np.array([b.x * w, b.y * h])
        c = np.array([c.x * w, c.y * h])
        
        ba = a - b
        bc = c - b
        
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)
    
    def calculate_elbow_angle(self, shoulder, elbow, wrist, w, h):
        """Elbow angle calculation from your original code"""
        shoulder = np.array([shoulder.x * w, shoulder.y * h])
        elbow = np.array([elbow.x * w, elbow.y * h])
        wrist = np.array([wrist.x * w, wrist.y * h])
        
        upper_arm = shoulder - elbow
        forearm = wrist - elbow
        
        cosine_angle = np.dot(upper_arm, forearm) / (
            np.linalg.norm(upper_arm) * np.linalg.norm(forearm)
        )
        
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)
    
    def draw_connections(self, frame, landmarks, connections, w, h):
        """Draw hand connections from your original code"""
        for start_idx, end_idx in connections:
            start = landmarks[start_idx]
            end = landmarks[end_idx]
            
            x1, y1 = int(start.x * w), int(start.y * h)
            x2, y2 = int(end.x * w), int(end.y * h)
            
            cv2.line(frame, (x1, y1), (x2, y2), (255, 200, 0), 4)
        
        for lm in landmarks:
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)
    
    def process_hand(self, frame, hand_result, w, h):
        """Process hand detection from your original code"""
        if hand_result.hand_landmarks and hand_result.handedness:
            for i in range(len(hand_result.hand_landmarks)):
                hand_landmarks = hand_result.hand_landmarks[i]
                hand_label = hand_result.handedness[i][0].category_name.lower()
                
                if hand_label != self.injured_hand:
                    continue
                
                self.draw_connections(frame, hand_landmarks, HAND_CONNECTIONS, w, h)
                
                # Calculate angles for each finger
                index_angle = self.calculate_angle(hand_landmarks[0], hand_landmarks[5], hand_landmarks[8], w, h)
                middle_angle = self.calculate_angle(hand_landmarks[0], hand_landmarks[9], hand_landmarks[12], w, h)
                ring_angle = self.calculate_angle(hand_landmarks[0], hand_landmarks[13], hand_landmarks[16], w, h)
                pinky_angle = self.calculate_angle(hand_landmarks[0], hand_landmarks[17], hand_landmarks[20], w, h)
                
                avg_angle = (index_angle + middle_angle + ring_angle + pinky_angle) / 4
                
                open_percentage = int(((avg_angle - 60) / (180 - 60)) * 100)
                open_percentage = max(0, min(100, open_percentage))
                closed_percentage = 100 - open_percentage
                
                if closed_percentage > self.max_grip:
                    self.max_grip = closed_percentage
                
                text_x = 30 if self.injured_hand == 'left' else w - 200
                cv2.putText(frame, f"Open: {open_percentage}%", (text_x, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(frame, f"Closed: {closed_percentage}%", (text_x, 160),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    def process_left_side(self, frame, landmarks, w, h):
        """Process left side from your original code"""
        # Landmark indices: 11=left_shoulder, 13=left_elbow, 15=left_wrist, 23=left_hip
        shoulder_angle = self.calculate_angle(landmarks[23], landmarks[11], landmarks[13], w, h)
        elbow_angle = self.calculate_elbow_angle(landmarks[11], landmarks[13], landmarks[15], w, h)
        
        shoulder_angle = self.smooth_angle(self.prev_left_shoulder, shoulder_angle)
        elbow_angle = self.smooth_angle(self.prev_left_elbow, elbow_angle)
        
        self.prev_left_shoulder = shoulder_angle
        self.prev_left_elbow = elbow_angle
        
        if shoulder_angle > self.max_shoulder:
            self.max_shoulder = shoulder_angle
        if elbow_angle > self.max_elbow:
            self.max_elbow = elbow_angle
        
        cv2.putText(frame, f"L Shoulder: {int(shoulder_angle)}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f"L Elbow: {int(elbow_angle)}", (20, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        return {
            'left_shoulder': int(shoulder_angle),
            'left_elbow': int(elbow_angle),
            'right_shoulder': 0,
            'right_elbow': 0
        }
    
    def process_right_side(self, frame, landmarks, w, h):
        """Process right side from your original code"""
        # Landmark indices: 12=right_shoulder, 14=right_elbow, 16=right_wrist, 24=right_hip
        shoulder_angle = self.calculate_angle(landmarks[24], landmarks[12], landmarks[14], w, h)
        elbow_angle = self.calculate_elbow_angle(landmarks[12], landmarks[14], landmarks[16], w, h)
        
        shoulder_angle = self.smooth_angle(self.prev_right_shoulder, shoulder_angle)
        elbow_angle = self.smooth_angle(self.prev_right_elbow, elbow_angle)
        
        self.prev_right_shoulder = shoulder_angle
        self.prev_right_elbow = elbow_angle
        
        if shoulder_angle > self.max_shoulder:
            self.max_shoulder = shoulder_angle
        if elbow_angle > self.max_elbow:
            self.max_elbow = elbow_angle
        
        cv2.putText(frame, f"R Shoulder: {int(shoulder_angle)}", (w - 220, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f"R Elbow: {int(elbow_angle)}", (w - 220, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        return {
            'left_shoulder': 0,
            'left_elbow': 0,
            'right_shoulder': int(shoulder_angle),
            'right_elbow': int(elbow_angle)
        }
    
    def generate_feedback(self, angles):
        """Generate feedback based on angles"""
        feedback = []
        
        if self.injured_hand == 'left':
            if angles['left_elbow'] < 30:
                feedback.append("Extend left arm more")
            elif angles['left_elbow'] > 160:
                feedback.append("Bend left elbow slightly")
            elif 60 <= angles['left_elbow'] <= 120:
                feedback.append("✓ Left arm good position")
            
            if angles['left_shoulder'] < 30:
                feedback.append("Raise left arm higher")
            elif angles['left_shoulder'] > 120:
                feedback.append("Lower left arm slightly")
        else:
            if angles['right_elbow'] < 30:
                feedback.append("Extend right arm more")
            elif angles['right_elbow'] > 160:
                feedback.append("Bend right elbow slightly")
            elif 60 <= angles['right_elbow'] <= 120:
                feedback.append("✓ Right arm good position")
            
            if angles['right_shoulder'] < 30:
                feedback.append("Raise right arm higher")
            elif angles['right_shoulder'] > 120:
                feedback.append("Lower right arm slightly")
        
        return " | ".join(feedback) if feedback else "Good form! Keep going!"