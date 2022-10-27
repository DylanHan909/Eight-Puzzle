from queue import PriorityQueue
import time
import math

goal_state = ([1, 2, 3], [4, 5, 6], [7, 8, 9])

def main():
    puzzle_select = input("Welcome to the 8-puzzle solver! Type '1' for a set puzzle. Type '2' for a custom puzzle. \n")
    puzzle = get_puzzle(puzzle_select)
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced TIle Heuristic, or (3) the Manhatten Distance Heuristic. \n")
    get_algorithm(algorithm)



    return 0

def get_puzzle(puzzle):
    if puzzle == '1':
        return difficulty_select()
    elif puzzle == '2':
        print('Put in some custom puzzle\n')
        return 0
    return 0

def get_algorithm(algorithm):
    chosen_algorithm = False
    while (chosen_algorithm is not True):
        if algorithm == '1':
            return getUCS()
        if algorithm == '2':
            return a_star_misplaced()
        if algorithm == '3':
            return a_star_manhatten()
        else:
            print('Invalid Choice. UCS will be selected instead.')
            return getUCS()

def difficulty_select():
    trivial_puzzle = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    very_easy_puzzle = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    easy_puzzle = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    doable_puzzle = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    oh_boy_puzzle = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    difficulty = input("Select difficulty from 0 to 4." + '\n')
    
    if difficulty == '0':
        print("Trivial puzzle selected.")
        return trivial_puzzle
    if difficulty == '1':
        print("Very Easy puzzle selected.")
        return very_easy_puzzle
    if difficulty == '2':
        print("Easy puzzle selected.")
        return easy_puzzle
    if difficulty == '3':
        print("Doable puzzle selected.")
        return doable_puzzle
    if difficulty == '4':
        print("Oh boy puzzle selected.")
        return oh_boy_puzzle
    

def getUCS():
    print('Uniform Cost Search was selected.')
    return 0

def a_star_misplaced():
    print('Misplaced Tile Heuristic was selected.')
    misplaced_tiles = 0
    return 0

def a_star_manhatten():
    print('Manhatten Distance Heuristic was selected.')
    return 0

def node_expansion():
    return 0

def search_puzzle():
    return 0

main()
