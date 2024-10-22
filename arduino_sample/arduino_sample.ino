int receivedValue;  // 시리얼로 받은 값을 저장할 변수

void setup() {
  Serial.begin(9600);  // 시리얼 통신 속도 설정
  pinMode(LED_BUILTIN, OUTPUT);  // LED를 예시로 사용 (내장 LED 핀)
}

void loop() {
  // 시리얼로 값 수신
  if (Serial.available() > 0) {
    receivedValue = Serial.read();  // 시리얼로 값 읽기

    // 받은 값이 0~254 범위에 있는지 확인 (1바이트 안에서)
    if (receivedValue >= 0 && receivedValue <= 254) {
      // 받은 값으로 LED 밝기를 제어 (PWM 출력)
      analogWrite(LED_BUILTIN, receivedValue);
      
      // 수신된 값을 시리얼 모니터에 출력 (디버깅용)
      Serial.print("Received analog value: ");
      Serial.println(receivedValue);
    }
  }
}
