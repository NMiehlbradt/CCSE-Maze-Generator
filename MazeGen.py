
import pgzrun
from itertools import product

TITLE = "Maze Generator"

# Set the dimensions of the window
WIDTH = 500
HEIGHT = 500

# Set the dimensions of a single square
square_size = 20

# The minimum padding around the edges of the maze
# Might be more to center it
padding = 10

# Calculates the number of squares across and down that can fit
squares_x = (WIDTH - 2 * padding) // square_size
squares_y = (HEIGHT - 2 * padding) // square_size

# The set that stores the walls of the maze
# Walls are represented as a frozen set containing the coordinates of the square the walls separate
# Don't interact with this directly, use the provided functions below to add/remove walls
walls = set()
# Set this to true if you want to start with all walls generated
generate_walls_at_start = False


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
        add_single_wall([square, (x + dx, y + dy)])


def add_single_wall(wall):
    """
    Adds a specific wall to the wall set, does not add it again if it already exists
    :param wall: The wall, represented as a pair of coordinates of adjacent squares
    :return:
    """
    (x1, y1), (x2, y2) = wall
    # Ignore walls where cells are not adjacent
    if abs(x1 - x2) + abs(y1 - y2) != 1:
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


# TODO: Put maze gen functions here

def update():
    # TODO: Put code you want to run every frame here
    pass


def draw():
    # Clear the background to white
    screen.fill((255, 255, 255))
    # Draw the walls
    draw_walls()


# TODO: Put code you want to run at startup here

# Generates walls if necessary then starts the window
if generate_walls_at_start:
    generate_all_walls()
pgzrun.go()
