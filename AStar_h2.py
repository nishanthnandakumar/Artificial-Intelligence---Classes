#! /usr/bin/env python
import numpy as np
import time

#Define the start state
start_state = np.array([[2,0,4],[6,7,1],[8,5,3]])

#Define the goal state
goal = np.array([[1,2,3],[4,5,6],[7,8,0]])

#Define predecessor for start_state
base = (np.array([0]*9)).reshape(3,3) #creates a 3x3 array of zeros

#My input to the function
node_s = [None]
node_s[0] = np.array([base,start_state, 0, 0]) #creates an array 


#Initialise
new_nodes = []
all_nodes = []

#1. All nodes generated in this process are saved in a list for finding the predecessor.
#2. Each node is a list of of [x,y,z,w] type where x is the predecossor of y.
#3. x and y are 2 dimensional numpy arrays.
#4. z is the value of Heuristics cost function.
#5. w is the depth value of said sucessor node.
#Calculating Heuristics

def h2(current_node, goal):


    target_node = goal #reassigning the goal to target node
    h2 = 0 #initiating h2

    for i in range(1,9):
        compare = (np.argwhere(current_node == i)) == (np.argwhere(target_node == i)) #comparing the positions of the tiles 
        if compare.all() == False:
            diff_vec = (np.argwhere(target_node == i)-np.argwhere(current_node == i)).flatten() #here we are calculating the distance of a single tile by subtracting the values
            h2 = h2 + abs(diff_vec[0]) + abs(diff_vec[1]) #adding the value obtained to heuristics
    return h2

#Defining the successor function

# 3 arguments > 2 positions to be exchanged and the Node in which this has to be done

def switch_tile(zp,sf,node):
    switch = np.copy(node)
    temp = switch[zp[0]][zp[1]] #we are moving the tiles
    switch[zp[0],zp[1]] = switch[sf[0],sf[1]]
    switch[sf[0],sf[1]] = temp
    return switch

def successor(node, level): #Each node is a list of of [x,y,z,w] type where x is the predecossor of y.
    global all_nodes

    #First we need to know where th zero tile is located
    zero_tile = np.argwhere(node==0) #Gives the location of zero in the node
    zero_tile = zero_tile.flatten() #converts 2D to 1D

    successor_state = [] #Empty list of succesor states

    #shift the tile down
    shift_tile = np.copy(zero_tile)
    shift_tile[0] = shift_tile[0]+1 #shifting the zero tile down

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2: #checking if it is within the boundary
        down_shift_tile = switch_tile(zero_tile, shift_tile, node) #move the zero tile down and put the tile in zero position
        down_shift_tile = np.array([node, down_shift_tile])

        all_nodes = all_nodes + [down_shift_tile]
        heuristics = h2(down_shift_tile[1], goal) + level + 1 #we are calculating f(x) where level is nothing but depth
        down_shift_tile = np.array([down_shift_tile[0], down_shift_tile[1], heuristics, level+1]) #level is increased by one after generating the successors
        successor_state = successor_state + [down_shift_tile] #append to successor_state

    #shift the tile up
    shift_tile = np.copy(zero_tile)
    shift_tile[0] = shift_tile[0]-1

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2:
        up_shift_tile = switch_tile(zero_tile, shift_tile, node)
        up_shift_tile = np.array([node, up_shift_tile])

        all_nodes = all_nodes + [up_shift_tile]
        heuristics = h2(up_shift_tile[1], goal) + level + 1
        up_shift_tile = np.array([up_shift_tile[0], up_shift_tile[1], heuristics, level+1])
        successor_state = successor_state + [up_shift_tile]

    #shift the tile right
    shift_tile = np.copy(zero_tile)
    shift_tile[1] = shift_tile[1]+1

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2:
        right_shift_tile = switch_tile(zero_tile, shift_tile, node)
        right_shift_tile = np.array([node, right_shift_tile])

        all_nodes = all_nodes + [right_shift_tile]
        heuristics = h2(right_shift_tile[1], goal) + level + 1
        right_shift_tile = np.array([right_shift_tile[0], right_shift_tile[1], heuristics, level+1])
        successor_state = successor_state + [right_shift_tile]

    #shift the tile left
    shift_tile = np.copy(zero_tile)
    shift_tile[1] = shift_tile[1]-1

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2:
        left_shift_tile = switch_tile(zero_tile, shift_tile, node)
        left_shift_tile = np.array([node, left_shift_tile])

        all_nodes = all_nodes + [left_shift_tile]
        heuristics = h2(left_shift_tile[1], goal) + level + 1
        left_shift_tile = np.array([left_shift_tile[0], left_shift_tile[1], heuristics, level+1])
        successor_state = successor_state + [left_shift_tile]

    return successor_state #Return the list of all successor node_list

#Predecessor function
def predecessor(node):
    global path, all_nodes

    compare = node == start_state #checking if we have reached the start state

    if compare.all() == True:
        print(np.array(path)) #if so just print the node alone
        quit()
    #Find element where 'y' array is eqaul to the node for which predecessor is to be found
    #Once done, take the 'x' array > this is one of the path elements
    #Set this 'x' and new 'y' and find its predecessor until we reach start node.
    
    else:
        for k in range(len(all_nodes)):  #its a 2D array
            if (all_nodes[k][1]==node).all() == True: # we are checking if the node is same as the required node
                new_node = all_nodes[k][0] #we are taking the node which generated this node
                path = path + [new_node] #appending this to path
                predecessor(new_node) #we are checking the previous state
            k += 1 #increment by 1

#Main function based on pseudo code
def a_star_h2(node_list, goal):
    global result, f_c, all_nodes, path, visited_nodes

    f_c = 0 #Intializing depth counting variable
    n_c = 0 #Intializing node counting variable
    level = 0 #This is the level g(x)


    while True:
        if node_list == []:
            result = 0
            print('Nothing!')
            return result

        node = node_list[0][1]
        level = node_list[0][3]
        node_list = node_list[1:]

        compare = node == goal
        if compare.all() == True:
            result = 1
            print('Goal state reached: \n {}'.format(node))
            print('Solution found at depth {}'.format(level))
            print('Total nodes generated {}'.format(n_c))
            print('Time taken to solve: {} sec'.format(time.clock()-s_t))
            print('Predecessor path is as follows:')
            path = [node]
            predecessor(node)
            return result


        successor_state = successor(node,level)

        node_list = successor_state + node_list

        node_list = sorted(node_list, key = lambda x:x[2]) #we are sorting the nodelist based on the heuristic value in the 2 position of the array

        f_c += 1 #increasing the depth count
        n_c = n_c + len(successor_state)


result = 0
s_t = time.clock()

result = a_star_h2(node_s, goal)
