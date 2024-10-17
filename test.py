# import cv2
# import mediapipe as mp
#
# # MediaPipe 초기화
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose
#
# # 포즈 추출을 위한 Pose 객체 생성
# pose = mp_pose.Pose()
#
# # 웹캡 캡처
# cap = cv2.VideoCapture(0)
#
# # neutral의 범위를 넉넉하게 설정
# NEUTRAL_THRESHOLD = 0.1  # 팔꿈치와 손목의 Y 좌표 차이에서의 허용 범위
#
#
# def check_hand_position(landmarks):
#     # 오른쪽 팔꿈치와 손목의 좌표 가져오기
#     elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
#     wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
#
#     # 손목과 팔꿈치의 Y 좌표 차이
#     y_diff = wrist.y - elbow.y
#
#     # 손이 팔꿈치보다 위에 있으면 up, 아래면 down, 중간이면 neutral
#     if y_diff < -NEUTRAL_THRESHOLD:
#         return "up"
#     elif y_diff > NEUTRAL_THRESHOLD:
#         return "down"
#     else:
#         return "neutral"
#
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     # BGR 이미지를 RGB로 변환
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = pose.process(image)
#
#     # BGR로 다시 변환 (화면 표시용)
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#
#     if results.pose_landmarks:
#         # 얼굴 랜드마크는 그리지 않음 (오른손 관련만 그리기)
#         # draw_landmarks 함수를 사용하여 필요한 랜드마크만 그리기, 점을 지우기 위해 style 매개변수 설정
#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             connections=[(mp_pose.PoseLandmark.RIGHT_ELBOW.value, mp_pose.PoseLandmark.RIGHT_WRIST.value)],
#             landmark_drawing_spec=None,  # 랜드마크 점을 그리지 않음
#             connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)  # 연결선만 그림
#         )
#
#         # 손과 팔꿈치 위치 확인 (오른손)
#         position = check_hand_position(results.pose_landmarks.landmark)
#
#         # 텍스트 표시
#         cv2.putText(image, position, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#
#     # 화면에 이미지 출력
#     cv2.imshow('Hand Position', image)
#
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
