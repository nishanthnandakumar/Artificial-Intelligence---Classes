#! /usr/bin/env python

import numpy as np
import time

#Define the start state
start_state = np.array([[1,0,3],[4,2,6],[7,5,8]])

#Define the goal state
goal = np.array([[1,2,3],[4,5,6],[7,8,0]])

#Define predecessor for start_state
base = (np.array([0]*9)).reshape(3,3) #creates a 3x3 array of zeros

#My input to the function
node_list = [None]
node_list[0] = np.array([base,start_state]) #creates an array of 2,3,3

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
        print(successor_state)
    return successor_state #Return the list of all successor node_list

#Predecessor function
def predecessor(node):
    global path

    compare = node == start_state #checking if we have reached the start state

    if compare.all() == True:
        print(np.array(path)) #if so just print the node alone
        quit()

    else:
        for k in range(len(all_nodes)): #its a 2D array 
            if (all_nodes[k][1]==node).all() == True: # we are checking if the node is same as the required node
                new_node = all_nodes[k][0] #we are taking the node which generated this node
                path = path + [new_node] #appending this to path
                predecessor(new_node) #we are checking the previous state
            k += 1 #increment by 1


#Breadth first search function based on the pseudo code provided
def bdt_fst_sch(node_list, goal):
    global f_c, new_nodes
    global n_c, all_nodes, path

    new_nodes = [] #The list of new nodes which will be created

    for i in range(len(node_list)):
        node_element = node_list[i][1] == goal #we are taking the start_state node to compare with goal


        if node_element.all() == True:
            print('Goal state reached: \n{}'.format(node_list[i][1]))
            print('Solution found at depth {}'.format(f_c))
            print('Total nodes generated {}'.format(n_c))
            print('Time Taken to solve: {}'.format(time.clock()-s_t))
            print('Predecessor path is as follows:')
            path = [node_list[i][1]]
            predecessor(node_list[i][1])
            #print("solution found: \n {}".format(node_list[i][1])) #printing the solution found

        else:
            new_nodes = new_nodes + successor(node_list[i][1]) #successor nodes generated are appended to new_nodes

        i += 1 #we increment to check the next node in the node_list

    all_nodes = all_nodes + new_nodes
    n_c = n_c + len(new_nodes) #total nodes generated 

    if new_nodes != []:
        f_c += 1 #for depth increment
        bdt_fst_sch(new_nodes, goal) #new nodes as the input to search now we have new_nodes with 3 succesors which will be checked one after the other
    else:
        print('No solution')

f_c = 0
n_c = 0

#calling my main function

s_t = time.clock() #checks the total time
bdt_fst_sch(node_list,goal)
