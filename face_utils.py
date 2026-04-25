import cv2
import mediapipe as mp
import face_recognition
import numpy as np
import json
from scipy.spatial import distance as dist

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def calculate_ear(eye_points):
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    C = dist.euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

def check_liveness(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            left_eye_pts = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE]
            right_eye_pts = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE]
            
            ear_left = calculate_ear(left_eye_pts)
            ear_right = calculate_ear(right_eye_pts)
            ear = (ear_left + ear_right) / 2.0
            
            if ear < 0.2:
                return True
    return False

def get_face_embedding(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)
    if len(encodings) > 0:
        return json.dumps(encodings[0].tolist())
    return None

def compare_faces(known_embedding_json, current_frame):
    rgb_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    current_encodings = face_recognition.face_encodings(rgb_frame)
    if len(current_encodings) > 0:
        known_enc = np.array(json.loads(known_embedding_json))
        curr_enc = current_encodings[0]
        match = face_recognition.compare_faces([known_enc], curr_enc, tolerance=0.4)[0]
        return match
    return False