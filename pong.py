import pygame
import random

pygame.init()
pygame.font.init()
pygame.display.set_caption("PONG")

WIN_WIDTH, WIN_HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
VEL = 5
VEL_AI = 5.5

COLLISION_PLAYER1 = pygame.USEREVENT +1
COLLISION_PLAYER2 = pygame.USEREVENT +2


WHITE = (255, 255, 255)
BLACK = (0,0,0)

SCORE_FONT = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 30)
WINNER_FONT = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 100)




def handle_player2_movement(keys_pressed, player2):
    if keys_pressed[pygame.K_UP] and player2.y > 0:
        player2.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and player2.y + player2.height < WIN_HEIGHT:
        player2.y += VEL

def handle_player1_movement(keys_pressed, player1, mode):
    if mode == "mp":
        if keys_pressed[pygame.K_w] and player1.y > 0:
            player1.y -= VEL
        elif keys_pressed[pygame.K_s] and player1.y + player1.height < WIN_HEIGHT:
            player1.y += VEL


def draw_window(player1, player2, ballpos_x, ballpos_y, ball_vel_x, ball_vel_y, player1_score, player2_score, mode):
    WIN.fill(WHITE)
    if mode == "sp":
        player1_score_text = SCORE_FONT.render("AI: " + str(player1_score), 1, BLACK)
        player2_score_text = SCORE_FONT.render("PLAYER: " + str(player2_score), 1, BLACK)
    elif mode == "mp":
        player1_score_text = SCORE_FONT.render("PLAYER1: " + str(player1_score), 1, BLACK)
        player2_score_text = SCORE_FONT.render("PLAYER2: " + str(player2_score), 1, BLACK)
    
    WIN.blit(player1_score_text, (40, 40))
    WIN.blit(player2_score_text, (WIN_WIDTH - player2_score_text.get_width() - 40, 20))

    pygame.draw.rect(WIN, BLACK, player1)
    pygame.draw.rect(WIN, BLACK, player2)
    ball = pygame.draw.ellipse(WIN, BLACK, [ballpos_x, ballpos_y, 20, 20])
    if ball.colliderect(player1):
        pygame.event.post(pygame.event.Event(COLLISION_PLAYER1))
    if ball.colliderect(player2):
        pygame.event.post(pygame.event.Event(COLLISION_PLAYER2))
    
    pygame.display.update()

def draw_winner(winner_text):
    text = WINNER_FONT.render(winner_text, 1, BLACK)
    WIN.blit(text, (WIN_WIDTH/2 - text.get_width() / 2, WIN_HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def pause_screen():
    pause = True
    while pause:
        WIN.fill(WHITE)
        Paused_text = WINNER_FONT.render("PAUSED", 1, BLACK)
        subtext = SCORE_FONT.render("Press ESC to resume!", 1, BLACK)
        WIN.blit(Paused_text, (WIN_WIDTH//2 - Paused_text.get_width()//2, WIN_HEIGHT//2 - Paused_text.get_height()//2))
        WIN.blit(subtext, (WIN_WIDTH//2 - subtext.get_width()//2, WIN_HEIGHT//2 - subtext.get_height()//2 + 70))
        rect1 = pygame.Rect(WIN_WIDTH//2 - 10 - 20, WIN_HEIGHT//2 - 50 - 120, 20 , 100)
        rect2 = pygame.Rect(WIN_WIDTH//2 - 10 + 20, WIN_HEIGHT//2 - 50 - 120, 20 , 100)
        pygame.draw.rect(WIN, BLACK, rect1)
        pygame.draw.rect(WIN, BLACK, rect2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False

def title_screen():
    ballpos_list = [7, -7]
    ball_vel_x = ballpos_list[random.randint(0,1)]
    ball_vel_y = ballpos_list[random.randint(0,1)]
    clock = pygame.time.Clock()
    title = True
    ballpos_x = WIN_WIDTH//2
    ballpos_y = WIN_HEIGHT//2
    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main("mp")
        WIN.fill(WHITE)
        title_text = WINNER_FONT.render("PONG", 1, BLACK)
        subtext = SCORE_FONT.render("Press Enter to start", 1, BLACK)
        WIN.blit(title_text, (WIN_WIDTH//2 - title_text.get_width() // 2, WIN_HEIGHT//2 - title_text.get_height()//2))
        WIN.blit(subtext, (WIN_WIDTH//2 - subtext.get_width()//2, WIN_HEIGHT//2 - subtext.get_height()//2 + 70))
        ball = pygame.draw.ellipse(WIN, BLACK, [ballpos_x, ballpos_y, 20, 20])
        if ballpos_y + 20 > WIN_HEIGHT or ballpos_y < 0:
            ball_vel_y = ball_vel_y * -1
        if ballpos_x + 20 > WIN_WIDTH or ballpos_x < 0:
            ball_vel_x = ball_vel_x * -1
        ballpos_x += ball_vel_x
        ballpos_y += ball_vel_y

        pygame.display.update()
        clock.tick(60)
    

def main(mode):
    ballpos_list = [6, -6]
    ball_vel_x = ballpos_list[random.randint(0,1)]
    ball_vel_y = ballpos_list[random.randint(0,1)]
    ballpos_x = WIN_WIDTH//2
    ballpos_y = WIN_HEIGHT//2
    player1 = pygame.Rect(20,WIN_HEIGHT//2-100//2, 20, 100)
    player2 = pygame.Rect(WIN_WIDTH-40,WIN_HEIGHT//2-100//2, 20, 100)
    player1_score = 0
    player2_score = 0
    winner_text = ""

    

    

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        # Abprallen von Oberer und unterer Wand
        if ballpos_y + 20 > WIN_HEIGHT or ballpos_y < 0:
            ball_vel_y = ball_vel_y * -1
        # Ball Außerhalb des Bildschirms RECHTS
        if ballpos_x > WIN_WIDTH:
            ballpos_x = WIN_WIDTH//2
            ballpos_y = WIN_HEIGHT//2
            player1_score += 1
            player1.y = WIN_HEIGHT/2 - 50
            player2.y = WIN_HEIGHT/2 - 50
            draw_window(player1, player2, ballpos_x, ballpos_y, ball_vel_x, ball_vel_y, player1_score, player2_score, mode)
            pygame.time.delay(1000)
        # Ball Außerhalb des Bildschirms LINKS
        if ballpos_x  < 0-20:
            ballpos_x = WIN_WIDTH//2
            ballpos_y = WIN_HEIGHT//2
            player2_score += 1
            player1.y = WIN_HEIGHT/2 - 50
            player2.y = WIN_HEIGHT/2 - 50
            draw_window(player1, player2, ballpos_x, ballpos_y, ball_vel_x, ball_vel_y, player1_score, player2_score, mode)
            pygame.time.delay(1000)
        
        
        

        
        ballpos_x += ball_vel_x
        ballpos_y += ball_vel_y

        # KI
        if mode == "sp":
            if ballpos_y > player1.y and player1.y + player1.height < WIN_HEIGHT:
                player1.y += VEL_AI
            elif ballpos_y < player1.y:
                player1.y -= VEL_AI
        
        

        
        if player1_score >= 5:
            winner_text = "AI WON!"
        if player2_score >= 5:
            winner_text = "PLAYER WON!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        
        
        
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == COLLISION_PLAYER1:
                ball_vel_x = ball_vel_x * -1
                ballpos_x += 15
            if event.type == COLLISION_PLAYER2:
                ball_vel_x = ball_vel_x * -1
                ballpos_x -= 15
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen()
            


        

        keys_pressed = pygame.key.get_pressed()
        handle_player2_movement(keys_pressed, player2)
        handle_player1_movement(keys_pressed, player1, mode)

        draw_window(player1, player2, ballpos_x, ballpos_y, ball_vel_x, ball_vel_y, player1_score, player2_score, mode)
    title_screen()
    
    
                
        
        

if __name__ == '__main__':
    mode = title_screen()
