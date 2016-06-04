import os
import random


i_count = input('Number of input neurons: ')
h_count = input('Number of hidden neurons: ')
o_count = input('Number of output neurons: ')

i_layer = [random.randint(0,1) for i in range(i_count)]
h_layer = [0 for i in range(h_count)]
o_layer = [0 for i in range(o_count)]


ih_weights = [random.randint(0,1) for i in range(i_count*h_count)]
ho_weights = [random.randint(0,1) for i in range(h_count*o_count)]


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
                temp_str = temp_str + '11'
            else:
                temp_str = temp_str + '00'
        
        temp_str = temp_str + post
        list_out[i] = temp_str

    # remainder word padded with zeroes
    temp_str = pre
    for i in [wwc*bpw + j for j in range(rem)]:
        if list_in[i] is 1:
            temp_str = temp_str + '01'
        elif list_in[i] is -1:
            temp_str = temp_str + '11'
        else:
            temp_str = temp_str + '00'

    temp_str = temp_str + '00' * (bpw-rem)
    temp_str = temp_str + post
    list_out.append(temp_str)

    return list_out
            
def strListToFile(filename, str_list):
    with open(filename,'w') as f:
        for i in str_list:
            f.write(i)


