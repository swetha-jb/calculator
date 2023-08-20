"""
File: formulas.py
Description: 
    Implements formulas for vector calculus (as well as more simple) calculations
    to be used on the calculator page for symbolic and calculus calculations in main.py.
"""

import sympy as smp


# Symbolic assignments (much easier for operational tasks)
x, y, z, t, n = smp.symbols("x y z t n")
poss_vars = ['x', 'y', 'z']
operators = ['+', '-', '*', '/', '^']
special = ['π', 'e', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'ln', 'log']

# ---------------- Functions ----------------

def derivative(expr, wrt):
    """
    Calculates derivative of an expression
    :param expr: expression
    :param wrt: with respect to
    :returns: evaluated derivative
    """
    return smp.diff(expr, wrt)

def partial_deriv(expr, wrt):
    """
    Calculates partial derivative of an expression
    :param expr: expression
    :param wrt: with respect to
    :returns: simplified evaluated partial derivative
    """
    return smp.simplify((smp.diff(expr, wrt)))

def integral(expr, wrt, r1, r2):
    """
    Calculates integral of an expression
    :param expr: expression
    :param wrt: with respect to
    :param r1: left bound
    :param r2: right bound
    :returns: evaluated integral
    """
    if r1 == '' and r2 == '':  
        # No bounds
        return smp.integrate(expr, wrt)
    else:
        # Numeric or infinite bounds
        return smp.integrate(expr, (wrt, r1, r2))

def limit(expr, var, toward, side=None):
    """
    Calculates limit of an expression
    :param expr: expression
    :param var: variable approaching
    :param towar: approaching
    :side: from left / right / None
    :returns: evaluated limit
    """
    if side == None:
        return smp.limit(expr, var, toward) + ' C' 
    else:
        return smp.limit(expr, var, toward, side) + ' C'
    
def series(expr, i, n):
    """
    Calculates series of an expression
    :param expr: expression
    :param i: i variable
    :param n: n variable
    :returns: evaluated series
    """
    return smp.Sum(expr, i, n)

def natural_log(expr):
    """
    Calculates natural log of an expression
    :param expr: expression
    :returns: evaluated ln
    """
    return smp.ln(expr)

def get_log(expr):
    """
    Calculates log of an expression
    :param expr: expression
    :returns: evaluated log
    """
    return smp.log(expr)

def regular(expr):
    """
    Evaluates non formulatic symbolic and 
    non symbolic expressions and segments

    :param expr: expression
    :returns: evaluated expression
    """

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
    result = eval(expr)
    return result

# ---------------- Clean up / Inside-eval ----------------

def clean(expr):
    """
    Cleans user input expression before evaluation 
    so that sympy can read and understand it

    :param expr: expression
    :returns: cleaned expression for evaluation
    """

    # Length edge-case
    if len(expr) < 1:
        return expr
    else:
        # Initialize to first char (loop starts from i=1, checking i-1)
        cleaned_expr = expr[0]

    try:
        # Lack of * sign
        for i in range(1, len(expr)):  # edge cases: 6x -> 6*x, x^2 -> x**2
            if (expr[i-1].isnumeric() and expr[i] in poss_vars) or (expr[i] == '(' or expr[i-1] == ')') \
                and (expr[i-1] not in operators and expr[i] not in operators):
                if (expr[i-1] in '()' and expr[i] in '()') or \
                    ((not expr[i-1].isnumeric() and expr[i-1] not in operators and expr[i-1] not in poss_vars) and expr[i] == '('):
                    # In case of parens
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
    except:
        return None
    
def inside_expr(operation, expr, c):
    """
    Evaluate inside expressions after expr cleaned with
    function conditions / specifications

    :param operation: string representation of operation
    :param expr: expression
    :param c: list of functions conditionals
    :returns: expression evaluation
    """

    wrt = x
    if c[0] == 'y':
        wrt = y
    elif c[0] == 'z':
        wrt = z

    try:
        if operation == 'd/dx':
            return derivative(expr, wrt)
        if operation == '∫':
            return integral(expr, wrt, c[2], c[3])
        if operation == 'lim':
            return limit(expr, wrt, c[1])
        if operation == '∂/∂x':
            return partial_deriv(expr, wrt)
        if operation == 'Σ':
            return series(expr, c[4], c[5])
        if operation == 'regular':
            return regular(expr)
    except:
        return None
    
def post_clean(expr):  
    """
    After evaluation return expression into a textually
    pleasing syntax, akin to what user would input

    :param expr: expression
    :return: user readable expression string
    """

    # ** -> ^  |  * to ''
    if expr == None:
        return None
    
    expr = expr.replace('pi', 'π')
    expr = expr.replace('E', 'e')

    new_expr = ''
    for i in range(len(expr)):
        if expr[i] == '*' and expr[i + 1] == '*':
            new_expr += '^'
        elif expr[i] == '*':
            new_expr += ''
        else:
            new_expr += expr[i]
    return new_expr

# ---------------- Main Calculation ----------------

def calculate(expr, conditions):
    """
    Calculates symbolic expressions

    :param expr: expression
    :param conditions: conditions
    :returns: finalized expression
    """

    expr = expr.replace(' ', '')
    table = expr.maketrans('[', ']')
    expr = expr.translate(table).split(']')
    poss_oper = ['d/dx', '∫', 'lim', '∂/∂x', 'Σ']
    for start in range(len(expr)):
    
        # 0: derivative, 1: integral, 2: limit, 3: partial_deriv, 4: series
        if expr[start] in poss_oper:
            new_expr = ''
            operation = expr[start]
            for calc in range(start+1, len(expr)):
                if expr[calc] == '':
                    break
                else:
                    new_expr += expr[calc]
            new_expr = clean(new_expr)

            # If clean doesn't pass, syntax error
            if new_expr == None: 
                return 'ERROR'
            
            new_expr = inside_expr(operation, new_expr, conditions)
            new_expr = str(new_expr)
            new_expr = post_clean(new_expr)
            return new_expr
        else:
            # Basic calculations
            new_expr = str(expr[start])
            new_expr = clean(new_expr)
            new_expr = inside_expr('regular', new_expr, conditions)
            new_expr = str(new_expr)
            new_expr = post_clean(new_expr)
            return new_expr
    return None


# Test:
if __name__ == '__main__':
    expression = 'arcsin(x)'
    print(calculate(expression, ['', '', '', '', '', '']))