import os
import random

# START DEBUGGING!!! Change back to user input!!!
# receive input from user to create files for simulator
i_count = 4 #int(input('Number of input neurons: '))
h_count = 4 #int(input('Number of hidden neurons: '))
o_count = 4 #int(input('Number of output neurons: '))
f_count = 1 #int(input('\nNumber of random input vectors: '))
# STOP DEBUGGING!!!

# number of zeros for fill number appended to end of file names
# this should be the number of digits in f_count - 1
zf_val = 4


# create input, hidden, and output layers
i_layer = [0 for i in range(i_count)]
h_layer = [0 for i in range(h_count)]
o_layer = [0 for i in range(o_count)]


# create randomized weights {-1,0,1}
ih_weights = [random.randint(-1,1) for i in range(i_count*h_count)]
ho_weights = [random.randint(-1,1) for i in range(h_count*o_count)]

# memory addresses to be used in generated assembly code
# order of data in memory: ih_weights, oh_weights, i_layer, h_layer, o_layer
ih_address = 0
ho_address = i_count * h_count
i_address = ho_address + h_count*o_count
h_address = i_address + i_count
o_address = h_address + h_count

## START DEBUGGING!!!
print(ih_address)
print(ho_address)
print(i_address)
print(h_address)
print(o_address)
## STOP DEBUGGING!!!



def randomInput(size):
    """Randomizes the input vector"""
    return [random.randint(0,1) for i in range(size)]



def zeroHO(h_count, o_count):
    """Zeroes out the hidden and output layers"""
    return [0 for i in range(h_count)], [0 for i in range(o_count)]



def calculateNet(ih_weights, ho_weights, i_layer, h_layer, o_layer):
    """Calculates the hidden layer values then the output layer values"""
    i_count = len(i_layer)
    h_count = len(h_layer)
    o_count = len(o_layer)
    # update hidden layer
    for i in range(h_count):
        total = 0
        for j in range(i_count):
            total = total + i_layer[j]*ih_weights[i*i_count+j]
        if total < 0:
            h_layer[i] = 0
        else:
            h_layer[i] = 1
    # update output layer
    for i in range(o_count):
        total = 0
        for j in range(h_count):
            total = total + h_layer[j]*ho_weights[i*h_count+j]
        if total < 0:
            o_layer[i] = 0
        else:
            o_layer[i] = 1

    return h_layer, o_layer



def printNet():
    """Prints the layers and the weights to console for debugging"""
    print(i_layer)
    print(ih_weights)
    print(h_layer)
    print(ho_weights)
    print(o_layer)



def listToHexStrings(list_in):
    """
    Converts a list of individual values (neuron states or weights)
    to a list of hexadecimal strings where each string is 4 bytes
    """
    # number of bytes per word
    bpw = 4
    # pre and post fixes for hex strings
    pre = '0x'    
    post = '\n'
    
    # whole word count and remainder
    list_len = len(list_in)
    wwc = list_len // bpw
    rem = list_len % bpw

    # output list
    list_out = [None for i in range(wwc)]

    # whole words
    for i in range(wwc):
        temp_str = pre    
        for j in range(bpw):
            k = i*bpw + j
            if list_in[k] is 1:
                temp_str = temp_str + '01'
            elif list_in[k] is -1:
                temp_str = temp_str + 'ff'
            else:
                temp_str = temp_str + '00'
        
        temp_str = temp_str + post
        list_out[i] = temp_str

    # remainder word padded with zeroes
    if rem:
        temp_str = pre
        for i in [wwc*bpw + j for j in range(rem)]:
            if list_in[i] is 1:
                temp_str = temp_str + '01'
            elif list_in[i] is -1:
                temp_str = temp_str + 'ff'
            else:
                temp_str = temp_str + '00'

        temp_str = temp_str + '00' * (bpw-rem)
        temp_str = temp_str + post
        list_out.append(temp_str)

    return list_out
            


def strListToFile(filename, str_list):
    """Creates a data memory file from a list of hex strings"""
    with open(filename,'w') as f:
        for i in str_list:
            f.write(i)




## Start creating files

# create list of hex strings for weights that will be the same for all
# data memory images
ih_hex = listToHexStrings(ih_weights)
## START DEBUGGING!!!
##print('ih_weights=')
##print(ih_weights)
##print('len(ih_weights)=')
##print(len(ih_weights))
##print('ih_hex=')
##print(ih_hex)
##print('len(ih_hex)=')
##print(len(ih_hex))
## STOP DEBUGGING!!!
ho_hex = listToHexStrings(ho_weights)
weight_hex = ih_hex + ho_hex

# create a list of hex strings for the hidden and output layers
h_hex = listToHexStrings(h_layer)
o_hex = listToHexStrings(o_layer)

# directory strings
d_in = 'input\\'
d_out = 'output\\'




            

# loop to create number of input data files that was specified by user
for i in range(f_count):
    file_num = str(i).zfill(zf_val)
    # create data memory file name
    f_in = d_in + 'd_mem_' + file_num + '.txt'
    # randomize input layer, zero hidden and output layers, and create layer_hex list
    i_layer = randomInput(i_count)
    i_hex = listToHexStrings(i_layer)
    h_layer, o_layer = zeroHO(h_count,o_count)
    layer_hex = i_hex + h_hex + o_hex
    # write the data memory file
    strListToFile(f_in, weight_hex + layer_hex)
    print(f_in + ' created!')
    # create calculated output file name
    f_calc_out = d_out + 'd_mem_' + file_num + '_calc_out.txt'
    # calculate output using randomized input
    h_layer, o_layer = calculateNet(ih_weights, ho_weights, i_layer, h_layer, o_layer)
    # write calculated output to separate file
    o_hex = listToHexStrings(o_layer)
    strListToFile(f_calc_out, o_hex)
    print(f_calc_out + ' created!')
    # create assembly code file

    # create machine code instruction file


# create human-readable assembly file and machine-readable hex file for instruction
# memory
fna = 'assembly.txt'
fnm = 'machine.txt'
with open(fna,'w') as fa:
    with open(fnm,'w') as fm:
        # load input pointer instruction
        fa.write('ldip, #' + str(i_address) + '\n')
        a,b = hex(i_address).rsplit(sep='x')
        b = b.zfill(7)
        fm.write('0x1' + b + '\n')
        # load weight pointer instruction
        fa.write('ldwp, #' + str(ih_address) + '\n')
        a,b = hex(ih_address).rsplit(sep='x')
        b = b.zfill(7)
        fm.write('0x2' + b + '\n')
        # load output pointer instruction
        fa.write('ldwp, #' + str(o_address) + '\n')
        a,b = hex(o_address).rsplit(sep='x')
        b = b.zfill(7)
        fm.write('0x3' + b + '\n')
        # calculating hidden layer
        for i in range(len(i_hex) + len(h_hex)):
            # current output byte variable for choosing threshold operation
            cob = 0
            # load input instruction
            fa.write('ldi\n')
            fm.write('0x8' + 7*'0' + '\n')
            for j in range(len(ih_hex)):
                # load weight instruction
                fa.write('ldw\n')
                fm.write('0x9' + 7*'0' + '\n')
                # no operation instruction
                fa.write('nop\n')
                fm.write('0x0' + 7*'0' + '\n')
                # multiply-sum-add instruction
                fa.write('msa\n')
                fm.write('0xb' + 7*'0' + '\n')
                # threshold instructions
                if cob == 0:
                    fa.write('t0\n')
                    fm.write('0xc' + 7*'0' + '\n')
                    cob = cob + 1
                elif cob == 1:
                    fa.write('t1\n')
                    fm.write('0xd' + 7*'0' + '\n')
                    cob = cob + 1
                elif cob == 2:
                    fa.write('t2\n')
                    fm.write('0xe' + 7*'0' + '\n')
                    cob = cob + 1
                elif cob == 3:
                    fa.write('t3\n')
                    fm.write('0xe' + 7*'0' + '\n')
                    # store output instruction
                    fa.write('sto\n')
                    fm.write('0xa' + 7*'0' + '\n')
                    cob = 0                
