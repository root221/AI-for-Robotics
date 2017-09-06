# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
actions = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 2] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):

  policy2D = [[ " " for row in range(len(grid[0]))] for col in range(len(grid))]
  policy = [[3 for row in range(len(grid[0]))] for col in range(len(grid))]
  value = [[ 999 for row in range(len(grid[0]))] for col in range(len(grid))]
          
  visit = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
  queue = []

  queue.append((init[0],init[1],init[2],0))
  visit[init[0]][init[1]] = 1
  value[init[0]][init[1]] = 0

  while len(queue):
    best_item = queue[0]
    for item in queue:
      if best_item[3] > item[2]:
        best_item = item
    visit[best_item[0]][best_item[1]] = 1
    queue.remove(best_item) 
    if(best_item[0] == goal[0] and best_item[1] == goal[1]):
      goal_orientation = best_item[2]
    for index,action in enumerate(actions):
      new_orientation = (best_item[2] + action) % 4
      new_x = best_item[0] + forward[new_orientation][0]
      new_y = best_item[1] + forward[new_orientation][1]
      
      # check boundary
      if not(new_x < 0  or new_y < 0 or new_x >= len(grid) or new_y >= len(grid[0])):
        if grid[new_x][new_y] == 0 and visit[new_x][new_y] == 0:
          if value[new_x][new_y] > best_item[3] + cost[index]:
            value[new_x][new_y] = best_item[3] + cost[index]
            print("policy")
            print(new_x,new_y,index,value[new_x][new_y])
            policy[new_x][new_y] = index
            
          queue.append((new_x,new_y,new_orientation,value[new_x][new_y]))

  policy2D[goal[0]][goal[1]] = "*"
  x = goal[0]
  y = goal[1]
  
  orientation = goal_orientation
  
  while x != init[0] or y!= init[1]:
    new_orientation =  (orientation - actions[policy[x][y]]) % 4
    
    new_x = x -  forward[orientation][0]
    new_y = y -  forward[orientation][1]
    
    policy2D[new_x][new_y] = action_name[policy[x][y]] 
    x = new_x
    y = new_y
    orientation = new_orientation
  return policy

result = optimum_policy2D(grid,init,goal,cost)
for i in result:
  print(i)
