
# coding: utf-8

# In[50]:


import numpy as np
from decimal import *
import re
import sys

# In[51]:


# Creat table_prob dictionary: key: a character or '.' or ' ', with value is tuple(low, high, range)
table_prob={}
letters_prob=[0.1138, 0.0443,0.0524,0.0317,0.028,0.0403,0.0164,0.042,0.0729,0.0051,0.0046,0.0242,0.0383,0.0228,0.0763,0.0432,0.0022,0.0283,0.0669,0.159,0.0118,0.0082,0.055,0.0005,0.0076,0.0005]
low = 0
high = 0

for i in range(ord('a'), ord('z')+1):
    rangei = round(Decimal(letters_prob[i-97]),4)
    low = round(Decimal(high),4)
    high = round(Decimal(low + rangei),4)
    table_prob[chr(i)] = (low,high,rangei)

# symbol '.': range 0.0001, ' ': range 0.0006
table_prob[','] = (high, high + round(Decimal(0.0006),4),round(Decimal(0.0006),4))
table_prob['.'] = (high +round(Decimal(0.0006),4),high + round(Decimal(0.0006),4)+round(Decimal(0.0011),4),round(Decimal(0.0011),4))
table_prob['~'] = (high + round(Decimal(0.0006),4)+ round(Decimal(0.0011),4) ,high + round(Decimal(0.0006),4) + round(Decimal(0.0011),4) + round(Decimal(0.002),4),round(Decimal(0.002),4))



def read_file(file):
    with open(file,'r') as file_input:
        #text = file_input.read().split(' ')
        text = re.findall(r"\S+", file_input.read())
        text = [x.lower() + '~' for x in text]
        #text.remove('\n')
        return text


# Compute value of string code
def value_code(code):
    value = Decimal(0.0)
    for i in range(len(code)):
        if (code[i] == '1'):
            value += Decimal(2**(-(i+1)))
    return value


# Convert binary the value between low and high of the encode
def convert_str_binary(low, high):
    code = ''
    while(value_code(code) < low):
        code += '1'
        if(value_code(code)>=high):
            code = code[:-1] + '0'
    return code

# Encode until reaching the symbol '.' --. send code
def encode(word, dict_table):
    low = Decimal(0.0)
    high = Decimal(1.0)
    com_range = Decimal(1.0)
    for i in word:
        high = low + com_range*dict_table[i][1]
        low = low + com_range*dict_table[i][0]
        com_range = high - low
    code_word = convert_str_binary(low, high)
    return code_word


# In[59]:


def encode_text(file_name, dict_table, saving_path):
    text = read_file(file_name)
    list_byte =[]
    list_bits = []
    for word in text:
        code_word = encode(word,dict_table)
        list_bits.append(code_word)
        
    str_bits = ''.join(list_bits)
    #print("Str: ", str_bits)
    list_8_bits = re.findall(r'\d{1,8}', str_bits)
    list_len_bits = [len(x) for x in list_bits]
    #print(list_8_bits)
    #print("Len: ", list_len_bits)
    
    with open(saving_path[:-6]+'_len.txt','w') as file:
        for x in list_len_bits:
            file.write(str(x) + ' ')
    
    with open(saving_path,'wb') as file:
        for byte in list_8_bits:
            temp = int(byte,2).to_bytes(1,byteorder = 'little')
            file.write(temp)
    
    


# In[60]:


def encode_txt(text, dict_table):
    text = text.split(' ')
    text = [x.lower() + '~' for x in text]
    list_en = []
    for word in text:
        code_word = encode(word,dict_table)
        list_en.append(code_word)
    return list_en


# In[61]:


# Decode cho 1 word
def decode(code_str_bin, dict_table):
    result = ''
    value = Decimal(value_code(code_str_bin))
    word =''
    while (True):
        for i in dict_table:
            if(dict_table[i][0] <= value and dict_table[i][1] > value):
                sym = i
                break
        if (sym == '~'):
            break
        result += sym
        low = dict_table[sym][0]
        value = (value - low)/dict_table[sym][2]
    return result


# In[62]:


def decode_text(file_name, dict_table, saving_path):
    result = ''
    
    with open(file_name[:-6]+'_len.txt','r') as file:
        str_len_bits = list(filter(None, file.read().split(' ')))
        len_bits = [int(x) for x in str_len_bits]
    
    with open(file_name,'rb') as file:
        encode_op = file.read()
        #print(encode_op)
        encode_op = [bytes([x]) for x in encode_op]
        list_bins = [bin(int.from_bytes(x,byteorder='little'))[2:].zfill(8) for x in encode_op]
        list_bins = list(filter(None, list_bins))
        list_bins[-1] = bin(int.from_bytes(encode_op[-1], byteorder='little'))[2:]
        str_bits = ''.join(list_bins)
        
        
    list_bits = []
    index = 0
    temp_index = 0
    for i in range(len(len_bits)):
        temp_index += len_bits[i]
        list_bits.append(str_bits[index:temp_index])
        index = temp_index
    
    with open(saving_path,'w') as file:
        for i in list_bits:
            word = decode(i,dict_table) + ' '
            file.write(word)
    


# In[63]:


def decode_txt(list_bins, dict_table):
    result = ''
    for i in list_bins:
        word = decode(i,dict_table) + ' '
        result += word
    return result



def arithmetic_compression(file_input, saving_path):
    """
    Apply arithmetic coding on file_input and save to saving path
    """
    encode_text(file_input, table_prob, saving_path)
    compression_ratio = sys.getsizeof(file_input)/sys.getsizeof(saving_path)

    return compression_ratio


def arithmetic_decompression(file_input, saving_path):
    str_rs = decode_text(file_input, table_prob, saving_path)





