# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']
my_delta_name = ['v', '>', '^', '<']

def compute_value(grid,goal,cost):
    my_delta_name = ['v', '>', '^', '<']

    visit = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    police = [[" " for row in range(len(grid[0]))] for col in range(len(grid))] 
    value = []
    for i in range(len(grid)):
        value.append([99]*len(grid[0])) 
    queue = []
    
    current_grid = goal
    queue.append((current_grid[0],current_grid[1],0))
    visit[goal[0]][goal[1]] = 1
    value[goal[0]][goal[1]] = 0
    police[goal[0]][goal[1]] = "*"
    while len(queue):
        current_grid = queue[0]
        for item in queue:
            if current_grid[2] > item[2]:
                current_grid = item
        visit[current_grid[0]][current_grid[1]] = 1
        queue.remove(current_grid) 
        for index,move in enumerate(delta):
                new_x = current_grid[0] + move[0]
                new_y = current_grid[1] + move[1]

                if not (new_x < 0 or new_y < 0 or new_x >= len(visit) or new_y >= len (visit[0])):
                    if (not visit[new_x][new_y]) and (grid[new_x][new_y] == 0):
                         
                        if value[new_x][new_y] > value[current_grid[0]][current_grid[1]] + 1:
                            police[new_x][new_y] = my_delta_name[index]
                            value[new_x][new_y] = value[current_grid[0]][current_grid[1]] + 1
                        queue.append((new_x,new_y,value[new_x][new_y]))
    return police 
result = compute_value(grid,goal,cost)
for i in result:
    print(i)