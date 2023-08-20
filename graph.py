"""
File: graph.py
Description:
    Implements graph representation of functions for the 
    graphs page in main.py.
"""

import sympy as smp
from calculator import clean


# Symbolic initialization
x, y, z, alpha, beta = smp.symbols('x y z alpha beta', real=True)
i, j, k = smp.symbols('i j k', integer=True, positive=True)

def graph(expr):
    """
    Graphs an expression using sympy's plot method

    :param expr: expression to be graphed
    :returns: graph window
    """

    # Cleans syntax
    expr = expr.replace(' ', '')
    f = clean(expr)
    try:
        plot = smp.plot(f, legend=True, show=False)
    except:
        return
    plot.show()


# Test:
if __name__ == '__main__':
    expression = '4x + x^2'
    print(graph(expression))