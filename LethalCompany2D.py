# Group3_CS2B_PIT
# Members:
# Chas Omer M. Madlos
# Krystal Heart Bacalso
# Shaira Jane Dadios
# Javier Raut
# Joseph Jose Deysolong

import pygame
import sys
import datetime
import random
import heapq 

SCREENWIDTH = 1200
SCREENHEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)

SCRAPTYPE = ['horn', 'gold bar', 'mug', 'pills', 'sign', 'cup', 'gold_cup', 'cat', 'magnifying_glass']
SCRAPIMAGE = {
    'horn': pygame.image.load("Game\Assets\Scraps\horn.png"),
    'gold bar': pygame.image.load("Game\Assets\Scraps\gold bar.png"),
    'mug': pygame.image.load("Game\Assets\Scraps\mug.png"),
    'pills': pygame.image.load("Game\Assets\Scraps\pills.png"),
    'sign': pygame.image.load("Game\Assets\Scraps\stop_sign.png"),
    'cup': pygame.image.load("Game\Assets\Scraps\cup.png"),
    'gold_cup': pygame.image.load("Game\Assets\Scraps\golden_cup.png"),
    'cat': pygame.image.load("Game\Assets\Scraps\cat.png"),
    'cola': pygame.image.load("Game\Assets\Scraps\cola.png"),
    'magnifying_glass': pygame.image.load("Game\Assets\Scraps\magnifying_glass.png"),
}

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.gameSceneManager = GameSceneManager('StartScreen')

        # Create a single instance of Player
        self.player = Player(self, self.screen, self.gameSceneManager)

        self.rooms = {'StartScreen': StartScreen(self.screen, self.gameSceneManager),
                      'Spaceship': Spaceship(self.screen, self.gameSceneManager, self.player),
                      'Moon': Moon(self.screen, self.gameSceneManager, self.player),
                      'Building': Building(self.screen, self.gameSceneManager, self.player),
                      'EndScreen': EndScreen(self.screen, self.gameSceneManager)}

        self.scene = {'StartScreen': self.rooms['StartScreen'], 'Spaceship': self.rooms['Spaceship'], 'Moon': self.rooms['Moon'], 'Building': self.rooms['Building'], 'EndScreen': self.rooms['EndScreen']}

    def run(self):  # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.scene[self.gameSceneManager.get_scene()].run()

            pygame.display.update()
            self.clock.tick(FPS)

class StartScreen():
    def __init__(self, display, gameSceneManager):
        self.display = display
        self.gameSceneManager = gameSceneManager

        self.cover = [pygame.image.load("Game\Assets\cover.png"), pygame.image.load("Game\Assets\controls.png")]
        self.cover_pos = 0

    def run(self):
        self.draw()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.cover_pos + 1 < len(self.cover):
                        self.cover_pos += 1
                    else:
                        self.gameSceneManager.set_scene('Spaceship')
        
    def draw(self):
        self.display.blit(pygame.transform.scale(self.cover[self.cover_pos], (SCREENWIDTH, SCREENHEIGHT)), (0,0))

class GameSceneManager:
    def __init__(self, currentScene):
        self.currentScene = currentScene
    
    def get_scene(self):
        return self.currentScene
    
    def set_scene(self, scene):
        self.currentScene = scene

class Player:
    def __init__(self, game, display, gameSceneManager):
        self.pos = pygame.Vector2(SCREENWIDTH // 2, SCREENHEIGHT // 2) # Middle of the screen
        self.game = game
        self.timer = GameTime()
        self.speed = 8
        self.size = 50
        self.display = display
        self.stored_value = 0
        self.ship_total_value = 0
        self.quota = 134
        self.inventory = []

        self.image = pygame.image.load("Game\Assets\player.png")

        self.gameSceneManager = gameSceneManager
        
    def draw(self):
        self.display.blit(self.image, self.pos)
        # Update Hitbox position
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y,self.size, self.size)
        #self.hitbox = image.get_rect()
        self.timer.tick()

        if self.timer.current_time.time() == self.timer.end_time.time():
            self.check_quota()
            self.timer.current_time = self.timer.start_time
        
        #Draw Inventory
        for i in range(len(self.inventory)):
            #pygame.draw.rect(self.display, self.color, [self.pos.x, self.pos.y, self.size, self.size])
            #image_width, image_height = self.image.get_size()
            #self.display.blit(pygame.transform.scale(self.image, (2 * image_width, 2 * image_height)), self.pos)
            pygame.draw.rect(self.display, BLACK, [10 * 3, 32 * 3 + ((34 * 3) * i), 32 * 3, 32 * 3])

            image_width, image_height = self.inventory[i].get_size()
            self.display.blit(pygame.transform.scale(self.inventory[i], (3 * image_width, 3 * image_height)), (10 * 3, 32 * 3 + ((34 * 3) * i)))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and self.pos.x < SCREENWIDTH - 2 * (self.size / 2):
            self.pos.x += self.speed
        if keys[pygame.K_a] and self.pos.x > 0:
            self.pos.x -= self.speed
        if keys[pygame.K_w] and self.pos.y > 0:
            self.pos.y -= self.speed
        if keys[pygame.K_s] and self.pos.y < SCREENHEIGHT - 2 * (self.size / 2):
            self.pos.y += self.speed
    
    def check_quota(self):
        #self.timer_running = False
        if self.ship_total_value < self.quota:
            print("Game Over! You did not meet the quota")
            self.gameSceneManager.set_scene('EndScreen')
        else:
            # Display day end pop-up
            FONT = pygame.font.Font(None, 72)
            day_end_text = FONT.render(f"Day Ended! You met the quota.", True, GREEN)
            text_rect = day_end_text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 - 50))
            self.display.blit(day_end_text, text_rect)
            
            # Update the quota
            self.ship_total_value -= self.quota
            self.quota += 100  # You can adjust this value as needed
            quota_text = FONT.render(f"New Quota: {self.quota}", True, GREEN)
            quota_rect = quota_text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
            self.display.blit(quota_text, quota_rect)
            
            day_end_text = FONT.render(f"Press 'Enter' to continue", True, GREEN)
            text_rect = day_end_text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 + 50))
            self.display.blit(day_end_text, text_rect)
            
            pygame.display.flip()
            
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            waiting_for_input = False

            #Reset Enemies
            self.game.scene['Building'].enemies.clear()
            self.game.scene['Building'].spawn_chance = self.game.scene['Building'].spawn_chance_base
            self.timer_running = True

class Enemy:
    def __init__(self, display, pos, speed = 5, size = 25, image=None):
        self.display = display
        self.speed = speed
        self.size = size
        self.pos = pos
        self.image = image

class Level:
    def __init__(self, display, gameSceneManager, player):
        self.display = display
        self.gameSceneManager = gameSceneManager
        self.player = player
        self.enemies = []

        self.FONT = pygame.font.Font(None, 36)

    def run(self):
        pass

    def transfer_room(self, room, start_x, start_y):
        self.gameSceneManager.set_scene(room)
        self.player.pos.x = start_x
        self.player.pos.y = start_y
    
    def draw_gui(self):
        pass

    def draw_time(self, FONT):
        # Draw the timer
        timer_text = FONT.render(f"Time: {self.player.timer.strftime('%I:%M%p')}", True, BLACK)
        self.display.blit(timer_text, (SCREENWIDTH// 2 - (timer_text.get_width()/2), 30))  # Adjust position as needed   
        

class Spaceship(Level):
    def __init__(self, display, gameSceneManager, player):
        self.display = display
        self.gameSceneManager = gameSceneManager
        self.player = player
        
        self.red_box = RedBox(self.display, self.player, self.gameSceneManager)

    def run(self):  # Code for the room here
        plain_bg = pygame.image.load(r"Game\Assets\bg_spaceship.png").convert()#JOEPH
        plain_bg_scaled = pygame.transform.scale(plain_bg, (SCREENWIDTH, SCREENHEIGHT))
        self.display.blit(plain_bg_scaled, (0,0))#JOEPHJ
        self.player.draw()
        self.draw_gui()
        self.player.move()
        keys = pygame.key.get_pressed()

        #Press "G" to drop scraps to ship
        if keys[pygame.K_g] and self.player.stored_value > 0:
            self.player.ship_total_value += self.player.stored_value
            self.player.stored_value = 0
            self.player.inventory.clear()

        self.red_box.draw()
        self.red_box.check_collision()
        
    def draw_gui(self):
        FONT = pygame.font.Font(None, 36)
        #Draw Room name
        room_name_text = FONT.render(f"Spaceship", True, BLACK)
        room_name_text_pos = ((SCREENWIDTH / 2) - (room_name_text.get_width()/2), 10)
        self.display.blit(room_name_text, room_name_text_pos)
        
        #Draw Player Scrap Value
        player_scrapval_text = FONT.render(f"Player Value: {self.player.stored_value}", True, BLACK)
        scrap_value_text_pos = (SCREENWIDTH - player_scrapval_text.get_width() - 10, 10)
        self.display.blit(player_scrapval_text, scrap_value_text_pos)

        #Draw Ship Scrap Value
        ship_scrapval_text = FONT.render(f"Ship Value: {self.player.ship_total_value}", True, BLACK)
        ship_scrapval_text_pos = (10, 10)
        self.display.blit(ship_scrapval_text, ship_scrapval_text_pos)

        #Draw Quota Value
        quota_text = FONT.render(f"Quota: {self.player.quota}", True, BLACK)
        quota_text_pos = (10, 30)
        self.display.blit(quota_text, quota_text_pos)

        #If the player have scraps, display guide
        if self.player.stored_value > 0:
            drop_scraps_text = FONT.render("Press 'G' to drop scraps", True, BLACK)
            # Calculate the x position to center the text
            text_x = (SCREENWIDTH / 2) - (drop_scraps_text.get_width() / 2)
            # Calculate the y position to place the text at the bottom with a margin
            text_y = SCREENHEIGHT - drop_scraps_text.get_height() - 20  # 20 pixels margin from the bottom
            self.display.blit(drop_scraps_text, (text_x, text_y))
            
        self.draw_time(FONT)

class Moon(Level):
    def __init__(self, display, gameSceneManager, player):
        self.display = display
        self.gameSceneManager = gameSceneManager
        self.player = player
        
        self.red_box = RedBox(self.display, self.player, self.gameSceneManager)
        
    def run(self):  # Code for the second room here
        plain_bg = pygame.image.load(r"Game\Assets\bg_moon.png").convert()#JOEPH
        plain_bg_scaled = pygame.transform.scale(plain_bg, (SCREENWIDTH, SCREENHEIGHT))
        self.display.blit(plain_bg_scaled, (0,0))#JOEPHJ
        #self.display.fill("blue")  #<-- Nara ang Background

        self.player.draw()
        self.draw_gui()
        self.player.move()

        self.red_box.draw()
        self.red_box.check_collision()
    
    def draw_gui(self):
        FONT = pygame.font.Font(None, 36)
        #Draw Room name
        room_name_text = FONT.render(f"Moon", True, BLACK)
        room_name_text_pos = ((SCREENWIDTH / 2) - (room_name_text.get_width()/2), 10)
        self.display.blit(room_name_text, room_name_text_pos)

        #Draw Player Scrap Value
        player_scrapval_text = FONT.render(f"Player Value: {self.player.stored_value}", True, BLACK)
        scrap_value_text_pos = (SCREENWIDTH - player_scrapval_text.get_width() - 10, 10)
        self.display.blit(player_scrapval_text, scrap_value_text_pos)

        self.draw_time(FONT)

class Building(Level):
    def __init__(self, display, gameSceneManager, player):
        super().__init__(display, gameSceneManager, player)
        
        self.obstacles = []
        self.spawn_obstacles()
        # Spawn scraps
        self.starting_scraps = 5
        self.spawned_scraps = []
        self.spawn_scraps(self.spawned_scraps)

        # Initialize enemies list for the Building room
        self.enemies = []
        self.spawn_chance_base = 0 # Initial base chance
        self.spawn_chance_increment = 0.10 # Increment in chance per hour
        self.spawn_chance = self.spawn_chance_base
        self.spawn_chance = 0 # Initial spawn chance for enemies in Building
        self.game_time = self.player.timer # Add this line
        
        self.red_box = RedBox(self.display, self.player, self.gameSceneManager)
        
        
    def spawn_obstacles(self):
        # Spawn obstacles randomly
        for _ in range(5):
            obstacle_x = random.randint(0, SCREENWIDTH - 50)
            obstacle_y = random.randint(0, SCREENHEIGHT - 50)
            obstacle_width = random.randint(100, 200)
            obstacle_height = random.randint(100, 120)
            self.obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))


    def a_star(self, start, goal):
        # A* algorithm for pathfinding
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start))
        came_from = {}

        g_score = {pos: float('inf') for pos in self.walkable_positions}
        g_score[start] = 0

        while open_set:
            current_pos = heapq.heappop(open_set)

            if current_pos == goal:
                path = []
                while current_pos in came_from:
                    path.append(current_pos)
                    current_pos = came_from[current_pos]
                path.reverse()
                return path

            closed_set.add(current_pos)

            for neighbor in self.get_neighbors(current_pos):
                tentative_g_score = g_score[current_pos] + 1 

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_pos
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score + self.heuristic(neighbor, goal), neighbor))

        return None

    def spawn_enemies(self):
        self.enemies = sorted(self.enemies, key=lambda enemy: (enemy['pos'].x, enemy['pos'].y))

        for enemy in self.enemies:
            # Calculate the direction towards the player
            direction_x = self.player.pos.x - enemy['pos'].x
            direction_y = self.player.pos.y - enemy['pos'].y

            # Normalize the direction vector
            length = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if length != 0:
                direction_x /= length
                direction_y /= length

            # Update enemy position based on the normalized direction
            enemy['pos'].x += direction_x * enemy['speed']
            enemy['pos'].y += direction_y * enemy['speed']

        # Spawn enemies based on the timer only in the Building room
        if self.game_time.previous_timer.hour != self.game_time.current_time.hour:
            if random.random() < self.spawn_chance:
                enemy_x = random.randint(0, SCREENWIDTH - self.player.size)
                enemy_y = random.randint(0, SCREENHEIGHT - self.player.size)
                enemy_image = pygame.image.load("Game\Assets\enemy.png")  # Replace with the actual path
                self.enemies.append({'pos': pygame.Vector2(enemy_x, enemy_y), 'speed': 5, 'image': enemy_image})

            self.game_time.previous_timer = self.game_time.current_time
            self.spawn_chance += self.spawn_chance_increment

            print(self.spawn_chance)
    
    def heuristic(self, pos, goal):
        # Euclidean distance as the heuristic for A* algorithm
        return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5

    def get_neighbors(self, pos):
        # Get neighboring positions for a given position
        x, y = pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [neighbor for neighbor in neighbors if neighbor in self.walkable_positions]
    
    def spawn_scraps(self, list):
        print(f"Current number of scraps: {len(list)}")
        scrap_pos = pygame.Vector2(random.randint(0, SCREENWIDTH - 30), random.randint(0, SCREENHEIGHT - 30))
        print(f"Generated scrap position: {scrap_pos}")
        
        scrap_type = random.choice([
            {'Value': 5, 'Image': SCRAPIMAGE['horn']},
            {'Value': 10, 'Image': SCRAPIMAGE['gold bar']},
            {'Value': 35, 'Image': SCRAPIMAGE['mug']},
            {'Value': 5, 'Image': SCRAPIMAGE['pills']},
            {'Value': 20, 'Image': SCRAPIMAGE['sign']},
            {'Value': 15, 'Image': SCRAPIMAGE['cup']},
            {'Value': 40, 'Image': SCRAPIMAGE['gold_cup']},
            {'Value': 45, 'Image': SCRAPIMAGE['cat']},
            {'Value': 20, 'Image': SCRAPIMAGE['cola']},
            {'Value': 30, 'Image': SCRAPIMAGE['magnifying_glass']},
        ])
        new_scrap = Scrap(self.display, scrap_pos, self.player, scrap_type['Value'], self, scrap_type['Image'])

        if any(obstacle.colliderect(new_scrap.hitbox) for obstacle in self.obstacles):
            print("Collision detected. Adjusting position.")
            new_scrap.pos = pygame.Vector2(random.randint(0, SCREENWIDTH - 30), random.randint(0, SCREENHEIGHT - 30))
        #for obs in self.obstacles:
        #    if obs.colliderect(new_scrap.hitbox):
        #        new_scrap.pos = pygame.Vector2(random.randint(0, SCREENWIDTH - 30), random.randint(0, SCREENHEIGHT - 30))

        list.append(new_scrap)
        print("Scrap added to the list.")

    def run(self):
        plain_bg = pygame.image.load(r"Game\Assets\bg_building.png").convert()
        window_size = (SCREENWIDTH, SCREENHEIGHT) # Get the size of the window
        scaled_bg = pygame.transform.scale(plain_bg, window_size) # Scale the background image to fit the window
        self.display.blit(scaled_bg, (0,0))
    
        self.player.draw()
        self.draw_gui()
        self.player.move()
        
        for obstacle in self.obstacles:
            pygame.draw.rect(self.display, GREY, obstacle)
            
        for obstacle in self.obstacles:
            if self.player.hitbox.colliderect(obstacle):
                # Player collided with an obstacle, adjust player's position to prevent passing through
                if self.player.pos.x < obstacle.x:
                    self.player.pos.x = obstacle.x - self.player.size
                elif self.player.pos.x > obstacle.x + obstacle.width:
                    self.player.pos.x = obstacle.x + obstacle.width
                if self.player.pos.y < obstacle.y:
                    self.player.pos.y = obstacle.y - self.player.size
                elif self.player.pos.y > obstacle.y + obstacle.height:
                    self.player.pos.y = obstacle.y + obstacle.height
        

        if len(self.spawned_scraps) < 5:
            self.spawn_scraps(self.spawned_scraps)

        for scrap in self.spawned_scraps:
            scrap.draw()
            scrap.update()

            # Check for collisions with obstacles
            #if any(obstacle.colliderect(scrap.hitbox) for obstacle in self.obstacles):
            #    self.spawn_scraps(self.spawned_scraps)
            #    break

        # Check for collisions between player and enemies
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(int(enemy['pos'].x), int(enemy['pos'].y), self.player.size, self.player.size)

            if self.player.hitbox.colliderect(enemy_rect):
                # Player collided with an enemy, reset player's stored scrap value
                self.player.stored_value = 0
                self.player.inventory.clear()

            for obstacle in self.obstacles:
                if enemy_rect.colliderect(obstacle):
                    # Enemy collided with an obstacle, adjust enemy's position to prevent passing through
                    if enemy['pos'].x < obstacle.x:
                        enemy['pos'].x = obstacle.x - self.player.size
                    elif enemy['pos'].x > obstacle.x + obstacle.width:
                        enemy['pos'].x = obstacle.x + obstacle.width
                    if enemy['pos'].y < obstacle.y:
                        enemy['pos'].y = obstacle.y - self.player.size
                    elif enemy['pos'].y > obstacle.y + obstacle.height:
                        enemy['pos'].y = obstacle.y + obstacle.height
            
            # Update and draw enemies
            self.display.blit(pygame.image.load("Game\Assets\enemy.png"), enemy['pos'])

        # Call the spawn_enemies method here
        self.spawn_enemies()

        for enemy in self.enemies:

            # Update enemy position based on the path
            if 'index' in enemy and enemy['index'] < len(enemy['path']):
                next_pos = enemy['path'][enemy['index']]
                direction_x = next_pos[0] - enemy['pos'].x
                direction_y = next_pos[1] - enemy['pos'].y

                length = (direction_x ** 2 + direction_y ** 2) ** 0.5
                if length != 0:
                    direction_x /= length
                    direction_y /= length

                enemy['pos'].x += direction_x * enemy['speed']
                enemy['pos'].y += direction_y * enemy['speed']

                # Check if the enemy has reached the next position
                if int(enemy['pos'].x) == next_pos[0] and int(enemy['pos'].y) == next_pos[1]:
                    enemy['index'] += 1

        self.red_box.draw()
        self.red_box.check_collision()

    def draw_gui(self):
        FONT = pygame.font.Font(None, 36)
        #Draw Room name
        room_name_text = FONT.render(f"Building", True, WHITE)
        room_name_text_pos = ((SCREENWIDTH / 2) - (room_name_text.get_width()/2), 10)
        self.display.blit(room_name_text, room_name_text_pos)
        
        #Draw Player Scrap Value
        player_scrapval_text = FONT.render(f"Player Value: {self.player.stored_value}", True, WHITE)
        scrap_value_text_pos = (SCREENWIDTH - player_scrapval_text.get_width() - 10, 10)
        self.display.blit(player_scrapval_text, scrap_value_text_pos)

        #Draw guide
        collect_scraps_text = FONT.render("Press 'Space' to collect scraps", True, WHITE)
        # Calculate the x position to center the text
        text_x = (SCREENWIDTH / 2) - (collect_scraps_text.get_width() / 2)
        # Calculate the y position to place the text at the bottom with a margin
        text_y = SCREENHEIGHT - collect_scraps_text.get_height() - 20  # 20 pixels margin from the bottom
        self.display.blit(collect_scraps_text, (text_x, text_y))

    def spawn_enemies(self):
        # Update and draw enemies only in the Building room
        for enemy in self.enemies:
            # Calculate the direction towards the player
            direction_x = self.player.pos.x - enemy['pos'].x
            direction_y = self.player.pos.y - enemy['pos'].y

            # Normalize the direction vector
            length = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if length != 0:
                direction_x /= length
                direction_y /= length

            # Update enemy position based on the normalized direction
            enemy['pos'].x += direction_x * enemy['speed']
            enemy['pos'].y += direction_y * enemy['speed']

            # Draw the enemy
            self.display.blit(pygame.image.load("Game\Assets\enemy.png"), enemy['pos'])

        # Spawn enemies based on the timer only in the Building room
        if self.game_time.previous_timer.hour != self.game_time.current_time.hour:
            if random.random() < self.spawn_chance:
                enemy_x = random.randint(0, SCREENWIDTH - self.player.size)
                enemy_y = random.randint(0, SCREENHEIGHT - self.player.size)
                self.enemies.append({'pos': pygame.Vector2(enemy_x, enemy_y), 'speed': 5})

            self.game_time.previous_timer = self.game_time.current_time
            self.spawn_chance += self.spawn_chance_increment
            print(self.spawn_chance)

class Scrap:
    def __init__(self, display, pos, player, value, room, image):
        self.display = display
        self.room = room
        self.player = player
        self.pos = pos
        self.size = 30

        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.image = image
        self.value = value

    def update(self): # Diri ang behavior sa scrap, kung naa moy gusto e dugang 
        keys = pygame.key.get_pressed()

        #Check for player hitbox
        if self.player.hitbox.colliderect(self.hitbox) and keys[pygame.K_SPACE]:
            if len(self.player.inventory) < 4:
                #Update player stored scrap value
                self.player.stored_value += self.value
                self.player.inventory.append(self.image)
                #Remove the scrap
                self.room.spawned_scraps.remove(self)

    def draw(self):
        FONT = pygame.font.Font(None, 36)

        #pygame.draw.rect(self.display, self.color, [self.pos.x, self.pos.y, self.size, self.size])
        image_width, image_height = self.image.get_size()
        self.display.blit(pygame.transform.scale(self.image, (2 * image_width, 2 * image_height)), self.pos)
        #value_text = FONT.render(f"{self.value}", True, BLACK)
        #self.display.blit(value_text, self.pos)

class EndScreen:
    def __init__(self, display, gameSceneManager):
        self.display = display
        self.gameSceneManager = gameSceneManager

    def run(self):
        # Display end screen content, e.g., game over message, final score, etc.
        FONT = pygame.font.Font(None, 72)
        game_over_text = FONT.render("Game Over! You did not meet the quota", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
        self.display.blit(game_over_text, text_rect)

class GameTime:
    def __init__(self):
        self.timer_interval = 2  # in seconds
        self.start_time = datetime.datetime(1, 1, 1, 9, 0)  # 9:00 AM and 500 milliseconds
        self.end_time = datetime.datetime(1, 1, 1, 0, 0)  # January 1, 1 AD, 12:00 AM
        self.current_time = self.start_time
        self.timer_ticks = pygame.time.get_ticks()
        self.timer_running = True
        self.previous_timer = self.current_time

    def tick(self):
        if pygame.time.get_ticks() - self.timer_ticks >= self.timer_interval * 1000 and self.timer_running:
            self.current_time += datetime.timedelta(minutes=30)
            self.timer_ticks = pygame.time.get_ticks()

    def strftime(self, format):
        return self.current_time.strftime(format)
    
class RedBox:
    def __init__(self, display, player, gameSceneManager):
        self.display = display
        self.player = player
        self.gameSceneManager = gameSceneManager
        self.size = 30
        self.color = RED
        
        self.image = pygame.image.load("Game\Assets\portal.png")
        
        self.spawn_red_box()

    def spawn_red_box(self):
        self.pos = pygame.Vector2(random.randint(0, SCREENWIDTH - self.size), random.randint(0, SCREENHEIGHT - self.size))
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def draw(self):
        self.display.blit(self.image, self.pos)
        
    def check_collision(self):
        current_scene = self.gameSceneManager.get_scene()
        # Check for collisions with the player
        keys = pygame.key.get_pressed()
        if current_scene == 'Moon':
            if self.player.hitbox.colliderect(self.hitbox) and keys[pygame.K_1]:
                self.gameSceneManager.set_scene('Spaceship')
            elif self.player.hitbox.colliderect(self.hitbox) and keys[pygame.K_2]:
                self.gameSceneManager.set_scene('Building')
        elif current_scene == 'Spaceship' or current_scene == 'Building':
            if self.player.hitbox.colliderect(self.hitbox) and keys[pygame.K_SPACE]:
                self.gameSceneManager.set_scene('Moon')
        

if __name__ == '__main__':
    game = Game()
    game.run()