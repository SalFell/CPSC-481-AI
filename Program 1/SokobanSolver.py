import tkinter as tk
from tkinter import messagebox, Canvas
from queue import PriorityQueue
import copy
import os
import time

# gui global variables
gui_boxRobot = []
gui_wallsStorageSpaces = []
gui_possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}
gui_maxRowLength = 0
gui_lines = 0
gui_tile_size = 50  # Size of each square tile
board=[]
maxLength=0

boxRobot=[]
wallsStorageSpaces=[]
possibleMoves = {'U':[-1,0], 'R':[0,1],'D':[1,0],'L':[0,-1]}
solutionMoveSet=[]

maxRowLength = 0	
lines=0
input_file = 'input.txt'

try:
	with open(input_file, 'r') as file:
        # read the file line by line
		for line in file:
			if line!="":
				lines+=1
				board.append(line)
			if len(line)>maxRowLength:
				maxRowLength=len(line)
        
		time_start = time.perf_counter()
		
		for i in range(0,lines):
			boxRobot.append([])
			wallsStorageSpaces.append([])
			for j in range(0,maxRowLength):
				boxRobot[-1].append('-')
				wallsStorageSpaces[-1].append('-')

		for i in range(0,len(board)):
			if len(board[i])<maxRowLength:
				for j in range(len(board[i]),maxRowLength):
					board[i]+='O'

		for i in range(0,len(board)):
			for j in range(0,maxRowLength):
				if board[i][j]=='B' or board[i][j]=='R':
					boxRobot[i][j]=board[i][j]
					wallsStorageSpaces[i][j]=' '
				elif board[i][j]=='S' or board[i][j]=='O':
					wallsStorageSpaces[i][j] = board[i][j]
					boxRobot[i][j] = ' '
				elif board[i][j]==' ':
					boxRobot[i][j] = ' '
					wallsStorageSpaces[i][j]=' '
				elif board[i][j] == '*':
					boxRobot[i][j] = 'B'
					wallsStorageSpaces[i][j] = 'S'
				elif board[i][j] == '.':
					boxRobot[i][j] = 'R'
					wallsStorageSpaces[i][j] = 'S'

		storages = []
		for i in range(0,lines):
			for j in range(0,maxRowLength):
				if wallsStorageSpaces[i][j]=='S':
					storages.append([i,j])

		# print storages
		def manhattan(state):
			distance = 0
			for i in range(0,lines):
				for j in range(0,maxRowLength):
					if state[i][j] == 'B':
						temp= 9999999
						for storage in storages:
							distanceToNearest = abs(storage[0]-i)+abs(storage[1]-j)
							if temp > distanceToNearest:
								temp = distanceToNearest
						# print i,j,temp
						distance+=temp
			return distance

		print("Solving using A star with Manhattan as heuristic\n")

		movesList = []
		visitedMoves=[]

		queue = PriorityQueue()
		source = [boxRobot,movesList]
		if boxRobot not in visitedMoves:
			visitedMoves.append(boxRobot)
		queue.put((manhattan(boxRobot),source))
		robot_x = -1
		robot_y = -1
		completed = 0

		while not queue.empty() and completed==0:
			temp = queue.get()
			curPosition = temp[1][0]
			movesTillNow = temp[1][1]
			stepsTillNow= len(movesTillNow)
			for i in range(0,lines):
				for j in range(0,maxRowLength):
					if curPosition[i][j]=='R':
						robot_y = j
						robot_x = i
						break
				else:
					continue
				break

			for key in possibleMoves:
				robotNew_x = robot_x+possibleMoves[key][0]
				robotNew_y = robot_y+possibleMoves[key][1] 
				curPositionCopy = copy.deepcopy(curPosition)
				movesTillNowCopy = copy.deepcopy(movesTillNow)

				if curPositionCopy[robotNew_x][robotNew_y] == 'B':
					boxNew_x = robotNew_x + possibleMoves[key][0]
					boxNew_y = robotNew_y + possibleMoves[key][1]
					if curPositionCopy[boxNew_x][boxNew_y]=='B' or wallsStorageSpaces[boxNew_x][boxNew_y]=='O':
						continue
					else:
						curPositionCopy[boxNew_x][boxNew_y]='B'
						curPositionCopy[robotNew_x][robotNew_y] = 'R'
						curPositionCopy[robot_x][robot_y] = ' '
						if curPositionCopy not in visitedMoves:
							matches= 0
							for k in range(0,lines):
								for l in range(0,maxRowLength):
									if wallsStorageSpaces[k][l]=='S':
										if curPositionCopy[k][l]!='B':
											matches=1
							movesTillNowCopy.append(key)
							if matches == 0:
								completed = 1
								solutionMoveSet = movesTillNowCopy
								print(movesTillNowCopy)
							else:
								queue.put((manhattan(curPositionCopy)+stepsTillNow,[curPositionCopy,movesTillNowCopy]))
								visitedMoves.append(curPositionCopy)
				else:
					if wallsStorageSpaces[robotNew_x][robotNew_y]=='O' or curPositionCopy[robotNew_x][robotNew_y]!=' ':
						continue
					else:
						curPositionCopy[robotNew_x][robotNew_y]='R'
						curPositionCopy[robot_x][robot_y]=' '
						if curPositionCopy not in visitedMoves:
							movesTillNowCopy.append(key)
							queue.put((manhattan(curPositionCopy)+stepsTillNow,[curPositionCopy,movesTillNowCopy]))
							visitedMoves.append(curPositionCopy)

		if completed==0:
			print("Can't make it")

		time_end = time.perf_counter()
		print("Run time: "+str(time_end - time_start))
except FileNotFoundError:
	print(f"File '{input_file}' not found.")
except IOError:
    print(f"Error reading from file '{input_file}'.")



# Initialize the main Tkinter window
root = tk.Tk()
root.title("Sokoban Solver")
canvas = Canvas(root)
canvas.pack()

def read_board_from_file(filename):
    global gui_lines, gui_maxRowLength, gui_board, gui_boxRobot, gui_wallsStorageSpaces
    gui_lines, gui_maxRowLength = 0, 0
    gui_board, gui_boxRobot, gui_wallsStorageSpaces = [], [], []
    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip()
            if line:
                gui_lines += 1
                gui_board.append(line)
                gui_maxRowLength = max(gui_maxRowLength, len(line))
                
def draw_board():
    canvas.delete('all')  
    for y, row in enumerate(gui_boxRobot):
        for x, cell in enumerate(row):
            color = 'white'  
            
            if cell == 'B' and gui_wallsStorageSpaces[y][x] == 'S':
                color = 'purple'  
            elif cell == 'B':
                color = 'blue' 
            elif cell == 'R':
                color = 'red' 
            elif gui_wallsStorageSpaces[y][x] == 'S':
                color = 'green'  
            elif gui_wallsStorageSpaces[y][x] == 'O':
                color = 'grey'  
            
            canvas.create_rectangle(x * gui_tile_size, y * gui_tile_size, (x + 1) * gui_tile_size, (y + 1) * gui_tile_size, fill=color)
    
    canvas.pack()
    root.update_idletasks()  

def initialize_board_state():
    global gui_boxRobot, gui_wallsStorageSpaces
    for i in range(gui_lines):
        gui_boxRobot.append([' ']*gui_maxRowLength)
        gui_wallsStorageSpaces.append([' ']*gui_maxRowLength)

    for y, row in enumerate(gui_board):
        for x, char in enumerate(row):
            if char in 'BR':
                gui_boxRobot[y][x] = char
                gui_wallsStorageSpaces[y][x] = ' '
            elif char in 'SO':
                gui_wallsStorageSpaces[y][x] = char
                gui_boxRobot[y][x] = ' '
            elif char == '*':
                gui_boxRobot[y][x] = 'B'
                gui_wallsStorageSpaces[y][x] = 'S'
            elif char == '.':
                gui_boxRobot[y][x] = 'R'
                gui_wallsStorageSpaces[y][x] = 'S'

def load_and_draw_board():
    filename = file_entry.get()
    if not os.path.isfile(filename):
        messagebox.showerror("Error", f"File '{filename}' not found.")
        return
    read_board_from_file(filename)
    initialize_board_state()
    
    canvas.config(width=gui_maxRowLength*gui_tile_size, height=gui_lines*gui_tile_size)
    draw_board()
    file_label.pack_forget()
    file_entry.pack_forget()
    submit_button.config(text="Solve", command=solve_puzzle)
    submit_button.pack(pady=10)


def apply_moves(moves):
    global gui_boxRobot, gui_wallsStorageSpaces
    robot_pos = next((i, j) for i, row in enumerate(gui_boxRobot) for j, val in enumerate(row) if val == 'R')
    
    for move in moves:
        dx, dy = gui_possibleMoves[move]
        next_pos = (robot_pos[0] + dx, robot_pos[1] + dy)

        if gui_boxRobot[next_pos[0]][next_pos[1]] == 'B':
            box_new_pos = (next_pos[0] + dx, next_pos[1] + dy)
            gui_boxRobot[box_new_pos[0]][box_new_pos[1]] = 'B'  
            gui_boxRobot[next_pos[0]][next_pos[1]] = 'R'  
        else:
            gui_boxRobot[next_pos[0]][next_pos[1]] = 'R' 
        
        gui_boxRobot[robot_pos[0]][robot_pos[1]] = ' '  
        robot_pos = next_pos 

        draw_board()  
        root.update_idletasks()  
        time.sleep(0.5) 


def solve_puzzle():
    apply_moves(solutionMoveSet)
    messagebox.showinfo("Solved", "Puzzle solved with moves: " + ' '.join(solutionMoveSet))

# Entry widget for filename
file_label = tk.Label(root, text="Enter the filename of the Sokoban board:")
file_label.pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()

# Submit button 
submit_button = tk.Button(root, text="Load Board", command=load_and_draw_board)
submit_button.pack(pady=10)

root.mainloop()
