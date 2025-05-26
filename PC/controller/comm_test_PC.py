import serial
import time

def init_serial():
    global ser
    ser = serial.Serial('COM3', 38400, timeout=1)
    time.sleep(2)

def joystick_read():
    ser.write(b'a')#コマンド送信
    xdata = ser.read(2)            # 2バイト受信
    ydata = ser.read(2)            # 2バイト受信
    if len(xdata) == 2:
        x = (xdata[0] << 8) | xdata[1]  # 上位バイト << 8 + 下位バイト
    else:
        print("受信失敗")
    if len(ydata) == 2:
        y = (ydata[0] << 8) | ydata[1]
        #print(f"{x},{y}")
    return x, y

def LED_0():
    command = b'b'
    count = b'0'
    ser.write(command+count)
def LED_1():
    command = b'b'
    count = b'1'
    ser.write(command+count)
def LED_2():
    command = b'b'
    count = b'2'
    ser.write(command+count)
def LED_3():
    command = b'b'
    count = b'3'
    ser.write(command+count)
def reply_read():
    reply = ser.read(1)
    if reply == b'\x06':
        print("ACK")
    elif reply == b'\x15':
        print("NACK")
    else:
        print("Unknown response")
def main():
    print('Aruduinoと通信開始')
    init_serial()
    print('q: 終了, a: ジョイスティックの値取得, 0-3: LED点灯')
    try:
        while True:
            key = input("> ")
            if key == 'q':
                print('終了')
                break
            elif key == 'a':
                x, y = joystick_read()
                print(f'(x,y)=({x},{y})')
            elif key == '0':
                LED_0()
            elif key == '1':
                LED_1()
            elif key == '2':
                LED_2()
            elif key == '3':
                LED_3()
            reply_read()    
    except KeyboardInterrupt:
            print('通信終了')
    finally:
        ser.close()
        print('Serial port closed')

if __name__ == '__main__':
    print('キーボード入力でArduinoと通信テスト')
    main()