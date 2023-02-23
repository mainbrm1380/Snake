import pygame, sys, random, time
from pygame.locals import *

pygame.init()
light_red = (255, 183, 183)
blue_sky = (134, 225, 253)
red = (255, 0, 0)
green = (0, 255, 0)
New = (238, 232, 170)
yellow = (255, 255, 0)
white = (255,255,255)
black = (0,0,0)
orangish = (250, 167, 22)
dark_blue = (5, 30, 155)
highest_score = []

snake_image = pygame.image.load("another_snake.png")
background = pygame.image.load("snake.png")
apple_image = pygame.image.load("apple.png")
ice_image = pygame.image.load("ice.png")
chili_image = pygame.image.load("chili-pepper.png")


dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")
pygame.display.set_icon(background)
clock = pygame.time.Clock()


class Button:
    def __init__(self, button_x, button_y, color, box_color):
        self.button_x = button_x
        self.button_y = button_y
        self.color = color
        self.box_color = box_color
        self.music = "click.mp3"

    def draw(self, text, text_x, text_y):
        self.text = text
        self.text_x = text_x
        self.text_y = text_y

        pygame.draw.rect(dis, self.box_color, (self.button_x, self.button_y, 150, 70), border_radius=5)
        pygame.draw.rect(dis, self.color, (self.button_x, self.button_y, 150, 70), 2, border_radius=5)
        font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 40)
        text = font.render(text, True, self.color)
        dis.blit(text, (self.text_x, self.text_y))

    def play_music(self):
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()

    def clicked(self, event, mouse_x, mouse_y):
        if self.button_x <= mouse_x <= self.button_x + 150 and self.button_y <= mouse_y <= self.button_y + 70:
            if event.type == MOUSEBUTTONDOWN:
                self.play_music()
                Game.snake_color = self.color
                Game.background_color = self.box_color
                Game.menu()

class Consumable:
    def __init__(self, music):
        self.x = random.randrange(0, 580, 20)
        self.y = random.randrange(0, 580, 20)
        self.music = music

    def get_coordinates(self):
        return (self.x, self.y)

    def new_coordinates(self):
        self.x = random.randrange(0, 580, 20)
        self.y = random.randrange(0, 580, 20)

    def eaten(self):
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()
        self.new_coordinates()


class Game:

    snake_color = orangish
    background_color = New

    @staticmethod
    def snakegrowing(snake_list, snake_x, snake_y, snake_color):
        g_over = False
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        for lst in snake_list:
            pygame.draw.rect(dis, snake_color, (lst[0], lst[1], 20, 20), border_radius=5)
            pygame.draw.rect(dis, black, (lst[0], lst[1], 20, 20), 2, border_radius=5)
        for member in snake_list[:-1]:
            if member == snake_head:
                g_over = True
        return g_over

    

    @staticmethod
    def menu():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                dis.fill(Game.background_color)
                dis.blit(snake_image, (250, 400))

                font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 100)
                text = font.render("Snake", True, Game.snake_color)
                dis.blit(text, (180, 20))

                start = Button(225, 150, Game.snake_color, Game.background_color)
                start.draw("Start", 260, 160)

                options = Button(225, 265, Game.snake_color, Game.background_color)
                options.draw("Options", 233, 275)
                
                pygame.display.update()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if 225 < mouse_x < 375 and 150 < mouse_y < 220:
                    if event.type == MOUSEBUTTONDOWN:
                        start.play_music()
                        Game.game_opening()
                        Game.gameloop()
            
                if 225 < mouse_x < 375 and 265 < mouse_y < 335:
                    if event.type == MOUSEBUTTONDOWN:
                        options.play_music()
                        while True:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                                dis.fill(Game.background_color)

                                font1 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 35)
                                text1 = font1.render("Back", True, Game.snake_color)
                                dis.blit(text1, (0, 0))
                                font2 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 100)
                                text2 = font2.render("Themes", True, Game.snake_color)
                                dis.blit(text2, (130, 110))
                                red = Button(50, 265, (255, 0, 0), light_red)
                                red.draw("Red", 90, 275)
                                blue = Button(225, 265, blue_sky, (0, 0, 255))
                                blue.draw("Blue", 264, 275)
                                orange = Button(400, 265, (250, 167, 22), New)
                                orange.draw("Orange", 418, 275)

                                pygame.display.update()

                                mouse_x, mouse_y = pygame.mouse.get_pos()

                                red.clicked(event, mouse_x, mouse_y)
                                    
                                blue.clicked(event, mouse_x, mouse_y)
                                        
                                orange.clicked(event, mouse_x, mouse_y)
                                    
                                if 0 < mouse_x < 80 and 0 < mouse_y < 80:
                                    if event.type == MOUSEBUTTONDOWN:
                                        orange.play_music()
                                        Game.menu()
                            
    @staticmethod                        
    def game():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 50)
                text = font.render("Press Space to start", True, orangish)
                dis.fill(Game.background_color)
                dis.blit(background, (44, 0))
                dis.blit(text, (110, 500))
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        Game.menu()
            pygame.display.update()
            

    @staticmethod
    def game_opening():
        dis.fill(Game.background_color)
        font = pygame.font.SysFont(None, 500)
        text = font.render("3", True, black)
        dis.blit(text, (200, 150))
        pygame.display.update()
        time.sleep(1)
        dis.fill(Game.background_color)
        text = font.render("2", True, black)
        dis.blit(text, (200, 150))
        pygame.display.update()
        time.sleep(1)
        dis.fill(Game.background_color)
        text = font.render("1", True, black)
        dis.blit(text, (200, 150))
        pygame.display.update()
        time.sleep(1)
        dis.fill(Game.background_color)
        text = font.render("GO", True, black)
        dis.blit(text, (40, 150))
        pygame.display.update()
        time.sleep(1)
        dis.fill(Game.background_color)

    @staticmethod
    def paused():
        loop = 1

        dis.fill(Game.background_color)
        largeText=pygame.font.Font(pygame.font.match_font("Times New Roman"), 50)
        text_pause = largeText.render('Paused', True, Game.snake_color)
        text_return = largeText.render("Press Esc to return to menu", True, Game.snake_color)
        dis.blit(text_pause, (220, 220))
        dis.blit(text_return, (25, 300))
        pygame.display.update()
    
        while loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Game.menu()
                    if event.key == K_SPACE:
                        dis.fill((0,0,0))
                        loop=0

    @staticmethod
    def game_over_screen(score, number_chili):
        pygame.mixer.music.load("LOOSE.wav")
        pygame.mixer.music.play()
        score += 3*number_chili
        
        while True:
            dis.fill(Game.background_color)
            highest_score.append(score)

            font1 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 60)
            font2 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 35)
            text1 = font1.render('Game Over', True, red)
            dis.blit(text1, (160, 240))
            text2 = font1.render("Your score: " + str(score), True, Game.snake_color)
            dis.blit(text2, (140, 120))
            text3 = font2.render('Press Space to play again', True, Game.snake_color)
            dis.blit(text3, (120, 360))
            text4 = font1.render("Highest score: " + str(max(highest_score)), True, Game.snake_color)
            dis.blit(text4, (100, 50))
            text5 = font2.render("Press Esc to return to menu", True, Game.snake_color)
            dis.blit(text5, (105, 450))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        Game.game_opening()
                        Game.gameloop()
                    if event.key == K_ESCAPE:
                        Game.menu()
        
    @staticmethod
    def gameloop():   
        fps = 10
        snake_x = 380
        snake_y = 280
        snake_x_speed = 20
        snake_y_speed = 0
        apple = Consumable("munchingfood--.mp3") 
        ice = Consumable("ice-cracking-01.mp3")
        chili = Consumable("mixkit-service-bell-double-ding-588.wav")
        ice_spawn = True
        chili_spawn = True
        keep_ice = False
        keep_chili = False
        number_chili = 0
        snake_list = list()
        snake_length = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Game.paused()
                    elif event.key == K_LEFT and snake_x_speed != 20:
                        snake_x_speed = -20
                        snake_y_speed = 0
                    elif event.key == K_RIGHT and snake_x_speed != -20:
                        snake_x_speed = 20
                        snake_y_speed = 0
                    elif event.key == K_DOWN and snake_y_speed != -20:
                        snake_y_speed = 20
                        snake_x_speed = 0
                    elif event.key == K_UP and snake_y_speed != 20:
                        snake_y_speed = -20
                        snake_x_speed = 0
            snake_x += snake_x_speed
            snake_y += snake_y_speed
            if snake_x < 0 or snake_x > 580 or snake_y < 0 or snake_y > 580:
                Game.game_over_screen(score, number_chili)
                   
            if snake_x == apple.get_coordinates()[0] and snake_y == apple.get_coordinates()[1]:
                fps += 0.5
                apple.eaten()
                for i in snake_list:
                    while (apple.get_coordinates()[0] == i[1] and apple.get_coordinates()[1] == i[1]) or (apple.get_coordinates()[0] == ice.get_coordinates()[0] and apple.get_coordinates()[1] == ice.get_coordinates()[1]):
                        apple.new_coordinates()
                snake_length += 1
                ice_spawn = True
                chili_spawn = True
            score = snake_length
            if snake_length >= 10 and snake_length % 5 == 0 and ice_spawn:
                if snake_x == ice.get_coordinates()[0] and snake_y == ice.get_coordinates()[1]:
                    fps -= 2
                    ice.eaten()
                    for i in snake_list:
                        while (ice.get_coordinates()[0] == i[0] and ice.get_coordinates()[1] == i[1]) or (ice.get_coordinates()[0] == apple.get_coordinates()[1] and ice.get_coordinates()[1] == apple.get_coordinates()[1]):
                            ice.new_coordinates()
                    ice_spawn = False
                    keep_ice = False
            elif keep_ice:
                if snake_x == ice.get_coordinates()[0] and snake_y == ice.get_coordinates()[1]:
                    fps -= 2
                    ice.eaten()
                    for i in snake_list:
                        while (ice.get_coordinates()[0] == i[0] and ice.get_coordinates()[1] == i[1]) or (ice.get_coordinates()[0] == apple.get_coordinates()[1] and ice.get_coordinates()[1] == apple.get_coordinates()[1]):
                            ice.new_coordinates()
                    ice_spawn = False
                    keep_ice = False
            if snake_length >= 10 and snake_length % 4 == 2 and chili_spawn:
                if snake_x == chili.get_coordinates()[0] and snake_y == chili.get_coordinates()[1]:
                    fps += 3
                    chili.eaten()
                    number_chili += 1
                    for i in snake_list:
                        while (chili.get_coordinates()[0] == i[0] and chili.get_coordinates()[1] == i[1]) or (chili.get_coordinates()[0] == apple.get_coordinates()[0] and chili.get_coordinates()[1] == apple.get_coordinates()[1]):
                            chili.new_coordinates()
                    chili_spawn = False
                    keep_chili = False
            elif keep_chili:
                if snake_x == chili.get_coordinates()[0] and snake_y == chili.get_coordinates()[1]:
                    fps += 3
                    chili.eaten()
                    number_chili += 1
                    for i in snake_list:
                        while (chili.get_coordinates()[0] == i[0] and chili.get_coordinates()[1] == i[1]) or (chili.get_coordinates()[0] == apple.get_coordinates()[0] and chili.get_coordinates()[1] == apple.get_coordinates()[1]):
                            chili.new_coordinates()
                    chili_spawn = False
                    keep_chili = False
            if len(snake_list) > snake_length:
                snake_list.pop(0)
            dis.fill(Game.background_color)
            if Game.snakegrowing(snake_list, snake_x, snake_y, Game.snake_color):
                Game.game_over_screen(score, number_chili)

            pygame.draw.rect(dis,Game.snake_color,[snake_x,snake_y,20,20], border_radius=5)
            pygame.draw.rect(dis,black,[snake_x,snake_y,20,20], 2, border_radius=5)
            if snake_x_speed == 20:
                pygame.draw.circle(dis,black,(snake_x+14,snake_y+6),4)
                pygame.draw.circle(dis,black,(snake_x+14,snake_y+14),4)
            elif snake_x_speed == -20:
                pygame.draw.circle(dis,black,(snake_x+6,snake_y+6),4)
                pygame.draw.circle(dis,black,(snake_x+6,snake_y+14),4) 
            elif snake_y_speed == 20:
                pygame.draw.circle(dis,black,(snake_x+6,snake_y+14),4)
                pygame.draw.circle(dis,black,(snake_x+14,snake_y+14),4)
            elif snake_y_speed == -20:
                pygame.draw.circle(dis,black,(snake_x+6,snake_y+6),4)
                pygame.draw.circle(dis,black,(snake_x+14,snake_y+6),4)     
                
            dis.blit(apple_image, (apple.get_coordinates()[0], apple.get_coordinates()[1]))
            if snake_length >= 10 and snake_length % 5 == 0 and ice_spawn:
                dis.blit(ice_image, (ice.get_coordinates()[0], ice.get_coordinates()[1]))
                keep_ice = True
            elif keep_ice:
                dis.blit(ice_image, (ice.get_coordinates()[0], ice.get_coordinates()[1]))
            if snake_length >= 10 and snake_length % 4 == 2 and chili_spawn:
                dis.blit(chili_image, (chili.get_coordinates()[0], chili.get_coordinates()[1]))
                keep_chili = True
            elif keep_chili:
                dis.blit(chili_image, (chili.get_coordinates()[0], chili.get_coordinates()[1]))

            pygame.display.update()
            clock.tick(fps)

Game.game()
                