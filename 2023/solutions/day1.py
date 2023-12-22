import time


class Utils:
    def read_input(filepath: str = "2023/solutions/inputs/day1.txt") -> str:
        """Read input file."""
        try:
            with open(filepath, "r") as file:
                return file.read()
        except TypeError as e:
            print(f"Error reading from file: {e}")

    def timer_wrapper(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Time taken for {func.__name__}: {elapsed_time:.6f} seconds")
            return result

        return wrapper


def find_digits(string: str) -> int:
    # Variables
    digit1, digit2 = (None, None)

    # Counters
    fwd = 0
    bwd = len(string) - 1

    # Find first digit
    while fwd < len(string):
        char = string[fwd]
        if char.isdigit():
            digit1 = char
            break
        fwd += 1

    if not digit2:
        # Find last digit
        while bwd >= 0:
            char = string[bwd]
            if char.isdigit():
                digit2 = char
                break
            bwd -= 1

    return int(f"{digit1}{digit2}")


@Utils.timer_wrapper
def solution():
    # 1. Set variables a, b
    # a is first digit, b is last digit

    # 2. loop forward until first digit reached
    # 3. Then loop backwards until last digit reached

    # 4. Combine first and last digit to form a single two-digit number

    input_data = Utils.read_input()
    input_data_list = input_data.split("\n")

    total = 0
    for string in input_data_list:
        total += find_digits(string)

    print("Total:", total)
    return total


if __name__ == "__main__":
    solution()
