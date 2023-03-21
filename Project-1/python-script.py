import sys 
import os 
from helper import simulator

global_vars = {
    'num_reg' : 0,
    'width' : 0,
    'instructions' : [],
    'schedule_map' : [],
    'cycle' : 0,

    'mapTable' : {},
    'readyTable' : {},
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
            }

            if meta['itype'] == 'R':
                meta['isMemout'] = False
                meta['destReg'] = int(line[1]) 
                meta['srcReg1'] = int(line[2]) 
                meta['srcReg2'] = int(line[3])
                meta['src1Ready'] = False
                meta['src2Ready'] = False

            if meta['itype'] == 'I':
                meta['isMemout'] = False
                meta['destReg'] = int(line[1]) 
                meta['srcReg1'] = int(line[2])
                meta['srcReg2'] = None,
                meta['src1Ready'] = False
                meta['src2Ready'] = True

            if meta['itype'] == 'L':
                meta['isMemout'] = False
                meta['destReg'] = int(line[1])
                meta['srcReg1'] = int(line[3]) 
                meta['srcReg2'] = None,
                meta['src1Ready'] = False
                meta['src2Ready'] = True

            if meta['itype'] == 'S':
                meta['isMemout'] = True
                meta['destReg'] = None, 
                meta['srcReg1'] = int(line[1]) 
                meta['srcReg2'] = int(line[3])
                meta['src1Ready'] = False
                meta['src2Ready'] = False

            instructions.append(meta)

        return num_reg, width, instructions

def generate_output(schedule):
    print(*global_vars['schedule_map'], sep='\n')
    with open('out.txt', 'w') as file:
        for schedule in global_vars['schedule_map']:
            file.write(','.join(map(str,schedule)) + "\n")

    return

def operation(type, source_reg, dest_reg):
    return 

def main() : 
    file_name = sys.argv[1]
    
    global_vars['num_reg'], global_vars['width'], global_vars['instructions'] = parse_input(file_name)
    global_vars['schedule_map'] = [[0]*7 for i in range(len(global_vars['instructions']))]
    global_vars['freeList'] = [i for i in range(32, global_vars['num_reg'])]
    
    for i in range(32):
        global_vars['readyTable'][i] = True 
        global_vars['mapTable'][i] = i
    
    # update schedule 
    obj1 = simulator(global_vars)
    global_vars['schedule_map'] = obj1.schedule()

    # generate output
    generate_output(global_vars['schedule_map'])


if __name__ == '__main__': 
    main()
