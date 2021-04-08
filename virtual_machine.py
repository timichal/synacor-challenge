#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict


# In[2]:


loaded_instructions = []
with open("challenge.bin", "rb") as file:
    byte_pair = file.read(2)
    while byte_pair:
        instruction = int(''.join([format(int(byte), "b").zfill(8) for byte in reversed(list(byte_pair))]), base=2)
        loaded_instructions.append(instruction)
        byte_pair = file.read(2)


# In[3]:


instructions = loaded_instructions.copy()
register = defaultdict(int) # 32768..32775 mean registers 0..7
stack = []
position = 0
log = False
instring = ""
while True:
    instruction = instructions[position]
    a = instructions[position + 1] 
    b = instructions[position + 2] 
    c = instructions[position + 3]
    
    if log:
        #print(stack)
        print("POS", position, "INF", instruction, a, b, c, ", ")

    if instruction == 0: # halt
        break
    elif instruction == 1: # set a b
        if 32768 <= b <= 32775:
            b = register[b]
        register[a] = b
        position += 3
    elif instruction == 2: # push a
        if 32768 <= a <= 32775:
            a = register[a]
        stack.append(a)
        position += 2
    elif instruction == 3: # pop a (remove the top element from the stack and write it into <a>)
        register[a] = stack.pop()
        position += 2
    elif instruction == 4: # eq a b c (set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise)
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        if (b == c):
            register[a] = 1
        else:
            register[a] = 0
        position += 4
    elif instruction == 5: # gt a b c (set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise)
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        if (b > c):
            register[a] = 1
        else:
            register[a] = 0
        position += 4
    elif instruction == 6: # jmp a
        position = a
    elif instruction == 7: # jt a b (jump if nonzero)
        if 32768 <= a <= 32775:
            a = register[a]
        if a != 0:
            position = b
        else:
            position += 3
    elif instruction == 8: # jf a b (jump if zero)
        if 32768 <= a <= 32775:
            a = register[a]     
        if a == 0:
            position = b
        else:
            position += 3
    elif instruction == 9: # add a b c
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        register[a] = (b + c) % 32768
        position += 4
    elif instruction == 10: # mult a b c
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        register[a] = (b * c) % 32768
        position += 4        
    elif instruction == 11: # mod a b c
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        register[a] = b % c
        position += 4 
    elif instruction == 12: # and a b c (stores into <a> the bitwise and of <b> and <c>)
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        register[a] = b & c
        position += 4
    elif instruction == 13: # or a b c (stores into <a> the bitwise or of <b> and <c>)
        if 32768 <= b <= 32775:
            b = register[b]
        if 32768 <= c <= 32775:
            c = register[c]
        register[a] = b | c
        position += 4
    elif instruction == 14: # not a b (stores 15-bit bitwise inverse of <b> in <a>)
        if 32768 <= b <= 32775:
            b = register[b]
        register[a] = 32768 - b - 1
        position += 3
    elif instruction == 15: # rmem a b (read memory at address <b> and write it to <a>)
        if 32768 <= b <= 32775:
            b = register[b]
        register[a] = instructions[b]
        position += 3
    elif instruction == 16: # wmem a b (write the value from <b> into memory at address <a>)
        if 32768 <= a <= 32775:
            a = register[a]
        if 32768 <= b <= 32775:
            b = register[b]
        instructions[a] = b
        position += 3
    elif instruction == 17: # call a (write the address of the next instruction to the stack and jump to <a>)
        stack.append(position + 2)
        if 32768 <= a <= 32775:
            a = register[a]
        position = a
    elif instruction == 18: # ret (remove the top element from the stack and jump to it; empty stack = halt)
        if len(stack) == 0:
            break
        position = stack.pop()  
    elif instruction == 19: # out a
        if 32768 <= a <= 32775:
            a = register[a]
        print(chr(a), end="")
        position += 2
    elif instruction == 20: # in a    
        if len(instring) == 0:
            instring = input("Prompt: ")
            instring = instring.strip() + "\n"
        register[a] = ord(instring[0])
        instring = instring[1:]
        position += 2            
    elif instruction == 21: # noop
        position += 1
    else: # skip the rest for now
        print(instruction)
        position += 1


# In[174]:




