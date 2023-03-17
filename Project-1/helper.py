class simulator :

    def __init__(self, instructions, schedule_maps) -> None:        
        self.instructions = instructions
        self.schedule_map = schedule_maps

        self.qfetch = []
        self.qdecode = []
        self.qrename = []
        self.qdispatch = []
        self.qissue = []
        self.qwrite_back = []
        self.qcommit = []
        self.cycle = 0 

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
        for i in range(2): 
            if self.instructions :
                instruction = self.instructions.pop(0)
                instruction['icycle'] = self.cycle
                self.qdecode.append(instruction)

                # update schedule
                self.schedule_map[instruction['icount']][0] = self.cycle

    def decode(self):
        for i in range(2):
            if self.qdecode :                                
                instruction = self.qdecode.pop(0)

                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qrename.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][1] = self.cycle
                else : 
                    self.qdecode = [instruction] + self.qdecode
                    break 


    def rename(self):
        for i in range(2):
            if self.qrename :
                instruction = self.qrename.pop(0)

                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qdispatch.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][2] = self.cycle
                else :
                    self.qrename = [instruction] + self.qrename
                    break 
    

    def dispatch(self):
        for i in range(2):
            if self.qdispatch :                                
                instruction = self.qdispatch.pop(0)
                
                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qissue.append(instruction)                
                    # update schedule
                    self.schedule_map[instruction['icount']][3] = self.cycle
                else :
                    self.qdispatch = [instruction] + self.qdispatch
                    break


    def issue(self):
        for i in range(2):
            if self.qissue :                                
                instruction = self.qissue.pop(0)

                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qwrite_back.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][4] = self.cycle                
                else:
                    self.qissue = [instruction]+ self.qissue
                    break


    def write_back(self):
        for i in range(2):
            if self.qwrite_back :                                
                instruction = self.qwrite_back.pop(0)
                
                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    self.qcommit.append(instruction)
                    # update schedule
                    self.schedule_map[instruction['icount']][5] = self.cycle
                else :
                    self.qwrite_back = [instruction] + self.qwrite_back
                    break


    def commit(self):
        for i in range(2):
            if self.qcommit :                                
                instruction = self.qcommit.pop(0)

                if instruction['icycle'] < self.cycle :
                    instruction['icycle'] = self.cycle
                    # update schedule
                    self.schedule_map[instruction['icount']][6] = self.cycle
                else : 
                    self.qcommit = [instruction] + self.qcommit
                    break
            