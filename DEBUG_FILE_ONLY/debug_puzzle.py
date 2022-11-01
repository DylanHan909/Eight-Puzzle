import copy
from queue import PriorityQueue
from tabnanny import verbose
import time

goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0)) #Tuples are faster than embedded lists
                                                #Changed inner lists to tuples to  allow for a hashable set for repeat states
verbose = False #A way to have debugging outputs for testing purposes

#EMPTY TILE IS REPRESENTED BY 0
#Changed node structure a lot
#Keeps track of the puzzle state, the path taken to solve the puzzle, the heuristic from our algorithms (h(n)), and our current depth (g(n))
class Node:
    def __init__ (self, puzzle):
        self.puzzle = puzzle
        self.path = []
        self.zeroRow = 0 #Track the zeroth position of a puzzle
        self.zeroColumn = 0  #Track the zeroth position of a puzzle
        self.heuristic = 0 #h(n)
        self.depth = 0 #g(n)
    
    #Implemented so the priorityqueue can compare objects and automatically preceed with the node with the lowest cost
    #https://stackoverflow.com/questions/9292415/i-notice-i-cannot-use-priorityqueue-for-objects
    def __lt__(self, other):
        self.distance = self.depth + self.heuristic 
        other.distance = other.depth + other.heuristic
        if (other.distance == self.distance):
            if (verbose):
                print("Tiebreaker found, sorting by lowest depth now.")                
            else:
                return other.depth > self.depth #Done because my search was bugged, when f(n) of two nodes equaled each other, it would choose a larger depth randomly, choose the smaller depth manually to solve 
        else:
            return other.distance > self.distance

#Driver FUNCTION
def main():
    debugging = input("DEBUGGING ONLY: PRESS 1 FOR EXTRA OUTPUTS: ")
    if (debugging == '1'):
        global verbose
        verbose = True
    puzzle = get_puzzle()
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhatten Distance Heuristic: ")
    while (int(algorithm) < 1 or int(algorithm) > 3):
        algorithm = input("Incorrect input, please choose the search type again: ")
    start = time.time()
    goal_state, expanded_nodes, max_queue_size  = search_puzzle(puzzle, algorithm)
    end = time.time()
    search_time = end - start
    print('Goal state!')
    print('The path to get to the node was: ')
    move_count = 0
    for element in range(len(goal_state.path)):
        if type(goal_state.path[element]) is tuple: #If the element in the list is a puzzle
            print_puzzle(goal_state.path[element]) #Print it
        else: #Otherwise
            move_count += 1
            print('Move ' + str(move_count) + ': ' + goal_state.path[element]) #Print the current move # and the direction a tile was moved here
    print('Solution depth was ' + str(goal_state.depth))
    print('Number of nodes expanded: ' + str(expanded_nodes)) #Minus 1 because it keeps into account expanding the first state
    print('Max queue size: ' + str(max_queue_size))
    print ('Search time was ' + str(round(search_time, 5))  + ' seconds')
    return 0

#SEARCH RELATED FUNCTIONS
def search_puzzle(puzzle, algorithm):
    #Using priority queue for the node frontier: https://docs.python.org/3/library/queue.html
    #HEAVILY inspired from psuedocode in: https://www.dropbox.com/sh/cp90q8nlk8od4cw/AADK4L3qOh-OJtFzdi_8Moaka?dl=0&preview=Project_1_The_Eight_Puzzle_CS_170_2022.pdf
    #INSPIRED BY https://plainenglish.io/blog/uniform-cost-search-ucs-algorithm-in-python-ec3ee03fca9f

    curr_puzzle = Node(puzzle) #Initial state is a Node of the chosen puzzle
    curr_puzzle.heuristic = get_algorithm(curr_puzzle.puzzle, algorithm) #Get algorithm via user input choice
    working_queue = PriorityQueue() #Chose priority queue to sort by the lowest heuristic when comparing each node (uses __lt__ operator)
    repeated_states = set() #Changed to a set, and modified puzzles to be all tuples to make repeat checking MUCH faster
    max_queue_size = 0 #Max queue size
    expanded_nodes = 0 #Node coun 
    curr_puzzle.path += [curr_puzzle.puzzle]

    working_queue.put(curr_puzzle) #Put initial state into the priority queue
    repeated_states.add(curr_puzzle.puzzle) #Add repeat state to the repeat set
    max_queue_size += 1 #Take into account the initial starting node
    track_time = time.time()
    max_time = 900 #15 minutes total for program to run
    while (working_queue.qsize() != 0):
        #https://raspberrypi.stackexchange.com/questions/15613/stop-program-after-a-period-of-time: Force exit the program after 15 mins
        if (time.time() >= track_time + max_time):
            print('Program time is up! Ending program now!')
            exit(0)
        max_queue_size = max(working_queue.qsize(), max_queue_size) #change max queue size to the biggest size between the working queue and the max queue
        curr_puzzle = working_queue.get() #Get the smallest heuristic node from the queue
        if curr_puzzle.puzzle == goal_state: #If you match the goal state
            return curr_puzzle, expanded_nodes, max_queue_size
        
        if (verbose):
            print('Puzzle will now be expanded...\n')
        expanded_nodes += 1 #Expand the node count per new node popped out of the queue
        print('The best state to expand with a g(n) = ' + str(curr_puzzle.depth) + ' and h(n) = ' + str(curr_puzzle.heuristic) + ' is...') #output the chosen state's heuristic
        print_puzzle(curr_puzzle.puzzle) #Print the puzzle

        node_expansion(curr_puzzle, repeated_states, working_queue, algorithm) #Expand nodes
    else:
        print('No solution')
        exit(0)

def node_expansion(puzzle, repeated_states, working_queue, algorithm):
    for row in range(len(puzzle.puzzle)): #range done so it can work for 15+ size puzzles
        for column in range(len(puzzle.puzzle)):
            if (puzzle.puzzle[row][column] == 0): #tile with the empty space
                puzzle.zeroRow = row #Row of the 0 element
                puzzle.zeroCol = column #Column of the 0 element
    if (puzzle.zeroRow < (len(puzzle.puzzle) - 1)): #If row < the bottom row
        move_tile(puzzle, (puzzle.zeroRow + 1), puzzle.zeroCol, repeated_states, ' upwards.', working_queue, algorithm)
    if (puzzle.zeroRow != 0): #if row > the top row
        move_tile(puzzle, (puzzle.zeroRow - 1), puzzle.zeroCol, repeated_states, ' downwards.', working_queue, algorithm)
    if (puzzle.zeroCol < (len(puzzle.puzzle) - 1)): #if column is to the left of the rightmost column
        move_tile(puzzle, puzzle.zeroRow, (puzzle.zeroCol + 1), repeated_states, ' leftwards.', working_queue, algorithm)
    if (puzzle.zeroCol != 0): #If the column is to the right of tthe leftmost column
        move_tile(puzzle, puzzle.zeroRow, (puzzle.zeroCol - 1), repeated_states, ' rightwards.', working_queue, algorithm)

#HELPER FUNCTIONS
#NEED DEEP COPY BECAUSE SHALLOW COPY SCREWED UP COPYING OBJECTS 
def move_tile(puzzle, new_row, new_column, repeated_states, direction, working_queue, algorithm): #WHERE CHILDREN ARE GENERATED AND ADDED INTO THE QUEUE
    path = []
    child = copy.deepcopy(puzzle.puzzle) #DEEP COPY because shallow copy is just a copy by reference, the original object still changes
    path += ['Moving tile ' + str(child[new_row][new_column]) + direction] #Adding the steps to solve the puzzle to the temp variable path
    child = convert_to_list(child) #Convert child to a list so we can modify the data inside the tuple
    child[puzzle.zeroRow][puzzle.zeroCol] = child[new_row][new_column] #Slide the tile to the position passed in the node expansion function
    child[new_row][new_column] = 0 #Change the spot to an empty spot that was moved
    child = convert_to_tuple(child) #Reconvert the data back into a tuple
    path += [child] #Adding the puzzle to the current path
    if (verbose):
        print('Moving tile ' + str(child[new_row][new_column]) + direction)
    if child not in repeated_states: #If this new puzzle is NOT a repeat 
        repeated_states.add(child) #Move the new puzzle into our repeat states
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

def convert_to_list(puzzle): #Convert tuple to a list for modifying the puzzle
    temp_list = []
    for row in range(len(puzzle)):
        temp_list.append(list(puzzle[row]))
    temp_list = tuple(temp_list)
    return temp_list

def convert_to_tuple(puzzle): #Convert back to a tuple
    temp_tuple = ()
    tuple_list = []
    for row in range(len(puzzle)):
        temp_tuple = tuple(puzzle[row])
        tuple_list.append(temp_tuple)
    tuple_list = tuple(tuple_list)
    return tuple_list

def get_puzzle():
    chosen_puzzle = False
    puzzle_select = input("Welcome to the 8-puzzle solver! Type '1' for a set puzzle. Type '2' for a custom puzzle: ")
    while (chosen_puzzle is not True):
        if puzzle_select == '1':
            return difficulty_select() #Function to choose a pre-made puzzle
        elif puzzle_select == '2':
            row_count = int(input('Enter the amount of rows you want for the puzzle. Below 1 will default to 3 rows: ' )) #Future proofing the program
            if (row_count < 1):
                row_count = 3
            print('Put in a custom puzzle (0 is a blank space): ')
            custom_puzzle = [] #Store initially as a list to easily add elements via a loop
            for row in range(row_count): #Loop to make lists per row entered in as an input for the puzzle
                custom_row = input('Type in row number ' + str(row + 1) + ' here. Put a space between each number: ')
                custom_puzzle.append(custom_row.split(' ')) #Split elements by space 
            custom_puzzle = tuple(custom_puzzle) #Convert the list into a tuple
            for row in range(len(custom_puzzle)): 
                for column in range(len(custom_puzzle)):
                    custom_puzzle[row][column] = int(custom_puzzle[row][column]) #Make every element an int so they can be modified later
            custom_puzzle = convert_to_tuple(custom_puzzle)
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
    all_puzzles = (((1, 2, 3), (4, 5, 6), (7, 8, 0)), ((1, 2, 3), (4, 5, 6), (0, 7, 8)), ((1, 2, 3), (5, 0, 6), (4, 7, 8)), 
                   ((1, 3, 6), (5, 0, 2), (4, 7, 8)), ((1, 3, 6), (5, 0, 7), (4, 8, 2)), ((1, 6, 7), (5, 0, 3), (4, 8, 2)), 
                   ((7, 1, 2), (4, 8, 5), (6, 3, 0)), ((0, 7, 2), (4, 6, 1), (3, 5, 8)), ((8, 6, 7), (2, 5, 4), (3, 0, 1))) 
    difficulty = int(input("Select difficulty from 1 to 9 (Lower = Easier, Difficulty of  >= 8 might take a LONG time to finish depending on the algorithm): "))
    chosen_difficulty = False
    while (chosen_difficulty is not True):
        if ((difficulty > 0) and (difficulty < 10)):
            print_puzzle(all_puzzles[difficulty - 1])
            return all_puzzles[difficulty - 1]
        else:
            difficulty = int(input("Incorrect input, please choose the difficulty again: "))

def get_goal_position(goal_state, misplaced_tile): #Helper function to get the goal coordinates for manhatten distance formula
    for row in range(len(goal_state)):
        for column in range(len(goal_state)):
            if (goal_state[row][column] == misplaced_tile):
                return row, column

def print_puzzle(puzzle): #Helper function to print out the puzzle in a neat manner
    printed_puzzle = ''
    for row in range(len(puzzle)):
        printed_puzzle += str(puzzle[row])
        printed_puzzle += '\n'
    print(printed_puzzle)
    if (verbose):
        return printed_puzzle

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