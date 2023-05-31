# tester_push_swap
A Python script that tests memory leaks, errors, and error handling for push_swap. 

# Usage
Run following command: (in the directory where your ./push_swap and checker_(linux or mac) programs are) 

```
curl https://raw.githubusercontent.com/hu8813/tester_push_swap/main/pstester.py | python3 -
```


OR you can install python package:


```
pip install test-push-swap
```
```
test_push_swap
```
# Uninstall
If you have installed via pip and want to uninstall it: 

```
pip uninstall test-push-swap -y
```

# Screenshot of a Test Result

![Push_swap tester screenshot](screenshot.png)

It works well with Valgrind on Linux, but will NOT check Memory on Mac.
