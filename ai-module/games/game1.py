import os
import sys
import cv2
import numpy as np
import socket
import json
import time
from collections import deque

# MediaPipe Tasks Vision
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Import your existing hand tracker and angle utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracker.hand_tracker import HandTracker
from utils.angle_math import AngleMath

# ------------------------------------------------------------
# UDP sender to Unity
# ------------------------------------------------------------
class UnitySender:
    def __init__(self, ip="127.0.0.1", port=5052):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (ip, port)

    def send(self, data_dict):
        try:
            msg = json.dumps(data_dict)
            self.sock.sendto(msg.encode(), self.addr)
        except Exception as e:
            print(f"UDP error: {e}")

# ------------------------------------------------------------
# Main tracker for Catching Stars (using Tasks API)
# ------------------------------------------------------------
class CatchStarsTracker:
    def __init__(self, injured_hand="left", unity_ip="127.0.0.1", unity_port=5052,
                 model_path="hand_landmarker.task"):
        self.injured_hand = injured_hand.lower()
        self.sender = UnitySender(unity_ip, unity_port)

        # Load the hand landmarker task model
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,   # we'll process frame by frame
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

        # Your hand tracker (for smoothing and angle storage)
        self.hand_tracker = HandTracker()

        # Smoothing buffer for hand closed state
        self.hand_closed_buffer = deque(maxlen=5)

        # Timestamp for video mode (milliseconds)
        self.timestamp_ms = 0

    def compute_hand_closed(self):
        """Return True if all fingers are sufficiently flexed (closed fist)."""
        angles = self.hand_tracker.finger_angles
        thresholds = {
            "thumb": 40,
            "index": 30,
            "middle": 30,
            "ring": 30,
            "pinky": 30
        }
        closed = True
        for finger, thresh in thresholds.items():
            ang = angles.get(finger)
            if ang is None or ang > thresh:
                closed = False
                break
        self.hand_closed_buffer.append(closed)
        # Majority vote
        return sum(self.hand_closed_buffer) > len(self.hand_closed_buffer) // 2

    def update_hand_tracker(self, hand_landmarks, frame, w, h):
        """
        Convert MediaPipe Tasks NormalizedLandmarks to your HandTracker format
        and compute smoothed angles.
        """
        # Tasks returns a list of NormalizedLandmark objects with x,y,z
        # We'll create a simple wrapper so AngleMath can access .x, .y, .z
        class LandmarkWrapper:
            def __init__(self, lm):
                self.x = lm.x
                self.y = lm.y
                self.z = lm.z if hasattr(lm, 'z') else 0.0

        lm_list = [LandmarkWrapper(lm) for lm in hand_landmarks]

        raw_angles = {
            "thumb": AngleMath.calculate_angle(lm_list[0], lm_list[1], lm_list[4]),
            "index": AngleMath.calculate_angle(lm_list[0], lm_list[5], lm_list[8]),
            "middle": AngleMath.calculate_angle(lm_list[0], lm_list[9], lm_list[12]),
            "ring": AngleMath.calculate_angle(lm_list[0], lm_list[13], lm_list[16]),
            "pinky": AngleMath.calculate_angle(lm_list[0], lm_list[17], lm_list[20])
        }
        for finger, angle in raw_angles.items():
            prev = self.hand_tracker.finger_angles.get(finger)
            cleaned = AngleMath.remove_spikes(prev, angle)
            velocity = 0 if prev is None else abs(cleaned - prev)
            smoothed = AngleMath.smooth_angle(prev, cleaned, velocity)
            self.hand_tracker.finger_angles[finger] = smoothed
            if smoothed is not None:
                self.hand_tracker.max_finger_angles[finger] = max(
                    self.hand_tracker.max_finger_angles[finger], smoothed
                )
        self.hand_tracker.current_hand_landmarks = hand_landmarks  # store raw

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # For timestamp increment (assuming ~30 fps)
        frame_timestamp_ms = 0

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            frame = cv2.flip(frame, 1)  # mirror
            h, w = frame.shape[:2]

            # Convert to MediaPipe Image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Detect hands using Tasks API (video mode)
            frame_timestamp_ms += 33  # approx 30 fps, adjust if needed
            detection_result = self.landmarker.detect_for_video(mp_image, frame_timestamp_ms)

            palm_x = 0.5
            palm_y = 0.5
            hand_closed = False

            if detection_result.hand_landmarks and detection_result.handedness:
                # Find the injured hand
                for idx, hand_landmarks in enumerate(detection_result.hand_landmarks):
                    handedness = detection_result.handedness[idx][0].category_name.lower()
                    if handedness == self.injured_hand:
                        # Update your hand tracker with the landmarks
                        self.update_hand_tracker(hand_landmarks, frame, w, h)

                        # Palm position = wrist (landmark 0)
                        wrist = hand_landmarks[0]
                        palm_x = wrist.x
                        palm_y = wrist.y

                        hand_closed = self.compute_hand_closed()
                        break

            # Prepare and send data
            data = {
                "palm_x": palm_x,
                "palm_y": palm_y,
                "hand_closed": hand_closed,
                "timestamp": time.time()
            }
            self.sender.send(data)

            # Optional debug drawing
            cv2.putText(frame, f"Hand closed: {hand_closed}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if detection_result.hand_landmarks:
                # Draw landmarks using MediaPipe's drawing utils (optional)
                for hand_landmarks in detection_result.hand_landmarks:
                    for lm in hand_landmarks:
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
            cv2.imshow("Catching Stars Tracker (Tasks)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.landmarker.close()

# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    # Provide the path to your hand_landmarker.task model file
    # You can download it from MediaPipe or use the one from Unity package
    MODEL_PATH = r"C:\Users\Mulik\physio-gamification-project\ai-module\hand_landmarker.task"   # change to actual path
    tracker = CatchStarsTracker(injured_hand="left", unity_ip="127.0.0.1",
                                unity_port=5052, model_path=MODEL_PATH)
    tracker.run()