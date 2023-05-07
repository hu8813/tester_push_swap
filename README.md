# tester_push_swap
A Python script that tests memory leaks, errors, and error handling for push_swap. 

# Usage
To use it, you can install python package: 

```
pip install test-push-swap
```

then, in the directory where your ./push_swap and checker programs are, run following command:

```
test_push_swap
```

OR (without need to install python package), just run:

```
curl https://raw.githubusercontent.com/hu8813/tester_push_swap/main/pstester.py | python3 -
```

# Uninstall
If you installed via pip and want to uninstall it: 

```
pip uninstall test-push-swap -y
```

![Push_swap tester screenshot](screenshot.png)

It works well with valgrind on Linux, but may not check memory on Mac.
