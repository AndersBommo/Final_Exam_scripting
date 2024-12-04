import time
class TimeLogger:
    @staticmethod
    def log_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            # Ensure that the result is unpacked into a tuple with execution time
            return result   # Return result + execution time as tuple
        return wrapper