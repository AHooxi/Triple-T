import random
import time
#THE BOARD:
#1     2     3
#4     5     6
#7     8     9

win=[
    {"1","2","3"},
    {"4","5","6"},
    {"7","8","9"},
    {"1","4","7"},
    {"2","5","8"},
    {"3","6","9"},
    {"1","5","9"},
    {"3","5","7"},
    ]

def who_first():
    first=["player","robot"]
    return random.choice(first)

def check_win(moves): #GOT FROM AI
    moves = set(moves)
    for combo in win:
        if combo.issubset(moves):
            return True
    return False

def robot(player1, CPU, game):
    board = {"1","2","3","4","5","6","7","8","9"}
    available = list(board - set(game))
    winning_move=[move for move in available if check_win(CPU + [move])]# got from AI
    blocking_move=[move for move in available if check_win(player1 + [move])]#USE logic based off of AI
    if blocking_move and not winning_move:
        return random.choice(blocking_move)

    if winning_move:
        return random.choice(winning_move)

    if "5" in available: #USE logic based off of AI
        return "5"

    corners= [m for m in ["1","3","7","9"] if m in available]
    if corners: #USE logic based off of AI
        return random.choice(corners)


    if not blocking_move or winning_move or corners:
        return random.choice(available)

def main_board():
    board = ["1","2","3","4","5","6","7","8","9"]

    game=[]
    player1=[]
    CPU=[]
    if who_first()=="player":
        print("You are first")
        time.sleep(3)
        for row in board:
                while True:
                    turn_player1=input("PLAYER 1, where would you like to go (1-9)?")
                    if turn_player1 in game or turn_player1 not in board:
                        print("sorry you have to retry, this is what is current:"+ f"{game}")
                    else:
                        game.append(turn_player1)
                        player1.append(turn_player1)
                        print(game)
                        if check_win(player1):
                            print("PLAYER1 WINS!")
                            return
                        if len(game) == 9:
                            print("Game over! It's a draw.")
                            return
                        break
                while True:
                    robot_move=robot(player1, CPU, game)
                    if robot_move in game:
                        print("sorry you have to retry, this is what is current:"+ f"{game}")
                    else:
                        game.append(robot_move)
                        CPU.append(robot_move)
                        print(game)
                        if check_win(CPU):
                            print("CPU WINS!")
                            return
                        if len(game) == 9:
                            print("Game over! It's a draw.")
                            return
                        break
    if who_first()=="robot":
        print("robot is first")
        time.sleep(3)
        for row in board:
                while True:
                    robot_move=robot(player1, CPU, game)
                    if robot_move in game:
                        print("sorry you have to retry, this is what is current:"+ f"{game}")
                    else:
                        game.append(robot_move)
                        CPU.append(robot_move)
                        print(game)
                        if check_win(CPU):
                            print("CPU WINS!")
                            return
                        if len(game) == 9:
                            print("Game over! It's a draw.")
                            return
                        break
                while True:
                    turn_player1=input("PLAYER 1, where would you like to go (1-9)?")
                    if turn_player1 in game or turn_player1 not in board:
                        print("sorry you have to retry, this is what is current:"+ f"{game}")
                    else:
                        game.append(turn_player1)
                        player1.append(turn_player1)
                        print(game)
                        if check_win(player1):
                            print("PLAYER1 WINS!")
                            return
                        if len(game) == 9:
                            print("Game over! It's a draw.")
                            return
                        break

main_board()