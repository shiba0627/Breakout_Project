const int X_pin = A0;
const int Y_pin = A1;

int LED1 = 2;
int LED2 = 3;
int LED3 = 4;

void setup() {
  Serial.begin(38400);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
}

void loop() {
  char c;//バッファから取り出したコマンドを格納
  char num;//LED表示数コマンドを格納
  char cmd;//バッファの先頭を見る用
  if( Serial.available() >= 1){
    cmd = Serial.peek();//バッファの先頭を確認
    int required_bytes = 0;//読み込むバイト数
    switch(cmd){
      case 'a':required_bytes = 1;break;//ジョイスティック値の読み取りコマンド
      case 'b':required_bytes = 2;break;//LED表示コマンド
      default:required_bytes = 1;break;//想定外 1byte読み出す
    }
    if(Serial.available() >= required_bytes){
      c = Serial.read();//コマンドを取り出す
      if (c == 'a'){
        //Serial.write('a');
        //Serial.write(analogRead(X_pin));
        int Xvalue = analogRead(X_pin);          //0〜1023
        Serial.write((Xvalue >> 8) & 0xFF);      //上位バイト
        Serial.write(Xvalue & 0xFF);             //下位バイト
        int Yvalue = analogRead(Y_pin);          //0〜1023
        Serial.write((Yvalue >> 8) & 0xFF);      //上位バイト
        Serial.write(Yvalue & 0xFF);             //下位バイト
        Serial.write(0x06);///ACK肯定応答
      }else if (c == 'b'){
        num = Serial.read();//LED表示貸数を取り出す(ライフ)
        if(num == '0'){
          digitalWrite(LED1, LOW);
          digitalWrite(LED2, LOW);
          digitalWrite(LED3, LOW);
          Serial.write(0x06);///ACK肯定応答
        }else if (num == '1'){
          digitalWrite(LED1, HIGH);
          digitalWrite(LED2, LOW);
          digitalWrite(LED3, LOW);
          Serial.write(0x06);///ACK肯定応答
        }else if (num == '2'){
          digitalWrite(LED1, HIGH);
          digitalWrite(LED2, HIGH);
          digitalWrite(LED3, LOW);
          Serial.write(0x06);///ACK肯定応答
        }else if (num == '3'){
          digitalWrite(LED1, HIGH);
          digitalWrite(LED2, HIGH);
          digitalWrite(LED3, HIGH);
          Serial.write(0x06);///ACK肯定応答
        }else {
          Serial.write(0x15);///NACK想定外
        }
      }else {
          Serial.write(0x15);///NACK想定外
        }
    }
  }
}    