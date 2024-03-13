# type: ignore
import pgzrun
import random

# setup các thông tin của game và trạng thái game
TITLE = "Game máy bay bắn quái vật"
HEIGHT = 700
WIDTH = 900
POINT = 0

TIME_CREATE_ENERMIES = 1.0

begining = 0
running = 1
ending = 2
STATE = begining

music.set_volume(0.5)
music.play('start_game')

# Khởi tạo các class nhân vật và chức năng
class ship:
    def __init__(self, image, pos) -> None:
        self.ship = Actor(image, pos)
        self.bullets = list()
        
    def draw(self):
        self.ship.draw()
        
    def add_bullets(self):
        self.bullets.append(
            Actor(
                'laser_bullet_60', 
                center=(self.ship.x, self.ship.y - 45)
            )
        )
        sounds.blaster_2.play()
    
    def move_bullets(self):
        for bullet in self.bullets:
            if (bullet.y <= 0):
                self.bullets.remove(bullet)
                continue
            bullet.y -= 7
    
    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()
    
    def ship_move(self):
        if keyboard.up:
            if 0 <= self.ship.y:
                self.ship.y -= 5
        if keyboard.down:
            if self.ship.y <= 700:
                self.ship.y += 5
        if keyboard.right:
            if self.ship.x <= 900:
                self.ship.x += 5
        if keyboard.left:
            if 0 <= self.ship.x:
                self.ship.x -= 5
                
    def check_ship_destroy(self, list_enermies):
        global STATE
        for enermy in list_enermies:
            if self.ship.distance_to(enermy) <= 34:
                clock.unschedule(enermies.create_monsters)
                clock.unschedule(delete_animation_enermies_die)
                music.stop()
                music.play_once('game_over')
                STATE = ending
        
class monsters:
    def __init__(self, list_images):
      self.list_images = list_images
      self.list_actors_enemy = list()
    
    def create_monsters(self):
        self.list_actors_enemy.append(
            Actor(
                random.choice(self.list_images), 
                center=(random.choice(range(40, 860)), 0)
            )
        )
    
    def move_enermies(self):
        for enermy in self.list_actors_enemy:
            if (enermy.y >= 700):
                self.list_actors_enemy.remove(enermy)
                continue
            enermy.y += 2
    
    def check_enermies_destroy(self, list_bullets):
        global POINT
        for bullet in list_bullets:
            for enermy in self.list_actors_enemy:
                if enermy.distance_to(bullet) <= 40:
                    list_animation_enermies_die.append(Actor('boom', enermy.pos))
                    self.list_actors_enemy.remove(enermy)
                    list_bullets.remove(bullet)
                    POINT += 1
                    sounds.boom.play()
                    check_point()
    
    def draw(self):
        for enermy in self.list_actors_enemy:
            enermy.draw()

# Khởi chạy các nhân vật và vẽ lên màn hình game
ship_1 = ship('ship_1_1', (450, 350))
enermies = monsters(['ship_e', 'ship_e_1', 'ship_e_2'])
list_animation_enermies_die = list()

button_reset_game = Actor('reset_game', center=(450, 600))
button_start = Actor('button_start', center=(450, 350))
button_ship_1 = Actor('ship_1_1', center=(350, 350))
button_ship_2 = Actor('ship_1_2', center=(550, 350))

def draw():
    if STATE == begining:
        screen.clear()
        screen.blit('bg_start_game', (0,0))
        button_ship_1.draw()
        button_ship_2.draw()
    
    if STATE == running:
        screen.clear()
        screen.blit('bg_star_sky', (0,0))
        screen.draw.text(
            f"Điểm số: {POINT}",
            (10, 10),
            fontsize=24,
            fontname='arial',
            color='white',
        )
        ship_1.draw()
        ship_1.draw_bullets()
        enermies.draw()
        for animation in list_animation_enermies_die:
            animation.draw()
            
    if STATE == ending:
        screen.clear()
        screen.blit('game-over', (0,0))
        screen.draw.text(
            f"Điểm số: {POINT}",
            (400, 50),
            fontsize=24,
            fontname='arial',
            color='white',
        )
        button_reset_game.draw()
    
def update():
    if STATE == running:
        ship_1.ship_move()
        ship_1.move_bullets()
        ship_1.check_ship_destroy(enermies.list_actors_enemy)
        enermies.move_enermies()
        enermies.check_enermies_destroy(ship_1.bullets)
    
def on_key_down(key):
    if STATE == running:
        if key == keys.SPACE:
            ship_1.add_bullets()

def on_mouse_down(button, pos):
    global STATE, POINT, TIME_CREATE_ENERMIES
    if STATE == begining:
        if button == mouse.LEFT:
            
            if button_ship_1.distance_to(pos) <= 30:
                ship_1.ship.image = 'ship_1_1'
                
            if button_ship_2.distance_to(pos) <= 30:
                ship_1.ship.image = 'ship_1_2'

            set_speed_create_enermies(TIME_CREATE_ENERMIES)
            clock.schedule_interval(delete_animation_enermies_die, 0.5)
            music.play('8bit_music')
            STATE = running
        
    if STATE == ending:
        if button == mouse.LEFT and button_reset_game.distance_to(pos) <= 40:
            POINT = 0
            TIME_CREATE_ENERMIES = 1.0
            ship_1.ship.pos = (450, 450)
            ship_1.bullets = list()
            enermies.list_actors_enemy = list()
            set_speed_create_enermies(TIME_CREATE_ENERMIES)
            clock.schedule_interval(delete_animation_enermies_die, 0.5)
            music.play('8bit_music')
            STATE = running
            
def delete_animation_enermies_die():
    if STATE == running:
        if len(list_animation_enermies_die) > 0:
            list_animation_enermies_die.pop(0)

# set up tăng độ khó cho game
def check_point():
    if POINT == 40:
        set_speed_create_enermies(0.8)
    elif POINT == 80:
       set_speed_create_enermies(0.6)
    elif POINT == 150:
        set_speed_create_enermies(0.4)
    elif POINT == 200:
        set_speed_create_enermies(0.2)

def set_speed_create_enermies(time):
    global TIME_CREATE_ENERMIES
    TIME_CREATE_ENERMIES = time
    clock.unschedule(enermies.create_monsters)
    clock.schedule_interval(enermies.create_monsters, TIME_CREATE_ENERMIES)

pgzrun.go()