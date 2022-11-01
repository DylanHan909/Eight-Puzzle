import copy
from queue import PriorityQueue
from tabnanny import verbose
import time

goal_state = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
verbose = False #A way to have debugging outputs for testing purposes

#EMPTY TILE IS REPRESENTED BY 0
#Changed node structure a lot
#Keeps track of the puzzle state, the path taken to solve the puzzle, the heuristic from our algorithms (h(n)), and our current depth (g(n))
class Node:
    def __init__ (self, puzzle):
        self.puzzle = puzzle
        self.path = ''
        self.heuristic = 0 #h(n)
        self.depth = 0 #g(n)
    
    #Implemented so the priorityqueue can compare objects and automatically preceed with the node with the lowest cost
    #https://stackoverflow.com/questions/9292415/i-notice-i-cannot-use-priorityqueue-for-objects
    def __lt__(self, other):
        self.distance = self.depth + self.heuristic 
        other.distance = other.depth + other.heuristic
        if (other.distance == self.distance):
            return other.depth > self.depth #Done because my search was bugged, when f(n) of two nodes equaled each other, it would choose a larger depth randomly, choose the smaller depth manually to solve 
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
    #INSPIRED BY https://plainenglish.io/blog/uniform-cost-search-ucs-algorithm-in-python-ec3ee03fca9f

    curr_puzzle = Node(puzzle) #Initial state is a Node of the chosen puzzle
    curr_puzzle.heuristic = get_algorithm(curr_puzzle.puzzle, algorithm) #Get algorithm via user input choice
    working_queue = PriorityQueue()
    repeated_states = [] #tried to use a set to speed up the process but it did not
    max_queue_size = 0 #Max queue size
    expanded_nodes = 0 #Node count, changed from the old implementation as the old one was SUPER redundant, old nodes would NEVER be revisited with my dupe implementation, so there is no need for a separate attribute for expansion

    working_queue.put(curr_puzzle) #Put initial state into the priority queue
    repeated_states.append(curr_puzzle.puzzle) #put the initial states puzzle into the duplicate list
    max_queue_size += 1 #Take into account the initial starting node
    track_time = time.time()
    max_time = 900 #15 minutes total for program to run
    while (working_queue.qsize() != 0):
        #https://raspberrypi.stackexchange.com/questions/15613/stop-program-after-a-period-of-time, Done in case a search depth takes way too long to finish
        if (time.time() >= track_time + max_time):
            print('Program time is up! Ending program now!')
            exit(0)
        max_queue_size = max(working_queue.qsize(), max_queue_size) #change max queue size to the biggest size between the working queue and the max queue
        curr_puzzle = working_queue.get() #Get the smallest heuristic node from the queue
        expanded_nodes += 1 #Expand the node count

        if curr_puzzle.puzzle == goal_state: #If you match the goal state
            print('Goal state!\n')
            print_puzzle(curr_puzzle.puzzle)
            print('Solution depth was ' + str(curr_puzzle.depth))
            print('Number of nodes expanded: ' + str(expanded_nodes - 1)) #Minus 1 because it keeps into account expanding the first state
            print('Max queue size: ' + str(max_queue_size))
            print('The path to get to the node was \n' + str(curr_puzzle.path))
            break
        
        if (verbose):
            print('Puzzle will now be expanded...\n')

        print('The best state to expand with a g(n) = ' + str(curr_puzzle.depth) + ' and h(n) = ' + str(curr_puzzle.heuristic) + ' is...') #output the chosen state's heuristic
        print_puzzle(curr_puzzle.puzzle) #Print the puzzle

        node_expansion(curr_puzzle, repeated_states, working_queue, algorithm) #Expand nodes

def node_expansion(puzzle, repeated_states, working_queue, algorithm):
    expand_row = 0 
    expand_column = 0
    for row in range(len(puzzle.puzzle)): #range done so it can work for 15+ size puzzles
        for column in range(len(puzzle.puzzle)):
            if (puzzle.puzzle[row][column] == 0): #tile with the empty space
                expand_row = row #Row of the 0 element
                expand_column = column #Column of the 0 element
    if (expand_row < (len(puzzle.puzzle) - 1)): #If row < the bottom row
        move_tile(puzzle, expand_row, expand_column, (expand_row + 1), expand_column, repeated_states, ' upwards.', working_queue, algorithm)
    if (expand_row != 0): #if row > the top row
        move_tile(puzzle, expand_row, expand_column, (expand_row - 1), expand_column, repeated_states, ' downwards.', working_queue, algorithm)
    if (expand_column < (len(puzzle.puzzle) - 1)): #if column is to the left of the rightmost column
        move_tile(puzzle, expand_row, expand_column, expand_row, (expand_column + 1), repeated_states, ' leftwards.', working_queue, algorithm)
    if (expand_column != 0): #If the column is to the right of tthe leftmost column
        move_tile(puzzle, expand_row, expand_column, expand_row, (expand_column - 1), repeated_states, ' rightwards.', working_queue, algorithm)

#HELPER FUNCTIONS
#NEED DEEP COPY BECAUSE SHALLOW COPY SCREWED UP COPYING OBJECTS 
def move_tile(puzzle, expand_row, expand_column, new_row, new_column, repeated_states, direction, working_queue, algorithm):
    child = copy.deepcopy(puzzle.puzzle) #DEEP COPY because shallow copy is just a copy by reference, the original object still changes
    path = 'Moving tile ' + str(child[new_row][new_column]) + direction + '\n' #Adding the steps to solve the puzzle to the node structure
    if (verbose):
        print('Moving tile ' + str(child[new_row][new_column]) + direction)
    child[expand_row][expand_column] = child[new_row][new_column] #Slide the tile to the position passed in the node expansion function
    child[new_row][new_column] = 0 #Change the spot to an empty spot that was moved
    if child not in repeated_states: #If this new puzzle is NOT a repeat 
        repeated_states.append(child) #Move the new puzzle into our repeat states
        child_node = Node(child) #Create a new Node with the puzzle state
        child_node.path += puzzle.path #Add the previous paths into the child 
        child_node.path += path #Add the new path we calculated for this step 
        child_node.depth = puzzle.depth + 1 #Need to do this or depth will be perma frozen at 1
        child_node.heuristic = get_algorithm(child_node.puzzle, algorithm) #Calculate our new heuristic for our child node
        working_queue.put(child_node) #Put the child node into the priority queue
        if (verbose):
            print('Child formed')
            print_puzzle(child_node.puzzle)
    else:
        if (verbose):
            print('Repeated state found, skipping.\n')

def get_puzzle():
    chosen_puzzle = False
    puzzle_select = input("Welcome to the 8-puzzle solver! Type '1' for a set puzzle. Type '2' for a custom puzzle: ")
    while (chosen_puzzle is not True):
        if puzzle_select == '1':
            return difficulty_select() #Function to choose a pre-made puzzle
        elif puzzle_select == '2':
            print('Put in a custom puzzle (0 is a blank space): ')
            custom_row_1 = input('Type in the first row here. Put a space between each number: ')
            custom_row_2 = input('Type in the first row here. Put a space between each number: ')
            custom_row_3 = input('Type in the first row here. Put a space between each number: ')
            custom_puzzle = (custom_row_1.split(' '), custom_row_2.split(' '), custom_row_3.split(' ')) #Make lists in a tuple to represent the puzzle state
            for row in range(len(custom_puzzle)):
                for column in range(len(custom_puzzle)):
                    custom_puzzle[row][column] = int(custom_puzzle[row][column]) #Make every element an int so they can be modified later
            if (verbose):
                print(custom_puzzle)
            print_puzzle(custom_puzzle)
            return custom_puzzle
        else:
            puzzle_select = input('Invalid input. Type a choice again: ')
    return 0

def get_algorithm(puzzle, algorithm):
    chosen_algorithm = False
    while (chosen_algorithm is not True): #Choose algorithm depending on the user input
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
    while (chosen_difficulty is not True): #Choose puzzle depending on the user input
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

def get_goal_position(goal_state, misplaced_tile): #Helper function to get the goal coordinates for manhatten distance formula
    for row in range(len(goal_state)):
        for column in range(len(goal_state)):
            if (goal_state[row][column] == misplaced_tile):
                return row, column

def print_puzzle(puzzle): #Helper function to print out the puzzle in a neat manner
    for row in range(len(puzzle)):
        print('[', end = "")
        for column in range(len(puzzle) - 1):
            print(str(puzzle[row][column]) + ', ', end = "")
        print(str(puzzle[row][2]), end = "")
        print(']')
    print('\n')

#HEURISTIC FUNCTIONS
def uniform_cost():
    if (verbose):
        print('Uniform Cost Search was selected.')
    return 0 #Heuristic is always 0

def a_star_misplaced(puzzle):
    if (verbose):
        print('Misplaced Tile Heuristic was selected.')
    misplaced_tiles = 0
    for row in range(len(puzzle)): #Loop through the puzzle
        for column in range(len(puzzle)):
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
    for row in range(len(puzzle)):
        for column in range(len(puzzle)):
            if (puzzle[row][column] != goal_state[row][column]):
                if (puzzle[row][column] != 0): #need to account for an empty tile
                    misplaced_tile = puzzle[row][column] #Find the misplaced tile
                    misplaced_row = row #Have the row
                    misplaced_column = column #Have the column
                    goal_row, goal_column = get_goal_position(goal_state, misplaced_tile) #Run our helper function to find our goal coordinates for the formula to work
                    if (verbose):
                        print('The misplaced tile ' + str(misplaced_tile) + ' is ' + str(abs(goal_row - misplaced_row) + abs(goal_column - misplaced_column)) + ' spaces away.') 
                    manhatten += (abs(goal_row - misplaced_row) + abs(goal_column - misplaced_column)) #Uses the formula linked above
    if (verbose):
        print('The Manhatten Distance of the puzzle provided would be: ' + str(manhatten) + '\n')
    return manhatten

main()
