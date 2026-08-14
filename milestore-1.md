# Student Management System

## functionalities

1. Add student
2. Remove student
3. Show all students
4. Show average score
5. Find highest score
6. Exit

## request

用 function, list, dictionary, try/except, loop

## example code

```python
students = [
    {
        "name": "Tom",
        "age": 20,
        "score": 85
    },
    {
        "name": "Alice",
        "age": 21,
        "score": 92
    }
]

command = input("Please input a command")
if command == 'add':
    # ask for more info
elif command == 'remove':
    # ask for name to remove
    # if not found the name, show a error message - student cannot be found.
elif command == 'show':
    # ask for name 
    # print score
elif command == 'find_high':
    # print highest score student's name
elif command == "exit":
    # end the app.

```