"""
Team Name: Triple T
Team Members: Kaiwen Chen, Anthony Xenos 
Last Edited: 6/7/2026

Brief description:
This is of the basic,non official version of the project. This was before AI corrected some mistakes and condensed some other things. This is of the full game logic like the main.py file.

Expanded description:
The robot uses a 3x3 grid of sensors to detect the player's moves. This grid is represented with coordinated, to help locate the distances from one sensor to another. Once the sensor has been activated, the robot will use the stepper motors to move a claw to pick up and place pieces on the board. The game logic includes a simple algorithm that will try to win if it can, block the player's winning move, or choose a strategic position otherwise. The main loop alternates between the player's turn and the robot's turn until there is a winner or a draw.

Citations:

AI Use & Logic Disclosure:
    - Tool: OpenAI ChatGPT (GPT-4o Model, Feb 2026 Version)
    - Transcript file: https://chatgpt.com/share/6a07a052-10a8-83ea-95a1-a534b02fd220
    - Scope: The game logic was made by AI. It follows a simple checklist type of function which is super easy to code, but regardless, AI was use.
"""

from machine import Pin
import time
import random



#THE BOARD:
#1     2     3
#4     5     6
#7     8     9

# Set up the sensor pins, 1-9
SS1= Pin(16, Pin.IN, Pin.PULL_DOWN)
SS2= Pin(17, Pin.IN, Pin.PULL_DOWN)
SS3= Pin(18, Pin.IN, Pin.PULL_DOWN)
SS4= Pin(19, Pin.IN, Pin.PULL_DOWN)
SS5= Pin(20, Pin.IN, Pin.PULL_DOWN)
SS6= Pin(21, Pin.IN, Pin.PULL_DOWN)
SS7= Pin(26, Pin.IN, Pin.PULL_DOWN)
SS8= Pin(27, Pin.IN, Pin.PULL_DOWN)
SS9= Pin(28, Pin.IN, Pin.PULL_DOWN)
current_square=None


# List for all the winning combinations
win=[
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [1,4,7],
    [2,5,8],
    [3,6,9],
    [1,5,9],
    [3,5,7],
    ]

# A B C D on driver
Ax = Pin(0, Pin.OUT)
Bx = Pin(1, Pin.OUT)
Cx = Pin(2, Pin.OUT)
Dx = Pin(3, Pin.OUT)

Ay = Pin(8, Pin.OUT)
By = Pin(9, Pin.OUT)
Cy = Pin(10, Pin.OUT)
Dy = Pin(11, Pin.OUT)

# Half-step sequence
step_sequence = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

SQR_x=0
SQR_y=0
initial=0
#This is the REALLY long, uncondense funciton which essentially detects what is the current square that the claw is on, and it goes to the new square
def MATRIX_SYSTEM(current_sqr, new_sqr):
    conversion= 1028/20.4 #1028 is one revolution, 20.4 is the distance in cm/revolution
    distance=5.5 #distance between squares (cm)
    #current square 1-9 is for when claw is on the board and needs to go back to the tic-tac-toe feeder.
    if current_sqr==1: #change to current square
        if new_sqr==initial:
            SRQ_x=distance*conversion
            SRQ_y=-distance*conversion*2.5
 

    if current_sqr==2: #change to current square
        if new_sqr==initial:
            SRQ_x=0
            SRQ_y=-distance*conversion*2.5
 

    if current_sqr==3: #change to current square
        if new_sqr==initial:
            SRQ_x=-distance*conversion
            SRQ_y=-distance*conversion*2.5

    if current_sqr==4: #change to current square
        if new_sqr==initial:
            SRQ_x=distance*conversion
            SRQ_y=-distance*conversion*1.5

    if current_sqr==5: #change to current square
        if new_sqr==initial:
            SRQ_x=0
            SRQ_y=-distance*conversion*1.5
        
    if current_sqr==6: #change to current square
        if new_sqr==initial:
            SRQ_x=-distance*conversion
            SRQ_y=-distance*conversion*1.5
            
    if current_sqr==7: #change to current square
        if new_sqr==initial:
            SRQ_x=distance*conversion
            SRQ_y=-distance*conversion*0.5
    
    if current_sqr==8: #change to current square
        if new_sqr==initial:
            SRQ_x=0
            SRQ_y=-distance*conversion*0.5
    if current_sqr==9: #change to current square
        if new_sqr==initial:
            SRQ_x=-distance*conversion
            SRQ_y=-distance*conversion*0.5

    #This is for when the claw is at the feeder and need to go to the board, so the coordinates are reversed.
    if current_sqr==initial:
        if new_sqr==1:
            SRQ_x=-distance*conversion
            SRQ_y=distance*conversion*2.5
        if new_sqr==2:
            SRQ_x=0
            SRQ_y=distance*conversion*2.5
        if new_sqr==3:
            SRQ_x=distance*conversion
            SRQ_y=distance*conversion*2.5
        if new_sqr==4:
            SRQ_x=-distance*conversion
            SRQ_y=distance*conversion*1.5
        if new_sqr==5:
            SRQ_x=0
            SRQ_y=distance*conversion*1.5
        if new_sqr==6:
            SRQ_x=distance*conversion
            SRQ_y=distance*conversion*1.5
        if new_sqr==7:
            SRQ_x=-distance*conversion
            SRQ_y=distance*conversion*0.5
        if new_sqr==8:
            SRQ_x=0
            SRQ_y=distance*conversion*0.5
        if new_sqr==9:
            SRQ_x=distance*conversion
            SRQ_y=distance*conversion*0.5
        if new_sqr==0:
            SRQ_x=0
            SRQ_y=0
    return SRQ_x, SRQ_y #They are calculate by taking the distance and converting them into steps. Then after multiplying based on how far away they are from the current square (This is a awful system but would theoretically work)


#The stepper motors only read in steps. This is for the motors to move forward or backwards. (both x and y axis)
def step_motor_x(steps, delay=0.001):
    for _ in range(int(steps)):
        for step in step_sequence:
            Ax.value(step[0])
            Bx.value(step[1])
            Cx.value(step[2])
            Dx.value(step[3])
            time.sleep(delay)

def step_motor_reverse_x(steps, delay=0.001):
    for _ in range(int(steps)):
        for step in reversed(step_sequence):
            Ax.value(step[0])
            Bx.value(step[1])
            Cx.value(step[2])
            Dx.value(step[3])
            time.sleep(delay)


def step_motor_y(steps, delay=0.001):
    for _ in range(int(steps)):
        for step in step_sequence:
            Ay.value(step[0])
            By.value(step[1])
            Cy.value(step[2])
            Dy.value(step[3])
            time.sleep(delay)

def step_motor_reverse_y(steps, delay=0.001):
    for _ in range(int(steps)):
        for step in reversed(step_sequence):
            Ay.value(step[0])
            By.value(step[1])
            Cy.value(step[2])
            Dy.value(step[3])
            time.sleep(delay)

#This is for the claw. Initiating pins for the solenoid and the stepper motor of the z-axis.
SOL=Pin(12, Pin.OUT)
A = Pin(4, Pin.OUT)
B = Pin(5, Pin.OUT)
C = Pin(6, Pin.OUT)
D = Pin(7, Pin.OUT)

#step sequence for the z-axis stepper motor
step_sequence = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

#height of the z-axis. Conversion is for converting height of cm to steps.
def height():
    conversion= 1028/20.4
    height= conversion * 10
    return int(height)

#For solenoid to "grab" the piece
def solenoid_on():
    SOL.value(1)
#For solenoid to "release" the piece
def solenoid_off():
    SOL.value(0)

#For the claw to move down
def Reels_down(steps, delay=0.02):
    for _ in range(int(steps)):
        for step in step_sequence:
            A.value(step[0])
            B.value(step[1])
            C.value(step[2])
            D.value(step[3])
            time.sleep(delay)
    return
#For the claw to move up
def Reels_up(steps, delay=0.02):
    for _ in range(int(steps)):
        for seq in reversed(step_sequence):
            A.value(seq[0])
            B.value(seq[1])
            C.value(seq[2])
            D.value(seq[3])
            time.sleep(delay)


solenoid_off()


def check_win(moves): #This was got from the logic of AI.
    moves = set(moves)
    for combo in win:
        if set(combo).issubset(moves):
            return True
    return False

def moving_claw_robot(new_sqr, current_sqr): #MOVING THE ROBOT
    SRQ_x, SRQ_y = MATRIX_SYSTEM(current_sqr, new_sqr)
    time.sleep(2)
    if SRQ_x >= 0:
        step_motor_x(SRQ_x)
    elif SRQ_x < 0:
        SRQ_x=-SRQ_x
        step_motor_reverse_x(SRQ_x)
    if SRQ_y >= 0:
        step_motor_y(SRQ_y)
    elif SRQ_y < 0:
        SRQ_y=-SRQ_y
        step_motor_reverse_y(SRQ_y)
    time.sleep(2)
    return

#To see if the sensors were pressed already. This is a security measure so that the same sensor does not activate twice.
def read_sensors(available):
    if SS1.value()==1 and 1 in available:
        return 1
    elif SS2.value()==1 and 2 in available:
        return 2
    elif SS3.value()==1 and 3 in available:
        return 3
    elif SS4.value()==1 and 4 in available:
        return 4
    elif SS5.value()==1 and 5 in available:
        return 5
    elif SS6.value()==1 and 6 in available:
        return 6
    elif SS7.value()==1 and 7 in available:
        return 7
    elif SS8.value()==1 and 8 in available:
        return 8
    elif SS9.value()==1 and 9 in available:
        return 9

def robot(player1, CPU, game): #LOGIC OF ROBOT. This was got from the logic of AI. However, this is very basic and follows a 'grocery list' logic. It is explained in main.py file
    board = {"1","2","3","4","5","6","7","8","9"}
    available = list(board - set(game))
    winning_move=[move for move in available if check_win(CPU + [move])]
    blocking_move=[move for move in available if check_win(player1 + [move])]
    if blocking_move and not winning_move:
        return blocking_move[random.randint(0, len(blocking_move)-1)]

    if winning_move:
        return winning_move[random.randint(0, len(winning_move)-1)]

    if 5 in available: 
        return 5
    
    corners= [m for m in [1,3,7,9] if m in available]
    if corners: 
        return corners[random.randint(0, len(corners)-1)]


    if not blocking_move or winning_move or corners or 5:
        return available[random.randint(0, len(available)-1)]


def main_board():
    board = [1,2,3,4,5,6,7,8,9]
    playable_move_1=True
    playable_move_2=True
    playable_move_3=True
    playable_move_4=True
    playable_move_5=True
    playable_move_6=True
    playable_move_7=True
    playable_move_8=True
    playable_move_9=True
 
    game=[]
    player1=[]
    CPU=[]
    print("You are first")
    time.sleep(3)
    for row in board:
        turn_player=False
        #if players turn
        while turn_player==False:
            turn_player1 = None
            turn_player1=read_sensors(board)#reads to see if the player played a move
 
            current_square= turn_player1   
            if turn_player1 is not None:
                    game.append(turn_player1)
                    player1.append(turn_player1)
                    turn_player = True

                    print(game)
            if check_win(player1): #check to see if player wins by seeing if the list of moves ressembles the winning combinations.
                        print("PLAYER1 WINS!")
                        return
            if len(game) == 9:#check to see if the game is drawn.
                        print("Game over! It's a draw.")
                        return
            time.sleep(2)

        while turn_player==True:
                print(f"{game}")

                robot_move=robot(player1, CPU, game) #Robot responds to the move
                if robot_move in game:
                    print("sorry you have to retry, this is what is current:"+ f"{game}")
                else:#This is useless but it is for security reasons. To make sure that the sensor is playable... from sensors 1-9
                    if playable_move_1==True and robot_move == 1:
                            playable_move_1=False
                            while SS1.value():
                                pass
                    elif playable_move_2==True and robot_move == 2:
                            playable_move_2=False
                            while SS2.value():
                                pass
                    elif playable_move_3==True and robot_move == 3:
                            playable_move_3=False
                            while SS3.value():
                                pass
                    elif playable_move_4==True and robot_move == 4:
                            playable_move_4=False
                            while SS4.value():
                                pass
                    elif playable_move_5==True and robot_move == 5:
                            playable_move_5=False
                            while SS5.value():
                                pass
                    elif playable_move_6==True and robot_move == 6:
                            playable_move_6=False
                            while SS6.value():
                                pass
                    elif playable_move_7==True and robot_move == 7:
                            playable_move_7=False
                            while SS7.value():
                                pass
                    elif playable_move_8==True and robot_move == 8:
                            playable_move_8=False
                            while SS8.value():
                                pass
                    elif playable_move_9==True and robot_move == 9:
                            playable_move_9=False
                            while SS9.value():
                                pass
                        
                    #This is actually applying the sequences of movements so that the claw and move, pick up, etc.
                    moving_claw_robot(robot_move, 0) 
                    print(f"{moving_claw_robot(robot_move, 0)}")
                    time.sleep(2)
                    Reels_down(height(), delay=0.02)
                    time.sleep(2)
                    solenoid_off()
                    Reels_up(height(), delay=0.02)
                    if robot_move is not None:
                            game.append(robot_move)
                            CPU.append(robot_move)
                    print(game)

                    if check_win(CPU):#Check to see if the robot wins
                            print("CPU WINS!")
                            return
                    if len(game) == 9:#Check to see if the game is drawn
                            print("Game over! It's a draw.")
                            return
                    turn_player=False

                    #Reel down and up to pick up a piece from the feeder
                    time.sleep(2)
                    moving_claw_robot(initial, robot_move)
                    time.sleep(2)
                    Reels_down(height(), delay=0.02)
                    solenoid_on()
                    time.sleep(2)
                    Reels_up(height(), delay=0.02)
                


main_board()