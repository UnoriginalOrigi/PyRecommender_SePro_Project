from CLI_implementation import CLI_program
from util.general_func import cls, clean_up


"""
Error Codes:
1. Expected integer, received invalid input
2. Input is incorrect length, possible overflow
3. Invalid characters provided
"""

def main():
    CLI_program()

if __name__ == "__main__":
    cls()
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, force closing program!")
        clean_up()