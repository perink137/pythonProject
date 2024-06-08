import pygame
import random
import os

# Initialize pygame/ starting it
pygame.init()

# Setting the games constants
GAME_WIDTH = 700
GAME_HEIGHT = 750
SPEED = 10
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)

# Direction constants they have to be different so no overlaps happen
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.direction = DOWN

        # Initialize the snake with its default starting position
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

    def move(self, invincibility_mode):
        # Setting up the ability for snake to go in these directions
        x, y = self.coordinates[0]
        if self.direction == UP:
            y -= SPACE_SIZE
        elif self.direction == DOWN:
            y += SPACE_SIZE
        elif self.direction == LEFT:
            x -= SPACE_SIZE
        elif self.direction == RIGHT:
            x += SPACE_SIZE

        # Handle what happens when there is a wall collision in invincibility mode (teleport snake to opposite side)
        if invincibility_mode:
            if x < 0:
                x = GAME_WIDTH - SPACE_SIZE
            elif x >= GAME_WIDTH:
                x = 0
            if y < 50:
                y = GAME_HEIGHT - SPACE_SIZE
            elif y >= GAME_HEIGHT:
                y = 50

        self.coordinates.insert(0, [x, y])

    def change_direction(self, new_direction):
        # When changing directions preventing the snake from moving directly backwards
        if new_direction == 'left' and self.direction != RIGHT:
            self.direction = LEFT
        elif new_direction == 'right' and self.direction != LEFT:
            self.direction = RIGHT
        elif new_direction == 'up' and self.direction != DOWN:
            self.direction = UP
        elif new_direction == 'down' and self.direction != UP:
            self.direction = DOWN


class PowerUp:
    def __init__(self):
        # This goes on to load the image which I have picked for the power-up and scale it to the size of a single box
        self.image = pygame.image.load('power_up.png')
        self.image = pygame.transform.scale(self.image, (SPACE_SIZE, SPACE_SIZE))
        self.randomize_position()  # This will go on to randomly place the power-up on the board even on the snake

    def randomize_position(self):
        # This is the function where it randomly selects a position in the game grid, while ensuring it's within bounds
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(1, ((GAME_HEIGHT - 50) // SPACE_SIZE) - 1) * SPACE_SIZE

    def draw(self, screen):
        # This will go on to draw the power-up at its current position on the screen
        screen.blit(self.image, (self.x, self.y))


class Food:
    def __init__(self):
        self.randomize_position()  # This will go on to randomly place the food within the board whenever it's created

    def randomize_position(self):
        # This will go on to randomly select a position within the game bored, ensuring it is within the bounds
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(1, ((GAME_HEIGHT - 50) // SPACE_SIZE) - 1) * SPACE_SIZE

    def draw(self, screen):
        # This goes on to draw the food slightly smaller and offset creating a very nice visual effect
        offset = 2  # Offset to shift the food to the right and down a little more to fit the box
        smaller_size = SPACE_SIZE - 1.5  # Making the food slightly smaller to fit insdie the box
        pygame.draw.rect(screen, FOOD_COLOR, (self.x + offset, self.y + offset, smaller_size, smaller_size), 0)


def check_collisions(snake, invincibility_mode):
    x, y = snake.coordinates[0]
    # If invincibility mode is turned off, then check if the snake's head has hit the wall
    if not invincibility_mode:
        if x < 0 or x >= GAME_WIDTH or y < 50 or y >= GAME_HEIGHT:
            return True
    # Check if the snake's head has gone on to collided with any part of its own body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over(screen, score):
    # This will go on to reset snake color and face image for a fresh start
    global SNAKE_COLOR
    SNAKE_COLOR = (0, 255, 0)
    global face_image
    face_image = pygame.image.load('Snake-Green.jpg')
    face_image = pygame.transform.scale(face_image, (SPACE_SIZE, SPACE_SIZE))

    # Clear the whole screen and display the "Game Over" message
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 70)
    text = font.render("You Died - Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

    # Display the player's score to end the game
    font = pygame.font.Font(None, 60)
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    score_rect = score_text.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2))
    screen.blit(score_text, score_rect)

    # Prompt the player an option to play again
    font = pygame.font.Font(None, 36)
    play_again_text = font.render("Press Space to Play Again", True, (255, 255, 255))
    play_again_rect = play_again_text.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50))
    screen.blit(play_again_text, play_again_rect)
    pygame.display.flip()

    # Wait for the users input to restart or even quit the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


def draw_snake_with_face(screen, snake, face_image):
    outline_thickness = 2  # This goes on to create a thick black outline around the snake
    for body_part in snake.coordinates[1:]:
        # Drawing the black outline around each body part for better visibility of  the snake
        pygame.draw.rect(screen, (0, 0, 0), (body_part[0] - outline_thickness, body_part[1] - outline_thickness,
                                             SPACE_SIZE + 2 * outline_thickness, SPACE_SIZE + 2 * outline_thickness))
        # Drawing the actual body parts on the screen
        pygame.draw.rect(screen, SNAKE_COLOR, (body_part[0], body_part[1], SPACE_SIZE, SPACE_SIZE))

    # Drawing the snake's head which will include a face image
    head_x, head_y = snake.coordinates[0]
    pygame.draw.rect(screen, (0, 0, 0), (head_x - outline_thickness, head_y - outline_thickness,
                                         SPACE_SIZE + 2 * outline_thickness, SPACE_SIZE + 2 * outline_thickness))
    screen.blit(face_image, (head_x, head_y))


def get_high_score():
    # This will go on to read the high score from a file, or even return 0 if the file doesn't exist or there's no score
    if not os.path.exists("high_score.txt"):
        return 0
    with open("high_score.txt", "r") as file:
        return int(file.read())


def save_high_score(high_score):
    # Saving the high score to a file
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))


def draw_grid(screen):
    # Drawing  the vertical and also horizontal grid lines to create the game board that snake will be played on
    for x in range(0, GAME_WIDTH, SPACE_SIZE):
        pygame.draw.line(screen, WHITE, (x, 50), (x, GAME_HEIGHT), 1)
    for y in range(50, GAME_HEIGHT, SPACE_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (GAME_WIDTH, y), 1)


def draw_border(screen):
    # Draw a border around the whole play area for better visuals
    pygame.draw.rect(screen, WHITE, (0, 50, GAME_WIDTH, GAME_HEIGHT - 50), 3)


invincibility_mode = False


def start_screen(screen, high_score):
    global invincibility_mode
    background_img = pygame.image.load('Snake-Green.jpg')
    background_img = pygame.transform.scale(background_img, (GAME_WIDTH, GAME_HEIGHT))
    screen.blit(background_img, (0, 0))
    button_width = 400
    button_height = 50
    button_color = (255, 0, 0)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Start Game", True, text_color)
    button_x = (GAME_WIDTH - button_width) // 2
    button_y = GAME_HEIGHT - 200
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, text_rect)

    instructions_text = font.render("Instructions", True, text_color)
    instructions_button_y = button_y + button_height + 20
    pygame.draw.rect(screen, button_color, (button_x, instructions_button_y, button_width, button_height))
    instructions_text_rect = instructions_text.get_rect(
        center=(button_x + button_width // 2, instructions_button_y + button_height // 2))
    screen.blit(instructions_text, instructions_text_rect)

    inv_button_text = font.render("Invincibility Mode: " + ("On" if invincibility_mode else "Off"), True, text_color)
    inv_button_y = instructions_button_y + button_height + 20
    pygame.draw.rect(screen, button_color, (button_x, inv_button_y, button_width, button_height))
    inv_text_rect = inv_button_text.get_rect(
        center=(button_x + button_width // 2, inv_button_y + button_height // 2))
    screen.blit(inv_button_text, inv_text_rect)

    high_score_text = font.render(f"High Score: {high_score}", True, text_color)
    high_score_rect = high_score_text.get_rect(center=(GAME_WIDTH // 2, 100))
    screen.blit(high_score_text, high_score_rect)
    pygame.display.flip()

    # This is the main loop for the start screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Start Game button was clicked
                if button_x <= event.pos[0] <= button_x + button_width and \
                        button_y <= event.pos[1] <= button_y + button_height:
                    return True
                # Check if the Instructions button was clicked
                elif button_x <= event.pos[0] <= button_x + button_width and \
                        instructions_button_y <= event.pos[1] <= instructions_button_y + button_height:
                    show_instructions(screen)
                    return True
                # Check if the Invincibility Mode button was clicked
                elif button_x <= event.pos[0] <= button_x + button_width and \
                        inv_button_y <= event.pos[1] <= inv_button_y + button_height:
                    invincibility_mode = not invincibility_mode  # Toggle the mode
                    inv_button_text = font.render("Invincibility Mode: " + ("On" if invincibility_mode else "Off"),
                                                  True, text_color)
                    screen.fill(BACKGROUND_COLOR, (button_x, inv_button_y, button_width, button_height))  # Clear the area behind the button
                    pygame.draw.rect(screen, button_color, (button_x, inv_button_y, button_width, button_height))  # Redraw the button
                    screen.blit(inv_button_text, inv_text_rect)
                    pygame.display.flip()




def show_instructions(screen):
    # Display the instructions for the game
    instructions = [
        "Instructions:",
        "1. Use arrow keys to move the snake.",
        "2. Eat food to grow and increase your score.",
        "3. Avoid colliding with walls and yourself.",
        "4. Collect power-ups for extra points.",
        "5. Press 'Q' to end the game.",
        "6. Invincibility Mode makes you teleport through walls.",
        "",
        "Press 'B' to go back to the main menu."
    ]
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 36)
    y_offset = 50
    # Rendering and also displaying all the instruction lines
    for line in instructions:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(GAME_WIDTH // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 40
    pygame.display.flip()

    # The Main loop for the instructions screen to enter and exit the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    start_screen(screen, high_score)
                    return  # Exiting the function and then returning to the main menu


def level_two(screen, snake, face_image):
    # Changing the snakes color and also the face image for level two
    global SNAKE_COLOR
    SNAKE_COLOR = (255, 0, 0)
    face_image = pygame.image.load('Snake-Red.jpg')
    face_image = pygame.transform.scale(face_image, (SPACE_SIZE, SPACE_SIZE))
    speed = 12  # Increasing the speed for level two
    return speed, snake, face_image


# Initialize the game screen
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Snake Game")

# Loading the snake with the face image
face_image = pygame.image.load('Snake-Green.jpg')
face_image = pygame.transform.scale(face_image, (SPACE_SIZE, SPACE_SIZE))

# Initialize the power-up, high score, and start screen
power_up = PowerUp()
high_score = get_high_score()
start_screen(screen, high_score)

# Initialize the snake, food, and game variables
snake = Snake()
food = Food()
clock = pygame.time.Clock()
score = 0
running = True
level = 1
speed = SPEED

# The Main game loop where the whole games runs off of
while running:
    #This is accounting for all the user inputs which are valid such as the movement keys and quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Handling the direction changes
            if event.key == pygame.K_UP:
                snake.change_direction('up')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('down')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('left')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('right')
            elif event.key == pygame.K_q:
                # Handling the game quit
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                if game_over(screen, score):
                    start_screen(screen, high_score)
                    snake = Snake()
                    food = Food()
                    power_up = PowerUp()
                    score = 0
                    level = 1
                    speed = SPEED

    # Move the snake and also check for food or even any power-up collection
    snake.move(invincibility_mode)

    if snake.coordinates[0][0] == food.x and snake.coordinates[0][1] == food.y:
        score += 1
        food.randomize_position()
    elif snake.coordinates[0][0] == power_up.x and snake.coordinates[0][1] == power_up.y:
        score += 2
        power_up.randomize_position()
    else:
        snake.coordinates.pop()

    # Drawing the game elements to the screen
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)  # Drawing the grid to the screen
    draw_border(screen)  # Drawing the border to the screen
    pygame.draw.rect(screen, WHITE, (0, 0, GAME_WIDTH, 50))
    font = pygame.font.Font(None, 36)
    level_text = font.render(f"Level {level}", True, FONT_COLOR)
    level_rect = level_text.get_rect(topleft=(10, 10))
    screen.blit(level_text, level_rect)
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    score_rect = score_text.get_rect(topright=(GAME_WIDTH - 10, 10))
    screen.blit(score_text, score_rect)

    draw_snake_with_face(screen, snake, face_image)
    food.draw(screen)
    power_up.draw(screen)

    # Check for collisions and also handle game over
    if check_collisions(snake, invincibility_mode):
        if not invincibility_mode:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            if game_over(screen, score):
                start_screen(screen, high_score)
                snake = Snake()
                food = Food()
                power_up = PowerUp()
                score = 0
                level = 1
                speed = SPEED
            else:
                running = False

    # How the Level up progression logic works you need 8 points to get to the next level
    if score >= 8:
        level = 2
        speed, snake, face_image = level_two(screen, snake, face_image)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()




