#!/usr/bin/env python3
import subprocess
import re
import os
import platform

# Get the current operating system
current_os = platform.system()
# Set the checker filename based on the operating system
if current_os == 'Linux':
    checker_filename = 'checker_linux'
elif current_os == 'Darwin':  # macOS
    checker_filename = 'checker_Mac'
print(f'Current OS: {current_os}')
print(f'Checker filename: {checker_filename}')
yellow = "\033[1;33m"
green = "\033[1;32m"
red = "\033[1;31m"
reset = "\033[0;0m"

filename = 'push_swap'
if not os.path.exists(filename):
    print(f'The file "{filename}" either does not exist or does not have execute permission.')
    exit (1)
if not os.path.exists(checker_filename) or not os.access("./"+checker_filename, os.X_OK):
    print(f'The file "{checker_filename}" either does not exist or does not have execute permission.')
    exit (1)


def testcase(nbrs):
    if current_os == 'Linux':
        result = subprocess.run(["valgrind", "--leak-check=full", "./push_swap", nbrs], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stderr.decode()
        memory_usage = re.search(r"in use at exit: (\d+) bytes in", output)
        memory_errors = re.search(r"ERROR SUMMARY: (\d+) errors", output)
        num_inuse = 0
        if memory_usage:
            num_inuse = int(memory_usage.group(1))
        num_memerr = 0
        if memory_errors:
            num_memerr = int(memory_errors.group(1))
    elif current_os == 'Darwin':  # macOS
        result = subprocess.run(["leaks", "./push_swap", nbrs], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        num_inuse = re.search(r"total\s+(\d+)\s+bytes\s+leaked", output)
        num_memerr = 0
    
    print(f"{yellow}[Numbers]:{reset} {nbrs.ljust(40)}", end="")
    exists_error = re.search(r"Error\n", output)
    result2 = subprocess.run(f"./push_swap {nbrs} | ./{checker_filename} {nbrs}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output2 = result2.stdout + result2.stderr
    res2 = ""
    is_error = re.search(r"Error", output2)
    if re.search(r"OK", output2):
        res2=f"{green}OK{reset}"
    if re.search(r"KO", output2):
        res2=f"{red}KO{reset}"
    if num_inuse:
        print(f"{red}MKO{reset} {num_inuse.group(1)} bytes still reachable!".ljust(40), end="")
    elif num_memerr:
        print(f"{red}MKO{reset} {num_memerr} memory errors!".ljust(40), end="")
    else:
        print(f"Memory: {green}OK{reset}".ljust(40), end="")
    if exists_error and is_error:
        print(f"Error handling: {green}OK{reset}".ljust(30), end="")
    if not exists_error and is_error:
        print(f"Error handling: {red}KO{reset}".ljust(30), end="")
    if not re.search(r"Error\n", output2):
        print(f"Sorting: {res2}".ljust(15), end="")
    
    print("")




testcase("")
testcase(" ")
testcase("-")
testcase("+")
testcase("a 3 2")
testcase("4 4 6")
testcase("6 4 4")
testcase("4 6 4")
testcase("6 3 4")
testcase("4 6 3")
testcase("4 6 3u")
testcase("4 6- 3")
testcase("2147483647 -2147483648")
testcase("2147483648 -2147483649")
testcase("0 1 2 3 4 5 6 7 8 9")
testcase("9 8 7 6 5 4 3 2 1 0")
testcase("5 3 1 2 4 6")
testcase("2147483649 2147483649 2147483649")
testcase("2 2 2 2 2 2 2")
testcase("10 9 8 7 6 5 4 3 2 1 0")

