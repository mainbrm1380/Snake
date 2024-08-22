import neat
import matplotlib.pyplot as plt
import pygame, sys, random, time
from pygame.locals import *
import numpy as np
from visualize import draw_net
import pickle

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

snake_image = pygame.image.load("another_snake.png")
background = pygame.image.load("snake.png")
apple_image = pygame.image.load("apple.png")
ice_image = pygame.image.load("ice.png")
chili_image = pygame.image.load("chili-pepper.png")


dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")
pygame.display.set_icon(background)
clock = pygame.time.Clock()


def distance(x1, y1, x2, y2):
    x_difference = np.square((x1-x2))
    y_difference = np.square((y1-y2))

    dist = np.sqrt(x_difference + y_difference)

    return dist


def normalizer(input, max, min):
    new_input = (input - min) / (max - min)
    return new_input


class Button:
    def __init__(self, button_x, button_y, color, button_width = 150, button_height = 70, box_color = None, width = 2):
        self.button_x = button_x
        self.button_y = button_y
        self.color = color
        self.box_color = box_color
        self.button_width = button_width
        self.button_height = button_height
        self.width = width
        self.music = "click.mp3"

    def draw(self, text, text_x, text_y):
        self.text = text
        self.text_x = text_x
        self.text_y = text_y

        if self.box_color == None:
            font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 40)
            button_surface = pygame.Surface((self.button_x, self.button_y), pygame.SRCALPHA)
            text = font.render(text, True, self.color)
            text_rect = text.get_rect(center=(self.button_x // 2, self.button_y // 2))
            
            if self.width != 0:
                pygame.draw.rect(dis, self.color, (self.button_x, self.button_y, self.button_width, self.button_height), self.width, border_radius=5)
            
            button_surface.blit(text, text_rect)
            dis.blit(text, (self.text_x, self.text_y))

        else:
            pygame.draw.rect(dis, self.box_color, (self.button_x, self.button_y, self.button_width, self.button_height), border_radius=5)
            pygame.draw.rect(dis, self.color, (self.button_x, self.button_y, self.button_width, self.button_height), self.width, border_radius=5)
            font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 40)
            text = font.render(text, True, self.color)
            dis.blit(text, (self.text_x, self.text_y))

    def play_music(self):
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()

    def create_rect(self):
        return pygame.Rect((self.button_x, self.button_y), (self.button_width, self.button_height))

    def clicked(self, event, mouse_x, mouse_y):
        if self.create_rect().collidepoint(mouse_x, mouse_y):
            if event.type == MOUSEBUTTONDOWN:
                self.play_music()
                Game.snake_color = self.color
                Game.background_color = self.box_color
                Game.menu()

class Consumable:
    def __init__(self, music = None):
        self.x = random.randrange(0, 580, 20)
        self.y = random.randrange(0, 580, 20)
        self.music = music

    def get_coordinates(self):
        return (self.x, self.y)

    def new_coordinates(self):
        self.x = random.randrange(0, 580, 20)
        self.y = random.randrange(0, 580, 20)

    def eaten(self):
        if self.music != None:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play()
        self.new_coordinates()


class Snake:
    def __init__(self, snake_x_speed = 20, snake_y_speed = 0, snake_x = 380, snake_y = 280):
        self.snake_x_speed = snake_x_speed
        self.snake_y_speed = snake_y_speed
        self.snake_x = snake_x
        self.snake_y = snake_y
        self.snake_list = []
        self.snake_length = 0

    def move(self):
        self.snake_x += self.snake_x_speed
        self.snake_y += self.snake_y_speed

    def rotate(self, theta):
        velocity_vec = np.array([self.snake_x_speed, self.snake_y_speed])
        
        if theta == 90:
            rotation_vec = np.array([[0, -1],
                                    [1, 0]])
        else:
            rotation_vec = np.array([[0, 1],
                                [-1, 0]])
        
        self.snake_x_speed, self.snake_y_speed = np.dot(velocity_vec, rotation_vec)

    def snake_growing(self):
        g_over = False
        snake_head = [self.snake_x, self.snake_y]
        self.snake_list.append(snake_head)

        for lst in self.snake_list:
            pygame.draw.rect(dis, Game.snake_color, (lst[0], lst[1], 20, 20), border_radius=5)
            pygame.draw.rect(dis, black, (lst[0], lst[1], 20, 20), 2, border_radius=5)

        for member in self.snake_list[:-1]:
            if member == snake_head:
                g_over = True
        return g_over
    
    def food_prox(self, food_x, food_y):
        above, right, below, left, same_x, same_y = 0, 0, 0, 0, 0, 0
        
        if food_x > self.snake_x:
            right = 1
        elif food_x < self.snake_x:
            left = 1
        else:
            same_x = 1
        
        if food_y > self.snake_y:
            below = 1
        elif food_y < self.snake_y:
            above = 1
        else:
            same_y = 1

        return above, right, below, left, same_x, same_y
    
    def move_dir(self, above, right, below, left):
        if above == 1 and self.snake_y_speed < 0:
            return True
        elif right == 1 and self.snake_x_speed > 0:
            return True
        elif below == 1 and self.snake_y_speed > 0:
            return True
        elif left == 1 and self.snake_x_speed < 0:
            return True
        else:
            return False
        
    def danger_dir(self):
        danger_ahead, danger_right, danger_left = 0, 0, 0
        
        if len(self.snake_list) > 2:
            for body in self.snake_list:
                if self.snake_x_speed > 0:
                    if body[1] == self.snake_y and body[0] - self.snake_x == 20:
                        danger_ahead = 1
                    
                    elif body[0] == self.snake_x and body[1] - self.snake_y == 20:
                        danger_right = 1

                    elif body[0] == self.snake_x and self.snake_y - body[1] == 20:
                        danger_left = 1

                if self.snake_x_speed < 0:
                    if body[1] == self.snake_y and self.snake_x - body[0] == 20:
                        danger_ahead = 1
                    
                    elif body[0] == self.snake_x and body[1] - self.snake_y == 20:
                        danger_left = 1

                    elif body[0] == self.snake_x and self.snake_y - body[1] == 20:
                        danger_right = 1

                if self.snake_y_speed > 0:
                    if body[0] == self.snake_x and body[1] - self.snake_y == 20:
                        danger_ahead = 1
                    
                    elif body[1] == self.snake_y and body[0] - self.snake_x == 20:
                        danger_left = 1

                    elif body[1] == self.snake_y and self.snake_x - body[0] == 20:
                        danger_right= 1
                        
                if self.snake_y_speed < 0:
                    if body[0] == self.snake_x and self.snake_y - body[1] == 20:
                        danger_ahead = 1
                    
                    elif body[1] == self.snake_y and body[0] - self.snake_x == 20:
                        danger_right = 1

                    elif body[1] == self.snake_y and body[0] - self.snake_x == 20:
                        danger_left = 1

        return danger_ahead, danger_right, danger_left

    

class Game:

    highest_score = 0
    gen = 0
    snake_color = orangish
    background_color = New
    high_scores = []
    left_turns = []
    right_turns = []
    best_genome = None
    

    @staticmethod
    def menu():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                dis.fill(Game.background_color)
                dis.blit(snake_image, (250, 470))

                font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 100)
                text = font.render("Snake", True, Game.snake_color)
                dis.blit(text, (180, 20))

                start = Button(225, 150, Game.snake_color)
                start.draw("Start", 260, 160)

                options = Button(225, 265, Game.snake_color)
                options.draw("Options", 233, 275)
                
                AI = Button(225, 380, Game.snake_color)
                AI.draw("AI", 275, 390)

                pygame.display.flip()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if start.create_rect().collidepoint(mouse_x, mouse_y):
                    if event.type == MOUSEBUTTONDOWN:
                        start.play_music()
                        Game.game_opening()
                        Game.gameloop()
            
                if options.create_rect().collidepoint(mouse_x, mouse_y):
                    if event.type == MOUSEBUTTONDOWN:
                        options.play_music()
                        
                        while True:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                                dis.fill(Game.background_color)

                                font2 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 100)
                                text2 = font2.render("Themes", True, Game.snake_color)
                                dis.blit(text2, (130, 110))
                                back = Button(0, 0, Game.snake_color, width=0)
                                back.draw("Back", 0, 0)
                                red = Button(50, 265, (255, 0, 0), box_color=light_red)
                                red.draw("Red", 90, 275)
                                blue = Button(225, 265, blue_sky, box_color=(0, 0, 255))
                                blue.draw("Blue", 264, 275)
                                orange = Button(400, 265, (250, 167, 22), box_color=New)
                                orange.draw("Orange", 418, 275)

                                pygame.display.flip()

                                mouse_x, mouse_y = pygame.mouse.get_pos()

                                red.clicked(event, mouse_x, mouse_y)
                                    
                                blue.clicked(event, mouse_x, mouse_y)
                                        
                                orange.clicked(event, mouse_x, mouse_y)
                                    
                                if back.create_rect().collidepoint(mouse_x,mouse_y):
                                    if event.type == MOUSEBUTTONDOWN:
                                        orange.play_music()
                                        Game.menu()

                if AI.create_rect().collidepoint(mouse_x, mouse_y):
                    if event.type == MOUSEBUTTONDOWN:
                        AI.play_music()
                        Game.AI_run("neat config")
    
    
    
    @staticmethod                        
    def AI_eval(genomes, config):
        Game.gen += 1
        num_left = 0
        num_right = 0

        for genome_id, genome in genomes:
            fps = 60
            
            genome.fitness = 0
            
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            snake = Snake()
            apple = Consumable()
            timer = 0
            left_turn = 0
            right_turn = 0
            above = 0
            right = 0
            below = 0
            left = 0
        
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        draw_net(config, Game.best_genome, True)
                        with open("best.pickle", "wb") as f:
                            pickle.dump(Game.best_genome, f)
                        
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            Game.paused()

                dis.fill(Game.background_color)

                #relative food position
                above, right, below, left, same_x, same_y = snake.food_prox(apple.x, apple.y)
                #relative danger
                danger_ahead, danger_right, danger_left = snake.danger_dir()


                inputs = (distance(apple.x, apple.y, snake.snake_x, snake.snake_y), 
                        (snake.snake_x - 0), (580 - snake.snake_x), (snake.snake_y - 0), 
                        (580 - snake.snake_y))
                new_inputs = (np.abs(snake.snake_x - apple.x), np.abs(snake.snake_y - apple.y))

                #the inputs are: the location of the apple relative to the snake's head,
                #whether the snake is moving towards the apple,
                #in what direction is there danger (risk of losing),
                #the distance between the snake's head and the apple's location,
                #the absolute distance between teh snake's head x coordinate and apple's x coordiante,
                #the absolute distance between teh snake's head y coordinate and apple's y coordiante.
                #these inputs are normalized to be between 0 and 1.
                normalized_inputs = (above, right, below, left, same_x, same_y, int(snake.move_dir(above, right, below, left)),
                                    danger_ahead, danger_right, danger_left, normalizer(inputs[0], 560*np.sqrt(2), 0), 
                                    normalizer(new_inputs[0], 560, 0), normalizer(new_inputs[1], 560, 0))
                
                output = net.activate(normalized_inputs)
                index = output.index(max(output))
                
                if index == 0:
                    snake.rotate(90)
                    left_turn += 1 
                    num_left += 1
                elif index == 1:
                    snake.rotate(-90)
                    right_turn += 1
                    num_right += 1
                else:
                    right_turn, left_turn = 0, 0

                snake.move()

                if snake.move_dir(above, right, below, left):
                    #rewarding the snake for going towards the apple.
                    genome.fitness += (400/fps)/(distance(snake.snake_x, snake.snake_y, apple.x, apple.y) + 1)

                if snake.snake_x < 0 or snake.snake_x > 580 or snake.snake_y < 0 or snake.snake_y > 580:
                    #punishing the snake for losing.
                    genome.fitness -= 10
                    if snake.snake_length > Game.highest_score:
                        Game.highest_score = snake.snake_length
                        Game.best_genome = genome
                    break

                if (snake.snake_x, snake.snake_y) == apple.get_coordinates():
                    #rewarding the snake for eating an apple.
                    genome.fitness += 100
                    apple.eaten()
                    snake.snake_length += 1
                    timer = 0

                    for i in snake.snake_list:
                        while apple.get_coordinates() == i:
                            apple.new_coordinates()

                elif snake.snake_length <= 15:
                    #rewarding the snake for being alive (this is awarded until the snake has eaten 15 apples).
                    genome.fitness += 2/fps
                    timer += 1/fps

                if right_turn > 4 or left_turn > 4:
                    #punishing the snake for rotating around itself.
                    genome.fitness -= 50
                    if snake.snake_length > Game.highest_score:
                        Game.highest_score = snake.snake_length
                        Game.best_genome = genome
                    break
                
                if timer > 20:
                    #punishing the snake for taking to long to eat an apple.
                    genome.fitness -= 50
                    if snake.snake_length > Game.highest_score:
                        Game.highest_score = snake.snake_length
                        Game.best_genome = genome
                    break

                if len(snake.snake_list) > snake.snake_length:
                    snake.snake_list.pop(0)
                
                if snake.snake_growing():
                    #punishing the snake for colliding with its own body.
                    genome.fitness -= 50
                    if snake.snake_length > Game.highest_score:
                        Game.highest_score = snake.snake_length
                        Game.best_genome = genome
                    break

                if snake.snake_x_speed == 20:
                    pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+6),4)
                    pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+14),4)
                elif snake.snake_x_speed == -20:
                    pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+6),4)
                    pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+14),4) 
                elif snake.snake_y_speed == 20:
                    pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+14),4)
                    pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+14),4)
                elif snake.snake_y_speed == -20:
                    pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+6),4)
                    pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+6),4)

                dis.blit(apple_image, apple.get_coordinates())

                font = pygame.font.Font(pygame.font.match_font("Times New Roman"), 40)
                text_gen = font.render("Generation: " + str(Game.gen), True, Game.snake_color)
                dis.blit(text_gen, (0, 0))
                text_max = font.render("Max score: " + str(Game.highest_score), True, Game.snake_color)
                dis.blit(text_max, (360, 0))
                
                pygame.display.flip()
                clock.tick(fps)

        Game.high_scores.append(Game.highest_score)
        Game.left_turns.append(num_left)
        Game.right_turns.append(num_right)


    @staticmethod
    def  AI_run(config):
        c = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                        neat.DefaultSpeciesSet, neat.DefaultStagnation, config)
        
        pop = neat.Checkpointer.restore_checkpoint("neat-checkpoint-54")
        #pop = neat.Population(c)
        pop.add_reporter(neat.StdOutReporter(True))
        #stats = neat.StatisticsReporter()
        #pop.add_reporter(stats)
        pop.add_reporter(neat.Checkpointer(5))
        winner = pop.run(Game.AI_eval)

        print('\nBest genome:\n{!s}'.format(winner))
        
                            
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
            pygame.display.flip()
            

    @staticmethod
    def game_opening():
        dis.fill(Game.background_color)
        font = pygame.font.SysFont(None, 500)
        text = font.render("3", True, black)
        dis.blit(text, (200, 150))
        pygame.display.flip()
        time.sleep(1)
        dis.fill(Game.background_color)
        text = font.render("2", True, black)
        dis.blit(text, (200, 150))
        pygame.display.flip()
        time.sleep(1)
        dis.fill(Game.background_color)
        text = font.render("1", True, black)
        dis.blit(text, (200, 150))
        pygame.display.flip()
        time.sleep(1)
        dis.fill(Game.background_color)
        text = font.render("GO", True, black)
        dis.blit(text, (40, 150))
        pygame.display.flip()
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
        pygame.display.flip()
    
        while loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Game.menu()
                    if event.key == K_SPACE:
                        loop=0

    @staticmethod
    def game_over_screen(score, number_chili=None):
        pygame.mixer.music.load("LOOSE.wav")
        pygame.mixer.music.play()
        score += 3*number_chili
        
        while True:
            dis.fill(Game.background_color)
            if score > Game.highest_score:
                Game.highest_score = score

            font1 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 60)
            font2 = pygame.font.Font(pygame.font.match_font("Times New Roman"), 35)
            text1 = font1.render('Game Over', True, red)
            dis.blit(text1, (160, 240))
            text2 = font1.render("Your score: " + str(score), True, Game.snake_color)
            dis.blit(text2, (140, 120))
            text3 = font2.render('Press Space to play again', True, Game.snake_color)
            dis.blit(text3, (120, 360))
            text4 = font1.render("Highest score: " + str(Game.highest_score), True, Game.snake_color)
            dis.blit(text4, (100, 50))
            text5 = font2.render("Press Esc to return to menu", True, Game.snake_color)
            dis.blit(text5, (105, 450))

            pygame.display.flip()

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
        apple = Consumable("munchingfood--.mp3") 
        ice = Consumable("ice-cracking-01.mp3")
        chili = Consumable("mixkit-service-bell-double-ding-588.wav")
        ice_spawn = True
        chili_spawn = True
        keep_ice = False
        keep_chili = False
        number_chili = 0
        snake = Snake()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Game.paused()
                    elif event.key == K_LEFT and snake.snake_x_speed != 20:
                        snake.snake_x_speed = -20
                        snake.snake_y_speed = 0
                    elif event.key == K_RIGHT and snake.snake_x_speed != -20:
                        snake.snake_x_speed = 20
                        snake.snake_y_speed = 0
                    elif event.key == K_DOWN and snake.snake_y_speed != -20:
                        snake.snake_y_speed = 20
                        snake.snake_x_speed = 0
                    elif event.key == K_UP and snake.snake_y_speed != 20:
                        snake.snake_y_speed = -20
                        snake.snake_x_speed = 0
            snake.move()
            
            if snake.snake_x < 0 or snake.snake_x > 580 or snake.snake_y < 0 or snake.snake_y > 580:
                Game.game_over_screen(score, number_chili)
                   
            if (snake.snake_x, snake.snake_y) == apple.get_coordinates():
                fps += 0.5
                apple.eaten()
                for i in snake.snake_list:
                    while (apple.get_coordinates() == i) or (apple.get_coordinates() == ice.get_coordinates()) or (apple.get_coordinates() == chili.get_coordinates()):
                        apple.new_coordinates()
                snake.snake_length += 1
                ice_spawn = True
                chili_spawn = True

            score = snake.snake_length
            if snake.snake_length >= 10 and snake.snake_length % 5 == 0 and ice_spawn:
                if (snake.snake_x, snake.snake_y) == ice.get_coordinates():
                    fps -= 2
                    ice.eaten()
                    for i in snake.snake_list:
                        while (ice.get_coordinates() == i) or (ice.get_coordinates() == apple.get_coordinates()) or ice.get_coordinates() == chili.get_coordinates():
                            ice.new_coordinates()
                    ice_spawn = False
                    keep_ice = False

            elif keep_ice:
                if (snake.snake_x, snake.snake_y) == ice.get_coordinates():
                    fps -= 2
                    ice.eaten()
                    for i in snake.snake_list:
                        while (ice.get_coordinates() == i) or (ice.get_coordinates() == apple.get_coordinates()) or ice.get_coordinates() == chili.get_coordinates():
                            ice.new_coordinates()
                    ice_spawn = False
                    keep_ice = False

            if snake.snake_length >= 10 and snake.snake_length % 4 == 2 and chili_spawn:
                if (snake.snake_x, snake.snake_y) == chili.get_coordinates():
                    fps += 3
                    chili.eaten()
                    number_chili += 1
                    for i in snake.snake_list:
                        while (chili.get_coordinates() == i) or (chili.get_coordinates() == apple.get_coordinates()) or chili.get_coordinates() == ice.get_coordinates():
                            chili.new_coordinates()
                    chili_spawn = False
                    keep_chili = False
                    
            elif keep_chili:
                if (snake.snake_x, snake.snake_y) == chili.get_coordinates():
                    fps += 3
                    chili.eaten()
                    number_chili += 1
                    for i in snake.snake_list:
                        while (chili.get_coordinates() == i) or (chili.get_coordinates() == apple.get_coordinates()) or chili.get_coordinates() == ice.get_coordinates():
                            chili.new_coordinates()
                    chili_spawn = False
                    keep_chili = False
                    
            if len(snake.snake_list) > snake.snake_length:
                snake.snake_list.pop(0)
            dis.fill(Game.background_color)
            if snake.snake_growing():
                Game.game_over_screen(score, number_chili)

            if snake.snake_x_speed == 20:
                pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+6),4)
                pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+14),4)
            elif snake.snake_x_speed == -20:
                pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+6),4)
                pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+14),4) 
            elif snake.snake_y_speed == 20:
                pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+14),4)
                pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+14),4)
            elif snake.snake_y_speed == -20:
                pygame.draw.circle(dis,black,(snake.snake_x+6,snake.snake_y+6),4)
                pygame.draw.circle(dis,black,(snake.snake_x+14,snake.snake_y+6),4)     
                
            dis.blit(apple_image, apple.get_coordinates())
            if snake.snake_length >= 10 and snake.snake_length % 5 == 0 and ice_spawn:
                dis.blit(ice_image, ice.get_coordinates())
                keep_ice = True
            elif keep_ice:
                dis.blit(ice_image, ice.get_coordinates())
            if snake.snake_length >= 10 and snake.snake_length % 4 == 2 and chili_spawn:
                dis.blit(chili_image, chili.get_coordinates())
                keep_chili = True
            elif keep_chili:
                dis.blit(chili_image, chili.get_coordinates())

            pygame.display.flip()
            clock.tick(fps)

Game.game()
