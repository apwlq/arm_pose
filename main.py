import cv2
import mediapipe as mp

# MediaPipe 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 포즈 추출을 위한 Pose 객체 생성
pose = mp_pose.Pose()

# 웹캠 캡처
cap = cv2.VideoCapture(0)


def check_hand_position(landmarks):
    # 팔꿈치와 손목의 좌표 가져오기
    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

    # 손이 팔꿈치보다 위에 있으면 up, 아래면 down, 중간이면 neutral
    if wrist.y < elbow.y:
        return "up"
    elif wrist.y > elbow.y:
        return "down"
    else:
        return "neutral"


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
        # 랜드마크 그리기
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 손과 팔꿈치 위치 확인
        position = check_hand_position(results.pose_landmarks.landmark)

        # 텍스트 표시
        cv2.putText(image, position, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 화면에 이미지 출력
    cv2.imshow('Hand Position', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
