# Smart calculator
> Also known as Noughts and Crosses or X's and O's. 

## Table of Contents
* [About](#About)
* [Examples](#Examples)
* [Technologies Used](#technologies-)
* [Github Link](#Github-link)


## About
A general expression can contain many parentheses and operations with different priorities. To calculate such expressions smart calculator uses postfix notation, also known as Reverse Polish notation (RPN). The calculator is able to store the results of previous calculations to variables

## Examples:
> 3 +++ 8 * ((4 + 3) * 2 -- 1) --- 6 / (2 + 1)
> 121

Note that a sequence of + (like +++ or +++++) is an admissible operator is
interpreted as a single plus. A sequence of - (like -- or ---) is also an
admissible operator and its meaning depends on the length. If a user enters
a sequence of * or /, the program will print a message that the expression
is invalid.

## Technologies Used
- Python v3.6 or more
- Reverse Polish notation
- Regular expressions (RE)

## Github link
https://github.com/savchenkonick/smart-calculator
