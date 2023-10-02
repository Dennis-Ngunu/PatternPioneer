import pygame
import sys
import random

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_DIAMETER = 10
BALL_RADIUS = BALL_DIAMETER // 2
BRICK_WIDTH, BRICK_HEIGHT = 60, 15
PADDLE_Y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
BRICK_ROWS = 5
BRICK_COLS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

class Ball:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, BALL_DIAMETER, BALL_DIAMETER)
        self.dx = dx
        self.dy = dy
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def move(self):
        self.rect.left += self.dx
        self.rect.top += self.dy
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

def create_bricks():
    bricks = []
    for i in range(BRICK_ROWS):
        for j in range(BRICK_COLS):
            color = random.choice([RED, GREEN, BLUE])
            bricks.append(Brick(j * (BRICK_WIDTH + 10) + 50, i * (BRICK_HEIGHT + 5) + 25, color))
    return bricks

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    bricks = create_bricks()
    paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, PADDLE_Y)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 2, 2)

    # Game variables
    score = 0
    high_score = 0
    start_time = pygame.time.get_ticks()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.rect.x -= 20
                elif event.key == pygame.K_RIGHT:
                    paddle.rect.x += 20

        # Update paddle position based on mouse movement
        mouse_x, _ = pygame.mouse.get_pos()
        paddle.rect.x = mouse_x - PADDLE_WIDTH // 2

        if not game_over:
            ball.move()

            # Check collision with paddle
            if ball.rect.colliderect(paddle.rect):
                ball.dy = -ball.dy

            # Check collision with bricks
            for brick in bricks:
                if ball.rect.colliderect(brick.rect):
                    ball.dy = -ball.dy
                    bricks.remove(brick)
                    score += 1

            # Check game over condition
            if all(brick.rect.colliderect(ball.rect) for brick in bricks):
                game_over = True
                if score > high_score:
                    high_score = score

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, brick.color, brick.rect)

        # Draw the paddle
        pygame.draw.rect(screen, WHITE, paddle.rect)

        # Draw the ball
        pygame.draw.circle(screen, ball.color, (ball.rect.centerx, ball.rect.centery), BALL_RADIUS)

        # Draw the timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = font.render("Time: {}".format(elapsed_time), True, WHITE)
        screen.blit(timer_text, (10, 10))

        # Draw the score and high score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        high_score_text = font.render("High Score: {}".format(high_score), True, WHITE)
        screen.blit(score_text, (10, 40))
        screen.blit(high_score_text, (10, 70))

        # Draw the reset button
        reset_text = font.render("Reset", True, WHITE)
        reset_rect = reset_text.get_rect(center=(SCREEN_WIDTH - 60, 30))
        pygame.draw.rect(screen, RED, reset_rect)
        screen.blit(reset_text, reset_rect.topleft)

        if game_over:
            # Display game over message
            game_over_text = font.render("Game Over! Press R to reset.", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect.topleft)

            # Update high score
            if score > high_score:
                high_score = score

        pygame.display.flip()
        clock.tick(60)

        # Check for reset
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            bricks = create_bricks()
            paddle.rect.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
            ball.reset()
            score = 0
            start_time = pygame.time.get_ticks()
            game_over = False

if __name__ == "__main__":
    main()
