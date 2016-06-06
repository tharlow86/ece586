import os


# files and directories needed to run simulation
d_inst = 'instruction\\'
inst_file = 'machine.txt'

d_in = 'input\\'
in_files = os.listdir(d_in)

d_out = 'output\\'

d_trace = 'trace\\'


def compareOutputs(calc_out_file, rO):
    """Compares current simulator output to calculated output for verification"""
    with open(calc_out_file) as f:
        s = f.read()        
        if s.rstrip() == rO:
            print('Success!   Simulated results match calculated results')
        else:
            print('Failure!   Simulated results DO NOT match calculated results')



def opcodeToStr(opcode):
    """Takes in an int opcode and returns the instruction string"""
    if opcode == 0:
        return 'nop'
    elif opcode == 1:
        return 'ldip'
    elif opcode == 2:
        return 'ldwp'
    elif opcode == 3:
        return 'ldop'
    elif opcode == 8:
        return 'ldi'
    elif opcode == 9:
        return 'ldw'
    elif opcode == 10:
        return 'sto'
    elif opcode == 11:
        return 'msa'
    elif opcode == 12:
        return 't0'
    elif opcode == 13:
        return 't1'
    elif opcode == 14:
        return 't2'
    elif opcode == 15:
        return 't3'


def hexByteToInt(byte):
    """Converts a string containing a hex byte (no leading 0x) and converts to a
    two's-complement int"""    
    if byte == '01':
        return 1
    elif byte == 'ff':
        return -1
    else:        
        return 0

def intToHexByte(x):
    """Converts a int to a hex byte string with no leading 0x"""
    if x == 1:
        return '01'
    elif x == -1:
        return 'ff'
    else:
        return '00'    
    

def splitWord(word):
    """Splits a word into 4 int bytes"""
    b0 = hexByteToInt(word[2:4])
    b1 = hexByteToInt(word[4:6])
    b2 = hexByteToInt(word[6:8])
    b3 = hexByteToInt(word[8:10])
    return b0,b1,b2,b3


def alu(opcode, a, b, rA):
    """Provides ALU functions msa, t0, t1, t2, and t3"""
    
    # multiply-sum-add instruction
    if opcode == 11:
        a0, a1, a2, a3 = splitWord(a)
        b0, b1, b2, b3 = splitWord(b)
        c0 = a0*b0
        c1 = a1*b1
        c2 = a2*b2
        c3 = a3*b3
        rA = rA + c0 + c1 + c2 + c3
        return rA, '0x00000000'
    # t0 instruction
    elif opcode == 12:
        if rA >= 0:
            rA = 0
            return rA,'0x' + '01' + a[4:]
        else:
            rA = 0
            return rA,'0x' + '00' + a[4:]
    # t1 instruction
    elif opcode == 13:
        if rA >= 0:
            rA = 0
            return rA,'0x' + a[2:4] + '01' + a[6:]
        else:
            rA = 0
            return rA,'0x' + a[2:4] + '00' + a[6:]
    # t2 instruction
    elif opcode == 14:
        if rA >= 0:
            rA = 0
            return rA,'0x' + a[2:6] + '01' + a[8:]
        else:
            rA = 0
            return rA,'0x' + a[2:6] + '00' + a[8:]
    # t3 instruction
    elif opcode == 15:
        if rA >= 0:
            rA = 0
            return rA,'0x' + a[2:8] + '01'
        else:
            rA = 0
            return rA,'0x' + a[2:8] + '00'


# read in instruction memory file
with open(d_inst + inst_file, 'r') as f:
    ins_mem = list(f)
    ins_mem = [s.rstrip() for s in ins_mem]

total_cycles = 0
total_inst = 0


# begin simulation
for i in in_files:
    print('Running',i,end='...... ')
    # initialize cycle count and PC register
    cycle = 0
    pc = 0
    # initalize main registers
    rIP = 0
    rWP = 0
    rOP = 0
    rI  = '0x00000000'
    rW  = '0x00000000'
    rO  = '0x00000000'
    rA  = 0
    # initialize IF/ID registers
    if_id_ir = 0
    if_id_imm = 0
    # initialize ID/EM registers
    id_em_ir = 0
    id_em_ma = 0
    id_em_a = '0x00000000'
    id_em_b = '0x00000000'
    # initialize EM/WB registers
    em_wb_ir = 0
    em_wb_dm = '0x00000000'
    em_wb_alu = '0x00000000'    
    # read in data memory file
    with open(d_in + i,'r') as f:
        data_mem = list(f)
        data_mem = [s.rstrip() for s in data_mem]
        file_num = f.name[12:16]
        ofn = d_out + 'd_mem_' + file_num + '_sim_out.txt'
        of = open(ofn,'w')
        cfn = d_out + 'd_mem_' + file_num + '_calc_out.txt'        
        tfn = d_trace + 'trace_' + file_num + '.txt'
        tf = open(tfn,'w')
        
        # begin executing instructions
        while(1):
     
            # WB stage
            if em_wb_ir == 8:                
                rI = em_wb_dm                
            elif em_wb_ir == 9:
                rW = em_wb_dm                
            elif (em_wb_ir == 12) or (em_wb_ir == 13) \
                 or (em_wb_ir == 14) or (em_wb_ir == 15):
                rO = em_wb_alu          
                
            # EB stage             
            if id_em_ir == 8:
                em_wb_dm = data_mem[id_em_ma]
                rIP = rIP + 1
            elif id_em_ir == 9:
                em_wb_dm = data_mem[id_em_ma]
                rWP = rWP + 1
            elif id_em_ir == 10:
                data_mem[id_em_ma] = rO                
                rOP = rOP + 1                
            elif (id_em_ir == 11) or (id_em_ir == 12) or (id_em_ir == 13) \
                 or (id_em_ir == 14) or (id_em_ir == 15):
                rA, em_wb_alu = alu(id_em_ir, id_em_a, id_em_b, rA)                

            # ID stage
            if if_id_ir == 1:
                rIP = if_id_imm
            if if_id_ir == 2:
                rWP = if_id_imm
            if if_id_ir == 3:
                rOP = if_id_imm                
            if if_id_ir == 8:
                id_em_ma = rIP
            if if_id_ir == 9:
                id_em_ma = rWP
            if if_id_ir == 10:
                id_em_ma = rOP                
            if if_id_ir == 11:
                id_em_a = rI
                id_em_b = rW
            elif (if_id_ir == 12) or (if_id_ir == 13) or (if_id_ir == 14) \
                 or (if_id_ir == 15):
                id_em_a = rO
            
            # IF stage
            ir_save = em_wb_ir
            em_wb_ir = id_em_ir
            id_em_ir = if_id_ir
            if pc < len(ins_mem):            
                a,b = ins_mem[pc].split(sep='x')
                oc_hex = list(b)[0]            
                imm_hex = ''.join(list(b)[1:])
                if_id_ir = int(oc_hex,16)            
                if_id_imm = int(imm_hex,16) // 4 
                pc = pc + 1
            else:
                if_id_ir = 0
                if_id_imm = 0         
    
            # increment the cycle count
            cycle = cycle + 1

            # print trace
            wb_s = opcodeToStr(ir_save)
            em_s = opcodeToStr(em_wb_ir)
            id_s = opcodeToStr(id_em_ir)
            if_s = opcodeToStr(if_id_ir)        
            s = 'Cycle:{:3}  IF: {:4}  ID: {:4}  EM: {:4}  WB: {:4}'.format(cycle,if_s,id_s,em_s,wb_s)
            tf.write(s+'\n')
            #print(s)
                                                          

            if (cycle > 0) and (ir_save==0) and (em_wb_ir==0) \
               and (id_em_ir==0) and (if_id_ir==0):                
                of.write(rO + '\n')
                compareOutputs(cfn,rO)
                of.close()
                #cf.close()
                tf.close()
                total_cycles = total_cycles + cycle
                total_inst = total_inst + len(ins_mem)
                break
        


print('Simulation finished!')
print('  Total cycle count:',total_cycles)
print('  Total instruction count:',total_inst)
print('  CPI: ',str(total_cycles/total_inst))

            
            




    
