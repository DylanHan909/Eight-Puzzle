from queue import PriorityQueue
import time
import math
from turtle import pu

goal_state = ([1, 2, 3], [4, 5, 6], [7, 8, 0])

#EMPTY TILE IS REPRESENTED BY 0
#Node structure should include the following operators. Move up/down/left/right. 
#Node structure should say: If the state was expanded or not. The heuristic cost for each node. (h(n)). The node depth

class Node:
    def __init__ (self, puzzle):
        self.puzzle = puzzle
        self.move_up = None
        self.move_down = None
        self.move_left = None
        self.move_right = None
        self.is_expanded = None
        self.heuristic = 0
        self.depth = 0

def main(): 
    chosen_puzzle = False
    puzzle_select = input("Welcome to the 8-puzzle solver! Type '1' for a set puzzle. Type '2' for a custom puzzle: ")
    while (chosen_puzzle is not True):
        if puzzle_select != '1' and puzzle_select != '2':
                puzzle_select = input("Incorrect input. Type '1' for a set puzzle. Type '2' for a custom puzzle: ")
        else:
            chosen_puzzle = True
    puzzle = get_puzzle(puzzle_select)
    algorithm = get_algorithm(puzzle)
    return 0

def get_puzzle(puzzle):
    if puzzle == '1':
        return difficulty_select()
    elif puzzle == '2':
        print('Put in a custom puzzle\n')
        return 0
    return 0


def get_algorithm(puzzle):
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhatten Distance Heuristic: ")
    chosen_algorithm = False
    while (chosen_algorithm is not True):
        if algorithm == '1':
            return getUCS()
        if algorithm == '2':
            return a_star_misplaced(puzzle)
        if algorithm == '3':
            return a_star_manhatten(puzzle)
        else:
            algorithm = input("Incorrect input, please choose the search type again: ")
        
def difficulty_select():
    trivial_puzzle = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    very_easy_puzzle = ([1, 2, 3], [4, 5, 6], [7, 0, 8])
    easy_puzzle = ([1, 2, 0], [4, 5, 3], [7, 8, 6])
    doable_puzzle = ([0, 1, 2], [4, 5, 3], [7, 8, 6])
    oh_boy_puzzle = ([8, 7, 1], [6, 0, 2], [5, 4, 3])
    difficulty = input("Select difficulty from 0 to 4: ")
    chosen_difficulty = False
    while (chosen_difficulty is not True):
        if difficulty == '0':
            print("Trivial puzzle selected.")
            print_puzzle(trivial_puzzle)
            return trivial_puzzle
        if difficulty == '1':
            print("Very Easy puzzle selected.")
            print_puzzle(very_easy_puzzle)
            return very_easy_puzzle
        if difficulty == '2':
            print("Easy puzzle selected.")
            print_puzzle(easy_puzzle)
            return easy_puzzle
        if difficulty == '3':
            print("Doable puzzle selected.")
            print_puzzle(doable_puzzle)
            return doable_puzzle
        if difficulty == '4':
            print("Oh boy puzzle selected.")
            print_puzzle(oh_boy_puzzle)
            return oh_boy_puzzle
        else:
            difficulty = input("Incorrect input, please choose the difficulty again: ")

def getUCS():
    print('Uniform Cost Search was selected.')
    return 0

def a_star_misplaced(puzzle):
    print('Misplaced Tile Heuristic was selected.')
    misplaced_tiles = 0
    for row in range(3):
        for column in range(3):
            if (puzzle[row][column] != goal_state[row][column]):
                if (puzzle[row][column] != 0): #need to account for an empty tile
                    misplaced_tiles += 1
    print("A total of " + str(misplaced_tiles) + " misplaced tiles were found.")
    return misplaced_tiles

def a_star_manhatten(puzzle):

    #[1, 2, 3]    [3, 2, 8] manhatten for 3 = 2, 2 to the right, manhatten for 8 = 3, 1 left, 2 down, manhatten for 1 = 3, 2 up, 1 down
    #[4, 5, 6]    [4, 5, 6] 
    #[7, 8, 0]    [7, 1, 0]
    #0, 2 should be at 2, 1
    #Distance formula = |x2 - x1| + |y2 - y1|, so goal state row - misplaced row + goal state column - misplaced column,  | 2 - 0 | + | 1 - 2 | = 3
    #https://cdn.codespeedy.com/wp-content/uploads/2020/03/manhattan.jpg
    print('Manhatten Distance Heuristic was selected.')
    goal_row = 0
    goal_column = 0
    misplaced_row = 0
    misplaced_column = 0
    misplaced_tile = 0
    manhatten = 0
    for row in range(3):
        for column in range(3):
            if (puzzle[row][column] != goal_state[row][column]):
                if (puzzle[row][column] != 0): #need to account for an empty tile
                    misplaced_tile = puzzle[row][column]
                    misplaced_row = row 
                    misplaced_column = column
                    if misplaced_tile == 1:
                        goal_row = 0
                        goal_column = 0
                    elif misplaced_tile == 2:
                        goal_row = 0
                        goal_column = 1
                    elif misplaced_tile == 3:
                        goal_row = 0
                        goal_column = 2
                    elif misplaced_tile == 4:
                        goal_row = 1
                        goal_column = 0
                    elif misplaced_tile == 5:
                        goal_row = 1
                        goal_column = 1
                    elif misplaced_tile == 6:
                        goal_row = 1
                        goal_column = 2
                    elif misplaced_tile == 7:
                        goal_row = 2
                        goal_column = 0
                    elif misplaced_tile == 8:
                        goal_row = 2
                        goal_column = 1
                    manhatten += (abs(goal_row - misplaced_row) + abs(goal_column - misplaced_column))   
    print('The manhatten distance of the puzzle provided would be: ' + str(manhatten))
    return manhatten

def print_puzzle(puzzle):
    for row in range(3):
        print('[', end = "")
        for column in range(2):
            print(str(puzzle[row][column]) + ', ', end = "")
        print(str(puzzle[row][2]), end = "")
        print(']')

def node_expansion():
    return 0

def search_puzzle():
    return 0

main()
