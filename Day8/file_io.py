# write file example
import io

def write_log(message: str):
    try:
        with open(r'/Users/wei.lu/Documents/python_tuto/Day8/tut2.log', 'a') as f:
            f.write(message + '\n')
    except FileNotFoundError:
        print("file not found")
    
    print("88")

write_log("cc")