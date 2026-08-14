face = '😀' # u'ff0011'


greet = "hello\nwo\"rld"

g = 'hll\'ddd'

greetTab="hello\tworld\thello\tguys\t12345\nlili\t100\t99\t98\t99"

# print(g)

path = r'c:\desk\folder_name\xxx.exe'

# print(path)

multiple_line = """
 heelo dsfkjdsklf
 sdkfjds
 sdlkfj
 
 
 dff
 
 
 ddd.   ereee
"""

# print(multiple_line)


def sum(a: int, b: int):
    """
    function summary
    """
    return a + b


word = 'python'

a = word[0:]

# for x in range(-1, -7, -1):
#     print(a[x]) # show all letter in one line
  
word = 'helllo'
w2 = word.replace('l', 'w', 1)

count = 0
found_index = -1
for index in range(0, len(word)):
    if word[index] == 'l':
        count +=1 
    
    if count == 2:
        found_index = index
        
# print(found_index)
    
if found_index != -1:
    new_word = word[0:3] + 'w' + word[4:]
    
# print(new_word)

yes_votes = 'lucas'
greet = f"morning {yes_votes}"
print(greet)