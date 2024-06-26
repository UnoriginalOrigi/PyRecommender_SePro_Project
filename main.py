from CLI_implementation import CLI_program
from tkinter_implementation import tkinter_program
from util.general_func import cls, clean_up, action_input

"""
Error Codes:
1. Expected integer, received invalid input
2. Input is incorrect length, possible overflow
3. Invalid characters provided
"""

def main():
    print("Welcome to PyRecommender \nChoose the Interface \n1 - CLI; 2 - TKinter interface")
    action = action_input()
    if action == 1:
        CLI_program()
    elif action == 2:
        tkinter_program()
    else:
        print("Invalid Input")

if __name__ == "__main__":
    cls()
    clean_up()
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, force closing program!")
        clean_up()