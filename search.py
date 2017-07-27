# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']


def search(grid,init,goal,cost):

    visit = []
    for i in range(len(grid)):
        visit.append([0]*len(grid[0]))
    expand = []
    for i in range(len(grid)):
        expand.append([-1]*len(grid[0]))

    expand_ord = 0
    
    open_lst = [[0,0,0]]
    visit[0][0] = 1
    while len(open_lst):
        # get the min g_value
        best_item = open_lst[0]
        for item in open_lst:
            if item[0] < best_item[0]:
                best_item = item
        open_lst.remove(best_item)
        expand[best_item[1]][best_item[2]] = expand_ord 
        expand_ord += 1
        path = best_item

        '''
        print ("take list item")
        print(best_item)
        print("----")
        '''
        for move in delta:
            new_g = best_item[0] + 1
            new_x = best_item[1] + move[0]
            new_y = best_item[2] + move[1]
            #check boundary
            if not (new_x < 0 or new_y < 0 or new_x >= len(visit) or new_y >= len (visit[0])):
                if not visit[new_x][new_y] and grid[new_x][new_y] == 0:
                    visit[new_x][new_y] = 1
                    open_lst.append([new_g,new_x,new_y])
        '''
        print("new open list")
        for item in open_lst:
            print (item)
        print("----")
        '''
    return expand 
print(search(grid,init,goal,cost))