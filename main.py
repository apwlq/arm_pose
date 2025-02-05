import cv2
import mediapipe as mp
import serial
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import math

# Tkinter GUI 설정
root = tk.Tk()
root.withdraw()

# 사용자에게 COM 포트를 입력받음
port = simpledialog.askstring("Input", "Enter COM port (e.g., COM3):", parent=root)

arduino = None

if port and port.strip():
    try:
        arduino = serial.Serial(port, 9600)
        time.sleep(2)
    except serial.SerialException:
        messagebox.showerror("Connection Error", f"포트 '{port}'를 열 수 없습니다.")
else:
    messagebox.showwarning("Input Error", "포트가 입력되지 않았습니다.")

# 웹캠 선택
def select_camera():
    camera_options = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_options.append(i)
            cap.release()

    if camera_options:
        camera_selection = simpledialog.askinteger("Select Camera", "사용가능 번호: " + ", ".join(map(str, camera_options)) + "\n카메라 번호 입력(기본=0):", parent=root)
        return camera_selection
    else:
        messagebox.showerror("Camera Error", "카메라를 찾을 수 없습니다.")
        return None

camera_index = select_camera()
if camera_index is None:
    exit()

# MediaPipe 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(camera_index)

NEUTRAL_THRESHOLD = 0.1
MIN_ARM_RATIO = 1 / 16


def calculate_distance(point1, point2):
    """두 랜드마크 간 거리 계산"""
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def check_hand_position(landmarks):
    """손목과 팔꿈치 Y 좌표 차이 기반 값 반환"""
    elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    y_diff = wrist.y - elbow.y

    mapped_value = 30 - int(((y_diff + 0.5) / 1.0) * 20)
    mapped_value = max(10, min(30, mapped_value))

    if abs(y_diff) <= NEUTRAL_THRESHOLD:
        mapped_value = 20

    return mapped_value


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    min_arm_length = MIN_ARM_RATIO * width

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    analog_value = 0

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        right_elbow = mp_pose.PoseLandmark.RIGHT_ELBOW.value
        right_wrist = mp_pose.PoseLandmark.RIGHT_WRIST.value

        # 오른쪽 팔 랜드마크 확인
        if landmarks[right_elbow].visibility > 0.5 and landmarks[right_wrist].visibility > 0.5:
            arm_length = calculate_distance(landmarks[right_elbow], landmarks[right_wrist]) * width

            # 거리 및 값 확인
            if arm_length >= min_arm_length:
                analog_value = check_hand_position(landmarks)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                connections=[(right_elbow, right_wrist)],
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )
        else:
            # 오른팔이 보이지 않는 경우 0으로 설정
            analog_value = 0

    if arduino:
        arduino.write(bytes([analog_value]))

    cv2.putText(image, f"Analog Value: {analog_value}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, "exit: q", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Position', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
