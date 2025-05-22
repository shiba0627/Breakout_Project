# joystick_mapper.py

# 中央（無操作）のしきい値を定義
CENTER_MIN = 490
CENTER_MAX = 530
THRESHOLD_LEFT = CENTER_MIN
THRESHOLD_RIGHT = CENTER_MAX

def parse_response(response):
    """
    :param response: 6文字のASCIIデータ（例："05101\n"）
    :return: dict {"direction": ..., "start": ..., "pause": ...}
    """
    result = {"direction": None, "start": False, "pause": False}

    if not response or len(response) < 6:
        return result

    try:
        x_val = int(response[:4])
        result["start"] = response[4] == '1'
        result["pause"] = response[5] == '1'

        if x_val < CENTER_MIN:
            result["direction"] = "left"
        elif x_val > CENTER_MAX:
            result["direction"] = "right"

        return result
    except ValueError:
        return result
