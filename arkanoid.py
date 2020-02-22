import pygame
from random import randint

class arkanoidMain:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Arkanoid')

        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.ball_velocity_x, self.ball_velocity_y = 5, -5


        self.points = 0
        self.run = True
        self.left_arrow_down = False
        self.right_arrow_down = False
        self.has_space_pressed = False
        self.lost = False
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.loss_text = self.font.render(str(self.points), True, (0, 0, 0), (255, 0, 0))
        self.loss_textRect = self.loss_text.get_rect()
        self.loss_textRect.center = (self.screen_width//2, self.screen_height//2)
                

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
            self.collide_check()
            self.eventmanager()
            self.movement()
            self.lose_screen()
            self.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
    
    def lose_screen(self):
        if self.lost:
            self.screen.fill((255, 0, 0))
            self.ball.kill()
            self.ball_velocity_x = 0
            self.ball_velocity_y = 0
            self.loss_text = self.font.render(str(self.points), True, (0, 0, 0), (255, 0, 0))
            self.loss_textRect = self.loss_text.get_rect()
            self.loss_textRect.center = (self.screen_width//2, self.screen_height//2)
            self.screen.blit(self.loss_text, self.loss_textRect)
        else:
            self.screen.fill((128, 128, 128))


    
    def collide_check(self):
        bricks = len(self.bricks.sprites())
        pygame.sprite.spritecollide(self.ball, self.bricks, 1)
        if len(self.bricks.sprites()) < bricks:
            self.points += bricks - len(self.bricks.sprites())

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
                self.ball.rect.midbottom = self.paddle.rect.midtop
        # moving paddle right if key is pressed also restricting movement in screen size
        if self.right_arrow_down:
            if self.paddle.rect.right + 20 > self.screen_width:
                self.paddle.rect.right = self.screen_width
            else:
                self.paddle.rect.right += 20
            if not self.has_space_pressed:
                self.ball.rect.midbottom = self.paddle.rect.midtop

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
                if (self.ball.rect.left > self.paddle.rect.left and self.ball.rect.right < self.paddle.rect.right) and (self.ball.rect.bottom + self.ball_velocity_y > self.paddle.rect.top):
                    self.ball.rect.bottom = self.paddle.rect.top
                    if self.ball.rect.midbottom == self.paddle.rect.midtop:
                        self.ball_velocity_y = 8
                    elif self.ball.rect.bottomleft < self.paddle.rect.midtop:
                        print(self.paddle.rect.midtop, self.ball.rect.midleft)
                        self.ball_velocity_x = -1 * (self.paddle.rect.midtop[0] - self.ball.rect.bottomleft[0])//9
                        self.ball_velocity_y = -8 - self.ball_velocity_x
                    elif self.ball.rect.bottomright > self.paddle.rect.midtop:
                        print(self.paddle.rect.midtop, self.ball.rect.midleft)
                        self.ball_velocity_x = (-1 * (self.paddle.rect.midtop[0] - self.ball.rect.bottomright[0])//9)
                        self.ball_velocity_y = -8 + self.ball_velocity_x

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
    