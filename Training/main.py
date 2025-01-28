"""
Write a program that finds the summation of every number from 1 to num. 
The number will always be a positive integer greater than 0.
Your function only needs to return the result, what is shown between parentheses in the example below is 
how you reach that result and it's not part of it, see the sample tests.

For example (Input -> Output):

2 -> 3 (1 + 2)
8 -> 36 (1 + 2 + 3 + 4 + 5 + 6 + 7 + 8)
"""
def summation(num):
    count = 0
    for i in range(num): count += i + 1

"""
Create a function that accepts a list/array and a number n, and returns a list/array of the first n elements from the list/array.
""" 
def take(arr,n):
    return arr[:n]

"""
Create a function add(n)/Add(n) which returns a function that always adds n to any number

add_one = add(1)
add_one(3)  # 4

add_three = add(3)
add_three(3) # 6
"""
def add(n):
    count = n
    def inner_add(x):
        return x + count
    return inner_add

def main():
    add_three = add(1)
    add_three(3)
    

if __name__ == '__main__':
    main()