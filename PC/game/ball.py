import pygame
from PC.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS, BALL_COLOR, BALL_SPEED

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vx = BALL_SPEED
        self.vy = -BALL_SPEED

    def update(self, paddle):
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.vx *= -1

        if self.y - self.radius <= 0:
            self.vy *= -1

        # パドルと衝突
        if (paddle.y <= self.y + self.radius <= paddle.y + paddle.height and
                paddle.x <= self.x <= paddle.x + paddle.width and
                self.vy > 0):
            self.vy *= -1

        # ミス判定（画面下に落ちた）
        if self.y - self.radius > SCREEN_HEIGHT:
            self.reset()
            return True  # ミスしたと返す

        return False


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
