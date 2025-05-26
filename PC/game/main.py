import pygame
from PC.game.paddle import Paddle
from PC.game.ball import Ball
from PC.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from PC.controller.serial_reader import (
    send_lives_to_arduino,
    get_input_from_serial,
    is_communication_error,
)
from PC.controller.joystick_mapper import parse_response

def main(control_input=None):
    print(control_input)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout Game")
    clock = pygame.time.Clock()

    paddle = Paddle()
    ball = Ball()
    lives = 3
    if control_input is not None:
        send_lives_to_arduino(lives)
    font = pygame.font.SysFont(None, 36)

    game_started = control_input is None
    paused = False
    running = True

    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 入力取得
        input_data = {"direction": None, "start": False, "pause": False}
        if control_input is None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                input_data["direction"] = "left"
            if keys[pygame.K_RIGHT]:
                input_data["direction"] = "right"
        else:
            raw = control_input()  # 例：serialからのraw文字列
            input_data = parse_response(raw)

        # スタート・ポーズ処理
        if input_data["start"]:
            game_started = True
            paused = False

        if input_data["pause"]:
            paused = not paused
            pygame.time.wait(300)  # 押しっぱなし防止のため一瞬待つ

        # ゲームがスタートしていて、ポーズ中でなく、通信エラーでもない場合
        if game_started and not paused and not is_communication_error():
            if input_data["direction"] == "left":
                paddle.move_left()
            elif input_data["direction"] == "right":
                paddle.move_right()

            paddle.update()
            is_missed = ball.update(paddle)

            if is_missed:
                lives -= 1
                if control_input is not None:
                    send_lives_to_arduino(lives)
                if lives <= 0:
                    print("Game Over")
                    running = False
                else:
                    pygame.time.wait(1000)

            paddle.draw(screen)
            ball.draw(screen)

        elif paused:
            msg = font.render("PAUSED", True, (255, 255, 0))
            screen.blit(msg, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        # 残機表示
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

        # 通信エラー表示
        if is_communication_error():
            err_text = font.render("通信エラー", True, (255, 0, 0))
            screen.blit(err_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()  # キーボード操作デバッグ用

