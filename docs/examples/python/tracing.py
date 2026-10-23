import sys

# Source: https://www.geeksforgeeks.org/python/python-sys-settrace/, https://docs.python.org/3.11/reference/datamodel.html#frame-objects
def my_tracer(frame, event, arg = None):

    # Extract local variables
    local_variables = frame.f_locals
    # print(local_variables)

    # Extract global variables
    global_variables = frame.f_globals
    # print(global_variables)

    print(global_variables['lst'])

    return my_tracer

lst = [1, 2, 3, 4, 5, 6]

def linear_search(lst, target):
    for e in lst:
        if e == target:
            return True
    return False

sys.settrace(my_tracer)

linear_search(lst, 6)