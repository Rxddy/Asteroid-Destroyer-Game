import os  # OS module for file handling
import random  # Random module for enemy spawning and movement
import turtle  # Turtle module for game graphics
import pygame  # Pygame module for sound effects
import time  # Time module for game loop delays

# Initialize Pygame mixer for sound effects
pygame.mixer.init()

# Registering images for sprites
turtle.register_shape("images/enemy.gif")
turtle.register_shape("images/ally.gif")

turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("images/background.gif")
turtle.title("ASTEROID DESTROYER")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)  # Enable smooth rendering

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
        self.speed = 4
        self.lives = 3
    
    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed = max(0, self.speed - 1)

# Enemy and Ally classes
class Enemy(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.speed = 5
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

# Missile class
class Missile(Sprite):
    def __init__(self, spriteshapes, color, startx, starty):
        super().__init__(spriteshapes, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.3)
        self.speed = 30
        self.status = "ready"
        self.goto(-1000, 1000)
    
    def fire(self):
        if self.status == "ready":
            pygame.mixer.Sound("Sounds/laser.mp3").play()
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "shooting"
    
    def move(self):
        if self.status == "shooting":
            self.fd(self.speed)
            if self.xcor() < -340 or self.xcor() > 340 or self.ycor() < -340 or self.ycor() > 340:
                self.goto(-1000, 1000)
                self.status = "ready"

# Game class
class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.lives = 3
        self.pen = turtle.Turtle()

    def draw_border(self):
        # Create a pen for drawing the border
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-350, 350)  # Starting point at the top-left corner
        self.pen.pendown()
        # Draw the border
        for _ in range(4):
            self.pen.fd(700)  # Move forward by 700 units
            self.pen.rt(90)   # Turn 90 degrees right
        self.pen.penup()  # Lift pen to avoid drawing unwanted lines
        self.pen.hideturtle()  # Hide the pen turtle after drawing the border
    
    def show_status(self):
        self.pen.undo()
        msg = "Score: %s Lives: %s" % (self.score, self.lives)
        self.pen.goto(-350, 360)
        self.pen.write(msg, font=("Arial", 16, "normal"))
    
    def game_over(self):
        self.pen.goto(0, 50)  
        
        for _ in range(6):  
            self.pen.clear()
            self.pen.color("red")
            self.pen.write("GAME OVER", align="center", font=("Arial", 30, "bold"))
            turtle.update()
            time.sleep(0.1)
            self.pen.color("yellow")
            self.pen.clear()
            self.pen.write("GAME OVER", align="center", font=("Arial", 30, "bold"))
            turtle.update()
            time.sleep(0.1)
        
        self.pen.goto(0, 0)
        self.pen.color("white")
        self.pen.write(f"Final Score: {self.score}", align="center", font=("Arial", 20, "bold"))
        
        self.pen.goto(0, -50)
        self.pen.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Arial", 16, "normal"))
        
        turtle.update()

    def cheat(self):
        game.lives += 5
        game.score += 1000
        game.show_status

def main():
    turtle.clearscreen()
    turtle.bgcolor("black")
    turtle.bgpic("images/background.gif")
    turtle.title("ASTEROID DESTROYER")
    turtle.tracer(0)

    global game, player, missile, enemies, allies

    game = Game()
    game.draw_border()
    game.show_status()

    player = Player("triangle", "springgreen", 0, 0)
    missile = Missile("turtle", "yellow", 0, 0)

    enemies = [Enemy("images/enemy.gif", "grey", random.randint(-300, 300), random.randint(-300, 300)) for _ in range(6)]
    allies = [Ally("images/ally.gif", "blue", random.randint(-300, 300), random.randint(-300, 300)) for _ in range(6)]

    turtle.onkeypress(player.turn_left, "a")
    turtle.onkeypress(player.turn_right, "d")
    turtle.onkeypress(player.accelerate, "Up")
    turtle.onkeypress(player.decelerate, "Down")
    turtle.onkeypress(missile.fire, "space")
    turtle.onkeypress(game.cheat, "0")
    turtle.listen()

    game_loop()

def game_loop():
    while True:
        turtle.update()
        time.sleep(0.035)

        player.move()
        missile.move()

        if game.lives == 0:
            game.game_over()

            def restart():
                main()  

            def quit_game():
                turtle.bye()

            turtle.onkeypress(restart, "r")
            turtle.onkeypress(quit_game, "q")
            turtle.listen()

            while True:
                turtle.update()

        for enemy in enemies:
            enemy.move()
            if missile.is_collision(enemy):
                pygame.mixer.Sound("Sounds/explosion.mp3").play()
                enemy.goto(random.randint(-300, 300), random.randint(-300, 300))
                missile.goto(-1000, 1000)
                missile.status = "ready"
                game.score += 100
                game.show_status()

            if player.is_collision(enemy):
                enemy.goto(random.randint(-300, 300), random.randint(-300, 300))
                missile.goto(-1000, 1000)
                missile.status = "ready"
                game.lives -= 1
                game.show_status()

        for ally in allies:
            ally.move()

            if player.is_collision(ally):
                game.lives -= 1
                ally.goto(random.randint(-300, 300), random.randint(-300, 300))
                game.score -= 50
                game.show_status()
                
            if missile.is_collision(ally):
                game.score -= 50
                ally.goto(random.randint(-300, 300), random.randint(-300, 300))
                game.show_status()

if __name__ == "__main__":
    main()
