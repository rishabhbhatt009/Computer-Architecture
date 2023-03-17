import sys 
import os 
from helper import simulator

global_vars = {
    'num_reg' : 0,
    'width' : 0,
    'instructions' : [],
    'schedule_map' : [],
    'cycle' : 0,

    'mapTable' : [i for i in range(32)],
    'readyList' : [True for i in range(32)],
    'freeList' : []
}

def parse_input(filename):

    with open(filename) as file :
        ret = file.readlines() 
    
        proc1 = lambda x : x.strip().split(',')

        ret = list(map(proc1,ret))
        num_reg, width = list(map(int,ret[0]))
        instructions = []

        for idx, line in enumerate(ret[1:]):            
            
            meta = {
                'icount' : idx, 
                'itype' : line[0], 
                'arg1' : int(line[1]), 
                'arg2' : int(line[2]), 
                'arg3' : int(line[3])
            }
            instructions.append(meta)

        return num_reg, width, instructions

def generate_output(schedule):
    print('Output File','-'*50, sep='\n')
    for x in schedule : print(*x, sep=',')

def init():
    # map_table
    # ready_table
    # free list, head, tail
    # schedule 
    
    # Ideas
    #   - Que for each resource 
    #   - Resource allocation in-order of exec

    
    return

def operation(type, source_reg, dest_reg):
    return 

def main() : 
    command = sys.argv[1]
    file_name = sys.argv[2]
    
    global_vars['num_reg'], global_vars['width'], global_vars['instructions'] = parse_input(file_name)
    global_vars['schedule_map'] = [[0]*7 for i in range(len(global_vars['instructions']))]
    global_vars['freeList'] = [i for i in range(32, global_vars['num_reg'])]

    # print(f'{command=}', f'{file_name=}', '-'*50,sep='\n')
    # print('Input File','-'*50, sep='\n')
    # print(f'{num_reg=}', f'{width=}',sep='\n')
    # print(*instructions, sep='\n')
    # print('-'*50)    
     
    # update schedule 
    obj1 = simulator(global_vars['instructions'], global_vars['schedule_map'])
    global_vars['schedule_map'] = obj1.schedule()

    # generate output
    generate_output(global_vars['schedule_map'])


if __name__ == '__main__': 
    main()
