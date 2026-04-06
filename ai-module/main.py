<<<<<<< HEAD
# %%
#===================imports=======================
import cv2  # OpenCV for video processing
import mediapipe as mp # MediaPipe for hand tracking
import numpy as np # NumPy for numerical operations
import time # Time module for measuring FPS
import sqlite3 # SQLite3 for database operations
import os # OS module for file operations
import datetime # Datetime module for timestamping

import threading
import asyncio
import websockets

from mediapipe.tasks import python  # Importing the Python API for MediaPipe tasks
from mediapipe.tasks.python import vision # Importing the vision module from MediaPipe tasks

# ================== MODEL PATHS ==================
POSE_MODEL_PATH = "pose_landmarker_full.task"
HAND_MODEL_PATH = "hand_landmarker.task"

# ================== BASE OPTIONS ==================
BaseOptions = python.BaseOptions
VisionRunningMode = vision.RunningMode

# ================== POSE SETUP ==================
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions

pose_options = PoseLandmarkerOptions(
=======
import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from database.db_manager import DatabaseManager
from tracker.pose_tracker import PoseTracker
from tracker.hand_tracker import HandTracker
from tracker.combined_tracker import CombinedTracker
from assessment.initial_assessment import InitialAssessment

from games.game_logic import CatchGame
from games.game_session import GameSession

POSE_MODEL_PATH = "pose_landmarker_full.task"
HAND_MODEL_PATH = "hand_landmarker.task"

BaseOptions = python.BaseOptions
VisionRunningMode = vision.RunningMode

pose_options = vision.PoseLandmarkerOptions(
>>>>>>> 8a0815e88fd7d9022a997057f6d1567eabe9e2a6
    base_options=BaseOptions(model_asset_path=POSE_MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

<<<<<<< HEAD
# ================== HAND SETUP ==================
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions

hand_options = HandLandmarkerOptions(
=======
hand_options = vision.HandLandmarkerOptions(
>>>>>>> 8a0815e88fd7d9022a997057f6d1567eabe9e2a6
    base_options=BaseOptions(model_asset_path=HAND_MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)

<<<<<<< HEAD
# ================== ANGLE SMOOTHING ==================
prev_left_elbow = None
prev_right_elbow = None
prev_left_shoulder = None
prev_right_shoulder = None

SMOOTHING = 0.7

def smooth_angle(previous, current, alpha=0.7):
    if previous is None:
        return current
    return alpha * previous + (1 - alpha) * current

# ================== ANGLE CALCULATION ==================
def calculate_angle(a, b, c, w, h):

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

#===================database functions=======================

def get_injured_hand():

    conn = sqlite3.connect("C:\\Users\\Mulik\\physio-gamification-project\\rehabdatabase.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT affected_hand FROM patients WHERE user_id = 25"
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return None

def update_strengths(patient_id, shoulder, elbow, grip):

    conn = sqlite3.connect("C:\\Users\\Mulik\\physio-gamification-project\\rehabdatabase.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET 
            shoulder_strength = ?,
            elbow_strength = ?,
            grip_strength = ?,
        WHERE user_id = 25
    """, (shoulder, elbow, grip, patient_id))

    conn.commit()
    conn.close()

# ================== DRAW CONNECTIONS ==================
def draw_connections(frame, landmarks, connections, w, h):

    line_color = (255, 200, 0)
    line_thickness = 4

    for start_idx, end_idx in connections:

        start = landmarks[start_idx]
        end = landmarks[end_idx]

        x1, y1 = int(start.x * w), int(start.y * h)
        x2, y2 = int(end.x * w), int(end.y * h)

        cv2.line(frame, (x1, y1), (x2, y2), line_color, line_thickness)

    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)

# ================== HAND CONNECTIONS ==================
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20)
]

# ================== LEFT SIDE ==================
def process_left_side(frame, landmarks, w, h):

    global prev_left_elbow, prev_left_shoulder

    left_connections = [(11,13),(13,15),(11,23)]
    draw_connections(frame, landmarks, left_connections, w, h)

    shoulder_angle = calculate_angle(
        landmarks[23], landmarks[11], landmarks[13], w, h
    )

    elbow_angle = calculate_elbow_angle(
        landmarks[11], landmarks[13], landmarks[15], w, h
    )

    shoulder_angle = smooth_angle(prev_left_shoulder, shoulder_angle, SMOOTHING)
    elbow_angle = smooth_angle(prev_left_elbow, elbow_angle, SMOOTHING)

    prev_left_shoulder = shoulder_angle
    prev_left_elbow = elbow_angle

    cv2.putText(frame, f"L Shoulder: {int(shoulder_angle)}°",
                (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0),2)

    cv2.putText(frame, f"L Elbow: {int(elbow_angle)}°",
                (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0),2)

# ================== RIGHT SIDE ==================
def process_right_side(frame, landmarks, w, h):

    global prev_right_elbow, prev_right_shoulder

    right_connections = [(12,14),(14,16),(12,24)]
    draw_connections(frame, landmarks, right_connections, w, h)

    shoulder_angle = calculate_angle(
        landmarks[24], landmarks[12], landmarks[14], w, h
    )

    elbow_angle = calculate_elbow_angle(
        landmarks[12], landmarks[14], landmarks[16], w, h
    )

    shoulder_angle = smooth_angle(prev_right_shoulder, shoulder_angle, SMOOTHING)
    elbow_angle = smooth_angle(prev_right_elbow, elbow_angle, SMOOTHING)

    prev_right_shoulder = shoulder_angle
    prev_right_elbow = elbow_angle

    cv2.putText(frame, f"R Shoulder: {int(shoulder_angle)}°",
                (w-220,40), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

    cv2.putText(frame, f"R Elbow: {int(elbow_angle)}°",
                (w-220,70), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)
    
# ================== hand setup ==================
def selectedhand(hand_type, frame, w, h, mp_image, timestamp_ms, hand_landmarker):
    hand_result = hand_landmarker.detect_for_video(mp_image, timestamp_ms)

    if hand_result.hand_landmarks and hand_result.handedness:

        for i in range(len(hand_result.hand_landmarks)):

            hand_landmarks = hand_result.hand_landmarks[i]
            hand_label = hand_result.handedness[i][0].category_name.lower()

            # Ignore the non-selected hand
            if hand_type == 'left' and hand_label != "left":
                continue

            if hand_type == 'right' and hand_label != "right":
                continue

            # Draw chosen hand
            draw_connections(frame, hand_landmarks, HAND_CONNECTIONS, w, h)

            # MCP Angles
            index_angle = calculate_angle(hand_landmarks[0], hand_landmarks[5], hand_landmarks[8], w, h)
            middle_angle = calculate_angle(hand_landmarks[0], hand_landmarks[9], hand_landmarks[12], w, h)
            ring_angle = calculate_angle(hand_landmarks[0], hand_landmarks[13], hand_landmarks[16], w, h)
            pinky_angle = calculate_angle(hand_landmarks[0], hand_landmarks[17], hand_landmarks[20], w, h)

            avg_angle = (index_angle + middle_angle + ring_angle + pinky_angle) / 4

            # Convert to percentage
            open_percentage = int(((avg_angle - 60) / (180 - 60)) * 100)
            open_percentage = max(0, min(100, open_percentage))
            closed_percentage = 100 - open_percentage

            text_x = 30 if hand_type == 'left' else w - 200

            cv2.putText(frame, f"Open: {open_percentage}%",
                (text_x, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0,255,0), 2)

            cv2.putText(frame, f"Closed: {closed_percentage}%",
                (text_x, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0,0,255), 2)
            
# ================== CAMERA ==================
cap = cv2.VideoCapture(0)
start_time = time.time()

window_name = "Physio Assessment - Hand + Arm"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

injured_hand = get_injured_hand()


hand_x = 0.0

async def handler(websocket):
    global hand_x
    while True:
        await websocket.send(str(hand_x))
        await asyncio.sleep(0.03)

async def websocket_main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

def start_websocket():
    asyncio.run(websocket_main())

threading.Thread(target=start_websocket, daemon=True).start()

with PoseLandmarker.create_from_options(pose_options) as pose_landmarker, \
     HandLandmarker.create_from_options(hand_options) as hand_landmarker:

    while True:

        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

=======
cap = cv2.VideoCapture(0)
start_time = time.time()

USER_ID = 1

# INIT CLASSES
db = DatabaseManager()
pose_tracker = PoseTracker()
hand_tracker = HandTracker()
combined = CombinedTracker(pose_tracker, hand_tracker)
#assessment = InitialAssessment(db, pose_tracker, hand_tracker,USER_ID)

session = GameSession()


affected_arm = db.get_affected_arm(USER_ID) # takes left or right as values

ret, frame = cap.read()
h, w, _ = frame.shape

game1 = CatchGame(w, h, side=affected_arm, session=session)

with vision.PoseLandmarker.create_from_options(pose_options) as pose_landmarker, \
     vision.HandLandmarker.create_from_options(hand_options) as hand_landmarker:

    while True:

>>>>>>> 8a0815e88fd7d9022a997057f6d1567eabe9e2a6
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

<<<<<<< HEAD
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int((time.time() - start_time) * 1000)
        
        selectedhand(injured_hand, frame, w, h, mp_image, timestamp_ms, hand_landmarker)
        # ================== POSE DETECTION ==================
        pose_result = pose_landmarker.detect_for_video(mp_image, timestamp_ms)

        if pose_result.pose_landmarks:
        
            landmarks = pose_result.pose_landmarks[0]
            
            hand_x = 1- landmarks[16].x
            
            min_hand = 0.4
            max_hand = 0.75
            
            hand_x = (hand_x - min_hand) / (max_hand - min_hand)            
            hand_x = max(0, min(1, hand_x))
            
            print(hand_x)
            
            
            message = str(hand_x)     
                
            if injured_hand == 'left':
                process_left_side(frame, landmarks, w, h)
            else:
                process_right_side(frame, landmarks, w, h)
                
            
        # ================== SHOW FRAME ==================
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
=======
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb_frame)
        timestamp_ms = int((time.time() - start_time) * 1000)

        combined.run(frame, w, h, mp_image, timestamp_ms,
                     hand_landmarker, pose_landmarker, affected_arm)

        #cv2.imshow("Rehab Game", frame)
        
        game1.update_basket(
            combined,
            w, h,
            frame,
            db,
            USER_ID
        )
        game1.update_object()
        game1.check_catch()
        game1.draw(frame)

        #session.add_data(
        #    pose_tracker.current_shoulder,
        #    pose_tracker.current_elbow,
        #    hand_tracker.current_grip,
        #    pose_tracker.current_shoulder  # external rotation approx
        #)

        cv2.imshow("eggs Game", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#averages = session.get_averages()

#db.submit_game_session(
#    USER_ID,
#    averages["shoulder"],
#    averages["elbow"],
#    averages["grip"],
#    averages["rotation"]
#)

cap.release()
cv2.destroyAllWindows()

#assessment.save()
session.submit(USER_ID)
>>>>>>> 8a0815e88fd7d9022a997057f6d1567eabe9e2a6
