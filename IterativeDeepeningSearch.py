#! /usr/bin/env python

import numpy as np
import time

#Define the start state
start_state = np.array([[4,1,3],[0,2,6],[7,5,8]])

#Define the goal state
goal = np.array([[1,2,3],[4,5,6],[7,8,0]])

#Define predecessor for start_state
base = (np.array([0]*9)).reshape(3,3)  #creates a 3x3 array of zeros

#My input to the function
node_s = [None]
node_s[0] = np.array([base,start_state]) #creates an array of 2,3,3

#Initialise
new_nodes = []
all_nodes = []



#Defining the successor function

def switch_tile(zp,sf,node):
    switch = np.copy(node)
    temp = switch[zp[0]][zp[1]] #we are moving the tiles
    switch[zp[0],zp[1]] = switch[sf[0],sf[1]]
    switch[sf[0],sf[1]] = temp
    return switch


def successor(node):

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

        successor_state = successor_state + [down_shift_tile] #append to successor_state

    #shift the tile up
    shift_tile = np.copy(zero_tile)
    shift_tile[0] = shift_tile[0]-1

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2:
        up_shift_tile = switch_tile(zero_tile, shift_tile, node)
        up_shift_tile = np.array([node, up_shift_tile])

        successor_state = successor_state + [up_shift_tile]

    #shift the tile right
    shift_tile = np.copy(zero_tile)
    shift_tile[1] = shift_tile[1]+1

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2:
        right_shift_tile = switch_tile(zero_tile, shift_tile, node)
        right_shift_tile = np.array([node, right_shift_tile])

        successor_state = successor_state + [right_shift_tile]

    #shift the tile left
    shift_tile = np.copy(zero_tile)
    shift_tile[1] = shift_tile[1]-1

    if 0<=shift_tile[0]<=2 and 0<=shift_tile[1]<=2:
        left_shift_tile = switch_tile(zero_tile, shift_tile, node)
        left_shift_tile = np.array([node, left_shift_tile])

        successor_state = successor_state + [left_shift_tile]

    return successor_state #Return the list of all successor node_list

#Predecessor function
def predecessor(node):
    global path, all_nodes

    compare = node == start_state #checking if we have reached the start state

    if compare.all() == True:
        print(np.array(path)) #if so just print the node alone
        quit()

    else:
        for k in range(len(all_nodes)): #its a 2D array
            if (all_nodes[k][1]==node).all() == True: # we are checking if the node is same as the required node
                new_node = all_nodes[k][0] #we are taking the node which generated this node
                path = path + [new_node] #appending this to path
                predecessor(new_node)  #we are checking the previous state
            k += 1 #increment by 1


#Iterative Deepening Search function based on the pseudo code provided
def dpt_fst_sch_b(node_list, goal, Depth, Limit):
    global n_c, all_nodes, path

    compare = node_list[0][1] == goal #comparing if start node is same as goal

    if compare.all() == True:
        result = 1 #This stops the loop
        return result

    else:
        new_nodes = successor(node_list[0][1])
        n_c = n_c + len(new_nodes) #Total nodel generated


    all_nodes = all_nodes + new_nodes



    while new_nodes != [] and Depth < Limit:

        result = dpt_fst_sch_b(new_nodes, goal, Depth + 1, Limit) #increasing the depth and checking the next succesor node

        if result == 1:
            print('Goal state reached: \n{}'.format(new_nodes[0][1]))
            print('Solution found at depth {}'.format(Limit))
            print('Total nodes generated (repeated nodes included): {}'.format(n_c))
            print('Time Taken to solve: {} sec'.format(time.clock()-s_t))
            print('Predecessor path is as follows:')
            path = [new_nodes[0][1]]
            predecessor(new_nodes[0][1])
            quit()

        else:
            new_nodes = new_nodes[1:] #we remove the first node and continue
    return("No Solution")

result = 0

def Iterative_deepening(node_list, goal):
    global result

    Limit = 0

    while True:
        result = dpt_fst_sch_b(node_list, goal, 0, Limit) #we get 1 from the function
        Limit = Limit + 1 #This is nothing but depth



n_c = 0 #total nodes initiation

#calling my main function

s_t = time.clock() #getting the time
Iterative_deepening(node_s,goal)
