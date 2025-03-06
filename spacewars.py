#!/usr/bin/env python3

import os
import random
import turtle
import pygame
import time
import sys

# Initialize Pygame mixer for sound effects
pygame.mixer.init()

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# Registering images for sprites
turtle.register_shape(os.path.join(base_path, "Images", "enemy.gif"))
turtle.register_shape(os.path.join(base_path, "Images", "ally.gif"))
turtle.bgpic(os.path.join(base_path, "Images", "background.gif"))


turtle.speed(0)
turtle.bgcolor("black")
turtle.title("ASTEROID DESTROYER")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

# Game settings
class GameSettings:
    def __init__(self):
        self.health_pickups_enabled = True
        self.player_color = "springgreen"
        self.current_state = "menu"  # menu, game, game_over
        self.backgrounds = ["purplebackground.gif", "bluebackground.gif",
                           "blackbackground.gif", "pinkbackground.gif", "greenbackground.gif"]
        self.current_background = 0

# Base Sprite class
class Sprite(turtle.Turtle):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(shape=spriteshapes)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx, starty)
        self.speed = 1
    
    def move(self):
        self.fd(self.speed)
        
        # Reflect at boundaries
        if self.xcor() > 335 or self.xcor() < -335:
            self.setx(max(min(self.xcor(), 335), -335))
            self.setheading(180 - self.heading())
        if self.ycor() > 335 or self.ycor() < -335:
            self.sety(max(min(self.ycor(), 335), -335))
            self.setheading(360 - self.heading())
    
    def is_collision(self, other):
        return abs(self.xcor() - other.xcor()) <= 20 and abs(self.ycor() - other.ycor()) <= 20

# Player class
class Player(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.shapesize(stretch_wid=0.7, stretch_len=1.1)
        self.speed = 2
        self.health = 100  # Player health
        self.health_bar = turtle.Turtle()
        self.health_bar.penup()
        self.health_bar.hideturtle()
        self.health_bar.goto(-350, 310)
        self.health_bar.color("green")
        self.health_bar.pensize(10)
        self.update_health_bar()
    
    def update_health_bar(self):
        self.health_bar.clear()
        self.health_bar.penup()
        self.health_bar.goto(-350, 310)
        self.health_bar.pendown()
        
        # Draw background (gray) health bar
        self.health_bar.color("gray")
        self.health_bar.forward(140)  # Max health bar length
        
        # Draw current health (green or red based on health)
        self.health_bar.penup()
        self.health_bar.goto(-350, 310)
        self.health_bar.pendown()
        
        # Change color based on health level
        if self.health > 50:
            self.health_bar.color("green")
        elif self.health > 25:
            self.health_bar.color("yellow")
        else:
            self.health_bar.color("red")
            
        # Draw actual health bar (max length 140)
        health_length = max(0, (self.health / 100) * 140)
        self.health_bar.forward(health_length)

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed = max(0, self.speed - 1)
    
    def set_color(self, color):
        self.color(color)

# Enemy and Ally classes
class Enemy(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.speed = 3
        self.health = 50  # Each enemy has health
        self.setheading(random.randint(0, 360))

    def move(self):
        super().move()
        if random.randint(0, 100) < 3:  # Random chance to change direction
            self.setheading(random.randint(0, 360))

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.goto(random.randint(-300, 300), random.randint(-300, 300))
            self.health = 50  # Reset enemy health

class Ally(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.speed = 2
        self.setheading(random.randint(0, 360))

# Health Pickup class
class HealthPickup(Sprite):
    def __init__(self, startx, starty):
        super().__init__("circle", "red", startx, starty)
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.active = True
    
    def respawn(self):
        self.goto(random.randint(-300, 300), random.randint(-300, 300))
        self.active = True

# Missile class
class Missile(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.8)  # Make missile more visible by increasing length
        self.speed = 20  # Reduced speed slightly to make movement more visible
        self.status = "ready"
        self.goto(-1000, 1000)  # Start off-screen initially
        self.hideturtle()  # Ensure it's hidden initially

    def fire(self):
        if self.status == "ready":
            try:
                pygame.mixer.Sound(os.path.join(base_path, "Sounds", "laser.mp3")).play()
            except:
                pass  # Silently fail if sound file doesn't exist
            
            # Set missile's position to the player's position
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "shooting"
            self.showturtle()  # Make missile visible
            turtle.update()  # Force screen update to show the missile

    def move(self):
        if self.status == "shooting":
            self.fd(self.speed)  # Move the missile forward
            
            # Check if missile is out of bounds
            if self.xcor() < -340 or self.xcor() > 340 or self.ycor() < -340 or self.ycor() > 340:
                self.hideturtle()  # Hide missile when out of bounds
                self.goto(-1000, 1000)  # Move missile off-screen
                self.status = "ready"

# Game class
class Game:
    def __init__(self):
        self.score = 0
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.color("white")

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-350, 350)
        self.pen.pendown()
        for _ in range(4):
            self.pen.fd(700)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.hideturtle()

    def show_status(self):
        self.pen.clear()
        msg = f"Score: {self.score}"
        self.pen.goto(-350, 360)
        self.pen.write(msg, font=("Comic Sans MS", 16, "normal"))

    def game_over(self):
        self.pen.clear()
        self.pen.goto(0, 50)
        self.pen.color("red")
        self.pen.write("GAME OVER", align="center", font=("Comic Sans MS", 30, "bold"))
        turtle.update()

        self.pen.goto(0, 0)
        self.pen.color("white")
        self.pen.write(f"Final Score: {self.score}", align="center", font=("Comic Sans MS", 20, "bold"))
        
        self.pen.goto(0, -50)
        self.pen.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Comic Sans MS", 16, "normal"))
        turtle.update()

    def cheat(self):
        self.score += 500
        player.health = 100
        player.update_health_bar()
        self.show_status()

class GameSettings:
    def __init__(self):
        self.health_pickups_enabled = True
        self.player_color = "springgreen"
        self.current_state = "menu"  # menu, game, game_over
        self.backgrounds = ["purplebackground.gif", "bluebackground.gif", 
                           "blackbackground.gif", "pinkbackground.gif", "greenbackground.gif"]
        self.current_background = 0  # Index of the current background

# Menu class
class Menu:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.color("white")
        self.selected_option = 0
        self.options = [
            "Start Game",
            "Health Pickups: ON",
            "Player Color: GREEN",
            "Bakcground Color: Default",
            "Quit"
        ]
        self.colors = ["springgreen", "red", "pink", "yellow", "white","lavender", "orange","cornflowerblue"]
        self.current_color_index = 0
        self.background = [""]

    def draw(self):
        self.pen.clear()
        
        # Draw title
        self.pen.goto(0, 150)
        self.pen.color("gold")
        self.pen.write("ASTEROID DESTROYER", align="center", font=("Comic Sans MS", 30, "bold"))
        
        # Draw menu options
        for i, option in enumerate(self.options):
            y = 50 - i * 50
            self.pen.goto(-150, y)
            
            # Highlight selected option
            if i == self.selected_option:
                self.pen.color("yellow")
                self.pen.write("> " + option, font=("Arial", 16, "normal"))
            else:
                self.pen.color("white")
                self.pen.write("  " + option, font=("Arial", 16, "normal"))
        
        # Draw instructions
        self.pen.goto(0, -200)
        self.pen.color("white")
        self.pen.write("Use UP/DOWN arrows to navigate", align="center", font=("Comic Sans MS", 12, "normal"))
        self.pen.goto(0, -230)
        self.pen.write("Press ENTER to select", align="center", font=("Comic Sans MS", 12, "normal"))
        
        turtle.update()

    def clear_menu(self):
        self.pen.clear()

    def move_up(self):
        self.selected_option = (self.selected_option - 1) % len(self.options)
        self.draw()

    def move_down(self):
        self.selected_option = (self.selected_option + 1) % len(self.options)
        self.draw()

    def select(self):
        if self.selected_option == 0:  # Start Game
            return "start_game"
        elif self.selected_option == 1:  # Toggle Health Pickups
            settings.health_pickups_enabled = not settings.health_pickups_enabled
            if settings.health_pickups_enabled:
                self.options[1] = "Health Pickups: ON"
            else:
                self.options[1] = "Health Pickups: OFF"
            self.draw()
        elif self.selected_option == 2:  # Change Player Color
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            color_name = self.colors[self.current_color_index].upper()
            self.options[2] = f"Player Color: {color_name}"
            settings.player_color = self.colors[self.current_color_index]
            self.draw()

        elif self.selected_option == 3:  # Change Background
            settings.current_background = (settings.current_background + 1) % len(settings.backgrounds)
            bg_name = settings.backgrounds[settings.current_background].replace("background.gif", "DEFAULT")
            bg_name = bg_name.replace("purplebackground.gif", "PURPLE")
            bg_name = bg_name.replace("bluebackground.gif", "BLUE")
            bg_name = bg_name.replace("blackbackground.gif", "BLACK")
            bg_name = bg_name.replace("pinkbackground.gif", "PINK")
            bg_name = bg_name.replace("greenbackground.gif", "GREEN")
            bg_name = bg_name.replace("background.gif", "DEFAULT")
            self.options[3] = f"Background: {bg_name}"
            # Update the background immediately to show the change
            turtle.bgpic(os.path.join(base_path, "Images", settings.backgrounds[settings.current_background]))
            self.draw()

        elif self.selected_option == 3:  # Quit
            return "quit"
        
        return None

def init_game():
    global game, player, missile, enemies, allies, health_pickups, menu, settings
    
    # Clear everything
    for t in turtle.turtles():
        t.hideturtle()
    
    turtle.clearscreen()
    turtle.bgcolor("black")
    turtle.bgpic(os.path.join(base_path, "Images", "background.gif"))
    turtle.title("ASTEROID DESTROYER")
    turtle.tracer(0)
    
    # Create game objects
    settings = GameSettings()
    game = Game()
    player = Player("triangle", settings.player_color, 0, 0)
    missile = Missile("triangle", "yellow", 0, 0)  # Changed shape to triangle for better visibility
    menu = Menu()
    
    # Create enemies and allies
    enemies = [Enemy(os.path.join(base_path, "Images", "enemy.gif"), "grey", 
                     random.randint(-300, 300), random.randint(-300, 300)) 
               for _ in range(6)]
    
    allies = [Ally(os.path.join(base_path, "Images", "ally.gif"), "blue", 
                   random.randint(-300, 300), random.randint(-300, 300)) 
              for _ in range(6)]
    
    # Create health pickups
    health_pickups = [HealthPickup(random.randint(-300, 300), random.randint(-300, 300)) 
                     for _ in range(3)]
    
    # Hide game objects initially
    player.hideturtle()
    player.health_bar.clear()
    missile.hideturtle()
    for enemy in enemies:
        enemy.hideturtle()
    for ally in allies:
        ally.hideturtle()
    for pickup in health_pickups:
        pickup.hideturtle()
    
    # Register key bindings for menu
    turtle.onkeypress(menu.move_up, "Up")
    turtle.onkeypress(menu.move_down, "Down")
    turtle.onkeypress(menu_select, "Return")
    turtle.listen()
    
    # Show menu
    menu.draw()
    settings.current_state = "menu"

def menu_select():
    action = menu.select()
    
    if action == "start_game":
        start_game()
    elif action == "quit":
        turtle.bye()

def start_game():
    # Clear the menu UI
    menu.clear_menu()
    
    # Set game state
    settings.current_state = "game"
    
    # Update player color from settings
    player.set_color(settings.player_color)
    
    # Show game elements
    player.showturtle()
    missile.hideturtle()  # Hide missile until fired
    
    for enemy in enemies:
        enemy.showturtle()
    
    for ally in allies:
        ally.showturtle()
    
    for pickup in health_pickups:
        if settings.health_pickups_enabled:
            pickup.showturtle()
        else:
            pickup.hideturtle()
    
    # Set up game area
    game.draw_border()
    game.show_status()
    player.update_health_bar()
    
    # Reset menu controls
    turtle.onkeypress(None, "Up")
    turtle.onkeypress(None, "Down")
    turtle.onkeypress(None, "Return")
    
    # Set game controls
    turtle.onkeypress(player.turn_left, "a")
    turtle.onkeypress(player.turn_right, "d")
    turtle.onkeypress(player.accelerate, "Up")
    turtle.onkeypress(player.decelerate, "Down")
    turtle.onkeypress(missile.fire, "space")
    turtle.onkeypress(game.cheat, "0")
    turtle.onkeypress(restart_game, "r")
    turtle.onkeypress(quit_game, "q")
    turtle.listen()
    
    # Start game loop
    gameloop()

def restart_game():
    init_game()

def quit_game():
    turtle.bye()

def gameloop():
    while settings.current_state == "game":
        turtle.update()
        time.sleep(0.005)

        player.move()
        missile.move()

        # Check if player is dead
        if player.health <= 0:
            settings.current_state = "game_over"
            game.game_over()
            break

        # Move and check enemies
        for enemy in enemies:
            enemy.move()
            
            # Check missile collision with enemy
            if missile.is_collision(enemy) and missile.status == "shooting":
                try:
                    pygame.mixer.Sound(os.path.join(base_path, "Sounds", "explosion.mp3")).play()
                except:
                    pass  # Silently fail if sound file doesn't exist
                enemy.decrease_health(50)
                missile.hideturtle()  # Explicitly hide the missile
                missile.goto(-1000, 1000)
                missile.status = "ready"
                game.score += 100
                game.show_status()

            # Check player collision with enemy
            if player.is_collision(enemy):
                enemy.goto(random.randint(-300, 300), random.randint(-300, 300))
                player.health -= 20
                player.update_health_bar()
                game.show_status()

        # Move and check allies
        for ally in allies:
            ally.move()

            # Check player collision with ally
            if player.is_collision(ally):
                player.health -= 20
                player.update_health_bar()
                ally.goto(random.randint(-300, 300), random.randint(-300, 300))
                game.show_status()

            # Check missile collision with ally
            if missile.is_collision(ally) and missile.status == "shooting":
                game.score -= 50
                ally.goto(random.randint(-300, 300), random.randint(-300, 300))
                missile.hideturtle()  # Explicitly hide the missile
                missile.goto(-1000, 1000)
                missile.status = "ready"
                game.show_status()
        
        # Check health pickups if enabled
        if settings.health_pickups_enabled:
            for pickup in health_pickups:
                if pickup.active and player.is_collision(pickup):
                    player.health = min(100, player.health + 25)  # Add health but cap at 100
                    player.update_health_bar()
                    pickup.active = False
                    pickup.hideturtle()
                    
                    # Respawn after a delay
                    turtle.ontimer(lambda p=pickup: respawn_pickup(p), 5000)  # 5 second delay
    
    # If game is over, wait for restart
    while settings.current_state == "game_over":
        turtle.update()
        time.sleep(0.01)

def respawn_pickup(pickup):
    if settings.current_state == "game" and settings.health_pickups_enabled:
        pickup.respawn()
        pickup.showturtle()

def main():
    init_game()
    turtle.mainloop()

if __name__ == "__main__":
    main()