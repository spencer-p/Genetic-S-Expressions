"""
gensexp

A module to generate and genetically manage s expressions.

Author: Spencer Peterson, 2018
"""

import json
import random as _random
random = _random.Random()
random.seed()

"""
Expressions in order:
    XOR, OR, AND, NOT, multiplication. division, modula, addition, subtraction,
    bitwise left shift, bitwise right shift, and index.

All of these satisfy a prefix s expression grammar:
    expr = (operator expr expr)

Except for 'i', index. With 'i', the first argument must be an array. Also note
that the index is not guarunteed by this package to be in bounds.

At the leafs, we have literals which are either a variable, an integer, or an
array.
"""
EXPRS = ['^', '|', '&', '%', '/', '*', '+', '-', '<<', '>>', 'i']
VAR = 't'

def serialize(expr):
    """
    Serialize an expression (list) into a string.
    """
    return json.dumps(expr)

def deserialize(expr):
    """
    Deserialize a string into a list.
    """
    return json.loads(expr)

def _generate_literal(odds_var, num_range):
    """
    Generate a literal with
        odds_var odds of it being a variable
        num_range range of numbers for ints
    """
    if random.random() <= odds_var:
        return VAR
    else:
        return random.randint(*num_range)

def _generate_array_literal(num_range):
    """
    Generate a literal array with numbers in num_range
    """
    # Correct the range to be valid for arrays
    size_range = num_range[:]
    if size_range[0] <= 0:
        difference = 1-size_range[0]
        size_range[0] += difference
        size_range[1] += difference

    return [random.randint(*num_range) for i in range(random.randint(*size_range))]

def generate(*, max_depth, num_range, odds_branch, odds_var):
    """
    Generates a new expression (list) with some parameters:
        max_depth: int, maximum recursive depth
        num_range: 2-tuple, range of random integers to use
        odds_branch: likelihood of branching instead of adding a literal (0-1)
        odds_var: likelihood of a literal being a variable vs int (0-1)
    """
    def recurse_or_literal():
        if random.random() <= odds_branch:
            return generate(
                    max_depth = max_depth - 1,
                    num_range = num_range,
                    odds_branch = odds_branch,
                    odds_var = odds_var,
                    )
        else:
            return _generate_literal(odds_var, num_range)

    if max_depth == 0:
        # Base case. Return a literal.
        return _generate_literal(odds_var, num_range)
    else:
        # Choose an operation
        op = random.choice(EXPRS)
        left, right = None, None

        # Generate left arg
        if op == 'i':
            # Index requires an array
            left = _generate_array_literal(num_range)
        else:
            left = recurse_or_literal()

        # Generate right arg
        right = recurse_or_literal()

        # Put together the sexp
        return [op, left, right]

def breed(expr1, expr2, percent_change):
    """
    Breed takes two expressions (lists) and a percent change (number). It
    returns a new expression (list) that is the product of randomly mixing,
    matching, and mutating the two expressions.

    NOTE I think we will need to add more parameters to finely tune the
    mutation.
    """
    pass

def convert_infix(expr):
    """
    Converts an s expression into infix notation (string).
    """
    if type(expr) == str or type(expr) == int:
        # Int and string (var t) literals first
        return '('+str(expr)+')'

    elif type(expr) == list:
        # Lists should always be expressions.
        # We will handle array literals without recursing.

        op, left, right = expr

        right = convert_infix(right)

        if op == 'i':
            left = '{'+str(left)[1:-1]+'}'
            return '(int[]){arr}[({index})%{length}]'.format(
                    arr=left, index=right, length=len(left))
        else:
            left = convert_infix(left)
            if op == '/' or op == '%':
                # Stop divide by zeroes
                right = zero_checker(right)
            return '({}{}{})'.format(left, op, right)

def zero_checker(expr):
    return '(({expr})==0?1:{expr})'.format(expr=expr)

"""
Notes on the genetic parts:

    Putting together the breeding and generating will be a little tricky, but
    nothing complicated algorithmically.

    Choosing which sexps to breed is tricky. Apparently we typically use
    selection algorithms (instead of just ranking everything and choosing the
    best). The Wikipedia page on selection algorithms has some good sources. It
    seems that what we want to do is generate a distribution for which sexps to
    choose, and then choose some of them (WITHOUT REPLACEMENT). The choice of
    distribution is interesting. Writing the random choice will be the tricky
    part. Python 3.6 introduced random.choices() which allows weighted choices,
    but this is with replacement. We may have to rewrite that algorithm for our
    own purposes.
"""
