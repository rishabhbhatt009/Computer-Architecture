# Your program will take one command line input, a filename, and output its results in a file named out.txt

import sys 
import os 

def input_file(filename):

    with open(filename) as file :
        ret = file.readlines() 
    
        proc1 = lambda x : x.strip().split(',')
        ret = list(map(proc1,ret))

        num_reg, width = list(map(int,ret[0]))
        proc2 = lambda x : [x[0]] + list(map(int,x[1:]))

        instructions = list(map(proc2,ret[1:]))

        return num_reg, width, instructions


def init():
    # map_table
    # ready_table

    # free list, head, tail
    
    return

def operation(type, source_reg, dest_reg):
    return 


def schedule() :
    # case for R, I, L, S
    return 
    

def main() : 
    command = sys.argv[1]
    file_name = sys.argv[2]
    num_reg, width,instructions = input_file(file_name)

    print(f'{command=}', f'{file_name=}', '-'*50,sep='\n')
    print('Input File','-'*50, sep='\n')
    print(f'{num_reg=}', f'{width=}',sep='\n')
    print(*instructions, sep='\n')
    print('-'*50)    

    schedule = [[0]*7 for i in range(len(instructions))]
    
    print('Output File','-'*50, sep='\n')
    for x in schedule : print(*x, sep=',')

    # Que for each resource 
    # Resource allocation in-order of exec






if __name__ == '__main__': 
    main()
