from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import mediapipe as mp
import numpy as np
import sqlite3
import os
import base64
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow connections from your website

# ================== IMPORTS ==================
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ================== CONFIG ==================
DB_PATH = "C:\\Users\\physio-gamification-project-grad\\physio-gamification-project\\rehabdatabase.db"
POSE_MODEL_PATH = "C:\\Users\\Dell\\physio-gamification-project-grad\\pose_landmarker_full.task"
HAND_MODEL_PATH = "C:\\Users\\Dell\\physio-gamification-project-grad\\hand_landmarker.task"

# ================== MODELS ==================
BaseOptions = python.BaseOptions
VisionRunningMode = vision.RunningMode

# POSE SETUP
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions

pose_options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=POSE_MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

# HAND SETUP
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions

hand_options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=HAND_MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)

# ================== DATABASE FUNCTIONS ==================
def get_injured_hand(user_id):
    """Get the injured hand for a patient"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT affected_hand FROM patients WHERE user_id = ?", 
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'right'

def save_session_results(user_id, measurements):
    """Save session results to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Update muscle strength
    cursor.execute("""
        UPDATE patients
        SET 
            shoulder_strength = ?,
            elbow_strength = ?,
            grip_strength = ?
        WHERE user_id = ?
    """, (
        measurements.get('shoulder', 0),
        measurements.get('elbow', 0),
        measurements.get('grip', 0),
        user_id
    ))
    
    # Record new session
    cursor.execute("""
        INSERT INTO game_sessions 
        (patient_id, game_type, score, duration, accuracy, completed)
        VALUES (
            (SELECT id FROM patients WHERE user_id = ?),
            ?, ?, ?, ?, ?
        )
    """, (
        user_id,
        measurements.get('game_type', 'assessment'),
        measurements.get('score', 0),
        measurements.get('duration', 0),
        measurements.get('accuracy', 0),
        1
    ))
    
    conn.commit()
    conn.close()

# ================== ANGLE FUNCTIONS ==================
def calculate_angle(a, b, c, w, h):
    """Calculate angle between three points"""
    a = np.array([a.x * w, a.y * h])
    b = np.array([b.x * w, b.y * h])
    c = np.array([c.x * w, c.y * h])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def calculate_elbow_angle(shoulder, elbow, wrist, w, h):
    """Calculate elbow flexion angle"""
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

# ================== API ENDPOINTS ==================

@app.route('/api/analyze/frame', methods=['POST'])
def analyze_frame():
    """Analyze a single video frame (for real-time use)"""
    try:
        data = request.json
        user_id = data.get('user_id')
        frame_data = data.get('frame')  # base64 encoded frame
        
        # Convert base64 to image
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Analyze image
        with PoseLandmarker.create_from_options(pose_options) as pose_landmarker:
            pose_result = pose_landmarker.detect(mp_image)
            
            if not pose_result.pose_landmarks:
                return jsonify({'success': False, 'message': 'No pose detected'})
            
            landmarks = pose_result.pose_landmarks[0]
            
            # Calculate angles
            injured_hand = get_injured_hand(user_id)
            
            if injured_hand == 'left':
                elbow_angle = calculate_elbow_angle(
                    landmarks[11], landmarks[13], landmarks[15], w, h
                )
                shoulder_angle = calculate_angle(
                    landmarks[23], landmarks[11], landmarks[13], w, h
                )
            else:
                elbow_angle = calculate_elbow_angle(
                    landmarks[12], landmarks[14], landmarks[16], w, h
                )
                shoulder_angle = calculate_angle(
                    landmarks[24], landmarks[12], landmarks[14], w, h
                )
            
            return jsonify({
                'success': True,
                'shoulder_angle': float(shoulder_angle),
                'elbow_angle': float(elbow_angle),
                'injured_hand': injured_hand
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze/session', methods=['POST'])
def analyze_session():
    """Analyze a complete session (after patient finishes)"""
    try:
        data = request.json
        user_id = data.get('user_id')
        game_type = data.get('game_type', 'assessment')
        measurements = data.get('measurements', {})
        
        # Save results to database
        save_session_results(user_id, measurements)
        
        return jsonify({
            'success': True,
            'message': 'Session saved successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patient/hand/<int:user_id>', methods=['GET'])
def get_patient_hand(user_id):
    """Get the injured hand for a patient"""
    try:
        hand = get_injured_hand(user_id)
        return jsonify({
            'success': True,
            'affected_hand': hand
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Use different port from your website (5000)