"""
Team Name: Triple T
Team Members: Kaiwen Chen, Anthony Xenos 
Last Edited: 6/7/2026 



Brief description: 
To start, this is the version that was refined by AI. There was slight personal touches to this code but regardless, it was refined by AI. All of the personal touches are found in original.py file. This is the main and only script for the Tic Tac Toe robot. It handles all the logic for reading sensors, controlling the stepper motors, and implementing the game logic. The robot will play against a human player, making strategic moves to try to win the game. The code is structured into sections for configuration, sensor handling, motor control, and game logic for clarity and maintainability.

Expanded description:
AI played a significant role in refining the code. It helped to condense many of the long functions and fix some logic mistakes. This made the robot more responsive and overall more functional. The robot uses a 3x3 grid of sensors to detect the player's moves. This grid is represented with coordinated, to help locate the distances from one sensor to another. Once the sensor has been activated, the robot will use the stepper motors to move a claw to pick up and place pieces on the board. The game logic includes a simple algorithm that will try to win if it can, block the player's winning move, or choose a strategic position otherwise. The main loop alternates between the player's turn and the robot's turn until there is a winner or a draw.


Citations:
AI Use & Refinement Disclosure:
    - Tool: OpenAI ChatGPT (GPT-4o Model, Feb 2026 Version)
    - Transcript file: https://chatgpt.com/share/6a07a257-0c18-83ea-8ed2-2d454191108f
    - Scope: The AI was used to refine the original code. It condensed many of the stupidly long functions. It also fixed some small logic mistakes that lag the robot down. 

AI Use & Logic Disclosure:
    - Tool: OpenAI ChatGPT (GPT-4o Model, Feb 2026 Version)
    - Transcript file: https://chatgpt.com/share/6a07a052-10a8-83ea-95a1-a534b02fd220
    - Scope: This was a chat that went for a while to talk about implementing AI. Later gave up on this and asked for a different way. The very bottom of the chat was the logic that was used. The game logic was made by AI. It follows a simple checklist type of function which is super easy to code, but regardless, AI was use.
"""







from machine import Pin
import time
import random


# Board layout
# 1  2  3
# 4  5  6
# 7  8  9

HOME = 0
DISTANCE = 6.5
CONVERSION = 1028 / 20.4
HEIGHT=8
HEIGHTRESET=5

#Activating Sensors, 1-9. Pin In and Pull down for on and off detection.
sensors = {
    1: Pin(16, Pin.IN, Pin.PULL_DOWN),
    2: Pin(17, Pin.IN, Pin.PULL_DOWN),
    3: Pin(18, Pin.IN, Pin.PULL_DOWN),
    4: Pin(19, Pin.IN, Pin.PULL_DOWN),
    5: Pin(20, Pin.IN, Pin.PULL_DOWN),
    6: Pin(21, Pin.IN, Pin.PULL_DOWN),
    7: Pin(22, Pin.IN, Pin.PULL_DOWN),
    8: Pin(26, Pin.IN, Pin.PULL_DOWN),
    9: Pin(28, Pin.IN, Pin.PULL_DOWN),
}

#Setting up stepper motor pins

Ax = Pin(0, Pin.OUT)
Bx = Pin(1, Pin.OUT)
Cx = Pin(2, Pin.OUT)
Dx = Pin(3, Pin.OUT)

Ay = Pin(8, Pin.OUT)
By = Pin(9, Pin.OUT)
Cy = Pin(10, Pin.OUT)
Dy = Pin(11, Pin.OUT)

A = Pin(4, Pin.OUT)
B = Pin(5, Pin.OUT)
C = Pin(6, Pin.OUT)
D = Pin(7, Pin.OUT)

SOL = Pin(12, Pin.OUT)


#Step Sequence for the stepper motors
STEP_SEQUENCE = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]


#What AI condensed. Changed coordinates to a simple dictionary to make it easier to read and maintain. This is the coordinate maping of the board and for the tic-tac-toe piece feeder (HOME).
coords = {
    1:(-1,3), 2:(0,3), 3:(1,3),
    4:(-1,2), 5:(0,2), 6:(1,2),
    7:(-1,1), 8:(0,1), 9:(1,1),
    HOME:(0,0)
}


#AI changed my logic to this function. Same principle but much more condensed and as its own seperate function, making it easier to read.
def move_to(current, target):
    cx, cy = coords[current]
    tx, ty = coords[target]

    dx = (tx - cx) * DISTANCE * CONVERSION
    dy = (ty - cy) * DISTANCE * CONVERSION

    move_x(dx)
    move_y(dy)

#Movement of the x and y Axis. All it does it turns the steps into a interger and then uses it in the step sequence. If it is negative, it reads its as reversed, going the opposite direction.
def move_x(steps):
    steps = int(abs(steps))
    seq = STEP_SEQUENCE if steps >= 0 else reversed(STEP_SEQUENCE)

    for _ in range(steps):
        for s in seq:
            Ax.value(s[0])
            Bx.value(s[1])
            Cx.value(s[2])
            Dx.value(s[3])
            time.sleep(0.001)

def move_y(steps):
    steps = int(abs(steps))
    seq = STEP_SEQUENCE if steps >= 0 else reversed(STEP_SEQUENCE)

    for _ in range(steps):
        for s in seq:
            Ay.value(s[0])
            By.value(s[1])
            Cy.value(s[2])
            Dy.value(s[3])
            time.sleep(0.001)


#This is for the claw, the height is just a conversion. It takes the variable height on top and converts it into steps because the stepper motors only reads in steps.
def height():
    return int(CONVERSION * HEIGHT)

#This is for the claw reseting. Since the feeder is lifted, it needs to go at a different height to reset the game (pick up the piece). This height would be smaller than the other.
def height_reset():
    return int(CONVERSION * HEIGHTRESET)

#This function is the same logic as for the x and y axis, but now moving in the z axis. This axis would take the height rather than the distance. There are 4 functions, 2 for the normal height/game, and 2 for the resseting height/resseting the game. Each of the two has one for going up and one for going down. (Reel up/Reel down)
def reels_down():
    for _ in range(height()):
        for s in STEP_SEQUENCE:
            A.value(s[0])
            B.value(s[1])
            C.value(s[2])
            D.value(s[3])
            time.sleep(0.02)
def reels_down_reset():
    for _ in range(height_reset()):
        for s in STEP_SEQUENCE:
            A.value(s[0])
            B.value(s[1])
            C.value(s[2])
            D.value(s[3])
            time.sleep(0.02)
def reels_up():
    for _ in range(height()):
        for s in reversed(STEP_SEQUENCE):
            A.value(s[0])
            B.value(s[1])
            C.value(s[2])
            D.value(s[3])
            time.sleep(0.02)
def reels_up_reset():
    for _ in range(height_reset()):
        for s in reversed(STEP_SEQUENCE):
            A.value(s[0])
            B.value(s[1])
            C.value(s[2])
            D.value(s[3])
            time.sleep(0.02)

# Grab and release are for the claw/solenoid. The solenoid either turns on (grab) or turns off (release)
def grab():
    SOL.value(1)

def release():
    SOL.value(0)

#This is to check if the sensor is pressed. This is just a security messure so that the same sensor does not activate twice.
def read_sensors(available):
    for pos, sensor in sensors.items():
        if sensor.value() == 1 and pos in available:
            time.sleep(0.02)  # short debounce
            if sensor.value() == 1:  # still pressed
                return pos
    return None



#The following are for the game logic: win, check win and robot move. Win is a list of all the winning combinations in tic tac toe. Check win checks if the player's moves form a winning combination. Robot move is for the robot, it checks if it can win in the next move. If it cannot win, it blocks. If there are no blocking moves, it plays center. If center is taken, it plays the corners. Finally, if everything in this list has gone through, it plays a random move.
win = [
    [1,2,3],[4,5,6],[7,8,9],
    [1,4,7],[2,5,8],[3,6,9],
    [1,5,9],[3,5,7]
]

def check_win(moves):
    moves = set(moves)
    return any(set(w).issubset(moves) for w in win)

def robot_move(player, cpu, game):
    available = [i for i in range(1,10) if i not in game] #Seeing what spaces are still available to play. 

    if not available:
        return None

    for m in available: #check to see if it can win
        if check_win(cpu + [m]):
            return m

    for m in available: #check to see if it can block using the player's winning chances as a reference
        if check_win(player + [m]):
            return m

    if 5 in available: #if cannot win or block, play center
        return 5

    corners = [c for c in [1,3,7,9] if c in available] #plays corners if cannot go center.
    if corners:
        return corners[random.randint(0, len(corners) - 1)]

    return available[random.randint(0, len(available) - 1)]#randomly picks a corner if nothing else works.



#Everything is comming together in the main function. It goes through a sequence of code starting with picking up the first piece, waiting for your move, responding with your move, moving the claw, placing the piece, and finally resetting.
def main():
    game = []
    player = []
    cpu = []
    release()
    current_pos = HOME
    reels_up()
    reels_down_reset()
    grab()
    reels_up_reset()
    print("You are first")
    time.sleep(2)

    while True:

        # PLAYER TURN
        move = None
        while move is None:
            move = read_sensors([i for i in range(1,10) if i not in game])# This is to read the sensors between 1-9. 

        print("Player:", move)
        game.append(move) #This is a list for the game to keep track of the game, determining if the game is drawn.
        player.append(move) #To declare the move as a part of a list with the player's move.

        if check_win(player): # Checks to see if the list of moves of the player has a winning combination.
            print("PLAYER WINS")
            return

        if len(game) == 9: #If all the spaces are filled and there is no winner, it is a draw.
            print("DRAW")
            return

        # ROBOT TURN
        r = robot_move(player, cpu, game) #This is the function for the robot to decide where to go.
        print("Robot:", r)

        move_to(current_pos, r) #This is the function for the x and y axis to move to the correct position.
        current_pos = r
        HEIGHT=6
        reels_down()
        release()
        reels_up()

        game.append(r)
        cpu.append(r)

        if check_win(cpu): #Same logic as the player to win, but for the robot.
            print("CPU WINS")
            return

        if len(game) == 9:
            print("DRAW")
            return

        # RETURN TO TIC-TAC-TOE FEEDER + PICK UP PIECE
        move_to(current_pos, HOME)
        current_pos = HOME
        reels_down_reset()
        grab()
        reels_up_reset()



#To start the game
release()
main()