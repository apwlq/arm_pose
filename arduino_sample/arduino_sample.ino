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