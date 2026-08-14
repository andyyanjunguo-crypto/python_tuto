#python 3.1x

# names = ["lucas", "lili", "james", "abc", "ddd", "abc", "abc"]
# nums = [131, 151, 18, 77, 15, 4]

# n = int(input())

arr = map(int, input().split(","))
list_num = list(arr)
list_num.sort(reverse=True)
result = list_num[1]

# print(list_num[0])

# nums.sort()
# print(nums) # [4, 15, 18,5 77, 131, 151]

# count = len(nums)
# print(count)

# runnerup = nums[count - 2]

# print(names2)

# for n in names:
#     n += "a"

# print(names[0][1])

# list2 = [[1,2,3], [4,5,6], [7,8,9]]
# print(list2[0][1])

# """
# 0 0 0
# 0 1 0
# 0 0 1
# """

# print(names[0:2])

# chris = ("man", 18)
# lili = ("woman", 22)

# print(lili[0])

# def exam():
#     return "lili", 100 , "pass"

# a = exam()
# print(a[2])

stu1 = {"name": "lili", "age": 18, "school": "WGS"}
stu2 = {"name": "lucase", "age": 19, "school": "MGS"}
stu3 = {"name": "lucase II", "age": 19, "school": "MGS"}

stus = [stu1, stu2, stu3]

# for stu in stus:
#     if stu["age"] >= 19:
#         print(stu["name"])

# for key in dict1:
#     print(key)

# print([dict1, dict2])

# for x in dict1: 
#     print(x) # only print key
    
# for x in dict1:
#     print(f"{x}:{dict1[x]}") # print key:value
    
