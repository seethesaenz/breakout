import pygame
from random import randint

class arkanoidMain:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Arkanoid')

        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.ball_velocity_x, self.ball_velocity_y = 18, -18

        self.points = 0
        self.run = True
        self.left_arrow_down = False
        self.right_arrow_down = False
        self.has_space_pressed = False
        self.lost = False

        self.arkanoid()

    def sprite_groups(self):
        self.bricks = pygame.sprite.Group()
        self.paddle = paddle()
        self.ball = ball()
        self.balls = pygame.sprite.GroupSingle(self.ball)
        self.paddles = pygame.sprite.GroupSingle(self.paddle)

    def arkanoid(self):
        self.sprite_groups()
        self.draw_brick()
        while self.run:
            pygame.time.delay(100)
            self.eventmanager()
            self.movement()
            self.screen.fill((128, 128, 128))
            ##make func for losing screen
            if self.lost:
                self.screen.fill((255, 0, 0))

            self.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def draw_brick(self):
        for i in range(0, 16):
            name = 's' + str(i)
            setattr(self, name, (self.bricks.add(brick(i*50))))

    def movement(self):
        # moving paddle left if key is pressed  also restricting movement in screen size
        if self.left_arrow_down:
            if self.paddle.rect.left - 20 < 0:
                self.paddle.rect.left = 0
            else:
                self.paddle.rect.left -= 20
            if not self.has_space_pressed:
                if self.paddle.rect.left - 20 < 0:
                    self.ball.rect.left = self.ball.rect.left
                else:
                    self.ball.rect.left -= 20
        # moving paddle right if key is pressed also restricting movement in screen size
        if self.right_arrow_down:
            if self.paddle.rect.right + 20 > self.screen_width:
                self.paddle.rect.right = self.screen_width
            else:
                self.paddle.rect.right += 20
            if not self.has_space_pressed:
                if self.paddle.rect.right + 20 > self.screen_width:
                    self.ball.rect.left = self.ball.rect.left
                else:
                    self.ball.rect.right += 20

        if self.has_space_pressed:
            # checking if ball is going right or left and if hits wall change the direction
            if self.ball_velocity_x > 0:
                if self.ball.rect.right + self.ball_velocity_x > self.screen_width:
                    self.ball.rect.right = self.screen_width
                    self.ball_velocity_x *= -1
                else:
                    self.ball.rect.right += self.ball_velocity_x
            else:
                if self.ball.rect.left + self.ball_velocity_x < 0:
                    self.ball.rect.left = 0
                    self.ball_velocity_x *= -1
                else:
                    self.ball.rect.right += self.ball_velocity_x
            # checking if ball is going up or down and if hits top, paddle, or bottom screen
            if self.ball_velocity_y > 0:
                if (self.ball.rect.bottom + self.ball_velocity_y > self.paddle.rect.top) and ((self.ball.rect.left > self.paddle.rect.left) and (self.ball.rect.right < self.paddle.rect.right)):
                    self.ball.rect.bottom = self.paddle.rect.top
                    self.ball_velocity_y *= -1
                elif self.ball.rect.bottom > self.screen_height:
                    self.lost = True
                else:
                    self.ball.rect.top += self.ball_velocity_y
            else:
                if self.ball.rect.top + self.ball_velocity_y < 0:
                    self.ball.rect.top = 0
                    self.ball_velocity_y *= -1
                else:
                    self.ball.rect.top += self.ball_velocity_y

    def draw(self, surface):
        self.balls.draw(surface)
        self.bricks.draw(surface)
        self.paddles.draw(surface)

    def eventmanager(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_arrow_down = True
                if event.key == pygame.K_RIGHT:
                    self.right_arrow_down = True
                if event.key == pygame.K_SPACE:
                    self.has_space_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_arrow_down = False
                if event.key == pygame.K_RIGHT:
                    self.right_arrow_down = False

class brick(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        width, height = 50, 25
        self.color = self.getrandomcolor()
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect().move(x, 30)

    def getrandomcolor(self):
        colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128)]
        color = colors[randint(1, 11)]
        return color

class paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width, height = 90, 15
        self.paddle_x, self.paddle_y = 355, 575
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 128))
        self.rect = self.image.get_rect().move(self.paddle_x, self.paddle_y)

class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width, height = 10, 10
        self.ball_x, self.ball_y = 395, 565
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.rect = pygame.rect.Rect(self.ball_x, self.ball_y, 10, 10)
        

if __name__ == "__main__":
    arkanoidMain()
    