import random

n = 9    # input neuron count
m = 4    # hidden neuron count
p = 4    # output neuron count

x =    # input layer
h = []   # hidden layer
o = []   # output layer

xhw = []  # input-to-hidden weights
how = []  # hidden-to-output weights


# growing and initializing layers
##for i in range(n):
##    x.append(random.randint(0,1))

for i in range(m):
    h.append(random.randint(0,1))

for i in range(p):
    o.append(random.randint(0,1))

# growing and initializing weights
for i in range(n*m):
    xhw.append(random.randint(-1,1))

for i in range(m*p):
    how.append(random.randint(-1,1))



def randWeights():    
    """Randomizes weights"""
    for i in range(n*m):
        xhw[i] = random.randint(-1,1)

    for i in range(m*p):
        how[i] = random.randint(-1,1)


def randInput():
    """Randomizes the input values"""
    for i in range(n):
        x[i] = random.randint(0,1)

def updateNet():
    """Calculates the hidden layer values then the output layer values"""
    # update hidden layer
    for i in range(m):
        total = 0
        for j in range(n):
            total = total + x[j]*xhw[i*m+j]
        if total < 0:
            h[i] = 0
        else:
            h[i] = 1
    # update output layer
    for i in range(p):
        total = 0
        for j in range(m):
            total = total + h[j]*how[i*p+j]
        if total < 0:
            o[i] = 0
        else:
            o[i] = 1

def listToHexString(list_in):
    """
    Converts a list of individual values (neuron states or weights)
    to a list of hexadecimal strings where each string is 4 bytes
    """
    # number of bytes per word
    bpw = 4
    # empty output list to be appended
    list_out = []
    # pre and post fixes for hex strings
    pre = '0x'    
    post = '\n'
    # whole word count and remainder
    list_len = len(list_in)
    wwc = list_len // bpw
    rem = list_len % bpw    

    # writing whole words (4 bytes)
    for i in range(wwc * bpw):
        # calculate index modulo 4
        modFour = i % bpw
        
        if modFour is 0:
            temp_str = pre

    
        if list_in[i] is 1:
            temp_str = temp_str + '01'
        elif list_in[i] is -1:
            temp_str = temp_str + '11'
        else:
            temp_str = temp_str + '00'

        if modFour is 3:
            temp_str = temp_str + post
            list_out.append(temp_str)

    # writing the remaining bytes and padding
    # the rest of the word with zeros
    for i in range(4) + (wwc * bpw):

        temp_str = pre
        
        if rem > 0:
            if list_in[i] is 1:
                temp_str = temp_str + '01'
            elif list_in[i] is -1:
                temp_str = temp_str + '11'
            else:
                temp_str = temp_str + '00'
        else:
            temp_str = temp_str + '00'

        temp_str = temp_str + post
        list_out.append(temp_str)                
            
    return list_out
  

def createInputFile(str_in):
    """
    Creates a text file to be used as data memory for neural processor.
    The file is created in the working directory and uses the str
    input as the file name.

    The file contains hexidecimal strings representing the input data
    and the weights for the neural processor.  Each line is 32 bits.
    """
    # open the file
    f = open(str_in,'w')
    # for i in range(n):
        
        



def printNet():
    """Prints the layers and the weights"""
    print(x)
    print(xhw)
    print(h)
    print(how)
    print(o)

def cycle():
    randInput()
    updateNet()
    printNet()

