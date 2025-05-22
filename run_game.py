from PC.game.main import main
from PC.controller.serial_reader import get_input_from_serial
from PC.controller.joystick_mapper import parse_response

def joystick_input():
    raw = get_input_from_serial()
    return raw

if __name__ == "__main__":
    import sys
    if "debug" in sys.argv:
        main()  # キーボードモード
    else:
        main(control_input=joystick_input)  # 通常モード
