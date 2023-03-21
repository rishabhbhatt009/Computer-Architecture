class simulator :

    def __init__(self, global_vars) -> None:        
        self.instructions = global_vars['instructions']
        self.schedule_map = global_vars['schedule_map']
        self.freeList = global_vars['freeList']
        self.pendingfreeList = []
        self.mapTable = global_vars['mapTable']
        self.readyTable = global_vars['readyTable']

        self.width = global_vars['width']
        self.cycle = global_vars['cycle']

        self.qfetch = []
        self.qdecode = []
        self.qrename = []
        self.qdispatch = []
        self.qissue = []
        self.qwrite_back = []
        self.qcommit = []
        

    def pipeline_completed(self):
        c1 = self.instructions == [] 
        c2 = self.qfetch == []
        c3 = self.qdecode == []
        c4 = self.qrename == []
        c5 = self.qdispatch == []
        c6 = self.qissue == []
        c7 = self.qwrite_back == []
        c8 = self.qcommit == []
        
        return all([c1,c2,c3,c4,c5,c6,c7,c8])

    def schedule(self) :
        while not self.pipeline_completed() :

            # pipeline
            self.fetch()
            self.decode()
            self.rename()
            self.dispatch()
            self.issue()
            self.write_back()
            self.commit()

            self.cycle += 1

        return self.schedule_map

    def fetch(self):
        for i in range(self.width): 
            if self.instructions :
                instruction = self.instructions.pop(0)
                instruction['icycle'] = self.cycle
                self.qdecode.append(instruction)

                # update schedule
                self.schedule_map[instruction['icount']][0] = self.cycle

    def decode(self):
        for i in range(self.width):
            if self.qdecode :                                
                instruction = self.qdecode[0]

                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qrename.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][1] = self.cycle
                    self.qdecode.pop(0)
                
    def rename(self):
        for i in range(self.width):
            if self.qrename :
                instruction = self.qrename[0]

                if instruction['icycle'] < self.cycle :

                    if not instruction['isMemout'] : 
                        if self.freeList :
                            instruction['src1Ready'] = instruction['src1Ready'] or self.readyTable[self.mapTable[instruction['srcReg1']]]
                            instruction['psrc1Reg'] = self.mapTable[instruction['srcReg1']]

                            if instruction['itype'] == 'R':
                                instruction['src2Ready'] = instruction['src2Ready'] or self.readyTable[self.mapTable[instruction['srcReg2']]]
                                instruction['psrc2Reg'] = self.mapTable[instruction['srcReg2']]

                            new_dest = self.freeList.pop(0) # front

                            instruction['overReg'] = self.mapTable[instruction['destReg']]
                            self.mapTable[instruction['destReg']] = new_dest
                            instruction['pdestReg'] = new_dest
                            self.readyTable[new_dest] = False

                            instruction['icycle'] = self.cycle
                            self.qdispatch.append(instruction)
                            # update schedule
                            self.schedule_map[instruction['icount']][2] = self.cycle
                            self.qrename.pop(0)    
                                                           
                    else : 
                        instruction['src1Ready'] = instruction['src1Ready'] or self.readyTable[self.mapTable[instruction['srcReg1']]]
                        instruction['psrc1Reg'] = self.mapTable[instruction['srcReg1']]
                        instruction['src2Ready'] = instruction['src2Ready'] or self.readyTable[self.mapTable[instruction['srcReg2']]]
                        instruction['psrc2Reg'] = self.mapTable[instruction['srcReg2']]
                        
                        instruction['icycle'] = self.cycle
                        self.qdispatch.append(instruction)
                        # update schedule
                        self.schedule_map[instruction['icount']][2] = self.cycle
                        self.qrename.pop(0)
    

    def dispatch(self):
        for i in range(self.width):
            if self.qdispatch :                                
                instruction = self.qdispatch[0]
                
                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qissue.append(instruction)                
                    # update schedule
                    self.schedule_map[instruction['icount']][3] = self.cycle
                    self.qdispatch.pop(0)
            
    # check if you have to go through all not just pop first 2
    def issue(self):
        i = 0
        it = 0
        while i < self.width and it < len(self.qissue) :  
            
            instruction = self.qissue[it]

            if instruction['icycle'] < self.cycle :
        
                instruction['src1Ready'] = instruction['src1Ready'] or self.readyTable[instruction['psrc1Reg']]

                if instruction['itype'] in ['R', 'S']:
                    instruction['src2Ready'] = instruction['src2Ready'] or self.readyTable[instruction['psrc2Reg']]

                if instruction['src1Ready'] and instruction['src2Ready']:
                    instruction['icycle'] = self.cycle
                    self.qwrite_back.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][4] = self.cycle                
                    self.qissue.pop(it)
                    i += 1
                    continue 
                
            it += 1
                            
    def write_back(self):
        for i in range(self.width):
            if self.qwrite_back :                                
                instruction = self.qwrite_back[0]
                
                if instruction['icycle'] < self.cycle :

                    if not instruction['isMemout']:
                        self.readyTable[instruction['pdestReg']]=True

                    instruction['icycle'] = self.cycle
                    self.qcommit.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][5] = self.cycle
                    self.qwrite_back.pop(0)
                

    def commit(self):
        while self.pendingfreeList :
            self.freeList.append(self.pendingfreeList.pop(0))

        i = 0
        idx = 0
        while i < self.width and idx < len(self.qcommit):
            instruction = self.qcommit[idx]
            
            if instruction['icycle'] < self.cycle :
                instruction['icycle'] = self.cycle
                if not instruction['isMemout']:
                    self.pendingfreeList.append(instruction['overReg'])
                # update schedule
                self.schedule_map[instruction['icount']][6] = self.cycle
                
                self.qcommit.pop(0)
                i += 1
            else :
                idx += 1
            