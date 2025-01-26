import pygame
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Pin Definitions
left_pin = 29
right_pin = 31
down_pin = 38
rotate_pin = 35
select_pin = 33
start_pin = 40

# Set up the GPIO pins
GPIO.setup(left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rotate_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(select_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to check GPIO pins state
def check_gpio():
    left = not GPIO.input(left_pin)
    right = not GPIO.input(right_pin)
    down = not GPIO.input(down_pin)
    rotate = not GPIO.input(rotate_pin)
    select = not GPIO.input(select_pin)
    start = not GPIO.input(start_pin)

    return left, right, down, rotate, select, start

# Function to save the high score
def save_high_score(score):
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0

    if score > high_score:
        with open("high_score.txt", "w") as file:
            file.write(str(score))

# Function to retrieve the high score
def get_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to calculate the ghost piece
def get_ghost_piece(current_piece, grid):
    ghost_piece = Piece(current_piece.x, current_piece.y, current_piece.shape)
    ghost_piece.rotation = current_piece.rotation

    while valid_space(ghost_piece, grid):
        ghost_piece.y += 1
    ghost_piece.y -= 1  # Step back to the last valid position

    return ghost_piece

def draw_ghost_piece(ghost_piece, surface):
    shape_pos = convert_shape_format(ghost_piece)

    # Make the ghost piece more visible by using a bright color and adding a glow
    ghost_color = (255, 255, 255, 100)  # Semi-transparent white color for the ghost piece
    glow_color = (255, 255, 255, 200)  # Slightly stronger glow around the ghost piece

    for x, y in shape_pos:
        if y > -1:
            # Glow effect for the ghost piece (outline effect)
            pygame.draw.rect(
                surface,
                glow_color,  # Glow effect around the ghost piece
                (top_left_x + x * block_size - 2, top_left_y + y * block_size - 2, block_size + 4, block_size + 4),
                border_radius=5
            )
            # Draw the main ghost piece with higher opacity
            pygame.draw.rect(
                surface,
                ghost_color,  # Main color for the ghost piece
                (top_left_x + x * block_size, top_left_y + y * block_size, block_size, block_size),
                border_radius=5
            )

# Pygame initialization
pygame.font.init()
#pygame.mixer.init()

# Screen dimensions and configurations
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

# Tetromino shapes
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece:
    rows = 20
    columns = 10

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# Create grid
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))

def clear_rows(grid, locked):
    global particles
    inc = 0
    full_rows = []

    for i in range(len(grid)):
        if (0, 0, 0) not in grid[i]:
            full_rows.append(i)

    for row in full_rows:
        inc += 1
        for col in range(len(grid[row])):
            particles.append(
                Particle(top_left_x + col * block_size + block_size // 2,
                         top_left_y + row * block_size + block_size // 2, (255, 255, 255))
            )
            try:
                del locked[(col, row)]
            except KeyError:
                continue

    if full_rows:
        full_rows.sort(reverse=True)
        new_locked = {}

        for (x, y), color in locked.items():
            shift = 0
            for row in full_rows:
                if y < row:
                    shift += 1
            new_locked[(x, y + shift)] = color

        locked.clear()
        locked.update(new_locked)

    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next:', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

def interpolate_color(color1, color2, t):
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )

def draw_window(surface, grid, score=0, high_score=0, current_piece=None, time_elapsed=0):
    # Dynamic Background Color
    base_color = (0, 0, 50)
    highlight_color = (50, 0, 100)
    t = (time_elapsed % 1000) / 1000
    background_color = interpolate_color(base_color, highlight_color, t)
    surface.fill(background_color)

    pygame.draw.rect(surface, (0, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_text_middle(f"Score: {score}", 30, (255, 255, 255), surface)
    draw_text_middle(f"High Score: {high_score}", 30, (255, 255, 255), surface)

# Main game loop
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    paused = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    time_elapsed = 0
    score = 0
    high_score = get_high_score()

    fall_speed = 0.5
    fast_drop = False

    move_time = 0  # Timer for smooth movement
    move_delay = 150  # Delay in milliseconds

    # Tracking button states to avoid multiple actions on a single press
    button_state = {'left': False, 'right': False, 'down': False, 'rotate': False, 'select': False, 'start': False}

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        time_elapsed += clock.get_rawtime()
        move_time += clock.get_rawtime()
        clock.tick()

        if not paused:
            # Calculate ghost piece position
            ghost_piece = get_ghost_piece(current_piece, grid)

            fall_speed = max(0.2, 0.5 - (score // 100) * 0.05)
            current_fall_speed = fall_speed if not fast_drop else 0.03

            if fall_time / 1000 >= current_fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
                    change_piece = True

        left, right, down, rotate, select, start = check_gpio()

        # Check if the button is pressed and avoid multiple actions on long press
        if move_time > move_delay:
            if left and not button_state['left']:
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1
                button_state['left'] = True
                move_time = 0

            if right and not button_state['right']:
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
                button_state['right'] = True
                move_time = 0

            if down:
                fast_drop = True
            else:
                fast_drop = False

            if rotate and not button_state['rotate']:
                target_rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                current_piece.rotation = target_rotation
                if not valid_space(current_piece, grid):
                    current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                button_state['rotate'] = True

            if select and not button_state['select']:
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1
                change_piece = True
                button_state['select'] = True

            if start and not button_state['start']:
                paused = not paused
                button_state['start'] = True

        # Reset button states after they are released
        if not left:
            button_state['left'] = False
        if not right:
            button_state['right'] = False
        if not rotate:
            button_state['rotate'] = False
        if not select:
            button_state['select'] = False
        if not start:
            button_state['start'] = False

        if not paused:
            shape_pos = convert_shape_format(current_piece)
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False
                score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, high_score, current_piece, time_elapsed)
        draw_ghost_piece(ghost_piece, win)  # Render the ghost piece
        draw_next_shape(next_piece, win)

        if paused:
            draw_text_middle("Paused", 60, (255, 255, 255), win)

        pygame.display.update()

        if check_lost(locked_positions):
            save_high_score(score)
            draw_text_middle("Try Again", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(3000)
            run = False

# Start the game
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

if __name__ == "__main__":
    main()
