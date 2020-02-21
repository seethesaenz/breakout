import pygame
from random import randint

class arkanoidMain:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Arkanoid')

        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.paddle_x, self.paddle_y = self.screen_width//2 - 45, self.screen_height - 25
        self.paddle = pygame.rect.Rect(self.paddle_x, self.paddle_y, 90, 15)

        self.ball_x, self.ball_y = self.paddle_x + 40, self.paddle_y - 10
        self.ball = pygame.rect.Rect(self.ball_x, self.ball_y, 10, 10)
        self.ball_velocity_x, self.ball_velocity_y = 18, -18

        self.points = 0
        self.run = True
        self.left_arrow_down = False
        self.right_arrow_down = False
        self.has_space_pressed = False
        self.lost = False

        self.arkanoid()

    def arkanoid(self):
        self.bricks = pygame.sprite.Group()
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

    def brick_collide(self):
        for brick in pygame.sprite.spritecollide(self.ball, self.bricks, 1):
            self.points += 1



    def draw_brick(self):
        for i in range(0, 16):
            count = i
            name = 's' + str(i)
            setattr(self, name, (self.bricks.add(brick(i*50, count))))

    def movement(self):
        # moving paddle left if key is pressed  also restricting movement in screen size
        if self.left_arrow_down:
            if self.paddle.left - 20 < 0:
                self.paddle.left = 0
            else:
                self.paddle.left -= 20
            if not self.has_space_pressed:
                if self.paddle.left - 20 < 0:
                    self.ball.left = self.ball.left
                else:
                    self.ball.left -= 20
        # moving paddle right if key is pressed also restricting movement in screen size
        if self.right_arrow_down:
            if self.paddle.right + 20 > self.screen_width:
                self.paddle.right = self.screen_width
            else:
                self.paddle.right += 20
            if not self.has_space_pressed:
                if self.paddle.right + 20 > self.screen_width:
                    self.ball.left = self.ball.left
                else:
                    self.ball.right += 20

        if self.has_space_pressed:
            # checking if ball is going right or left and if hits wall change the direction
            if self.ball_velocity_x > 0:
                if self.ball.right + self.ball_velocity_x > self.screen_width:
                    self.ball.right = self.screen_width
                    self.ball_velocity_x *= -1
                else:
                    self.ball.right += self.ball_velocity_x
            else:
                if self.ball.left + self.ball_velocity_x < 0:
                    self.ball.left = 0
                    self.ball_velocity_x *= -1
                else:
                    self.ball.right += self.ball_velocity_x
            # checking if ball is going up or down and if hits top, paddle, or bottom screen
            if self.ball_velocity_y > 0:
                if (self.ball.bottom + self.ball_velocity_y > self.paddle.top) and ((self.ball.left > self.paddle.left) and (self.ball.right < self.paddle.right)):
                    self.ball.bottom = self.paddle.top
                    self.ball_velocity_y *= -1
                elif self.ball.bottom > self.screen_height:
                    self.lost = True
                else:
                    self.ball.top += self.ball_velocity_y
            else:
                if self.ball.top + self.ball_velocity_y < 0:
                    self.ball.top = 0
                    self.ball_velocity_y *= -1
                else:
                    self.ball.top += self.ball_velocity_y

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 128), self.paddle)
        pygame.draw.rect(surface, (0, 0, 0), self.ball)
        self.bricks.draw(surface)

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
    def __init__(self, x, count):
        pygame.sprite.Sprite.__init__(self)
        width, height = 50, 25
        self.count = count
        self.color = self.getrandomcolor()
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect().move(x, 30)

    def getrandomcolor(self):
        colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128)]
        color = colors[randint(1, 11)]
        self.count += 1
        return color


if __name__ == "__main__":
    arkanoidMain()
    