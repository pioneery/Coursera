# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2 , HEIGHT/2]
    x = random.randrange(120,240) /float(100)
    y = random.randrange(60,180)  /float(100) 
    if direction == RIGHT:
        ball_vel = [x, -y]
    elif direction == LEFT:
        ball_vel = [-x,-y]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #bounce top and bottom
    if ball_pos[1] > HEIGHT - BALL_RADIUS or ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # determine whether paddle and ball collide 
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and \
       paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = 1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH and \
       paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = 1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
    elif ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
        spawn_ball(RIGHT)
        score2 += 1
    elif ball_pos[0] > WIDTH - BALL_RADIUS - PAD_WIDTH:
        spawn_ball(LEFT)
        score1 += 1
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS,1,'green','green')
    
    # update paddle's vertical position, keep paddle on the screen
    if HALF_PAD_HEIGHT <= paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
        
    if HALF_PAD_HEIGHT <= paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),\
               (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT),PAD_WIDTH , 'yellow')
    canvas.draw_line((WIDTH- HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT),\
        (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT),PAD_WIDTH , 'yellow')   
    
    # draw scores
    canvas.draw_text(str(score1), (200, 100), 40, 'pink')
    canvas.draw_text(str(score2), (380, 100), 40, 'pink')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == "W":
        if paddle1_pos > HALF_PAD_HEIGHT:
            paddle1_vel += -5   
    elif chr(key) == "S":
        if paddle1_pos < HEIGHT - HALF_PAD_HEIGHT:
            paddle1_vel += 5
    elif chr(key) == "&":
        if paddle2_pos > HALF_PAD_HEIGHT:
            paddle2_vel += -5
    elif chr(key) == "(":
        if paddle2_pos < HEIGHT - HALF_PAD_HEIGHT:
            paddle2_vel += 5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart = frame.add_button('Restart', new_game)


# start frame
new_game()
frame.start()
