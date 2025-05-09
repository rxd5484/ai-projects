############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Rakshit Dongre"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

from math import factorial

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return factorial(n * n) // (factorial(n) * factorial(n * n - n))

def num_placements_one_per_row(n):
    return n ** n

def n_queens_valid(board):
    n = len(board)
    for a in range(n):
        for b in range(a + 1, n):
            if (board[a] is board[b] or abs(board[a] - board[b])) == b - a:
                return False
    return True

def n_queens_helper(n, board):
    if len(board) is n:
        yield board
    else:
        for col in range(n):
            if all(col is not board[i] and (col - board[i]) is not (len(board) - i) and (col - board[i]) != -(len(board) - i) for i in range(len(board))):
                yield from n_queens_helper(n, board + [col])

def n_queens_solutions(n):
    yield from n_queens_helper(n, [])

print(num_placements_all(4))       #1.1
print(num_placements_one_per_row(4)) 

print(n_queens_valid([0, 0]))    # 1.2
print(n_queens_valid([0, 2]))  
print(n_queens_valid([0, 1]))  
print(n_queens_valid([0, 3, 1]))

solutions = n_queens_solutions(4)   #1.3
print(next(solutions)) 
print(next(solutions))  
print(list(n_queens_solutions(6)))
print(len(list(n_queens_solutions(8))))  




############################################################
# Section 2: Lights Out
############################################################
import random

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = [row[:] for row in board]  
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0

    def get_board(self):
        return [row[:] for row in self.board]
    
    def onoffs(self, row, col):
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.board[row][col] = not self.board[row][col]

    def perform_move(self, row, col):
        
        self.onoffs(row, col)  
        self.onoffs(row - 1, col)  
        self.onoffs(row + 1, col)  
        self.onoffs(row, col - 1)  
        self.onoffs(row, col + 1) 
    

    

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < 0.5:  
                    self.perform_move(row, col)

    def is_solved(self):
          return all(not light for row in self.board for light in row)
        

    def copy(self):
        return LightsOutPuzzle(self.get_board())

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(row, col)
                yield ((row, col), new_puzzle)
    
    def find_solution(self):
        from collections import deque

        queue = deque([(self, [])])  
        visited = set() 
        visited.add(tuple(map(tuple, self.board)))  

        while queue:
            present_puzzle, moves = queue.popleft()  

            
            if present_puzzle.is_solved():
                return moves  

          
            for move, new_puzzle in present_puzzle.successors():
                board_tuple = tuple(map(tuple, new_puzzle.board)) 
                if board_tuple not in visited:
                    visited.add(board_tuple) 
                    queue.append((new_puzzle, moves + [move])) 

      
        return None


        

    
def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False] * cols for k in range(rows)])


b = [[True, False], [False, True]]    #2.1
p = LightsOutPuzzle(b)
print(p.get_board())



b = [[True, True], [True, True]]      #2.1
p = LightsOutPuzzle(b)
print(p.get_board())



p = create_puzzle(2, 2)               #2.2
print(p.get_board())


p = create_puzzle(2, 3)               #2.2
print(p.get_board())




p = create_puzzle(3, 3)               #2.3
p.perform_move(1, 1)
print(p.get_board())



p = create_puzzle(3, 3)               #2.3
p.perform_move(0, 0)
print(p.get_board())

b = [[True, False], [False, True]]      #2.5
p = LightsOutPuzzle(b)
print(p.is_solved())



b = [[False, False], [False, False]]    #2.5
p = LightsOutPuzzle(b)
print(p.is_solved())




p = create_puzzle(3, 3)               #2.6
p2 = p.copy()
print(p.get_board() == p2.get_board()) 
p.perform_move(1, 1)
print(p.get_board() == p2.get_board())  


p = create_puzzle(2, 2)               #2.7
for move, new_p in p.successors():
    print(move,new_p.get_board())


for i in range(2,6):
    p=create_puzzle(i,i+1)
    print(len(list(p.successors())))    #2.7







                                      #2.8
puzzle = create_puzzle(3, 3)
print("When all lights are turned off:")
print(puzzle.get_board())



puzzle.perform_move(1, 1)
print("What happens to the board after move (1,1):")
print(puzzle.get_board())

puzzle.scramble()
print("What happens to the board after scramble?")
print(puzzle.get_board())


print("Puzzle solved?")
print(puzzle.is_solved())



puzzle_copy = puzzle.copy()
print("Copy:")
print(puzzle_copy.get_board())



print("successors:")
for move, new_puzzle in puzzle.successors():
    print( f"Move:{move}, Result: {new_puzzle.get_board()}")


solution = puzzle.find_solution()
print("Solution to solve")
print(solution)

puzzle.perform_move(0, 0)  
print("Original board:")
print(puzzle.get_board())

print("Copied board remains unchanged:")
print(puzzle_copy.get_board())


#2.8 continued
p = create_puzzle(2, 3)

for row in range(2):
    for col in range(3):
        p.perform_move(row, col)

p.find_solution()


b = [[False, False, False],
     [False, False, False]]
b[0][0] = True
p = LightsOutPuzzle(b)
print(p.find_solution() is None) 


solution = p.find_solution()
print("Solution to solve the puzzle:", solution)

b = [[False, False, False], [False, False, False]]
p = LightsOutPuzzle(b)


print("Solution to a solved puzzle:", p.find_solution())

b = [[False, False, False], [True, False, False]]
p = LightsOutPuzzle(b)


print("Solution to a  unsolvable puzzle:", p.find_solution())






############################################################
# Section 3: Linear Disk Movement
############################################################

from collections import deque

def solve_identical_disks(length, n):
    
    present_s_disk = tuple([1] * n + [0] * (length - n))
    goal = tuple([0] * (length - n) + [1] * n)

   
    ftier = deque([(present_s_disk, [])])  
    v = {present_s_disk}

    while ftier:
        present_s, moves = ftier.popleft()

      
        if present_s == goal:
            return moves

        
        for i in range(length):
            if present_s[i] == 1: 
                if i + 1 < length and present_s[i + 1] == 0:
                    x = list(present_s)
                    x[i], x[i + 1] = x[i + 1], x[i]
                    x= tuple(x)
                    if x not in v:
                        v.add(x)
                        ftier.append((x, moves + [(i, i + 1)]))

                
                if i + 2 < length and present_s[i + 2] == 0 and present_s[i + 1] == 1:
                    x = list(present_s)
                    x[i], x[i + 2] = x[i + 2], x[i]
                    x = tuple(x)
                    if x not in v:
                        v.add(x)
                        ftier.append((x, moves + [(i, i + 2)]))

    
    return None

print(solve_identical_disks(4, 2))        #3.1

print(solve_identical_disks(5, 2))

print(solve_identical_disks(4,3))

print(solve_identical_disks(5,3))




   

def solve_distinct_disks(length, n):
    from collections import deque

    
    initial = tuple(range(n)) + (None,) * (length - n)
    
    
    final_state = (None,) * (length - n) + tuple(reversed(range(n)))

    
    queue = deque([(initial, [])])
    
   
    v = {initial}

    
    while queue:
        current, moves = queue.popleft()
        
        
        if current == final_state:
            return moves
        
        
        for i in range(length):
            
            if current[i] is not None:
               
                for direction in [-1, 1]:
                    new_position = i + direction
                    if 0 <= new_position < length and current[new_position] is None:
                        y = list(current)
                        y[i], y[new_position] = None, current[i]  
                        y = tuple(y)
                        if y not in v:
                            v.add(y)
                            queue.append((y, moves + [(i, new_position)]))

                
                for direction in [-2, 2]:
                    new_position = i + direction
                    mid_position = i + direction // 2
                    if 0 <= new_position < length and current[new_position] is None and current[mid_position] is not None:
                        y = list(current)
                        y[i], y[new_position] = None, current[i]  
                        y = tuple(y)
                        if y not in v:
                            v.add(y)
                            queue.append((y, moves + [(i, new_position)]))

    
    return None

    
    
print(solve_distinct_disks(4, 2))


print(solve_distinct_disks(5, 2))


print(solve_distinct_disks(4, 3))


print(solve_distinct_disks(5, 3))               #3.2

    

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
I spent around 2 hours everyday since Sunday this week.
"""

feedback_question_2 = """
 The most challenging part of this assignment might have been implementing the breadth-first search (BFS) for both part-2 and 3 
 and finding the solution in the Lights Out puzzle and ensuring that all states were 
 tracked correctly in the visited set. It was very hard to see if the unsolvable puzzles returned None correctly.
"""

feedback_question_3 = """
I enjoyed the puzzle-solving aspects,especially the satisfaction of seeing BFS work for both solvable and unsolvable puzzles. 
 I wouldn’t change much honestly.
"""

#python3 ~/Downloads/homework1_lights_out_gui.py 3 3