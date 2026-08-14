import copy

list1 = [1,2,3]

list2 = copy.copy(list1)

list2[2] = 4

if list1 == list2:
    print("equal list")
    
if list1 is list2:
    print("ok")
else:
    print("no")

dict1 = {"a": 1, "b": 2}

dict2 = copy.copy(dict1)

dict2["a"] = 3

print(dict1)
print(dict2)
