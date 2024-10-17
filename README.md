# 나우유씨미 2 빗방울 마술
## 1. 구현 방법
Python으로 제작한 프로그램으로, MediaPipe를 사용하여 손과 팔꿈치의 위치를 인식하고, 손이 팔꿈치보다 위에 있는지, 아래에 있는지, 중간인지에 따라 "up", "down", "neutral" 상태를 표시합니다.

## 2. 세팅 방법

### 1) 소스 코드 실행 방법
- Python 3.12 이상 설치
- 프로젝트 디렉토리에서 필요한 패키지를 설치:
  ```bash
  pip install -r requirements.txt
  ```
- 실행:
  ```bash
  python main.py
  ```

### 2) 실행 파일로 실행하는 방법
- Release에서 제공된 exe 파일을 다운로드
- exe 파일을 직접 실행

exe 파일 제작 방법
- pyinstaller 패키지 설치:
  ```bash
  pip install pyinstaller
  ```
- exe 파일 제작:
  ```bash
  pyinstaller --onefile --noconsole --name arm_pose main.py --add-data "C:/dev/arm_pose/.venv/Lib/site-packages/mediapipe/modules/pose_landmark/pose_landmark_cpu.binarypb;mediapipe/modules/pose_landmark/" --add-data "C:/dev/arm_pose/.venv/Lib/site-packages/mediapipe/modules/pose_landmark/pose_landmark_full.tflite;mediapipe/modules/pose_landmark/" --add-data "C:/dev/arm_pose/.venv/Lib/site-packages/mediapipe/modules/pose_detection/pose_detection.tflite;mediapipe/modules/pose_detection/"
  ```

## 3. 주요 라이브러리
- OpenCV: 실시간 웹캠 영상을 처리하고 화면에 표시하는 데 사용됩니다.
- MediaPipe: 손과 팔꿈치의 위치를 인식하고 추적하는 데 사용됩니다.
- PySerial: Arduino와 시리얼 통신을 하기 위해 사용됩니다.

## 4. 아두이노 예제 코드
아두이노와 연결하여 손의 위치에 따라 LED를 제어하는 예제 코드입니다.

```cpp
char receivedCommand;

void setup() {
  Serial.begin(9600);  // 시리얼 통신 속도 설정
  pinMode(LED_BUILTIN, OUTPUT);  // LED를 예시로 사용
}

void loop() {
  // 시리얼로 명령어 수신
  if (Serial.available() > 0) {
    receivedCommand = Serial.read();

    if (receivedCommand == 'U') {
      // 'U' 명령어를 받으면 (손이 위에 있을 때) LED 켜기
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("UP command received.");
    } 
    else if (receivedCommand == 'D') {
      // 'D' 명령어를 받으면 (손이 아래에 있을 때) LED 끄기
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("DOWN command received.");
    } 
    else if (receivedCommand == 'N') {
      // 'N' 명령어를 받으면 (중립) LED 깜빡이기
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
      Serial.println("NEUTRAL command received.");
    }
  }
}
```