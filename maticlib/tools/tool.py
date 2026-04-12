

def tool(func):
    """
    A decorator to mark a function as a tool that can be used by an agent.
    
    This decorator can be used to wrap functions to provide a consistent 
    interface for tool execution and potentially add logging or validation 
    metadata in the future.
    
    Args:
        func (Callable): The function to be decorated.
        
    Returns:
        Callable: The wrapped function.
    """
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