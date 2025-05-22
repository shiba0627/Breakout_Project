# PC/controller/serial_reader.py

import serial
import time

# シリアルポートとボーレートは適宜変更
SERIAL_PORT = 'COM3'
BAUD_RATE = 38400
REQUEST_COMMAND = b'R'  # 状態要求コマンド（例）

ser = None

MAX_RETRY = 3
RETRY_INTERVAL = 0.05
ERROR_TIMEOUT = 1.0  # 秒

last_valid_response = "0500"  # 仮の初期値
retry_count = 0
error_flag = False

def init_serial():
    global ser
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # 初期化待ち

def get_input_from_serial():
    global last_valid_response, retry_count
    try:
        if ser is None:
            init_serial()

        # 状態要求コマンドを送信
        ser.write(REQUEST_COMMAND)

        # 応答受信（最大50ms待機）
        time.sleep(0.05)
        if ser.in_waiting >= 6:  # 4バイト + 1bit + 1bit を想定（ここは仕様に合わせて調整）
            data = ser.read(6).decode('ascii', errors='ignore')
            last_valid_response = data
            retry_count = 0
            return data
        else:
            retry_count += 1
            if retry_count >= 3:
                print("通信エラー：3回連続で応答不正")
            return last_valid_response
    except Exception as e:
        print(f"通信エラー: {e}")
        return last_valid_response
    
def send_lives_to_arduino(lives: int):
    if ser is None:
        init_serial()

    # lives = 0〜3 の範囲のみ送信
    if 0 <= lives <= 3:
        try:
            command = f"L{lives}".encode()
            ser.write(command)
            ack = ser.read(1)
            if ack == b'\x06':
                print(f"残機 {lives} をArduinoに送信 → ACK")
            else:
                print("ArduinoからNACKまたは無応答")
        except Exception as e:
            print(f"送信エラー: {e}")

def get_input_from_serial():
    global retry_count, last_valid_response, error_flag

    try:
        if ser is None:
            init_serial()

        start_time = time.time()
        response = None

        # 状態要求送信
        ser.write(REQUEST_COMMAND)

        # 応答待機（50ms x 最大3回）
        while time.time() - start_time < ERROR_TIMEOUT:
            if ser.in_waiting >= 6:
                response = ser.read(6).decode('ascii', errors='ignore')
                if len(response) == 6:
                    retry_count = 0
                    last_valid_response = response
                    error_flag = False
                    return response
                else:
                    break
            time.sleep(RETRY_INTERVAL)

        # 応答不正またはなし
        retry_count += 1
        if retry_count >= MAX_RETRY:
            error_flag = True
            print("通信エラー: 応答不正または無応答")
        return last_valid_response

    except Exception as e:
        error_flag = True
        print(f"通信例外: {e}")
        return last_valid_response

def is_communication_error():
    return error_flag
