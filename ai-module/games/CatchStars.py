import cv2
import mediapipe as mp
import socket
import json
import time
from collections import deque

# Import your existing hand tracker
from hand_tracker import HandTracker
from angle_math import AngleMath

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
# Main tracker for Catching Stars
# ------------------------------------------------------------
class CatchStarsTracker:
    def __init__(self, injured_hand="left", unity_ip="127.0.0.1", unity_port=5052):
        self.injured_hand = injured_hand.lower()
        self.sender = UnitySender(unity_ip, unity_port)

        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Your hand tracker (for smoothing and angle storage)
        self.hand_tracker = HandTracker()

        # Smoothing buffer for hand closed state
        self.hand_closed_buffer = deque(maxlen=5)

    def compute_hand_closed(self):
        """Return True if all fingers are sufficiently flexed (closed fist)."""
        angles = self.hand_tracker.finger_angles
        # Thresholds (degrees) – adjust as needed
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
        # Smooth the boolean over last few frames
        self.hand_closed_buffer.append(closed)
        # Return true if majority of recent frames are closed
        return sum(self.hand_closed_buffer) > len(self.hand_closed_buffer) // 2

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            frame = cv2.flip(frame, 1)  # mirror
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            palm_x = 0.5
            palm_y = 0.5
            hand_closed = False

            if result.multi_hand_landmarks and result.multi_handedness:
                # Find the injured hand
                for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                    handedness = result.multi_handedness[idx].classification[0].label.lower()
                    if handedness == self.injured_hand:
                        # Update hand tracker with current landmarks
                        self.update_hand_tracker(hand_landmarks, frame, w, h)

                        # Get palm position (wrist landmark index 0)
                        wrist = hand_landmarks.landmark[0]
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

            # Optional: draw on frame for debugging
            cv2.putText(frame, f"Hand closed: {hand_closed}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if result.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            cv2.imshow("Catching Stars Tracker", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def update_hand_tracker(self, hand_landmarks, frame, w, h):
        """Calculate smoothed finger angles using your HandTracker logic."""
        raw_angles = {
            "thumb": AngleMath.calculate_angle(hand_landmarks.landmark[0],
                                               hand_landmarks.landmark[1],
                                               hand_landmarks.landmark[4]),
            
            "index": AngleMath.calculate_angle(hand_landmarks.landmark[0],
                                               hand_landmarks.landmark[5],
                                               hand_landmarks.landmark[8]),
            
            "middle": AngleMath.calculate_angle(hand_landmarks.landmark[0],
                                                hand_landmarks.landmark[9],
                                                hand_landmarks.landmark[12]),
            
            "ring": AngleMath.calculate_angle(hand_landmarks.landmark[0],
                                              hand_landmarks.landmark[13],
                                              hand_landmarks.landmark[16]),
            
            "pinky": AngleMath.calculate_angle(hand_landmarks.landmark[0],
                                               hand_landmarks.landmark[17],
                                               hand_landmarks.landmark[20])
        }
        for finger, angle in raw_angles.items():
            prev = self.hand_tracker.finger_angles.get(finger)
            cleaned = AngleMath.remove_spikes(prev, angle)
            velocity = 0 if prev is None else abs(cleaned - prev)
            smoothed = AngleMath.smooth_angle(prev, cleaned, velocity)
            self.hand_tracker.finger_angles[finger] = smoothed
            # Update max (if needed for assessment)
            if smoothed is not None:
                self.hand_tracker.max_finger_angles[finger] = max(
                    self.hand_tracker.max_finger_angles[finger], smoothed
                )
        self.hand_tracker.current_hand_landmarks = hand_landmarks


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    # For left injured hand, change to "right" if needed
    tracker = CatchStarsTracker(injured_hand="left", unity_ip="127.0.0.1", unity_port=5052)
    tracker.run()