import pygame, sys, os, random

pygame.init()
# Get the absolute path to the script or the bundled executable
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the Pygame window
screen = pygame.display.set_mode((920, 700))
pygame.display.set_caption('Duck Hunt')

# Load the background and other images using absolute file paths
bg = pygame.image.load(os.path.join(script_dir, "Wood_BG.png"))
land = pygame.image.load(os.path.join(script_dir, "Land_BG.png"))
water = pygame.image.load(os.path.join(script_dir, "Water_BG.png"))
cloud = pygame.image.load(os.path.join(script_dir, "Cloud1.png"))
duck = pygame.image.load(os.path.join(script_dir, 'duck.png'))
gunshot = pygame.mixer.Sound(os.path.join(script_dir, "vine boom.mp3"))

pygame.display.set_icon(duck)  # game icon
clock = pygame.time.Clock()  # for fps

# Create a list to store the clouds' positions and speeds
clouds = []
num_clouds = 10
for _ in range(num_clouds):
    cloud_x = random.randrange(0, 900 - cloud.get_width())
    cloud_y = random.randrange(30, 70)
    cloud_speed = 1
    clouds.append((cloud_x, cloud_y, cloud_speed))

# Create a list to store the ducks' positions and speeds
ducks = []
num_ducks = random.randint(14, 21)
for _ in range(num_ducks):
    duck_x = random.randrange(0, 900 - duck.get_width())
    duck_y = random.randrange(0, 600)
    duck_speed = random.randint(1, 3)
    ducks.append((duck_x, duck_y, duck_speed))

crosshair = pygame.image.load(os.path.join(script_dir, 'crosshair.png'))

# Speed and positioning
land_pos_y = 500
land_speed = 1
water_pos_y = 550
water_speed = 1.5

# Hide the mouse pointer
pygame.mouse.set_visible(False)
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Mouse work
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.get_pos()
            crosshair_rect = crosshair.get_rect(center=pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            gunshot.play()#plays gunshot
            # Check if the crosshair collides with any of the ducks
            for i, duck_data in enumerate(ducks):
                duck_x, duck_y, duck_speed = duck_data[:3]
                duck_hitbox = duck.get_rect().move(duck_x, duck_y)
                if duck_hitbox.collidepoint(event.pos):
                    # Remove the duck if it is clicked
                    ducks.pop(i)
                    break

    screen.blit(bg, (0, 0))

    if len(ducks) == 0 and not game_over:
        # All ducks have been removed
        game_over = True
        font = pygame.font.Font(None, 60)  # Choose the desired font and size
        text = font.render("Mission Passed!Press Space for new game", True, (255, 100, 10))  # Render the text
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Center the text on the screen
        screen.blit(text, text_rect)

    # Land animation
    land_pos_y += land_speed
    if land_pos_y >= 550:
        land_speed *= -1
    if land_pos_y <= 500:
        land_speed *= -1
    screen.blit(land, (0, land_pos_y))

    # Water animation
    water_pos_y += water_speed
    if water_pos_y >= 560:
        water_speed *= -1
    if water_pos_y <= 510:
        water_speed *= -1
    screen.blit(water, (0, water_pos_y))

    # Load and move the set of clouds
    for i, cloud_data in enumerate(clouds):
        cloud_x, cloud_y, cloud_speed = cloud_data
        cloud_x += cloud_speed

        # Wrap the clouds to the other side if they go off-screen
        if cloud_x > 900:
            cloud_x = -cloud.get_width()

        screen.blit(cloud, (cloud_x, cloud_y))
        clouds[i] = (cloud_x, cloud_y, cloud_speed)

    # Load and move the ducks
    for i, duck_data in enumerate(ducks):
        duck_x, duck_y, duck_speed = duck_data
        duck_x += duck_speed  # Move the duck horizontally

        # Wrap the duck around to the other side if it goes off-screen
        if duck_x > 900:
            duck_x = -duck.get_width()

        ducks[i] = (duck_x, duck_y, duck_speed)  # Update the duck's position in the list

        screen.blit(duck, (duck_x, duck_y))

    screen.blit(crosshair, crosshair.get_rect(center=pygame.mouse.get_pos()))  # Crosshair

    if game_over:
        # Pause the game and wait for user input
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Reset the game and start a new game
                        game_over = False
                        ducks = []
                        num_ducks = random.randint(14, 21)
                        for _ in range(num_ducks):
                            duck_x = random.randrange(0, 900 - duck.get_width())
                            duck_y = random.randrange(0, 600)
                            duck_speed = random.randint(1, 3)
                            ducks.append((duck_x, duck_y, duck_speed))
                        break

            pygame.display.update()
            clock.tick(60)
    else:
        # Update the game if it's not game over
        pygame.display.update()
        clock.tick(60)
