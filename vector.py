"""
File: vector.py
Description:
    Implements vector calculations for more complicated and specific 
    expressions than in calculator.py, for the functions page in main.py.
"""

import numpy as np
import sympy as smp
from scipy.integrate import quad
from calculator import post_clean


# Symbolic initialization
t, x, y, z = smp.symbols('t x y z')
poss_vars = ['t', 'x', 'y', 'z']
operators = ['+', '-', '*', '/', '^']


# ------------------ Conversion / Cleaning ------------------

def clean(expr):
    """
    Cleans user input and translates symbols to sympy

    :param expr: expression
    :returns: cleaned expression for evaluation
    """

    expr = expr.replace(' ', '')
    expr = expr.replace('sqrt', 'smp.sqrt')
    expr = expr.replace('e', 'smp.E')
    expr = expr.replace('π', 'smp.pi')
    expr = expr.replace('ln', 'smp.ln')
    expr = expr.replace('log', 'smp.log')
    expr = expr.replace('sin', 'smp.sin')
    expr = expr.replace('cos', 'smp.cos')
    expr = expr.replace('tan', 'smp.tan')
    expr = expr.replace('csc', 'smp.csc')
    expr = expr.replace('cot', 'smp.cot')
    expr = expr.replace('sec', 'smp.sec')
    expr = expr.replace('^', '**')
    return expr

def clean_symbolic(expr):
    """
    Cleans user input expression before evaluation 
    so that sympy can read and understand it

    :param expr: expression
    :returns: cleaned symbolic expression
    """

    # Inital clean
    expr = clean(expr) 

    if len(expr) < 1:
        return expr
    else:
        # Initialize to first char (loop starts from i=1, checking i-1)
        cleaned_expr = expr[0]

    for i in range(1, len(expr)):  # edge cases: 6x -> 6*x, x^2 -> x**2
            if (expr[i-1].isnumeric() and expr[i] in poss_vars) or (expr[i] == '(' or expr[i-1] == ')') \
                and (expr[i-1] not in operators and expr[i] not in operators):
                if (expr[i-1] in '()' and expr[i] in '()') or \
                    ((not expr[i-1].isnumeric() and expr[i-1] not in operators and expr[i-1] not in poss_vars) and expr[i] == '('):
                    # In case of parens and (ex.) sqrt(x)
                    cleaned_expr += expr[i]
                else:
                    # Sandwich a '*'
                    cleaned_expr += '*' + expr[i]
            elif expr[i] == '^':
                # '^' -> '**'
                cleaned_expr += '**'
            else:
                cleaned_expr += expr[i]
    return cleaned_expr

def str_to_array(vec):
    """
    Change string into an array of integers

    :param vec: expression
    :returns: array of expression
    """

    # Clean before split
    vec = vec.replace(' ', '')
    vec = vec.replace('(', '')
    vec = vec.replace(')', '')
    vec = vec.replace('[', '')
    vec = vec.replace(']', '')

    # Create array
    vec = vec.split(',')
    arr = []
    for num in vec:
        # Turn string nums into ints
        arr.append(int(num))
    return arr

def str_to_array_dim(matrix):
    """
    Change string into an array of integers
    for a dimensional expression (matrixes)

    :param matrix: matrix expression
    :returns: matrix expression as a cleaned & seperated array
    """

    # Clean before split
    matrix = matrix.replace(' ', '')
    matrix = matrix.replace('[', '')
    matrix = matrix.replace(']', '')

    # Create array
    matrix_rows = matrix.split(';')
    arr = []
    for row in matrix_rows:
        # Split row into individual numbers
        row_nums = row.split(',')

        # Convert string nums into ints and append to the row
        arr.append([int(num) for num in row_nums])  
    return arr

def str_to_array_expr(vec):
    """
    Changes string expression into an array of expressions

    :param vec: expression
    :returns: array of expression
    """

    temp_str = ''
    vec = vec.replace(' ', '')
    if (vec[0] == '(' or vec[0] == '[') and (vec[len(vec)-1] == ')' or vec[len(vec)-1] == ']'):
        # Remove possible outside parenthesis / brackets
        temp_str = vec[1:len(vec)-1]
    else:
        temp_str = vec
    
    # Format / clean and turn into array
    temp_arr = temp_str.split(',')
    arr = []
    for expr in temp_arr:
        arr.append(clean_symbolic(expr))
    return arr


# ------------------ Operations ------------------

def add(a, b):
    """
    Vector addition
    :param a: vector a
    :param b: vector b
    :returns: added vectors
    """
    a = np.array(str_to_array(a))
    b = np.array(str_to_array(b))
    return a+b

def sub(a, b):
    """
    Vector subtraction
    :param a: vector a
    :param b: vector b
    :returns: subtracted vectors
    """
    a = np.array(str_to_array(a))
    b = np.array(str_to_array(b))
    return a-b

def dot_product(a, b):
    """
    Dot product
    :param a: vector a
    :param b: vector b
    :returns: dot product of the two vectors
    """
    a = np.array(str_to_array(a))
    b = np.array(str_to_array(b))
    return np.dot(a, b)

def det(a):
    """
    Determinant
    :param a: vector
    :returns: determinant
    """
    a = np.array(str_to_array_dim(a))
    det = np.linalg.det(a)
    return det

def cross_product(a, b):
    """
    Cross product
    :param a: vector a
    :param b: vector b
    :returns: cross product of the two vectors
    """
    a = np.array(str_to_array(a))
    b = np.array(str_to_array(b))
    return np.cross(a, b)

def norm_length(a):
    """
    Norm of a vector
    :param a: vector
    :returns: norm of vector
    """
    a = np.array(str_to_array(a))
    return np.linalg.norm(a)

def projection(a, b):
    """
    Projection of a vector onto another vector
    :param a: vector
    :param b: vector b
    :returns: projection of vector a on vector b
    """
    a = np.array(str_to_array(a))
    b = np.array(str_to_array(b))
    proj = np.dot(a, b) / np.linalg.norm(b) ** 2 * b
    return proj

def arc_length(a):
    """
    Arc length of a vector
    :param a: vector
    :returns: arc length of vector
    """
    a = np.array(str_to_array_expr(a))
    n_a = []
    for i in a:
        n_a.append(int(i))
    expr = smp.Matrix([n_a[0], n_a[1], n_a[2]])
    arc = smp.lambdify([t], smp.diff(expr,t).norm())

    # Evaluate integral from [0-1] using scipy quad method
    arc = quad(arc, 0, 1)[0]
    arc = str(arc)
    arc = post_clean(arc)
    return arc

def derivative(a):
    """
    Derivative of a vector
    :param a: vector
    :returns: derivative of the vector
    """
    a = np.array(str_to_array_expr(a))
    expr = smp.Matrix([a[0], a[1], a[2]])
    deriv = smp.diff(expr, t)
    deriv = str(deriv)

    # Clean derivative output
    deriv = deriv.replace('Matrix(', '')
    deriv = deriv.replace('[', '')
    deriv = deriv.replace('])', '')
    deriv = deriv.replace(']', '')
    cleaned_deriv = post_clean(deriv)
    return '[' + cleaned_deriv + ']'


# ------------------ Main Calculation ------------------

def vector_calc(oper, a, b=None):
    """
    Calculates vector / matrix operations

    :param oper: operation
    :param a: vector a or matrix expression
    :param b: vector b
    :returns: calculation based on operation
    """

    if oper == 'add':
        return add(a, b)
    if oper == 'sub':
        return sub(a, b)
    if oper == 'dot':
        return dot_product(a, b)
    if oper == 'det':
        return det(a)
    if oper == 'cross':
        return cross_product(a, b)
    if oper == 'projection':
        return projection(a, b)
    if oper == 'norm':
        return norm_length(a)
    if oper == 'length':
        return arc_length(a)
    if oper == 'deriv':
        return derivative(a)


# Test:
if __name__ == '__main__':
    expression = vector_calc('length', '[1, 2, 8]')
    print(expression)