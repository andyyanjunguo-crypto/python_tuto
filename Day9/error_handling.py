try:
    n = 0
    
    if n == 0:
        raise ValueError("n cannot be 0")
    res = 100 / n
    
    # b = [1,2,3]
    # res = 100 / b[4]
# except ZeroDivisionError:
#     print("You can't divide by zero!")
    
except ValueError as e:
    print(e)

except IndexError:
    print("index out of range")
    
else:
    print("Result is", res)
    
finally:
    print("Execution complete.")