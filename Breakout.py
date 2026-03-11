######################################################################
# Name: Michael Cotten 
# Collaborators (if any): Dr. Michael Vignal
# Section leader's name: Marnie
# List of extensions made (if any): inelastic collisions (energy loss), gravity, pinball launching mechanic on click or keypress, varying send angles based on paddle collision location, easter egg by clicking the lose message
######################################################################

"""
This program (once you have finished it) implements the Breakout game
"""

from pgl import GWindow, GOval, GRect, GLabel
import random
import math

# Constants
GWINDOW_WIDTH = int(800/1.66666667)     # Width of the graphics window      # 360
GWINDOW_HEIGHT = 800                    # Height of the graphics window     # 600
N_ROWS = 10                             # Number of brick rows
N_COLS = 10                             # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1              # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 1             # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3           # Ratio of brick to paddle width
BRICK_SEP = 4                           # Separation between bricks (in pixels)
TOP_FRACTION = 0.1                      # Fraction of window above bricks
BOTTOM_FRACTION = 0.05                  # Fraction of window below paddle
N_BALLS = 5                             # Number of balls (lives) in a game
TIME_STEP = 10                          # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0                # Starting y velocity downwards
MIN_X_VELOCITY = 1.0                    # Minimum random x velocity
MAX_X_VELOCITY = 3.0                    # Maximum random x velocity
SPEED_LIMIT = 18                        # Velocity limit constant
ENERGY_LOSS = 0.75                      # Velocity loss constant for inelastic collisions

# Derived Constants
BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_DIAMETER = BRICK_WIDTH / BRICK_TO_BALL_RATIO


# Function: breakout
def breakout():
    """The main program for the Breakout game."""
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)


    '''BRICK STUFF'''
    gw.totalBricks=0
    for row in range(N_ROWS):
        for col in range(N_COLS):
            topLeftX = (GWINDOW_WIDTH-(((BRICK_WIDTH+BRICK_SEP)*N_COLS)-BRICK_SEP))/2
            topLeftY = TOP_FRACTION*GWINDOW_HEIGHT
            brick = GRect(topLeftX + (BRICK_WIDTH + BRICK_SEP)*col, 
                            topLeftY + (BRICK_HEIGHT + BRICK_SEP)*row, 
                            BRICK_WIDTH, BRICK_HEIGHT)
            
            colors = ["Red","Orange","Green","Cyan","Blue"]
            brick.set_color(colors[row%5])
            brick.set_fill_color(colors[row%5])
            brick.set_filled(True)
            gw.add(brick)
            gw.totalBricks+=1
    
    #testing only (easy win):
    # gw.add(GRect(GWINDOW_WIDTH/2 - BRICK_WIDTH/2,TOP_FRACTION*GWINDOW_HEIGHT,BRICK_WIDTH,BRICK_HEIGHT))
    # gw.totalBricks+=1


    '''PADDLE STUFF'''
    def mousemove_function(event): # this moves the paddle
        mx = event.get_x()
        if mx<PADDLE_WIDTH/2:
            mx += PADDLE_WIDTH/2 - mx
        if mx>GWINDOW_WIDTH-PADDLE_WIDTH/2:
            mx -= PADDLE_WIDTH/2 - (GWINDOW_WIDTH-mx) + 1
        paddle.set_location(mx-PADDLE_WIDTH/2,paddle.get_y())
        
    paddle = GRect(GWINDOW_WIDTH/2-PADDLE_WIDTH/2,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
    gw.add(paddle)
    gw.add_event_listener("mousemove", mousemove_function)


    '''BALL STUFF'''
    ball = GOval(GWINDOW_WIDTH/2-BALL_DIAMETER/2, PADDLE_Y-GWINDOW_HEIGHT/3, BALL_DIAMETER, BALL_DIAMETER)
    ball.set_color("PURPLE")
    ball.set_fill_color("PURPLE")
    ball.set_filled(True)
    gw.add(ball)
    gw.vy, gw.vx = 3.0, random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
    if random.uniform(0,1) < 0.5:
        gw.vx = -gw.vx
    ball.send_to_back()

    #label easter egg stuff
    loseLabel = GLabel("")
    loseLabel.send_to_back()
    gw.following = False

    gw.hasLastChance = True
    gw.lives = N_BALLS
    gw.isMoving = False
    gw.whackTimer = 0
    gw.whackDuration = 20
    whacker_colors = ["#00FFD2","#35FFDB","#62FFE3","#84FFE9","#A6FFEF","#E0FFFF","#FFFFFF"]
    eachColorTime = (gw.whackDuration/len(whacker_colors))

    def redo():
        if gw.lives!=0:
            ball.set_location(GWINDOW_WIDTH/2-BALL_DIAMETER/2, PADDLE_Y-GWINDOW_HEIGHT/3)
            gw.vy, gw.vx = 3.0, random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
            if random.uniform(0,1) < 0.5:
                gw.vx = -gw.vx
        else:
            gw.remove(ball)
            gw.isMoving=False
            if gw.hasLastChance:
                ball.set_filled(False)
                ball.set_color("white")
                ball.set_visible(False)
                gw.add(ball)
                gw.vy, gw.vx = 3.0, random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
                if random.uniform(0,1) < 0.5:
                    gw.vx = -gw.vx
                ball.set_location(GWINDOW_WIDTH/2-BALL_DIAMETER/2, PADDLE_Y-GWINDOW_HEIGHT/3)

                loseLabel.set_label("LOST")
                loseLabel.set_location((ball.get_x()+BALL_DIAMETER/2)-loseLabel.get_width()/2, (ball.get_y()+BALL_DIAMETER/2)+loseLabel.get_height()/2)
                gw.add(loseLabel)
                loseLabel.send_to_back()
                gw.lives+=1
            gw.hasLastChance=False

    def input_for_click_or_key():
        if gw.hasLastChance:
            gw.isMoving = True
        if gw.whackTimer < gw.whackDuration:
            gw.whackTimer+= gw.whackDuration
    
    def click_function(event):
        #easter egg stuff:
        if gw.hasLastChance == False:
            input_for_click_or_key()
            mx = event.get_x()
            my = event.get_y()
            if loseLabel.contains(mx,my):
                gw.following = True
                gw.isMoving = True
        else:
            input_for_click_or_key()
    gw.add_event_listener("click",click_function)

    def key_function(event):
            if gw.hasLastChance:
                input_for_click_or_key()
            if gw.following:
                input_for_click_or_key()
    gw.add_event_listener("key",key_function)
    
    def get_colliding_object():
        if gw.get_element_at(ball.get_x()+BALL_DIAMETER, ball.get_y()) != None and gw.get_element_at(ball.get_x()+BALL_DIAMETER, ball.get_y()) != loseLabel:                 #quadrant 1
            return gw.get_element_at(ball.get_x()+BALL_DIAMETER, ball.get_y())
        elif gw.get_element_at(ball.get_x(), ball.get_y()) != None and gw.get_element_at(ball.get_x(), ball.get_y()) != loseLabel:                             #quadrant 2
            return gw.get_element_at(ball.get_x(), ball.get_y())
        elif gw.get_element_at(ball.get_x(), ball.get_y()+BALL_DIAMETER) != None and gw.get_element_at(ball.get_x(), ball.get_y()+BALL_DIAMETER) != loseLabel:               #quadrant 3
            return gw.get_element_at(ball.get_x(), ball.get_y()+BALL_DIAMETER)
        elif gw.get_element_at(ball.get_x()+BALL_DIAMETER, ball.get_y()+BALL_DIAMETER) != None and gw.get_element_at(ball.get_x()+BALL_DIAMETER, ball.get_y()+BALL_DIAMETER) != loseLabel: #quadrant 4
            return gw.get_element_at(ball.get_x()+BALL_DIAMETER, ball.get_y()+BALL_DIAMETER)

    def general_collision(hitSides):
        vMag = (((gw.vx)**2 + (gw.vy)**2)**0.5)
        theta = math.atan(gw.vy/gw.vx)
        vMag_new = vMag - ENERGY_LOSS
        vx_new = vMag_new*math.cos(theta)
        vy_new = vMag_new*math.sin(theta)
        #print(f"gw.vx: {gw.vx}\ngw.vy: {gw.vy}\nvy_new: {vy_new}\nvMag initial: {vMag}\nvMag final: {vMag_new}\ndistFromPadCenter: {distFromPadCenter}\npaddleFactor: {paddleFactor}\ntheta: {theta}\n")
        if (vx_new>0) != (gw.vx>0) and not hitSides: #stops x from switching directions
            vx_new = -vx_new
        if (vx_new>0) == (gw.vx>0) and hitSides: #guarantees x switches directions
            vx_new = -vx_new
        if (vy_new>0) != (gw.vy>0) and hitSides: #stops y from switching directions
            vy_new = -vy_new
        if (vy_new>0) == (gw.vy>0) and not hitSides: #guarantees y switches directions
            vy_new = -vy_new
        return vx_new, vy_new

    def step():
        if gw.isMoving and gw.lives>0:
            if gw.hasLastChance:
                ball.move(gw.vx,gw.vy)
            elif gw.following:
                ball.move(gw.vx,gw.vy)
            if loseLabel!=None and gw.following:
                loseLabel.set_location((ball.get_x()+BALL_DIAMETER/2)-loseLabel.get_width()/2, (ball.get_y()+BALL_DIAMETER/2)+loseLabel.get_height()/2)
            
            vMagCheckerBefore = round((((gw.vx)**2 + (gw.vy)**2)**0.5),3)
            if abs(gw.vx)>SPEED_LIMIT:       # speed limit on x
                if gw.vx>0:
                    gw.vx = SPEED_LIMIT
                else:
                    gw.vx = -SPEED_LIMIT
            if abs(gw.vy)>SPEED_LIMIT:       # speed limit on y
                if gw.vy>0:
                    gw.vy = SPEED_LIMIT
                else:
                    gw.vy = -SPEED_LIMIT
            vMagCheckerAfter = round((((gw.vx)**2 + (gw.vy)**2)**0.5),3)
            if vMagCheckerBefore!=vMagCheckerAfter:
                print(f"Init: {vMagCheckerBefore} Fin: {vMagCheckerAfter}")


            #checking for bounces off the wall
            if ball.get_x() + BALL_DIAMETER >= GWINDOW_WIDTH:  #right wall
                gw.vx, gw.vy = general_collision(True)
                gw.vx = -abs(gw.vx)
            if ball.get_x() <= 0:                              #left wall
                gw.vx, gw.vy = general_collision(True)
                gw.vx = abs(gw.vx)
            if ball.get_y() < 0:                               #top wall
                gw.vx, gw.vy = general_collision(False)
                gw.vy = abs(gw.vy)
            if ball.get_y() + BALL_DIAMETER > GWINDOW_HEIGHT:  #bottom wall
                gw.isMoving = False
                gw.lives-=1
                redo()

            collider = get_colliding_object()
            if collider==paddle and collider != loseLabel:
                #gw.vy = -abs(gw.vy)

                # vMag = (((gw.vx)**2 + (gw.vy)**2)**0.5)
                # distFromPadCenter=abs((paddle.get_x()+PADDLE_WIDTH/2)-(ball.get_x()+BALL_DIAMETER/2))
                # paddleFactor = 1 - distFromPadCenter/(PADDLE_WIDTH/2)

                # theta = math.atan(gw.vy/gw.vx)
                # vx_new = vMag*math.cos(theta*(paddleFactor+1)/1.5)
                # vy_new = -abs(vMag*math.sin(theta*(paddleFactor+1)/1.5))
                # vMag_new = (((vx_new)**2 + (vy_new)**2)**0.5)
                # print(f"gw.vx: {gw.vx}\ngw.vy: {gw.vy}\nvy_new: {vy_new}\nvMag initial: {vMag}\nvMag final: {vMag_new}\ndistFromPadCenter: {distFromPadCenter}\npaddleFactor: {paddleFactor}\ntheta: {theta}\n")

                # if (vx_new>0) != (gw.vx>0):
                #     vx_new = vx_new*(-1)

                # gw.vx = vx_new
                # gw.vy = vy_new

                distFromPadCenter = abs((paddle.get_x()+PADDLE_WIDTH/2)-(ball.get_x()+BALL_DIAMETER/2))
                paddleFactor = distFromPadCenter/(PADDLE_WIDTH/2)
                b = 1 - paddleFactor
                c = 0.2*b + 0.25

                vMag = (((gw.vx)**2 + (gw.vy)**2)**0.5)
                vMag_new = vMag - ENERGY_LOSS
                vx_new = vMag_new*math.cos(math.pi*c)
                vy_new = -abs(vMag_new*math.sin(math.pi*c))
                #print(f"gw.vx: {gw.vx}\ngw.vy: {gw.vy}\nvy_new: {vy_new}\nvMag initial: {vMag}\nvMag final: {vMag_new}\ndistFromPadCenter: {distFromPadCenter}\npaddleFactor: {paddleFactor}\ntheta: {theta}\n")
                if (vx_new>0) != (gw.vx>0):
                    vx_new = -vx_new

                gw.vx = vx_new
                gw.vy = vy_new

                if gw.whackTimer > 0:
                    gw.vy = -abs(abs(gw.vy) + 7)

            elif collider != None and collider != loseLabel:
                #gw.vy = -gw.vy
                gw.vx, gw.vy = general_collision(False)
                gw.remove(collider)
                gw.totalBricks-=1
            
            #gravity
            if gw.isMoving:
                gw.vy = gw.vy + 0.1

        #winning
        if gw.totalBricks==0:
            gw.vx, gw.vy = 0,0
            winLabel= GLabel("WON")
            winLabel.set_location(GWINDOW_WIDTH/2-winLabel.get_width()/2, PADDLE_Y-GWINDOW_HEIGHT/3)
            gw.add(winLabel)
            loseLabel.set_label("WON")

        #whacker
        if gw.whackTimer > gw.whackDuration:
            gw.whackTimer = gw.whackDuration
        if gw.whackTimer > 0:
            # paddle.set_color("#ADD8E6")
            # paddle.set_fill_color("#ADD8E6")    # you could make it so whacking sets the color to brightest possible and then you fade out over time
            # paddle.set_filled(True)             # you could also add a trail to the ball after getting hit by the whacker that fades over time using more balls but that would be so hard
            # gw.whackTimer = gw.whackTimer - 2

            chunk = int(gw.whackTimer / eachColorTime) #should be 6,5,4,3,2,1,0
            if chunk==7: chunk=6
            paddle.set_color(whacker_colors[chunk])
            paddle.set_fill_color(whacker_colors[chunk])
            paddle.set_filled(True)
            gw.whackTimer = gw.whackTimer - 2
        else:
            paddle.set_color("black")
            paddle.set_filled(False)

    timer = gw.set_interval(step, 10)


# Startup code
if __name__ == "__main__":
    breakout()
