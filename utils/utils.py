import time

def get_unique_variable():
    current_time = time.time()
    unique_variable_prefix = str(current_time)[4:10]
    unique_variable_suffix = str(current_time)[11:15]
    unique_variable = unique_variable_prefix + unique_variable_suffix
    return unique_variable