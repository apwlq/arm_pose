import cv2
import mediapipe as mp
import serial
import time
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

# Tkinter GUI 설정
root = tk.Tk()
root.withdraw()  # 메인 윈도우 숨김

# 사용자에게 COM 포트를 입력받음
port = simpledialog.askstring("Input", "Enter COM port (e.g., COM3):", parent=root)

arduino = None  # 아두이노 시리얼 객체 초기화

if port and port.strip():  # 입력값이 없거나 빈 문자열이 아닐 경우
    try:
        arduino = serial.Serial(port, 9600)  # 입력받은 포트 사용
        time.sleep(2)  # 연결 안정화를 위해 대기
    except serial.SerialException:
        messagebox.showerror("Connection Error", f"포트 '{port}'를 열 수 없습니다. 아두이노가 연결되지 않았습니다.")
else:
    messagebox.showwarning("Input Error", "포트가 입력되지 않았습니다. 아두이노가 연결되지 않아 아두이노 없이 계속 진행합니다.")

# 웹캠 선택을 위한 함수
def select_camera():
    # 사용 가능한 카메라 목록
    camera_options = []
    for i in range(10):  # 0부터 9까지의 카메라 인덱스를 확인
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_options.append(i)
            cap.release()

    if camera_options:
        # 카메라 선택을 위한 새로운 다이얼로그 생성
        camera_selection = simpledialog.askinteger("Select Camera", "사용가능 번호: " + ", ".join(map(str, camera_options)) + "\n카메라 번호 입력(기본=0):", parent=root)
        return camera_selection
    else:
        messagebox.showerror("Camera Error", "카메라를 찾을 수 없습니다. 종료.")
        return None

camera_index = select_camera()

if camera_index is None:
    exit()  # 카메라가 없으면 프로그램 종료

# MediaPipe 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 포즈 추출을 위한 Pose 객체 생성
pose = mp_pose.Pose()

# 웹캡 캡처
cap = cv2.VideoCapture(camera_index)

# neutral의 범위를 넉넉하게 설정
NEUTRAL_THRESHOLD = 0.1  # 팔꿈치와 손목의 Y 좌표 차이에서의 허용 범위

def check_hand_position(landmarks):
    # 오른쪽 팔꿈치와 손목의 좌표 가져오기
    elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

    # 손목과 팔꿈치의 Y 좌표 차이
    y_diff = wrist.y - elbow.y

    # y_diff 값을 0~254로 매핑하기
    # y_diff의 값이 -0.5 ~ 0.5라고 가정하고, 이를 0 ~ 254로 변환
    mapped_value = int(((y_diff + 0.5) / 1.0) * 254)

    # 값이 0 미만이면 0, 254 초과이면 254로 클램핑
    mapped_value = max(0, min(254, mapped_value))

    return mapped_value

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # BGR 이미지를 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # BGR로 다시 변환 (화면 표시용)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        # 오른손 관련 랜드마크만 그리기, 점을 그리지 않음
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            connections=[(mp_pose.PoseLandmark.RIGHT_ELBOW.value, mp_pose.PoseLandmark.RIGHT_WRIST.value)],
            landmark_drawing_spec=None,  # 랜드마크 점을 그리지 않음
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)  # 연결선만 그림
        )

        # 손과 팔꿈치 위치 확인 (오른손)
        analog_value = check_hand_position(results.pose_landmarks.landmark)

        # 아두이노로 아날로그 값 전송 (아두이노가 연결된 경우에만)
        if arduino:
            arduino.write(bytes([analog_value]))  # 0~254 범위의 값을 전송

        # 텍스트 표시
        cv2.putText(image, f"Analog Value: {analog_value}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "exit: q", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 화면에 이미지 출력
    cv2.imshow('Hand Position', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()  # 시리얼 포트 닫기 (아두이노가 연결된 경우)
