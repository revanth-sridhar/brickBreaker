"""
File: brickbreaker.py
----------------
In this program (i.e., Breakout game), a layer of bricks lines the top third of the screen and the goal is to destroy
them all. A ball moves straight around the screen, bouncing off the top and two sides of the screen.
When a brick is hit, the ball bounces back and the brick is destroyed. The player loses a turn when the
ball touches the bottom of the screen; to prevent this from happening, the player has a horizontally movable paddle
to bounce the ball upward, keeping it in play.
"""

import tkinter
import time
import random

# How big is the playing area?
CANVAS_WIDTH = 500      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 680     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 5             # How many rows of bricks are there?
N_COLS = 10              # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING) / N_COLS  # ~55

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80

# Determines the maximum number of lives
N_ROUNDS = 2


def main():
    """
    This method builds the canvas required for the player to play the brick breaker game. It set's up the
    required condition to play the game. Eventually it determines whether the player won the game or
    lost the game!
    """
    counter = True
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    r_bricks = draw_bricks(canvas)
    paddle = draw_paddle(canvas)
    play_game(canvas, paddle, counter, r_bricks)


def play_game(canvas, paddle, counter, r_bricks):
    """
    play_game method allows the user to play the brick breaker game for N_ROUNDS time and it determines whether
    the player destroyed all the bricks in the canvas.
    """
    for i in range(N_ROUNDS):
        ball = draw_ball(canvas)
        move_ball(canvas, ball, paddle, counter, r_bricks)

        # checks whether all the bricks are destroyed
        if len(r_bricks) == 0 and i <= N_ROUNDS:
            canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text='YOU WIN!', font='Helvetica 20')
            break
        elif len(r_bricks) > 0 and i == N_ROUNDS-1:
            canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text='YOU LOST!', font='Helvetica 20')
    canvas.mainloop()


def move_ball(canvas, ball, paddle, counter, r_bricks):
    """
    A moving paddle is used to set it's movement relative to the movement of the cursor.
    This method allows the ball to move around the canvas and it bounces differently based on where it
    hits on the canvas.
    """
    change_x = 10
    change_y = 10
    while counter:
        # mouse_x receives the co-ordinates of the mouse relative to our screen
        mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx() - PADDLE_WIDTH/2
        # moves the paddle within the canvas (x-axis changes, y-axis remains constant)
        canvas.moveto(paddle, min(max(mouse_x, 0), CANVAS_WIDTH-PADDLE_WIDTH), PADDLE_Y)
        # keeps moving the ball with the canvas
        canvas.move(ball, change_x, change_y)

        # depending on where the ball had hit, the direction of ball movement is changed
        if hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):
            change_x *= -1
        if hit_top_wall(canvas, ball):
            change_y *= -1
        if hit_brick(canvas, ball, paddle, r_bricks):
            change_y *= -1
            if len(r_bricks) == 0:  # exit the loop if all the bricks are destroyed
                break
        if hit_bottom_wall(canvas, ball):
            counter = False
            canvas.delete(ball)     # one life is lost, if the ball hits the bottom wall
        canvas.update()
        time.sleep(1 / 30)


def hit_brick(canvas, ball, paddle, r_bricks):
    """
    Identifies whether the ball had hit the bricks at the top of the canvas.
    If hit, then the number remaining bricks is reduced accordingly.
    or if the ball hits the paddle, returns that it had hit the paddle.
    """
    # this graphics method gets the location of the ball as a list
    ball_coords = canvas.coords(ball)
    # the list has four elements:
    x0 = ball_coords[0]
    y0 = ball_coords[1]
    x1 = ball_coords[2]
    y1 = ball_coords[3]
    # find_overlapping method determines whether there are two colliding objects
    colliding_list = canvas.find_overlapping(x0, y0, x1, y1)

    # determines where the ball the hit (i.e., paddle, bricks)
    for item in colliding_list:
        if item == paddle:
            return len(colliding_list) > 1
        if item != paddle and item != ball:
            r_bricks.remove(item)   # removes the brick-hit from the r_bricks list
            canvas.delete(item)     # deletes the brick from the canvas
            return len(colliding_list) > 1
    return len(colliding_list) > 1


def hit_bottom_wall(canvas, ball):
    """
    Identifies whether the ball had hit the bottom-wall
    """
    ball_top_y = get_top_y(canvas, ball)
    return ball_top_y > CANVAS_HEIGHT - BALL_SIZE


def hit_top_wall(canvas, ball):
    """
    Identifies whether the ball had hit the top-wall
    """
    ball_top_y = get_top_y(canvas, ball)
    return ball_top_y <= 0


def hit_left_wall(canvas, ball):
    """
    Identifies whether the ball had hit the left-wall
    """
    ball_left_x = get_left_x(canvas, ball)
    return ball_left_x <= 0


def hit_right_wall(canvas, ball):
    """
    Identifies whether the ball had hit the right-wall
    """
    ball_left_x = get_left_x(canvas, ball)
    return ball_left_x > CANVAS_WIDTH - BALL_SIZE


def draw_paddle(canvas):
    """
    Draws a paddle close to the bottom of the screen
    """
    x0 = 0
    y0 = PADDLE_Y
    x1 = PADDLE_WIDTH
    y1 = PADDLE_Y + BRICK_HEIGHT
    return canvas.create_rectangle(x0, y0, x1, y1, fil='black')


def draw_ball(canvas):
    """
    Draws a ball at the center of the canvas
    """
    x0 = CANVAS_WIDTH/2 - BALL_SIZE/2
    y0 = CANVAS_HEIGHT/2 - BALL_SIZE/2
    x1 = CANVAS_WIDTH/2 + BALL_SIZE/2
    y1 = CANVAS_HEIGHT/2 + BALL_SIZE/2
    return canvas.create_oval(x0, y0, x1, y1, fil='black')


def draw_bricks(canvas):
    """
    This method builds the bricks(N_ROWS * N_COLUMNS) at the top of the canvas.
    calculates and returns the total number of bricks in the canvas.
    """
    # the below nested for loop is used to build the bricks at the top of the canvas
    for row in range(N_ROWS):
        for col in range(N_COLS):
            x0 = col * BRICK_WIDTH + (col+1) * SPACING
            y0 = row * (BRICK_HEIGHT + SPACING) + BRICK_START_Y
            x1 = x0 + BRICK_WIDTH
            y1 = y0 + BRICK_HEIGHT
            color = get_color(row)
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    # the below if..else condition, calculates the number of bricks
    r_bricks = list(range(1, N_ROWS * N_COLS + 1))
    return r_bricks


def get_color(row):
    """
    get_color returns the color depending on the row number
    """
    if row == 0 or row == 1:
        return 'red'
    elif row == 2 or row == 3:
        return 'orange'
    elif row == 4 or row == 5:
        return 'yellow'
    elif row == 6 or row == 7:
        return 'light green'
    elif row == 8 or row == 9:
        return 'cyan'


def get_top_y(canvas, object):
    """
    This method returns the y coordinate of the top of an object.
    canvas.coords(object) returns a list of the object bounding box: [x_1, y_1, x_2, y_2].
    The element at index 1 is the top-y
    """
    return canvas.coords(object)[1]


def get_left_x(canvas, object):
    """
    This method returns the x coordinate of the left of an object.
    canvas.coords(object) returns a list of the object bounding box: [x_1, y_1, x_2, y_2].
    The element at index 0 is the left-x
    """
    return canvas.coords(object)[0]


def make_canvas(width, height, title):
    """
    Creates and returns a drawing canvas of the given int size (width*height), ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    # canvas.bind("<Motion>", mouse_moved)
    return canvas


def mouse_moved(event):
    """
    This method prints the x and y coordinate of the mouse relative to screen.
    """
    print('x = ' + str(event.x), 'y = ' + str(event.y))


if __name__ == '__main__':
    main()
