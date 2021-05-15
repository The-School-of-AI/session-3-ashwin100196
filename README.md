# Base Encodings, Floating points and Python rounding

## Base Encoding

A simple way to understand different bases is to consider that there are numbers (decimal as we understand them) and their representation in an encoding .a.k.a the base. Say we consider 5, which would be the number, and 101 would be its representation in base 2. 

This module provides the capability to convert from a number from any base representation to any other

### Classes

1. __BaseEncoder__ - An encoder class that provides functionality to convert from one base to another

    > Attributes</br>
    > source_base - the base of the number that will be sent as input</br>
    > to_base - the base in which the number is to be encoded. needs to lie between [2,36] or a ValueError is raised</br>
    > digit_map - the map of the base to be converted into. This needs to be as long as to_base, else a ValueError is raised</br>
    > source_digit_map - this is an optional attribute that gets initialised automatically from the map '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' based on value of source_base</br>

    > Methods</br>
    > __init__ : initializes the encoder object which initializes the bases and digit maps</br>
    > __repr__ : Provides the details of the encoder object</br>
    > __decode__to_decimal__ : internally invoked during encoding when source_base is not 10</br>
    > __encode__ : accepts a number and returns its encoded representation</br>

### Functions

1. __encoded_from_base10__ - Converts a number from decimal to the required base. Internally creates a base encoder object with source_base 10 and target base as passed. 

    > Arguments</br>
    > number - the number to be encoded</br>
    > base - the base to be represented in</br>
    > digit_map -the representation map of digits to be used in target base</br>
    
    > Returns</br>
    > encoded_number - this is the encoded representation of the passed number in the required base</br>
    
    > Usage</br>
    > BaseEncoder() by default creates an encoder from decimal to hexadecimal working as the hex() inbuilt function</br>
    > encoded_from_base10(10, 2, '01') works as the bin() internal function converting a number into binary</br>

## Floating points

Wait, how can points float? You may be wondering this, but it seems the naming is purely metaphorical. Like how the point I am making in this readme is floating away from you. In reality, a floating point is nothing but a number which has digits on either side of the dot like pi 3.14159265.

Python has a funny way of saving these numbers, as rational numbers - a number in the form p/q. Basically as fractions. But some numbers just cant be represented accurately in floating point, like 1/3 = 0.33333333....3tillendoftheworld. As we know, computers dont work in the decimal system like the human minds, but work in binary. And big surprise, here there are even more such numbers which we cannot represent properly. For example 0.1 itself cannot be represented using binary as it is a recurring 0.00011001100110011...0011tilltheendoftheworld.

This espescially becomes a problem when we want to check equality. In python, if we attempt to check if 0.1x5 is equal to 0.5, the result comes out to be false. This is because 0.1 is represented as something like this: Fraction(3602879701896397, 36028797018963968) to achieve a high level of precision. however it is not truly precise. Checking precision to 25 significant digits we can see that 0.1 is actually 0.1000000000000000055511151. This is the hard truth of any number system, and hence our equality testing needs to be upgraded.

One solution would be to check if the difference between two numbers a and b is less than an absolute tolerance

```python
abs(a - b) < tol
```

While this works, it is not perfect because this will nto work when the scale of the numbers changes, for eg 0.5 maybe a good tolerance to say if 9999.9 is close to 10000.3, and we could say they are equal, but it breaks when we compare numbers in the range of 0.1 and 0.2.

A solution would be to to consider relative tolerances and scale them based on the scale of numbers like so

```python
rel_tol * max(abs(a), abs(b))
```

This is more elegant but also faces a challenge, namely when dealing with very small numbers of the range of 1e-10. In such case, the relative tol makes the tolerance very strict failing equality

Hence the ideal solution recommended by PEP is shown below where both the solutions are combined

```python
tol = max(rel_tol * max(abs(a), abs(b)), abs_tol)
```
Checking if the difference lies within this tolerance will indicate equality for us in python. Wow, what a rollercoaster!!!!

Fortunately, math library in python has the solution for us in a single line wiht the math.isclose() function

```python
from math import isclose
x = 0.00000000000003
y = 0.00000000000005
isclose(x, y, rel_tol=0.01, abs_tol=0.01)
True
```
### Functions

1. __float_equality_testing__ - Checks if two numbers are equal using the concept of tolerances. Relative tolerance is considered as 1e-12 and absolute tolerance as 1e-5

    > Arguments</br>
    > a - one of the number for equality comparison</br>
    > b - the other number for equality comparison</br>

    > Returns</br>
    > is_equal - a boolean indicating if the numbers are equalt</br>
    
    > Usage</br>
    > float_equality_testing(0.00000000000003, 0.00000000000005)</br>
    > True</br>

## Python rounding

Rounding of numbers is an important funtionality to represent a floating point number in the required precision. Python employs the bankers rouning which rounds numbers to the closest even significant digit. This is done to maintain averages while rounding and minimize biases due to rounding. It is facilated with the in-built function round()
 
```python
round(1.25, 1)
1.2
round(1.35, 1)
1.4
```

Another common methodolgy used is to round away from zero, the rounding we expect mathematically. Using this approach 1.25 would get rounded to 1.3, and -1.25 to -1.3.

Sometimes we would also not want to round the value and instead just truncate the decimals. This can be done either using the math.trunc() function or the inbuilt constructor of int and float.

```python
import math
math.trunc(1.25)
1
int(1.25)
1
```

### Functions

Functions for rounding, truncation and rounding away from zero have been implemented from scratch as well here. The rounding is done to the nearest integer for simplicity of illustration. Also, an error is raised if the passed number is not an integer or floating point

> Arguments</br>
> f_num - the number to be rounded/truncated
    
> Returns</br>
> truncated/rounded - the result of truncating/rounding

1. __manual_truncation_function__ - This function truncates the float number passed preserving only the integer part of it
2. __manual_rounding_function__ - This function rounds the number by the method of Banker's rounding - the same way as the python round() function
3. **rounding_away_from_zero** - this function rounds away from zero as explained above

### Test Case Results

The test cases have all passed as shown below.
![TestCases](/test_cases_results.png)