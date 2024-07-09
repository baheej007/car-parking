import pygame as pg
import sys
import random

# Initialize Pygame
pg.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT =1370, 600
BG_COLOR = (255, 255, 255)
ROAD_COLOR = (50, 50, 50)
PARKING_COLOR = (0, 255, 0)
FPS = 30

# Car properties
car_width, car_height = 100, 100
car_speed = 5

# Parking position
parking_x, parking_y = 350, 100
parking_width, parking_height = 100, 200

# Setup display
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Car Parking Game')

# Clock to control FPS
clock = pg.time.Clock()

def create_random_road():
    road_blocks = []
    for i in range(10):
        block_x = random.randint(0, SCREEN_WIDTH - 100)
        block_y = i * 60
        road_blocks.append(pg.Rect(block_x, block_y, 100, 60))
    return road_blocks

def find_initial_car_position(road_blocks):
    while True:
        car_x = random.randint(0, SCREEN_WIDTH - car_width)
        car_y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - car_height)
        car_rect = pg.Rect(car_x, car_y, car_width, car_height)
        if not any(car_rect.colliderect(block) for block in road_blocks):
            return car_x, car_y

def draw(car_image, car_rect, road_blocks):
    screen.fill(BG_COLOR)
    # Draw road
    for block in road_blocks:
        pg.draw.rect(screen, ROAD_COLOR, block)
    # Draw parking spot
    pg.draw.rect(screen, PARKING_COLOR, (parking_x, parking_y, parking_width, parking_height))
    # Draw car
    screen.blit(car_image, car_rect)
    pg.display.flip()

def check_collision(car_rect, road_blocks):
    for block in road_blocks:
        if car_rect.colliderect(block):
            return True
    return False

def game_loop(car_image):
    road_blocks = create_random_road()
    car_x, car_y = find_initial_car_position(road_blocks)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            car_x -= car_speed
        if keys[pg.K_RIGHT]:
            car_x += car_speed
        if keys[pg.K_UP]:
            car_y -= car_speed
        if keys[pg.K_DOWN]:
            car_y += car_speed

        # Create car rectangle for collision detection
        car_rect = pg.Rect(car_x, car_y, car_width, car_height)

        # Check for collision with road blocks
        if check_collision(car_rect, road_blocks):
            print("Failed!")
            pg.quit()
            sys.exit()

        # Check for parking success
        if (parking_x < car_x < parking_x + parking_width and 
            parking_y < car_y < parking_y + parking_height):
            print("Parked successfully!")
            return  # Exit the loop to restart the game

        draw(car_image, car_rect, road_blocks)
        clock.tick(FPS)

def main():
    # Load images
    car_image = pg.image.load('car.png')
    car_image = pg.transform.scale(car_image, (car_width, car_height))

    while True:
        game_loop(car_image)
        print("Restarting game...")

if __name__ == '__main__':
    main()
