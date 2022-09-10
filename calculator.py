r"""A smart calculator app.
A general expression can contain many parentheses and operations with different
priorities. To calculate such expressions smart calculator uses postfix
notation, also known as Reverse Polish notation (RPN).
The calculator is able to store the results of previous calculations to
variables

Examples:
> 3 +++ 8 * ((4 + 3) * 2 -- 1) --- 6 / (2 + 1)
121
Note that a sequence of + (like +++ or +++++) is an admissible operator is
interpreted as a single plus. A sequence of - (like -- or ---) is also an
admissible operator and its meaning depends on the length. If a user enters
a sequence of * or /, the program will print a message that the expression
is invalid.

> a = 2
> b = 3
> c = a * b
> c
6
"""

import re

OPERATOR_PRIORITY = {'-': 1,
                     '+': 1,
                     '*': 2,
                     '/': 2,
                     '=': 0,
                     '(': 3,
                     ')': 3
                     }
LETTER = r'[a-zA-Z]'
DIGIT = r'[0-9]'
OPERAND = r'[a-zA-Z0-9]'
OPERATOR = r'[*/+=-]'
ABANDONED_PATTERNS = [r'\*\-',
                      r'\*\+',
                      r'\*\*',
                      r'\*\/',
                      r'\/\/',
                      r'\/\*',
                      r'\/\+',
                      r'\/\-',
                      r'\+\/',
                      r'\+\*',
                      r'\-\/',
                      r'\-\*', ]
VARIABLES = {}


def validate_input(eq):
    if eq.count('(') != eq.count(')'):
        print('Invalid expression')
        return False
    if re.match(r'[*/=]', eq[0]) or re.match(OPERATOR, eq[-1]):
        print('Invalid expression')
        return False
    for pattern in ABANDONED_PATTERNS:
        if re.search(pattern, eq):
            print('Invalid expression')
            return False
    if re.search(r'[\d][a-zA-Z]', eq):
        print('Invalid identifier')
        return False
    if re.search(r'[a-zA-Z][\d]', eq):
        print('Invalid identifier')
        return False
    if eq.count('=') > 1:
        print('Invalid expression')
        return False
    return True


def start(eq):
    if not validate_input(eq):
        return False
    eq = [x for x in eq if x != ' ']
    return eq


def get_operator(template, eq, temp):
    try:
        if re.match(template, eq[1]):
            temp += get_operator(template, eq[1:], temp)
        else:
            return eq[0]
    except IndexError:
        pass
    temp = eq[0] + temp
    return temp


def operator_analyze(item):
    if len(item) == 1:
        return item
    result = '+'
    for i in item:
        if i == '+':
            pass
        elif i == '-':
            if result == '+':
                result = '-'
            elif result == '-':
                result = '+'
    return result


def prepare_equation(eq):
    initial_eq = []
    temp = ''
    eq = list(eq)
    while len(eq) > 0:
        if re.match(DIGIT, eq[0]):
            operator = get_operator(DIGIT, eq, temp)
            del (eq[0:len(operator)])
            initial_eq.append(int(operator))
        elif re.match(LETTER, eq[0]):
            operator = get_operator(LETTER, eq, temp)
            del (eq[0:len(operator)])
            initial_eq.append(operator)
        elif re.match(OPERATOR, eq[0]):
            operator = get_operator(OPERATOR, eq, temp)
            del (eq[0:len(operator)])
            initial_eq.append(operator)
        elif re.match(r'[(]', eq[0]):
            initial_eq.append('(')
            del (eq[0])
        elif re.match(r'[)]', eq[0]):
            initial_eq.append(')')
            del (eq[0])
    for index, value in enumerate(initial_eq):
        try:
            if re.match(r'[+-]+$', value):
                initial_eq[index] = operator_analyze(value)
        except TypeError:
            pass
    return initial_eq


def make_rpn(eq):
    stack = []
    result = []
    for item in eq:
        if isinstance(item, int):
            result.append(item)
        elif re.match(LETTER, item):
            result.append(item)
        elif item == '(':
            stack.append(item)
        elif re.match(OPERATOR, item):
            if len(stack) == 0 or stack[-1] == '(':
                stack.append(item)
                continue
            if re.match(OPERATOR, stack[-1]):
                if OPERATOR_PRIORITY[item] > OPERATOR_PRIORITY[stack[-1]]:
                    stack.append(item)
                elif OPERATOR_PRIORITY[item] <= OPERATOR_PRIORITY[stack[-1]]:
                    while len(stack) >= 0:
                        if stack[-1] == '(':
                            break
                        elif OPERATOR_PRIORITY[stack[-1]] < OPERATOR_PRIORITY[item]:
                            stack.append(item)
                            # result.append(stack.pop())
                            break
                        else:
                            result.append(stack.pop())
                            stack.append(item)
                            break

            else:
                stack.append(item)  # ?
        elif item == ')':
            while len(stack) > 0:
                if stack[-1] != '(':
                    result.append(stack.pop())
                else:
                    del stack[-1]
                    break
    while len(stack) > 0:
        result.append(stack.pop())
    return result


def calculate_rpn(rev_pol_notation):
    stack = []
    assign = False
    if rev_pol_notation[-1] == '=':
        assign = True
    for item in rev_pol_notation:
        if isinstance(item, int):
            stack.append(item)
        elif re.match(LETTER, item):
            if assign and rev_pol_notation.index(item) == 0:
                stack.append(item)
            else:
                if item in VARIABLES:
                    stack.append(VARIABLES[item])
                else:
                    print('Unknown variable')
                    return None

        elif re.match(OPERATOR, item):
            a = stack.pop()
            b = stack.pop()
            if item == '=':
                VARIABLES[b] = a
                return None
            else:
                temp_eq = str(b) + str(item) + str(a)
                # temp = int(eval(temp_eq))
                temp = eval(temp_eq)
                stack.append(temp)
    print(stack[-1])


if __name__ == '__main__':

    while True:
        user_input = input()
        if user_input == '':
            continue
        if user_input[0] == r'/':
            if user_input == '/exit':
                print('Bye!')
                break
            elif user_input == '/help':
                print('The program calculates the sum of numbers')
                continue
            else:
                print('Unknown command')
                continue
        valid_equation = start(user_input)
        if valid_equation:
            prepared_equation = prepare_equation(valid_equation)
            if prepared_equation is None:
                continue
            rpn = make_rpn(prepared_equation)
            calculate_rpn(rpn)
            # print(VARIABLES)
