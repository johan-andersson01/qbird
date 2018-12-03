import sys, pygame

def check_collision(screen, birdrect, obstacles):
    top_collision      = birdrect.top < 0
    obstacle_collision = birdrect.collidelist(list(map(lambda obs: obs[1], obstacles)))
    ground_collision   = birdrect.bottom > screen.get_height()
    return ground_collision or top_collision or obstacle_collision != -1


def move_obstacle(screen, obstacle_rect, movement):
    if obstacle_rect.right < 0:
        obstacle_rect.left = screen.get_width()
    else:
        obstacle_rect = obstacle_rect.move(movement)
    return obstacle_rect


def move_obstacles(screen, obstacles, movement):
    return list(map(lambda obs: (obs[0], move_obstacle(screen, obs[1], movement)), obstacles))


if __name__ == "__main__":
    pygame.init()
    w, h = 320, 240
    jump = [0,-60]
    gravity = [0, 3]
    obstacle_speed = [-3, 0]
    white = 255,255,255
    screen = pygame.display.set_mode((w,h))

    bird = pygame.image.load("bird.png")
    birdrect = bird.get_rect(left=5, centery=screen.get_height()/2)

    obstacle_top = pygame.transform.scale(pygame.image.load("obstacle-top.png"), (64,64))
    ob_top_rect = obstacle_top.get_rect(topleft=(screen.get_width()/2, 0))

    obstacle_bot = pygame.transform.scale(pygame.image.load("obstacle-bottom.png"), (64,64))
    ob_bot_rect = obstacle_bot.get_rect(bottomleft=(screen.get_width()/2, screen.get_height()))

    obstacles = [(obstacle_bot, ob_bot_rect), (obstacle_top, ob_top_rect)]

    clock = pygame.time.Clock()
    game_over = False
    while True:
        if game_over:
            print('game over!')
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                birdrect = birdrect.move(jump)

        clock.tick(30)
        birdrect = birdrect.move(gravity)
        obstacles = move_obstacles(screen, obstacles, obstacle_speed)
        game_over = check_collision(screen, birdrect, obstacles)

        # draw
        screen.fill(white)

        for img, rect in obstacles:
            screen.blit(img, rect)
        screen.blit(bird, birdrect)

        pygame.display.flip()
