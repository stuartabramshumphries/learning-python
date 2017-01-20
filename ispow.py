#!/usr/bin/python
# simple script to see if number is a power of 2 - think quicker way using math (log?) or bitwise comparison
def is_power(n):
    if n == 2: return True
    n = n/2.0
    if n == 2:
        return True
    elif n > 2:
        return is_power(n)
    else:
        return False


print map(is_power,range(33))
