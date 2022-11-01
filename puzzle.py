import copy
from queue import PriorityQueue
from tabnanny import verbose
import time

goal_state = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
verbose = False

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
        self.heuristic = 0 #h(n)
        self.depth = 0 #g(n)
    
    #Implemented so the priorityqueue can compare objects and automatically preceed with the node with the lowest cost
    #https://stackoverflow.com/questions/9292415/i-notice-i-cannot-use-priorityqueue-for-objects
    def __lt__(self, other):
        self.distance = self.depth + self.heuristic 
        other.distance = other.depth + other.heuristic
        if (other.distance == self.distance):
            return other.depth > self.depth #Done because my search was bugged, when f(n) equalled, it would choose a larger depth randomly, choose the smaller depth manually to solve 
        else:
            return other.distance > self.distance
#Driver FUNCTION
def main():
    '''
    debugging = input("DEBUGGING ONLY: PRESS 1 FOR EXTRA OUTPUTS: ")
    if (debugging == '1'):
        global verbose
        verbose = True
    '''
    puzzle = get_puzzle()
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhatten Distance Heuristic: ")
    while (int(algorithm) < 1 or int(algorithm) > 3):
        algorithm = input("Incorrect input, please choose the search type again: ")
    start = time.time()
    search_puzzle(puzzle, algorithm)
    end = time.time()
    print ('Search time was ' + str(end - start)  + ' seconds')
    return 0

#SEARCH RELATED FUNCTIONS
def search_puzzle(puzzle, algorithm):
    #Using priority queue for the node frontier: https://docs.python.org/3/library/queue.html
    #HEAVILY inspired from psuedocode in: https://www.dropbox.com/sh/cp90q8nlk8od4cw/AADK4L3qOh-OJtFzdi_8Moaka?dl=0&preview=Project_1_The_Eight_Puzzle_CS_170_2022.pdf
    #INSPIRED BY https://plainenglish.io/blog/uniform-cost-search-ucs-algorithm-in-python-ec3ee03fca9fhttps://plainenglish.io/blog/uniform-cost-search-ucs-algorithm-in-python-ec3ee03fca9f as well
    curr_puzzle = Node(puzzle)
    curr_puzzle.heuristic = get_algorithm(curr_puzzle.puzzle, algorithm)
    working_queue = PriorityQueue()
    repeated_states = []
    max_queue_size = 0
    expanded_nodes = 0

    working_queue.put(curr_puzzle)
    repeated_states.append(curr_puzzle.puzzle)
    max_queue_size += 1
    while (working_queue.qsize() != 0):
        max_queue_size = max(working_queue.qsize(), max_queue_size)
        curr_puzzle = working_queue.get()
        if (curr_puzzle.is_expanded is not True):
            curr_puzzle.is_expanded = True
            expanded_nodes += 1
        print('The best state to expand with a g(n) = ' + str(curr_puzzle.depth) + ' and h(n) = ' + str(curr_puzzle.heuristic) + ' is...')
        print_puzzle(curr_puzzle.puzzle)

        if curr_puzzle.puzzle == goal_state:
            print('Goal state!\n')
            print_puzzle(curr_puzzle.puzzle)
            print('Solution depth was ' + str(curr_puzzle.depth))
            print('Number of nodes expanded: ' + str(expanded_nodes - 1)) #Minus 1 because it keeps into account expanding the first state
            print('Max queue size: ' + str(max_queue_size))
            break
        
        if (verbose):
            print('Puzzle will now be expanded...\n')
        expanded = node_expansion(curr_puzzle, repeated_states)
        children_nodes = [expanded.move_up, expanded.move_down, expanded.move_left, expanded.move_right]
        children_nodes = list(filter(lambda item: item is not None, children_nodes))
        #https://www.geeksforgeeks.org/python-remove-none-values-from-list/
        for child in children_nodes:
            if child not in repeated_states:
                child.depth = curr_puzzle.depth + 1 #Need to do this or depth will be perma frozen at 1
                child.heuristic = get_algorithm(child.puzzle, algorithm)
                working_queue.put(child)
                repeated_states.append(child.puzzle)

def node_expansion(puzzle, repeated_states):
    expand_row = 0
    expand_column = 0
    for row in range(3):
        for column in range(3):
            if (puzzle.puzzle[row][column] == 0): #tile with the empty space
                expand_row = row
                expand_column = column 
    if (expand_row < 2):
        move_up(puzzle, expand_row, expand_column, repeated_states)
    if (expand_row != 0):
        move_down(puzzle, expand_row, expand_column, repeated_states)
    if (expand_column < 2):
        move_left(puzzle, expand_row, expand_column, repeated_states)
    if (expand_column != 0):
        move_right(puzzle, expand_row, expand_column, repeated_states)
    return puzzle

#HEURISTIC FUNCTIONS
def uniform_cost():
    if (verbose):
        print('Uniform Cost Search was selected.')
    return 0

def a_star_misplaced(puzzle):
    if (verbose):
        print('Misplaced Tile Heuristic was selected.')
    misplaced_tiles = 0
    for row in range(3):
        for column in range(3):
            if (puzzle[row][column] != goal_state[row][column]):
                if (puzzle[row][column] != 0): #need to account for an empty tile
                    if (verbose):
                        print('The misplaced tile is ' + str(puzzle[row][column]))
                    misplaced_tiles += 1
    if (verbose):
        print("A total of " + str(misplaced_tiles) + " misplaced tiles were found." + '\n')
    return misplaced_tiles

def a_star_manhatten(puzzle):
    #[1, 2, 3]    [3, 2, 8] manhatten for 3 = 2, 2 to the right, manhatten for 8 = 3, 1 left, 2 down, manhatten for 1 = 3, 2 up, 1 down
    #[4, 5, 6]    [4, 5, 6] 
    #[7, 8, 0]    [7, 1, 0]
    #0, 2 should be at 2, 1
    #Distance formula = |x2 - x1| + |y2 - y1|, so goal state row - misplaced row + goal state column - misplaced column,  | 2 - 0 | + | 1 - 2 | = 3
    #https://cdn.codespeedy.com/wp-content/uploads/2020/03/manhattan.jpg
    if (verbose):
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
                    goal_row, goal_column = get_goal_position(goal_state, misplaced_tile)
                    if (verbose):
                        print('The misplaced tile ' + str(misplaced_tile) + ' is ' + str(abs(goal_row - misplaced_row) + abs(goal_column - misplaced_column)) + ' spaces away.')
                    manhatten += (abs(goal_row - misplaced_row) + abs(goal_column - misplaced_column))   
    if (verbose):
        print('The Manhatten Distance of the puzzle provided would be: ' + str(manhatten) + '\n')
    return manhatten

#HELPER FUNCTIONS
#NEED DEEP COPY BECAUSE SHALLOW COPY SCREWED UP COPYING OBJECTS 
def move_up(puzzle, expand_row, expand_column, repeated_states):
    child = copy.deepcopy(puzzle.puzzle)
    if (verbose):
        print('Moving tile ' + str(child[expand_row + 1][expand_column]) + ' upwards')
    child[expand_row][expand_column] = child[expand_row + 1][expand_column]
    child[expand_row + 1][expand_column] = 0
    if child not in repeated_states:
        puzzle.move_up = Node(child)
        if (verbose):
            print_puzzle(puzzle.move_up.puzzle) 
    else:
        if (verbose):
            print('Repeated state found, skipping.\n')

def move_down(puzzle, expand_row, expand_column, repeated_states):
    child = copy.deepcopy(puzzle.puzzle)
    if (verbose):
        print('Moving tile ' + str(child[expand_row - 1][expand_column]) + ' downwards')
    child[expand_row][expand_column] = child[expand_row - 1][expand_column]
    child[expand_row - 1][expand_column] = 0
    if child not in repeated_states:
        puzzle.move_down = Node(child)
        if (verbose):
            print_puzzle(puzzle.move_down.puzzle)
    else:
        if (verbose):
            print('Repeated state found, skipping.\n')

def move_left(puzzle, expand_row, expand_column, repeated_states):
    child = copy.deepcopy(puzzle.puzzle)
    if (verbose):
        print('Moving tile ' + str(child[expand_row][expand_column + 1]) + ' leftwards')
    child[expand_row][expand_column] = child[expand_row][expand_column + 1]
    child[expand_row][expand_column + 1] = 0
    if child not in repeated_states:
        puzzle.move_left = Node(child)
        if (verbose):
            print_puzzle(puzzle.move_left.puzzle) 
    else:
        if (verbose):
            print('Repeated state found, skipping.\n')

def move_right(puzzle, expand_row, expand_column, repeated_states):
    child = copy.deepcopy(puzzle.puzzle)
    if (verbose):
        print('Moving tile ' + str(child[expand_row][expand_column - 1]) + ' rightwards')
    child[expand_row][expand_column] = child[expand_row][expand_column - 1]
    child[expand_row][expand_column - 1] = 0
    if child not in repeated_states:
        puzzle.move_right = Node(child)
        if (verbose):
            print_puzzle(puzzle.move_right.puzzle) 
    else:
        if (verbose):
            print('Repeated state found, skipping.\n')

def get_puzzle():
    chosen_puzzle = False
    puzzle_select = input("Welcome to the 8-puzzle solver! Type '1' for a set puzzle. Type '2' for a custom puzzle: ")
    while (chosen_puzzle is not True):
        if puzzle_select == '1':
            return difficulty_select()
        elif puzzle_select == '2':
            print('Put in a custom puzzle (0 is a blank space): ')
            custom_row_1 = input('Type in the first row here. Put a space between each number: ')
            custom_row_2 = input('Type in the first row here. Put a space between each number: ')
            custom_row_3 = input('Type in the first row here. Put a space between each number: ')
            custom_puzzle = (custom_row_1.split(' '), custom_row_2.split(' '), custom_row_3.split(' '))
            for row in range(3):
                for column in range(3):
                    custom_puzzle[row][column] = int(custom_puzzle[row][column])
            if (verbose):
                print(custom_puzzle)
            print_puzzle(custom_puzzle)
            return custom_puzzle
        else:
            puzzle_select = input('Invalid input. Type a choice again: ')
    return 0

def get_algorithm(puzzle, algorithm):
    chosen_algorithm = False
    while (chosen_algorithm is not True):
        if algorithm == '1':
            return uniform_cost()
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
            print("Trivial puzzle selected.\n")
            print_puzzle(trivial_puzzle)
            return trivial_puzzle
        if difficulty == '1':
            print("Very Easy puzzle selected.\n")
            print_puzzle(very_easy_puzzle)
            return very_easy_puzzle
        if difficulty == '2':
            print("Easy puzzle selected.\n")
            print_puzzle(easy_puzzle)
            return easy_puzzle
        if difficulty == '3':
            print("Doable puzzle selected.\n")
            print_puzzle(doable_puzzle)
            return doable_puzzle
        if difficulty == '4':
            print("Oh boy puzzle selected.\n")
            print_puzzle(oh_boy_puzzle)
            return oh_boy_puzzle
        else:
            difficulty = input("Incorrect input, please choose the difficulty again: ")

def get_goal_position(goal_state, misplaced_tile):
    for row in range(3):
        for column in range(3):
            if (goal_state[row][column] == misplaced_tile):
                return row, column

def print_puzzle(puzzle):
    for row in range(3):
        print('[', end = "")
        for column in range(2):
            print(str(puzzle[row][column]) + ', ', end = "")
        print(str(puzzle[row][2]), end = "")
        print(']')
    print('\n')

main()
