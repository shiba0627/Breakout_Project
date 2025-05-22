// ピン定義
const int joystickXPin = A0;
const int startButtonPin = 2;
const int pauseButtonPin = 3;
const int ledPins[3] = {4, 5, 6};  // 残機表示用LED（最大3）

void setup() {
  Serial.begin(38400);

  pinMode(startButtonPin, INPUT_PULLUP);
  pinMode(pauseButtonPin, INPUT_PULLUP);

  for (int i = 0; i < 3; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    // 状態要求コマンド
    if (command == 'R') {
      int xValue = analogRead(joystickXPin);
      bool startPressed = digitalRead(startButtonPin) == LOW;
      bool pausePressed = digitalRead(pauseButtonPin) == LOW;

      char buffer[8];
      snprintf(buffer, sizeof(buffer), "%04d%d%d", xValue, startPressed, pausePressed);
      Serial.print(buffer);
    }

    // 残機表示コマンド（L<1バイト>）
    else if (command == 'L') {
      while (!Serial.available());  // 1バイト待機
      char lifeChar = Serial.read();

      if (lifeChar >= '0' && lifeChar <= '3') {
        int lives = lifeChar - '0';
        updateLivesLED(lives);
        Serial.write(0x06);  // ACK
      } else {
        Serial.write(0x15);  // NACK
      }
    }

    // 想定外のコマンド
    else {
      Serial.write(0x15);  // NACK
    }
  }
}

// 残機に応じてLED点灯
void updateLivesLED(int lives) {
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPins[i], (i < lives) ? HIGH : LOW);
  }
}
