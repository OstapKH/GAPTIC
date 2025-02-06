import os
import subprocess
import sys
import time
import random
import string

# This script demonstrates unsafe usage of subprocess in several parts.
# It also shows other unsafe practices like using eval and exec with untrusted input.
# Use this code only for educational purposes and security testing.
#
# WARNING: The unsafe functions in this script can lead to code injection and other vulnerabilities.
#
# Author: Example Author
# Date: 2025-02-05

def generate_random_string(length=8):
    # Generates a random string of letters and digits.
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for _ in range(length))

def unsafe_shell_command(user_input):
    """
    Executes a shell command unsafely using the user_input directly.
    This is vulnerable to shell injection.
    """
    command = "echo " + user_input
    print("Executing unsafe command:", command)
    # Unsafe usage: passing a concatenated string to subprocess.call with shell=True
    subprocess.call(command, shell=True)

def safe_shell_command(user_input):
    """
    Executes a shell command safely by passing arguments as a list.
    """
    print("Executing safe command with user input:", user_input)
    subprocess.call(["echo", user_input])

def run_system_command():
    # Runs a system command that lists directory contents.
    print("Listing current directory using system command")
    # Unsafe usage: using os.system which can be dangerous if concatenated with untrusted input.
    os.system("ls -la")

def execute_custom_command():
    # Gets a custom command from the user and executes it unsafely.
    user_command = input("Enter a command to execute: ")
    # This is unsafe and can lead to code injection if user_command is malicious.
    print("Executing user-provided command unsafely...")
    subprocess.call(user_command, shell=True)

def execute_safe_custom_command():
    # Gets a custom command and executes it safely by splitting arguments.
    user_command = input("Enter a command to echo safely: ")
    print("Executing user-provided command safely...")
    # Here we assume the command is just a simple echo.
    subprocess.call(["echo", user_command])

def main_menu():
    print("=" * 50)
    print("Python Unsafe Subprocess Demo")
    print("=" * 50)
    print("1. Run unsafe shell command with predefined input")
    print("2. Run safe shell command with predefined input")
    print("3. Execute system command to list directory")
    print("4. Execute custom command unsafely (dangerous)")
    print("5. Execute custom command safely (limited to echo)")
    print("6. Generate a random string and echo it unsafely")
    print("7. Exit")

def main():
    while True:
        main_menu()
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            user_input = "Hello World!"
            unsafe_shell_command(user_input)
        elif choice == "2":
            user_input = "Hello Secure World!"
            safe_shell_command(user_input)
        elif choice == "3":
            run_system_command()
        elif choice == "4":
            execute_custom_command()
        elif choice == "5":
            execute_safe_custom_command()
        elif choice == "6":
            rand_str = generate_random_string(12)
            unsafe_shell_command(rand_str)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select from 1-7")
        print("\nSleeping for 2 seconds before showing menu again...\n")
        time.sleep(2)

if __name__ == "__main__":
    main()

# Additional functions to simulate more complexity and unsafe usage

def process_data(data):
    # Process data unsafely by using eval on untrusted input.
    print("Processing data unsafely with eval:")
    try:
        result = eval(data)  # unsafe usage!
        print("Result of eval:", result)
    except Exception as e:
        print("Error during eval:", e)

def load_and_run_script():
    # Loads a script file provided by user and executes it unsafely.
    file_name = input("Enter the script filename to run unsafely: ")
    try:
        with open(file_name, 'r') as file:
            code = file.read()
        print("Executing the script code unsafely using exec:")
        exec(code)  # unsafe usage!
    except Exception as e:
        print("Error executing script:", e)

def simulate_vulnerability():
    # Simulates a vulnerability where user input is directly passed to a command.
    user_arg = input("Enter an argument for the simulated command: ")
    command = "echo Simulated vulnerability: " + user_arg
    print("Simulated command (unsafe):", command)
    subprocess.call(command, shell=True)  # unsafe usage!

def extended_menu():
    print("=" * 50)
    print("Extended Options")
    print("=" * 50)
    print("8. Process data with unsafe eval")
    print("9. Load and run a script unsafely using exec")
    print("10. Simulate a vulnerability with unsafe subprocess call")
    print("11. Return to main menu")

def extended_main():
    while True:
        extended_menu()
        choice = input("Enter your choice (8-11): ")
        if choice == "8":
            data = input("Enter data to process: ")
            process_data(data)
        elif choice == "9":
            load_and_run_script()
        elif choice == "10":
            simulate_vulnerability()
        elif choice == "11":
            break
        else:
            print("Invalid choice, please select from 8-11")
        print("\nSleeping for 2 seconds before showing extended menu again...\n")
        time.sleep(2)

# Modify main to include extended options
def main_with_extended():
    while True:
        main_menu()
        print("12. Extended options")
        print("7. Exit")
        choice = input("Enter your choice (1-7, 12 for extended): ")
        if choice == "1":
            user_input = "Hello World!"
            unsafe_shell_command(user_input)
        elif choice == "2":
            user_input = "Hello Secure World!"
            safe_shell_command(user_input)
        elif choice == "3":
            run_system_command()
        elif choice == "4":
            execute_custom_command()
        elif choice == "5":
            execute_safe_custom_command()
        elif choice == "6":
            rand_str = generate_random_string(12)
            unsafe_shell_command(rand_str)
        elif choice == "12":
            extended_main()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select a valid option")
        print("\nSleeping for 2 seconds before showing menu again...\n")
        time.sleep(2)

if __name__ == "__main__":
    # Uncomment the line below to run with extended options
    # main_with_extended()
    main()
