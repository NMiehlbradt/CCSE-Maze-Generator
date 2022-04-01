
import pgzrun
import random
from itertools import product
from pgzero import keyboard
from pgzero.rect import Rect
from collections import deque

TITLE = "Maze Generator"

# Set the dimensions of the window
WIDTH = 500
HEIGHT = 500

# Set the dimensions of a single square
square_size = 40

# The minimum padding around the edges of the maze
# Might be more to center it
padding = 10

# Calculates the number of squares across and down that can fit
squares_x = (WIDTH - 2*padding) // square_size
squares_y = (HEIGHT - 2*padding) // square_size

# The set that stores the walls of the maze
# Walls are represented as a frozen set containing the coordinates of the square the walls separate
# Don't interact with this directly, use the provided functions below to add/remove walls
walls = set()
# Set this to true if you want to start with all walls generated
generate_walls_at_start = True


def generate_all_walls():
    """
    Generates all the walls in the grid and adds them to the wall set
    Includes the boundary walls
    :return:
    """
    for square in product(range(squares_x), range(squares_y)):
        add_square_walls(square)


def add_square_walls(square):
    """
    Adds all the walls around the specified square to the wall set
    :param square: A pair representing the coordinates of the square
    :return:
    """
    x, y = square
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        add_single_wall([square, (x+dx, y+dy)])


def add_single_wall(wall):
    """
    Adds a specific wall to the wall set, does not add it again if it already exists
    :param wall: The wall, represented as a pair of coordinates of adjacent squares
    :return:
    """
    (x1, y1), (x2, y2) = wall
    if abs(x1-x2) + abs(y1-y2) != 1:
        return
    walls.add(frozenset(wall))


def remove_single_wall(wall):
    """
    Removes the specified wall if it exists, otherwise does nothing
    :param wall: The wall to remove
    :return:
    """
    walls.remove(frozenset(wall))


def get_surrounding_walls(square):
    """
    Gets a list of all existing walls around a specified square from the wall set
    :param square: The coordinates of the square as a pair
    :return: The list of surrounding walls
    """
    return list(filter(lambda x: square in x, walls))


def draw_walls():
    """
    Draws the walls in the wall set to the screen
    :return:
    """
    off_x = (WIDTH - square_size * squares_x) / 2
    off_y = (HEIGHT - square_size * squares_y) / 2
    for (x1, y1), (x2, y2) in walls:
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        screen.draw.line((x_max * square_size + off_x, y_max * square_size + off_y),  # Start point of line
                         ((x_max + dy) * square_size + off_x, (y_max + dx) * square_size + off_y),  # End point of line
                         (0, 0, 0))  # Colour of line


def is_in_bounds(pt):
    x, y = pt
    return 0 <= x < squares_x and 0 <= y < squares_y


def get_adjacent_squares(square):
    x, y = square
    return list(filter(is_in_bounds, [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]))


def get_adjacent_not_connected(square):
    return list(filter(lambda x: len(get_surrounding_walls(x)) == 4, get_adjacent_squares(square)))


stack = deque()
stack.append((0, 0))


def gen_maze_step():
    global stack
    if len(stack) == 0:
        return False
    head = stack[-1]
    possible_next = get_adjacent_not_connected(head)
    if len(possible_next) == 0:
        stack.pop()
    else:
        next = random.choice(possible_next)
        remove_single_wall([head, next])
        stack.append(next)
    if len(stack) == 0:
        print("Done")
    return True


def reset():
    global stack
    walls.clear()
    generate_all_walls()
    stack = deque([(0, 0)])


def gen_maze():
    reset()
    while gen_maze_step():
        pass


do_reset = False
do_gen = False
running = True
draw_trail = False
step = False


def update():
    global do_reset, do_gen, running, step
    if do_reset:
        reset()
        do_reset = False
    if do_gen:
        gen_maze()
        do_gen = False
    if running:
        gen_maze_step()
    elif step:
        gen_maze_step()
        step = False


def draw():
    global draw_trail
    # Clear the background to white
    screen.fill((255, 255, 255))
    # Draw the walls
    if draw_trail and len(stack) > 0:
        off_x = (WIDTH - square_size * squares_x) / 2
        off_y = (HEIGHT - square_size * squares_y) / 2
        for x, y in stack:
            screen.draw.filled_rect(Rect((x*square_size+off_x, y*square_size+off_y), (square_size, square_size)), (0, 200, 0))
        x, y = stack[-1]
        screen.draw.filled_rect(Rect((x * square_size + off_x, y * square_size + off_y), (square_size, square_size)),
                                (255, 255, 0))
    draw_walls()


def on_key_down(key):
    global do_reset, do_gen, running, draw_trail, step
    if key is keyboard.keys.R:
        do_reset = True
    if key is keyboard.keys.G:
        do_gen = True
    if key is keyboard.keys.P:
        running = not running
    if key is keyboard.keys.D:
        draw_trail = not draw_trail
    if key is keyboard.keys.S:
        step = True


# Put code you want to run at startup here

# Generates walls if necessary then starts the window
if generate_walls_at_start:
    generate_all_walls()
pgzrun.go()
