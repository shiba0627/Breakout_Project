import pygame
from PC.utils.config import SCREEN_WIDTH, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR, PADDLE_SPEED

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = 550  # 画面下に配置（SCREEN_HEIGHTよりやや上）
        self.vx = 0

    def move_left(self):
        self.vx = -PADDLE_SPEED

    def move_right(self):
        self.vx = PADDLE_SPEED

    def stop(self):
        self.vx = 0

    def update(self):
        self.x += self.vx
        # 画面端の制限
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        # フレームごとに速度をリセット
        self.vx = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
