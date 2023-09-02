#!/usr/bin/env python3
import subprocess
import re
import os
import platform
import random
import tempfile

testnbr=0
# Get the current operating system
current_os = platform.system()
timeout_duration = 2
# Set the checker filename based on the operating system
if current_os == 'Linux':
    checker_filename = 'checker_linux'
elif current_os == 'Darwin':  # macOS
    checker_filename = 'checker_Mac'
print(f'Current OS: {current_os}')
print(f'Checker filename: {checker_filename}')
#if current_os == 'Darwin':
    #print("*** Memory Leak check is supported on Linux only. Skipping memory leak check on macOS. ***")
yellow = "\033[1;33m"
green = "\033[1;32m"
red = "\033[1;31m"
reset = "\033[0;0m"

filename = 'push_swap'
if not os.path.exists(filename):
    print(f'The file "{filename}" either does not exist or does not have execute permission.')
    print(f'Please run make and put the file in the same folder')
    exit (1)
if not os.path.exists(checker_filename) or not os.access("./"+checker_filename, os.X_OK):
    print(f'The file "{checker_filename}" either does not exist or does not have execute permission.')
    print("Please download it from https://projects.intra.42.fr/42cursus-push_swap/mine")
    print(f"and give it execute permission (chmod +x {checker_filename})")
    exit (1)


def testcase(nbrs):
    global testnbr
    testnbr += 1
    segfault = ""
    if current_os == 'Linux':
        result = subprocess.run(["timeout", str(timeout_duration), "valgrind", "--leak-check=full", "./push_swap", nbrs], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output = result.stderr + result.stdout
        #output = output.decode()
        memory_usage = re.search(r"in use at exit: (\d+) bytes in", output)
        memory_errors = re.search(r"ERROR SUMMARY: (\d+) errors", output)
        num_inuse = 0
        if memory_usage:
            num_inuse = int(memory_usage.group(1))
        num_memerr = 0
        if memory_errors:
            num_memerr = int(memory_errors.group(1))
        result3 = subprocess.run(f"./push_swap {nbrs}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result2 = subprocess.run(f"./push_swap {nbrs} | ./{checker_filename} {nbrs}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if "Segmentation fault" in result3.stderr or "Segmentation fault" in result2.stdout:
            segfault = f"{red}SegFault!{reset}"
    elif current_os == 'Darwin':  # macOS
        output= ""
        with tempfile.TemporaryFile() as temp_file:
            result = subprocess.run(["leaks" ,"-q","-atExit", "--", "./push_swap", nbrs],   stdout=temp_file, stderr=subprocess.DEVNULL, timeout=5)
            temp_file.seek(0)
            output = temp_file.read().decode().rstrip()
        #print(result)
        #output = result.stdout.decode().rstrip()
        #output = output.decode()
        #print(output)
        #exit(1)
        pattern = r"(\d+)\s+total leaked bytes"
        match = re.search(pattern, output)
        num_inuse = 0
        if match:
            num_inuse = int(match.group(1))
        else:
            num_inuse = 0
        num_memerr = 0
        result3 = subprocess.run(f"./push_swap {nbrs}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result2 = subprocess.run(f"./push_swap {nbrs} | ./{checker_filename} {nbrs}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    print(f"#{str(testnbr).rjust(2)} {yellow}{nbrs.ljust(40)}{reset}", end=" ")
    output3 = result3.stdout + result3.stderr
    exists_error = re.search(r"Error\n", output3)
    output2 = ""; output2 = result2.stdout + result2.stderr
    res2 = ""
    is_error = re.search(r"Error", output2)
    if "OK" in str(output2):
        res2=f"{green}OK{reset}"
    if "KO" in str(output2):
        res2=f"{red}KO{reset}"
    if len(segfault):
        print(f"{segfault}".ljust(15), end=" ")
    if num_inuse:
        print(f"{red}MKO: {reset} {num_inuse} byte(s) still reachable!".ljust(40), end="")
    elif num_memerr:
        print(f"{red}MKO: {reset} {num_memerr} memory error(s)!".ljust(40), end="")
    else:
        print(f"Memory: {green}OK{reset}".ljust(40), end="")
    if exists_error and is_error:
        print(f" Error handling: {green}OK{reset}".ljust(30), end="")
    elif not exists_error and is_error:
        print(f" Error handling: {red}KO{reset}".ljust(30), end="")
    if "Error\n" not in output2:
        print(f" Sorting: {res2}".ljust(15), end="")     
    print("")

testcase("\"\"")
testcase("\" \"")
testcase("")
testcase(" ")
testcase("-")
testcase("+")
testcase("6")
testcase("6 4")
testcase("a 3 2")
testcase("4 4 6")
testcase("6 -1 4")
testcase("4 6 4")
testcase("6 3 4")
testcase("4 6 3")
testcase("4 6 3u")
testcase("4 6- 3")
testcase("4 6-1 3")
testcase("4 6+1 3")
testcase("9 8 7 -6")
testcase("2147483647 -2147483648")
testcase("2147483648 -2147483649")
testcase("9 9223372036854775807")
testcase("9 -9223372036854775808")
testcase("9 9223372036854775808")
testcase("9 -9223372036854775809")
testcase("0 1 2 3 4 5 6 7 8 9")
testcase("5 3 1 2 4 6")
testcase("2147483649 2147483649 2147483649")
testcase("2 22 12 +0")
testcase("2 22 12 -0")
testcase("2 22 0 +0")
testcase("2 22 0 -0")
testcase("10 9 8 7  1 4 3 2 0")

def test_with_random_numbers(num_random_numbers):
    random.seed(42)
    nbrs_set = set()
    while len(nbrs_set) < num_random_numbers:
        nbrs_set.add(random.randint(-2147483648, 2147483647))
    nbrs = " ".join(str(n) for n in nbrs_set)
    print(f"Testing with {num_random_numbers} random numbers...")
    testcase(nbrs)

test_with_random_numbers(5)
test_with_random_numbers(100)
test_with_random_numbers(500)
