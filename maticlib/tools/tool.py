

def tool(func):
    def wrapper(*args, **kwargs):
        # print("Before execution")
        result = func(*args, **kwargs)
        # print("After execution")
        return result
    return wrapper

# @tool
# def add(a, b):
#     return a + b

# print(add(5, 3))