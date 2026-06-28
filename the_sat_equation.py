"""
MIT License

Copyright (c) 2025 Oscar Riveros

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def bits(n, p):
    s = []
    while n:
        s = [n % 2 == 0] + s
        n //= 2
    s = (p - len(s)) * [True] + s
    return s


def sat_equation(cnf, n):
    sat = 0
    for j in range(len(cnf)):
        v = 0
        for i in range(n):
            v += int(cnf[j][n - 1 - i] > 0) * 2 ** i
        sat += 2 ** v
    return sat

"""
# Optimized (OR instead of addition, same semantics for balanced CNFs)
def sat_equation(cnf, n):
    sat = 0
    for j in range(len(cnf)):
        v = 0
        for i in range(n):
            v |= (cnf[j][n - 1 - i] > 0) << i
        sat |= 1 << v
    return sat
"""


# Generalized SAT Equation Theorem
#
# For an arbitrary CNF formula F = C_1 ∧ ... ∧ C_m over n Boolean variables
# (clauses may omit variables), the SAT equation number S is:
#
#   S = ⋁_{j=1}^{m}  ⋁_{M' ⊆ M_{C_j}}  2^{ B(C_j) + Σ_{i∈M'} 2^{n-i} }
#
# where:
#   P_C  = { i | variable i appears in clause C }
#   M_C  = {1..n} \ P_C                         (missing/absent variables)
#   r_i(C) = 1 if literal +i, 0 if literal -i   (required bit)
#   B(C) = Σ_{i∈P_C} r_i(C) ⋅ 2^{n-i}          (base contribution)
#
# The binary expansion of S (with 2^n bits) has bit k = 1 iff assignment
# whose binary representation equals k does NOT satisfy the formula.
# Clauses missing t variables generate a t-dimensional subcube of 2^t
# falsifying assignments. Bitwise OR eliminates carries, making the
# construction valid for CNF formulas with clauses of any size.

def sat_equation_generalized(cnf, n):
    sat = 0
    for clause in cnf:
        # Map variable index -> literal value
        lit_map = {abs(lit): lit for lit in clause}

        # B(C): base value encoding required bits of present variables
        B = 0
        for var in range(1, n + 1):
            if var in lit_map:
                lit = lit_map[var]
                if lit > 0:  # positive literal -> variable must be 1(False) to falsify
                    B |= 1 << (n - var)

        # Enumerate missing variables and iterate over the subcube
        missing = sorted(var for var in range(1, n + 1) if var not in lit_map)
        t = len(missing)
        for mask in range(1 << t):
            v = B
            for j in range(t):
                if mask & (1 << j):
                    v |= 1 << (n - missing[j])
            sat |= 1 << v

    return sat


if __name__ == '__main__':
    cnf = [(1, -2, 3), (1, -2, -3), (-1, 2, -3)]

    n = 3

    print(bits(sat_equation(cnf, n), 2 ** n))

    print("""
    (a|~b|c)&(a|~b|~c)&(~a|b|~c)
    a      b      c      value
    False  False  False  True
    False  False  True   True
    False  True   False  False
    False  True   True   False
    True   False  False  True
    True   False  True   False
    True   True   False  True
    True   True   True   True
    """)

    cnf = [(1, 2, 3, -4), (1, 2, -3, -4), (1, -2, 3, -4), (1, -2, -3, -4), (-1, 2, 3, -4), (-1, 2, -3, 4),
           (-1, -2, 3, 4), (-1, -2, -3, 4)]

    n = 4
    m = len(cnf)

    print(bits(sat_equation(cnf, n), 2 ** n))

    print("""
    (a|b|c|~d)&(a|b|~c|~d)&(a|~b|c|~d)&(a|~b|~c|~d)&(~a|b|c|~d)&(~a|b|~c|d)&(~a|~b|c|d)&(~a|~b|~c|d)
    a      b      c      d      value
    False  False  False  False  True
    False  False  False  True   False
    False  False  True   False  True
    False  False  True   True   False
    False  True   False  False  True
    False  True   False  True   False
    False  True   True   False  True
    False  True   True   True   False
    True   False  False  False  True
    True   False  False  True   False
    True   False  True   False  False
    True   False  True   True   True
    True   True   False  False  False
    True   True   False  True   True
    True   True   True   False  False
    True   True   True   True   True
    """)

    cnf = [(1, 2, 3, 4, 5), (1, 2, 3, -4, 5), (1, 2, 3, -4, -5), (1, 2, -3, 4, 5), (1, 2, -3, -4, 5),
           (1, 2, -3, -4, -5), (1, -2, 3, 4, 5), (1, -2, 3, -4, 5), (1, -2, 3, -4, -5), (1, -2, -3, 4, 5),
           (1, -2, -3, -4, 5), (1, -2, -3, -4, -5), (-1, 2, 3, 4, 5), (-1, 2, 3, -4, 5), (-1, 2, 3, -4, -5),
           (-1, 2, -3, 4, -5), (-1, -2, 3, 4, -5), (-1, -2, -3, 4, -5)]

    n = 5
    m = len(cnf)

    print(bits(sat_equation(cnf, n), 2 ** n))

    print("""
    (a|b|c|d|e)&(a|b|c|~d|e)&(a|b|c|~d|~e)&(a|b|~c|d|e)&(a|b|~c|~d|e)&(a|b|~c|~d|~e)&(a|~b|c|d|e)&(a|~b|c|~d|e)&(a|~b|c|~d|~e)&(a|~b|~c|d|e)&(a|~b|~c|~d|e)&(a|~b|~c|~d|~e)&(~a|b|c|d|e)&(~a|b|c|~d|e)&(~a|b|c|~d|~e)&(~a|b|~c|d|~e)&(~a|~b|c|d|~e)&(~a|~b|~c|d|~e)
    a      b      c      d      e      value
    False  False  False  False  False  False
    False  False  False  False  True   True
    False  False  False  True   False  False
    False  False  False  True   True   False
    False  False  True   False  False  False
    False  False  True   False  True   True
    False  False  True   True   False  False
    False  False  True   True   True   False
    False  True   False  False  False  False
    False  True   False  False  True   True
    False  True   False  True   False  False
    False  True   False  True   True   False
    False  True   True   False  False  False
    False  True   True   False  True   True
    False  True   True   True   False  False
    False  True   True   True   True   False
    True   False  False  False  False  False
    True   False  False  False  True   True
    True   False  False  True   False  False
    True   False  False  True   True   False
    True   False  True   False  False  True
    True   False  True   False  True   False
    True   False  True   True   False  True
    True   False  True   True   True   True
    True   True   False  False  False  True
    True   True   False  False  True   False
    True   True   False  True   False  True
    True   True   False  True   True   True
    True   True   True   False  False  True
    True   True   True   False  True   False
    True   True   True   True   False  True
    True   True   True   True   True   True
    """)

    cnf = [(1, 2, 3, 4), (1, 2, 3, -4), (1, 2, -3, 4), (1, 2, -3, -4), (1, -2, 3, 4), (1, -2, 3, -4), (1, -2, -3, 4),
           (1, -2, -3, -4), (-1, 2, 3, 4), (-1, 2, 3, -4), (-1, 2, -3, 4), (-1, 2, -3, -4), (-1, -2, 3, 4),
           (-1, -2, 3, -4), (-1, -2, -3, 4), (-1, -2, -3, -4)]

    n = 4
    m = len(cnf)

    print(bits(sat_equation(cnf, n), 2 ** n))

    print("""
    (a|b|c|d)&(a|b|c|~d)&(a|b|~c|d)&(a|b|~c|~d)&(a|~b|c|d)&(a|~b|c|~d)&(a|~b|~c|d)&(a|~b|~c|~d)&(~a|b|c|d)&(~a|b|c|~d)&(~a|b|~c|d)&(~a|b|~c|~d)&(~a|~b|c|d)&(~a|~b|c|~d)&(~a|~b|~c|d)&(~a|~b|~c|~d)
    a      b      c      d      value
    False  False  False  False  False
    False  False  False  True   False
    False  False  True   False  False
    False  False  True   True   False
    False  True   False  False  False
    False  True   False  True   False
    False  True   True   False  False
    False  True   True   True   False
    True   False  False  False  False
    True   False  False  True   False
    True   False  True   False  False
    True   False  True   True   False
    True   True   False  False  False
    True   True   False  True   False
    True   True   True   False  False
    True   True   True   True   False
    """)

    cnf = [(1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, -6), (1, 2, 3, 4, -5, -6), (1, 2, 3, -4, 5, 6), (1, 2, 3, -4, 5, -6),
           (1, 2, 3, -4, -5, 6), (1, 2, 3, -4, -5, -6), (1, 2, -3, 4, 5, 6), (1, 2, -3, 4, 5, -6), (1, 2, -3, 4, -5, 6),
           (1, 2, -3, 4, -5, -6), (1, 2, -3, -4, 5, 6), (1, 2, -3, -4, 5, -6), (1, 2, -3, -4, -5, 6),
           (1, 2, -3, -4, -5, -6), (1, -2, 3, 4, 5, 6), (1, -2, 3, 4, 5, -6), (1, -2, 3, 4, -5, 6),
           (1, -2, 3, 4, -5, -6), (1, -2, 3, -4, 5, 6), (1, -2, 3, -4, 5, -6), (1, -2, 3, -4, -5, 6),
           (1, -2, 3, -4, -5, -6), (1, -2, -3, 4, 5, 6), (1, -2, -3, 4, 5, -6), (1, -2, -3, 4, -5, 6),
           (1, -2, -3, 4, -5, -6), (1, -2, -3, -4, 5, 6), (1, -2, -3, -4, 5, -6), (1, -2, -3, -4, -5, 6),
           (1, -2, -3, -4, -5, -6), (-1, 2, 3, 4, 5, 6), (-1, 2, 3, 4, 5, -6), (-1, 2, 3, 4, -5, 6),
           (-1, 2, 3, 4, -5, -6), (-1, 2, 3, -4, 5, 6), (-1, 2, 3, -4, 5, -6), (-1, 2, 3, -4, -5, 6),
           (-1, 2, 3, -4, -5, -6), (-1, 2, -3, 4, 5, 6), (-1, 2, -3, 4, 5, -6), (-1, 2, -3, 4, -5, 6),
           (-1, 2, -3, 4, -5, -6), (-1, 2, -3, -4, 5, 6), (-1, 2, -3, -4, 5, -6), (-1, 2, -3, -4, -5, 6),
           (-1, 2, -3, -4, -5, -6), (-1, -2, 3, 4, 5, 6), (-1, -2, 3, 4, 5, -6), (-1, -2, 3, 4, -5, 6),
           (-1, -2, 3, 4, -5, -6), (-1, -2, 3, -4, 5, 6), (-1, -2, 3, -4, 5, -6), (-1, -2, 3, -4, -5, 6),
           (-1, -2, 3, -4, -5, -6), (-1, -2, -3, 4, 5, 6), (-1, -2, -3, 4, 5, -6), (-1, -2, -3, 4, -5, 6),
           (-1, -2, -3, 4, -5, -6), (-1, -2, -3, -4, 5, 6), (-1, -2, -3, -4, 5, -6), (-1, -2, -3, -4, -5, 6),
           (-1, -2, -3, -4, -5, -6)]

    n = 6
    m = len(cnf)

    print(bits(sat_equation(cnf, n), 2 ** n))

    print("""
    (a|b|c|d|e|f)&(a|b|c|d|e|~f)&(a|b|c|d|~e|~f)&(a|b|c|~d|e|f)&(a|b|c|~d|e|~f)&(a|b|c|~d|~e|f)&(a|b|c|~d|~e|~f)&(a|b|~c|d|e|f)&(a|b|~c|d|e|~f)&(a|b|~c|d|~e|f)&(a|b|~c|d|~e|~f)&(a|b|~c|~d|e|f)&(a|b|~c|~d|e|~f)&(a|b|~c|~d|~e|f)&(a|b|~c|~d|~e|~f)&(a|~b|c|d|e|f)&(a|~b|c|d|e|~f)&(a|~b|c|d|~e|f)&(a|~b|c|d|~e|~f)&(a|~b|c|~d|e|f)&(a|~b|c|~d|e|~f)&(a|~b|c|~d|~e|f)&(a|~b|c|~d|~e|~f)&(a|~b|~c|d|e|f)&(a|~b|~c|d|e|~f)&(a|~b|~c|d|~e|f)&(a|~b|~c|d|~e|~f)&(a|~b|~c|~d|e|f)&(a|~b|~c|~d|e|~f)&(a|~b|~c|~d|~e|f)&(a|~b|~c|~d|~e|~f)&(~a|b|c|d|e|f)&(~a|b|c|d|e|~f)&(~a|b|c|d|~e|f)&(~a|b|c|d|~e|~f)&(~a|b|c|~d|e|f)&(~a|b|c|~d|e|~f)&(~a|b|c|~d|~e|f)&(~a|b|c|~d|~e|~f)&(~a|b|~c|d|e|f)&(~a|b|~c|d|e|~f)&(~a|b|~c|d|~e|f)&(~a|b|~c|d|~e|~f)&(~a|b|~c|~d|e|f)&(~a|b|~c|~d|e|~f)&(~a|b|~c|~d|~e|f)&(~a|b|~c|~d|~e|~f)&(~a|~b|c|d|e|f)&(~a|~b|c|d|e|~f)&(~a|~b|c|d|~e|f)&(~a|~b|c|d|~e|~f)&(~a|~b|c|~d|e|f)&(~a|~b|c|~d|e|~f)&(~a|~b|c|~d|~e|f)&(~a|~b|c|~d|~e|~f)&(~a|~b|~c|d|e|f)&(~a|~b|~c|d|e|~f)&(~a|~b|~c|d|~e|f)&(~a|~b|~c|d|~e|~f)&(~a|~b|~c|~d|e|f)&(~a|~b|~c|~d|e|~f)&(~a|~b|~c|~d|~e|f)&(~a|~b|~c|~d|~e|~f)
    a      b      c      d      e      f      value
    False  False  False  False  False  False  False
    False  False  False  False  False  True   False
    False  False  False  False  True   False  True
    False  False  False  False  True   True   False
    False  False  False  True   False  False  False
    False  False  False  True   False  True   False
    False  False  False  True   True   False  False
    False  False  False  True   True   True   False
    False  False  True   False  False  False  False
    False  False  True   False  False  True   False
    False  False  True   False  True   False  False
    False  False  True   False  True   True   False
    False  False  True   True   False  False  False
    False  False  True   True   False  True   False
    False  False  True   True   True   False  False
    False  False  True   True   True   True   False
    False  True   False  False  False  False  False
    False  True   False  False  False  True   False
    False  True   False  False  True   False  False
    False  True   False  False  True   True   False
    False  True   False  True   False  False  False
    False  True   False  True   False  True   False
    False  True   False  True   True   False  False
    False  True   False  True   True   True   False
    False  True   True   False  False  False  False
    False  True   True   False  False  True   False
    False  True   True   False  True   False  False
    False  True   True   False  True   True   False
    False  True   True   True   False  False  False
    False  True   True   True   False  True   False
    False  True   True   True   True   False  False
    False  True   True   True   True   True   False
    True   False  False  False  False  False  False
    True   False  False  False  False  True   False
    True   False  False  False  True   False  False
    True   False  False  False  True   True   False
    True   False  False  True   False  False  False
    True   False  False  True   False  True   False
    True   False  False  True   True   False  False
    True   False  False  True   True   True   False
    True   False  True   False  False  False  False
    True   False  True   False  False  True   False
    True   False  True   False  True   False  False
    True   False  True   False  True   True   False
    True   False  True   True   False  False  False
    True   False  True   True   False  True   False
    True   False  True   True   True   False  False
    True   False  True   True   True   True   False
    True   True   False  False  False  False  False
    True   True   False  False  False  True   False
    True   True   False  False  True   False  False
    True   True   False  False  True   True   False
    True   True   False  True   False  False  False
    True   True   False  True   False  True   False
    True   True   False  True   True   False  False
    True   True   False  True   True   True   False
    True   True   True   False  False  False  False
    True   True   True   False  False  True   False
    True   True   True   False  True   False  False
    True   True   True   False  True   True   False
    True   True   True   True   False  False  False
    True   True   True   True   False  True   False
    True   True   True   True   True   False  False
    True   True   True   True   True   True   False
    """)

    cnf = [(1, 2, 3, 4, 5, 6, 7, 8, 9), (1, 2, 3, 4, 5, 6, 7, 8, -9), (1, 2, 3, 4, 5, 6, 7, -8, 9),
           (1, 2, 3, 4, 5, 6, 7, -8, -9), (1, 2, 3, 4, 5, 6, -7, 8, 9), (1, 2, 3, 4, 5, 6, -7, 8, -9),
           (1, 2, 3, 4, 5, 6, -7, -8, 9), (1, 2, 3, 4, 5, 6, -7, -8, -9), (1, 2, 3, 4, 5, -6, 7, 8, 9),
           (1, 2, 3, 4, 5, -6, 7, 8, -9), (1, 2, 3, 4, 5, -6, 7, -8, 9), (1, 2, 3, 4, 5, -6, 7, -8, -9),
           (1, 2, 3, 4, 5, -6, -7, 8, 9), (1, 2, 3, 4, 5, -6, -7, 8, -9), (1, 2, 3, 4, 5, -6, -7, -8, 9),
           (1, 2, 3, 4, 5, -6, -7, -8, -9), (1, 2, 3, 4, -5, 6, 7, 8, 9), (1, 2, 3, 4, -5, 6, 7, 8, -9),
           (1, 2, 3, 4, -5, 6, 7, -8, 9), (1, 2, 3, 4, -5, 6, 7, -8, -9), (1, 2, 3, 4, -5, 6, -7, 8, 9),
           (1, 2, 3, 4, -5, 6, -7, 8, -9), (1, 2, 3, 4, -5, 6, -7, -8, 9), (1, 2, 3, 4, -5, 6, -7, -8, -9),
           (1, 2, 3, 4, -5, -6, 7, 8, 9), (1, 2, 3, 4, -5, -6, 7, 8, -9), (1, 2, 3, 4, -5, -6, 7, -8, 9),
           (1, 2, 3, 4, -5, -6, 7, -8, -9), (1, 2, 3, 4, -5, -6, -7, 8, 9), (1, 2, 3, 4, -5, -6, -7, 8, -9),
           (1, 2, 3, 4, -5, -6, -7, -8, 9), (1, 2, 3, 4, -5, -6, -7, -8, -9), (1, 2, 3, -4, 5, 6, 7, 8, 9),
           (1, 2, 3, -4, 5, 6, 7, 8, -9), (1, 2, 3, -4, 5, 6, 7, -8, 9), (1, 2, 3, -4, 5, 6, 7, -8, -9),
           (1, 2, 3, -4, 5, 6, -7, 8, 9), (1, 2, 3, -4, 5, 6, -7, 8, -9), (1, 2, 3, -4, 5, 6, -7, -8, 9),
           (1, 2, 3, -4, 5, 6, -7, -8, -9), (1, 2, 3, -4, 5, -6, 7, 8, 9), (1, 2, 3, -4, 5, -6, 7, 8, -9),
           (1, 2, 3, -4, 5, -6, 7, -8, 9), (1, 2, 3, -4, 5, -6, 7, -8, -9), (1, 2, 3, -4, 5, -6, -7, 8, 9),
           (1, 2, 3, -4, 5, -6, -7, 8, -9), (1, 2, 3, -4, 5, -6, -7, -8, 9), (1, 2, 3, -4, 5, -6, -7, -8, -9),
           (1, 2, 3, -4, -5, 6, 7, 8, 9), (1, 2, 3, -4, -5, 6, 7, 8, -9), (1, 2, 3, -4, -5, 6, 7, -8, 9),
           (1, 2, 3, -4, -5, 6, 7, -8, -9), (1, 2, 3, -4, -5, 6, -7, 8, 9), (1, 2, 3, -4, -5, 6, -7, 8, -9),
           (1, 2, 3, -4, -5, 6, -7, -8, 9), (1, 2, 3, -4, -5, 6, -7, -8, -9), (1, 2, 3, -4, -5, -6, 7, 8, 9),
           (1, 2, 3, -4, -5, -6, 7, 8, -9), (1, 2, 3, -4, -5, -6, 7, -8, 9), (1, 2, 3, -4, -5, -6, 7, -8, -9),
           (1, 2, 3, -4, -5, -6, -7, 8, 9), (1, 2, 3, -4, -5, -6, -7, 8, -9), (1, 2, 3, -4, -5, -6, -7, -8, 9),
           (1, 2, 3, -4, -5, -6, -7, -8, -9), (1, 2, -3, 4, 5, 6, 7, 8, 9), (1, 2, -3, 4, 5, 6, 7, 8, -9),
           (1, 2, -3, 4, 5, 6, 7, -8, 9), (1, 2, -3, 4, 5, 6, 7, -8, -9), (1, 2, -3, 4, 5, 6, -7, 8, 9),
           (1, 2, -3, 4, 5, 6, -7, 8, -9), (1, 2, -3, 4, 5, 6, -7, -8, 9), (1, 2, -3, 4, 5, 6, -7, -8, -9),
           (1, 2, -3, 4, 5, -6, 7, 8, 9), (1, 2, -3, 4, 5, -6, 7, 8, -9), (1, 2, -3, 4, 5, -6, 7, -8, 9),
           (1, 2, -3, 4, 5, -6, 7, -8, -9), (1, 2, -3, 4, 5, -6, -7, 8, 9), (1, 2, -3, 4, 5, -6, -7, 8, -9),
           (1, 2, -3, 4, 5, -6, -7, -8, 9), (1, 2, -3, 4, 5, -6, -7, -8, -9), (1, 2, -3, 4, -5, 6, 7, 8, 9),
           (1, 2, -3, 4, -5, 6, 7, 8, -9), (1, 2, -3, 4, -5, 6, 7, -8, 9), (1, 2, -3, 4, -5, 6, 7, -8, -9),
           (1, 2, -3, 4, -5, 6, -7, 8, 9), (1, 2, -3, 4, -5, 6, -7, 8, -9), (1, 2, -3, 4, -5, 6, -7, -8, 9),
           (1, 2, -3, 4, -5, 6, -7, -8, -9), (1, 2, -3, 4, -5, -6, 7, 8, 9), (1, 2, -3, 4, -5, -6, 7, 8, -9),
           (1, 2, -3, 4, -5, -6, 7, -8, 9), (1, 2, -3, 4, -5, -6, 7, -8, -9), (1, 2, -3, 4, -5, -6, -7, 8, 9),
           (1, 2, -3, 4, -5, -6, -7, 8, -9), (1, 2, -3, 4, -5, -6, -7, -8, 9), (1, 2, -3, 4, -5, -6, -7, -8, -9),
           (1, 2, -3, -4, 5, 6, 7, 8, 9), (1, 2, -3, -4, 5, 6, 7, 8, -9), (1, 2, -3, -4, 5, 6, 7, -8, 9),
           (1, 2, -3, -4, 5, 6, 7, -8, -9), (1, 2, -3, -4, 5, 6, -7, 8, 9), (1, 2, -3, -4, 5, 6, -7, 8, -9),
           (1, 2, -3, -4, 5, 6, -7, -8, 9), (1, 2, -3, -4, 5, 6, -7, -8, -9), (1, 2, -3, -4, 5, -6, 7, 8, 9),
           (1, 2, -3, -4, 5, -6, 7, 8, -9), (1, 2, -3, -4, 5, -6, 7, -8, 9), (1, 2, -3, -4, 5, -6, 7, -8, -9),
           (1, 2, -3, -4, 5, -6, -7, 8, 9), (1, 2, -3, -4, 5, -6, -7, 8, -9), (1, 2, -3, -4, 5, -6, -7, -8, 9),
           (1, 2, -3, -4, 5, -6, -7, -8, -9), (1, 2, -3, -4, -5, 6, 7, 8, 9), (1, 2, -3, -4, -5, 6, 7, 8, -9),
           (1, 2, -3, -4, -5, 6, 7, -8, 9), (1, 2, -3, -4, -5, 6, 7, -8, -9), (1, 2, -3, -4, -5, 6, -7, 8, 9),
           (1, 2, -3, -4, -5, 6, -7, 8, -9), (1, 2, -3, -4, -5, 6, -7, -8, 9), (1, 2, -3, -4, -5, 6, -7, -8, -9),
           (1, 2, -3, -4, -5, -6, 7, 8, 9), (1, 2, -3, -4, -5, -6, 7, 8, -9), (1, 2, -3, -4, -5, -6, 7, -8, 9),
           (1, 2, -3, -4, -5, -6, 7, -8, -9), (1, 2, -3, -4, -5, -6, -7, 8, 9), (1, 2, -3, -4, -5, -6, -7, 8, -9),
           (1, 2, -3, -4, -5, -6, -7, -8, 9), (1, 2, -3, -4, -5, -6, -7, -8, -9), (1, -2, 3, 4, 5, 6, 7, 8, 9),
           (1, -2, 3, 4, 5, 6, 7, 8, -9), (1, -2, 3, 4, 5, 6, 7, -8, 9), (1, -2, 3, 4, 5, 6, 7, -8, -9),
           (1, -2, 3, 4, 5, 6, -7, 8, 9), (1, -2, 3, 4, 5, 6, -7, 8, -9), (1, -2, 3, 4, 5, 6, -7, -8, 9),
           (1, -2, 3, 4, 5, 6, -7, -8, -9), (1, -2, 3, 4, 5, -6, 7, 8, 9), (1, -2, 3, 4, 5, -6, 7, 8, -9),
           (1, -2, 3, 4, 5, -6, 7, -8, 9), (1, -2, 3, 4, 5, -6, 7, -8, -9), (1, -2, 3, 4, 5, -6, -7, 8, 9),
           (1, -2, 3, 4, 5, -6, -7, 8, -9), (1, -2, 3, 4, 5, -6, -7, -8, 9), (1, -2, 3, 4, 5, -6, -7, -8, -9),
           (1, -2, 3, 4, -5, 6, 7, 8, 9), (1, -2, 3, 4, -5, 6, 7, 8, -9), (1, -2, 3, 4, -5, 6, 7, -8, 9),
           (1, -2, 3, 4, -5, 6, 7, -8, -9), (1, -2, 3, 4, -5, 6, -7, 8, 9), (1, -2, 3, 4, -5, 6, -7, 8, -9),
           (1, -2, 3, 4, -5, 6, -7, -8, 9), (1, -2, 3, 4, -5, 6, -7, -8, -9), (1, -2, 3, 4, -5, -6, 7, 8, 9),
           (1, -2, 3, 4, -5, -6, 7, 8, -9), (1, -2, 3, 4, -5, -6, 7, -8, 9), (1, -2, 3, 4, -5, -6, 7, -8, -9),
           (1, -2, 3, 4, -5, -6, -7, 8, 9), (1, -2, 3, 4, -5, -6, -7, 8, -9), (1, -2, 3, 4, -5, -6, -7, -8, 9),
           (1, -2, 3, 4, -5, -6, -7, -8, -9), (1, -2, 3, -4, 5, 6, 7, 8, 9), (1, -2, 3, -4, 5, 6, 7, 8, -9),
           (1, -2, 3, -4, 5, 6, 7, -8, 9), (1, -2, 3, -4, 5, 6, 7, -8, -9), (1, -2, 3, -4, 5, 6, -7, 8, 9),
           (1, -2, 3, -4, 5, 6, -7, 8, -9), (1, -2, 3, -4, 5, 6, -7, -8, 9), (1, -2, 3, -4, 5, 6, -7, -8, -9),
           (1, -2, 3, -4, 5, -6, 7, 8, 9), (1, -2, 3, -4, 5, -6, 7, 8, -9), (1, -2, 3, -4, 5, -6, 7, -8, 9),
           (1, -2, 3, -4, 5, -6, 7, -8, -9), (1, -2, 3, -4, 5, -6, -7, 8, 9), (1, -2, 3, -4, 5, -6, -7, 8, -9),
           (1, -2, 3, -4, 5, -6, -7, -8, 9), (1, -2, 3, -4, 5, -6, -7, -8, -9), (1, -2, 3, -4, -5, 6, 7, 8, 9),
           (1, -2, 3, -4, -5, 6, 7, 8, -9), (1, -2, 3, -4, -5, 6, 7, -8, 9), (1, -2, 3, -4, -5, 6, 7, -8, -9),
           (1, -2, 3, -4, -5, 6, -7, 8, 9), (1, -2, 3, -4, -5, 6, -7, 8, -9), (1, -2, 3, -4, -5, 6, -7, -8, 9),
           (1, -2, 3, -4, -5, 6, -7, -8, -9), (1, -2, 3, -4, -5, -6, 7, 8, 9), (1, -2, 3, -4, -5, -6, 7, 8, -9),
           (1, -2, 3, -4, -5, -6, 7, -8, 9), (1, -2, 3, -4, -5, -6, 7, -8, -9), (1, -2, 3, -4, -5, -6, -7, 8, 9),
           (1, -2, 3, -4, -5, -6, -7, 8, -9), (1, -2, 3, -4, -5, -6, -7, -8, 9), (1, -2, 3, -4, -5, -6, -7, -8, -9),
           (1, -2, -3, 4, 5, 6, 7, 8, 9), (1, -2, -3, 4, 5, 6, 7, 8, -9), (1, -2, -3, 4, 5, 6, 7, -8, 9),
           (1, -2, -3, 4, 5, 6, 7, -8, -9), (1, -2, -3, 4, 5, 6, -7, 8, 9), (1, -2, -3, 4, 5, 6, -7, 8, -9),
           (1, -2, -3, 4, 5, 6, -7, -8, 9), (1, -2, -3, 4, 5, 6, -7, -8, -9), (1, -2, -3, 4, 5, -6, 7, 8, 9),
           (1, -2, -3, 4, 5, -6, 7, 8, -9), (1, -2, -3, 4, 5, -6, 7, -8, 9), (1, -2, -3, 4, 5, -6, 7, -8, -9),
           (1, -2, -3, 4, 5, -6, -7, 8, 9), (1, -2, -3, 4, 5, -6, -7, 8, -9), (1, -2, -3, 4, 5, -6, -7, -8, 9),
           (1, -2, -3, 4, 5, -6, -7, -8, -9), (1, -2, -3, 4, -5, 6, 7, 8, 9), (1, -2, -3, 4, -5, 6, 7, 8, -9),
           (1, -2, -3, 4, -5, 6, 7, -8, 9), (1, -2, -3, 4, -5, 6, 7, -8, -9), (1, -2, -3, 4, -5, 6, -7, 8, 9),
           (1, -2, -3, 4, -5, 6, -7, 8, -9), (1, -2, -3, 4, -5, 6, -7, -8, 9), (1, -2, -3, 4, -5, 6, -7, -8, -9),
           (1, -2, -3, 4, -5, -6, 7, 8, 9), (1, -2, -3, 4, -5, -6, 7, 8, -9), (1, -2, -3, 4, -5, -6, 7, -8, 9),
           (1, -2, -3, 4, -5, -6, 7, -8, -9), (1, -2, -3, 4, -5, -6, -7, 8, 9), (1, -2, -3, 4, -5, -6, -7, 8, -9),
           (1, -2, -3, 4, -5, -6, -7, -8, 9), (1, -2, -3, 4, -5, -6, -7, -8, -9), (1, -2, -3, -4, 5, 6, 7, 8, 9),
           (1, -2, -3, -4, 5, 6, 7, 8, -9), (1, -2, -3, -4, 5, 6, 7, -8, 9), (1, -2, -3, -4, 5, 6, 7, -8, -9),
           (1, -2, -3, -4, 5, 6, -7, 8, 9), (1, -2, -3, -4, 5, 6, -7, 8, -9), (1, -2, -3, -4, 5, 6, -7, -8, 9),
           (1, -2, -3, -4, 5, 6, -7, -8, -9), (1, -2, -3, -4, 5, -6, 7, 8, 9), (1, -2, -3, -4, 5, -6, 7, 8, -9),
           (1, -2, -3, -4, 5, -6, 7, -8, 9), (1, -2, -3, -4, 5, -6, 7, -8, -9), (1, -2, -3, -4, 5, -6, -7, 8, 9),
           (1, -2, -3, -4, 5, -6, -7, 8, -9), (1, -2, -3, -4, 5, -6, -7, -8, 9), (1, -2, -3, -4, 5, -6, -7, -8, -9),
           (1, -2, -3, -4, -5, 6, 7, 8, 9), (1, -2, -3, -4, -5, 6, 7, 8, -9), (1, -2, -3, -4, -5, 6, 7, -8, 9),
           (1, -2, -3, -4, -5, 6, 7, -8, -9), (1, -2, -3, -4, -5, 6, -7, 8, 9), (1, -2, -3, -4, -5, 6, -7, 8, -9),
           (1, -2, -3, -4, -5, 6, -7, -8, 9), (1, -2, -3, -4, -5, 6, -7, -8, -9), (1, -2, -3, -4, -5, -6, 7, 8, 9),
           (1, -2, -3, -4, -5, -6, 7, 8, -9), (1, -2, -3, -4, -5, -6, 7, -8, 9), (1, -2, -3, -4, -5, -6, 7, -8, -9),
           (1, -2, -3, -4, -5, -6, -7, 8, 9), (1, -2, -3, -4, -5, -6, -7, 8, -9), (1, -2, -3, -4, -5, -6, -7, -8, 9),
           (1, -2, -3, -4, -5, -6, -7, -8, -9), (-1, 2, 3, 4, 5, 6, 7, 8, 9), (-1, 2, 3, 4, 5, 6, 7, 8, -9),
           (-1, 2, 3, 4, 5, 6, 7, -8, 9), (-1, 2, 3, 4, 5, 6, 7, -8, -9), (-1, 2, 3, 4, 5, 6, -7, 8, 9),
           (-1, 2, 3, 4, 5, 6, -7, 8, -9), (-1, 2, 3, 4, 5, 6, -7, -8, 9), (-1, 2, 3, 4, 5, 6, -7, -8, -9),
           (-1, 2, 3, 4, 5, -6, 7, 8, -9), (-1, 2, 3, 4, 5, -6, 7, -8, 9), (-1, 2, 3, 4, 5, -6, 7, -8, -9),
           (-1, 2, 3, 4, 5, -6, -7, 8, -9), (-1, 2, 3, 4, 5, -6, -7, -8, 9), (-1, 2, 3, 4, 5, -6, -7, -8, -9),
           (-1, 2, 3, 4, -5, 6, 7, 8, 9), (-1, 2, 3, 4, -5, 6, 7, 8, -9), (-1, 2, 3, 4, -5, 6, 7, -8, 9),
           (-1, 2, 3, 4, -5, 6, 7, -8, -9), (-1, 2, 3, 4, -5, 6, -7, 8, 9), (-1, 2, 3, 4, -5, 6, -7, 8, -9),
           (-1, 2, 3, 4, -5, 6, -7, -8, 9), (-1, 2, 3, 4, -5, 6, -7, -8, -9), (-1, 2, 3, 4, -5, -6, 7, 8, -9),
           (-1, 2, 3, 4, -5, -6, 7, -8, 9), (-1, 2, 3, 4, -5, -6, 7, -8, -9), (-1, 2, 3, 4, -5, -6, -7, 8, -9),
           (-1, 2, 3, 4, -5, -6, -7, -8, 9), (-1, 2, 3, 4, -5, -6, -7, -8, -9), (-1, 2, 3, -4, 5, 6, 7, 8, 9),
           (-1, 2, 3, -4, 5, 6, 7, 8, -9), (-1, 2, 3, -4, 5, 6, 7, -8, 9), (-1, 2, 3, -4, 5, 6, 7, -8, -9),
           (-1, 2, 3, -4, 5, 6, -7, 8, 9), (-1, 2, 3, -4, 5, 6, -7, 8, -9), (-1, 2, 3, -4, 5, 6, -7, -8, 9),
           (-1, 2, 3, -4, 5, 6, -7, -8, -9), (-1, 2, 3, -4, 5, -6, 7, 8, -9), (-1, 2, 3, -4, 5, -6, 7, -8, 9),
           (-1, 2, 3, -4, 5, -6, 7, -8, -9), (-1, 2, 3, -4, 5, -6, -7, 8, -9), (-1, 2, 3, -4, 5, -6, -7, -8, 9),
           (-1, 2, 3, -4, 5, -6, -7, -8, -9), (-1, 2, 3, -4, -5, 6, 7, 8, 9), (-1, 2, 3, -4, -5, 6, 7, 8, -9),
           (-1, 2, 3, -4, -5, 6, 7, -8, 9), (-1, 2, 3, -4, -5, 6, 7, -8, -9), (-1, 2, 3, -4, -5, 6, -7, 8, 9),
           (-1, 2, 3, -4, -5, 6, -7, 8, -9), (-1, 2, 3, -4, -5, 6, -7, -8, 9), (-1, 2, 3, -4, -5, 6, -7, -8, -9),
           (-1, 2, 3, -4, -5, -6, 7, 8, -9), (-1, 2, 3, -4, -5, -6, 7, -8, 9), (-1, 2, 3, -4, -5, -6, 7, -8, -9),
           (-1, 2, 3, -4, -5, -6, -7, 8, -9), (-1, 2, 3, -4, -5, -6, -7, -8, 9), (-1, 2, 3, -4, -5, -6, -7, -8, -9),
           (-1, 2, -3, 4, 5, 6, 7, 8, 9), (-1, 2, -3, 4, 5, 6, 7, 8, -9), (-1, 2, -3, 4, 5, 6, 7, -8, 9),
           (-1, 2, -3, 4, 5, 6, 7, -8, -9), (-1, 2, -3, 4, 5, 6, -7, 8, 9), (-1, 2, -3, 4, 5, 6, -7, 8, -9),
           (-1, 2, -3, 4, 5, 6, -7, -8, 9), (-1, 2, -3, 4, 5, 6, -7, -8, -9), (-1, 2, -3, 4, 5, -6, 7, 8, -9),
           (-1, 2, -3, 4, 5, -6, 7, -8, 9), (-1, 2, -3, 4, 5, -6, 7, -8, -9), (-1, 2, -3, 4, 5, -6, -7, 8, -9),
           (-1, 2, -3, 4, 5, -6, -7, -8, 9), (-1, 2, -3, 4, 5, -6, -7, -8, -9), (-1, 2, -3, 4, -5, 6, 7, 8, 9),
           (-1, 2, -3, 4, -5, 6, 7, 8, -9), (-1, 2, -3, 4, -5, 6, 7, -8, 9), (-1, 2, -3, 4, -5, 6, 7, -8, -9),
           (-1, 2, -3, 4, -5, 6, -7, 8, 9), (-1, 2, -3, 4, -5, 6, -7, 8, -9), (-1, 2, -3, 4, -5, 6, -7, -8, 9),
           (-1, 2, -3, 4, -5, 6, -7, -8, -9), (-1, 2, -3, 4, -5, -6, 7, 8, -9), (-1, 2, -3, 4, -5, -6, 7, -8, 9),
           (-1, 2, -3, 4, -5, -6, 7, -8, -9), (-1, 2, -3, 4, -5, -6, -7, 8, -9), (-1, 2, -3, 4, -5, -6, -7, -8, 9),
           (-1, 2, -3, 4, -5, -6, -7, -8, -9), (-1, 2, -3, -4, 5, 6, 7, 8, 9), (-1, 2, -3, -4, 5, 6, 7, 8, -9),
           (-1, 2, -3, -4, 5, 6, 7, -8, 9), (-1, 2, -3, -4, 5, 6, 7, -8, -9), (-1, 2, -3, -4, 5, 6, -7, 8, 9),
           (-1, 2, -3, -4, 5, 6, -7, 8, -9), (-1, 2, -3, -4, 5, 6, -7, -8, 9), (-1, 2, -3, -4, 5, 6, -7, -8, -9),
           (-1, 2, -3, -4, 5, -6, 7, 8, -9), (-1, 2, -3, -4, 5, -6, 7, -8, 9), (-1, 2, -3, -4, 5, -6, 7, -8, -9),
           (-1, 2, -3, -4, 5, -6, -7, 8, -9), (-1, 2, -3, -4, 5, -6, -7, -8, 9), (-1, 2, -3, -4, 5, -6, -7, -8, -9),
           (-1, 2, -3, -4, -5, 6, 7, 8, 9), (-1, 2, -3, -4, -5, 6, 7, 8, -9), (-1, 2, -3, -4, -5, 6, 7, -8, 9),
           (-1, 2, -3, -4, -5, 6, 7, -8, -9), (-1, 2, -3, -4, -5, 6, -7, 8, 9), (-1, 2, -3, -4, -5, 6, -7, 8, -9),
           (-1, 2, -3, -4, -5, 6, -7, -8, 9), (-1, 2, -3, -4, -5, 6, -7, -8, -9), (-1, 2, -3, -4, -5, -6, 7, 8, -9),
           (-1, 2, -3, -4, -5, -6, 7, -8, 9), (-1, 2, -3, -4, -5, -6, 7, -8, -9), (-1, 2, -3, -4, -5, -6, -7, 8, -9),
           (-1, 2, -3, -4, -5, -6, -7, -8, 9), (-1, 2, -3, -4, -5, -6, -7, -8, -9), (-1, -2, 3, 4, 5, 6, 7, 8, 9),
           (-1, -2, 3, 4, 5, 6, 7, 8, -9), (-1, -2, 3, 4, 5, 6, 7, -8, 9), (-1, -2, 3, 4, 5, 6, 7, -8, -9),
           (-1, -2, 3, 4, 5, 6, -7, 8, 9), (-1, -2, 3, 4, 5, 6, -7, 8, -9), (-1, -2, 3, 4, 5, 6, -7, -8, 9),
           (-1, -2, 3, 4, 5, 6, -7, -8, -9), (-1, -2, 3, 4, 5, -6, 7, 8, -9), (-1, -2, 3, 4, 5, -6, 7, -8, 9),
           (-1, -2, 3, 4, 5, -6, 7, -8, -9), (-1, -2, 3, 4, 5, -6, -7, 8, -9), (-1, -2, 3, 4, 5, -6, -7, -8, 9),
           (-1, -2, 3, 4, 5, -6, -7, -8, -9), (-1, -2, 3, 4, -5, 6, 7, 8, 9), (-1, -2, 3, 4, -5, 6, 7, 8, -9),
           (-1, -2, 3, 4, -5, 6, 7, -8, 9), (-1, -2, 3, 4, -5, 6, 7, -8, -9), (-1, -2, 3, 4, -5, 6, -7, 8, 9),
           (-1, -2, 3, 4, -5, 6, -7, 8, -9), (-1, -2, 3, 4, -5, 6, -7, -8, 9), (-1, -2, 3, 4, -5, 6, -7, -8, -9),
           (-1, -2, 3, 4, -5, -6, 7, 8, -9), (-1, -2, 3, 4, -5, -6, 7, -8, 9), (-1, -2, 3, 4, -5, -6, 7, -8, -9),
           (-1, -2, 3, 4, -5, -6, -7, 8, -9), (-1, -2, 3, 4, -5, -6, -7, -8, 9), (-1, -2, 3, 4, -5, -6, -7, -8, -9),
           (-1, -2, 3, -4, 5, 6, 7, 8, 9), (-1, -2, 3, -4, 5, 6, 7, 8, -9), (-1, -2, 3, -4, 5, 6, 7, -8, 9),
           (-1, -2, 3, -4, 5, 6, 7, -8, -9), (-1, -2, 3, -4, 5, 6, -7, 8, 9), (-1, -2, 3, -4, 5, 6, -7, 8, -9),
           (-1, -2, 3, -4, 5, 6, -7, -8, 9), (-1, -2, 3, -4, 5, 6, -7, -8, -9), (-1, -2, 3, -4, 5, -6, 7, 8, -9),
           (-1, -2, 3, -4, 5, -6, 7, -8, 9), (-1, -2, 3, -4, 5, -6, 7, -8, -9), (-1, -2, 3, -4, 5, -6, -7, 8, -9),
           (-1, -2, 3, -4, 5, -6, -7, -8, 9), (-1, -2, 3, -4, 5, -6, -7, -8, -9), (-1, -2, 3, -4, -5, 6, 7, 8, 9),
           (-1, -2, 3, -4, -5, 6, 7, 8, -9), (-1, -2, 3, -4, -5, 6, 7, -8, 9), (-1, -2, 3, -4, -5, 6, 7, -8, -9),
           (-1, -2, 3, -4, -5, 6, -7, 8, 9), (-1, -2, 3, -4, -5, 6, -7, 8, -9), (-1, -2, 3, -4, -5, 6, -7, -8, 9),
           (-1, -2, 3, -4, -5, 6, -7, -8, -9), (-1, -2, 3, -4, -5, -6, 7, 8, -9), (-1, -2, 3, -4, -5, -6, 7, -8, 9),
           (-1, -2, 3, -4, -5, -6, 7, -8, -9), (-1, -2, 3, -4, -5, -6, -7, 8, -9), (-1, -2, 3, -4, -5, -6, -7, -8, 9),
           (-1, -2, 3, -4, -5, -6, -7, -8, -9), (-1, -2, -3, 4, 5, 6, 7, 8, 9), (-1, -2, -3, 4, 5, 6, 7, 8, -9),
           (-1, -2, -3, 4, 5, 6, 7, -8, 9), (-1, -2, -3, 4, 5, 6, 7, -8, -9), (-1, -2, -3, 4, 5, 6, -7, 8, 9),
           (-1, -2, -3, 4, 5, 6, -7, 8, -9), (-1, -2, -3, 4, 5, 6, -7, -8, 9), (-1, -2, -3, 4, 5, 6, -7, -8, -9),
           (-1, -2, -3, 4, 5, -6, 7, 8, -9), (-1, -2, -3, 4, 5, -6, 7, -8, 9), (-1, -2, -3, 4, 5, -6, 7, -8, -9),
           (-1, -2, -3, 4, 5, -6, -7, 8, -9), (-1, -2, -3, 4, 5, -6, -7, -8, 9), (-1, -2, -3, 4, 5, -6, -7, -8, -9),
           (-1, -2, -3, 4, -5, 6, 7, 8, 9), (-1, -2, -3, 4, -5, 6, 7, 8, -9), (-1, -2, -3, 4, -5, 6, 7, -8, 9),
           (-1, -2, -3, 4, -5, 6, 7, -8, -9), (-1, -2, -3, 4, -5, 6, -7, 8, 9), (-1, -2, -3, 4, -5, 6, -7, 8, -9),
           (-1, -2, -3, 4, -5, 6, -7, -8, 9), (-1, -2, -3, 4, -5, 6, -7, -8, -9), (-1, -2, -3, 4, -5, -6, 7, 8, -9),
           (-1, -2, -3, 4, -5, -6, 7, -8, 9), (-1, -2, -3, 4, -5, -6, 7, -8, -9), (-1, -2, -3, 4, -5, -6, -7, 8, -9),
           (-1, -2, -3, 4, -5, -6, -7, -8, 9), (-1, -2, -3, 4, -5, -6, -7, -8, -9), (-1, -2, -3, -4, 5, 6, 7, 8, 9),
           (-1, -2, -3, -4, 5, 6, 7, 8, -9), (-1, -2, -3, -4, 5, 6, 7, -8, 9), (-1, -2, -3, -4, 5, 6, 7, -8, -9),
           (-1, -2, -3, -4, 5, 6, -7, 8, 9), (-1, -2, -3, -4, 5, 6, -7, 8, -9), (-1, -2, -3, -4, 5, 6, -7, -8, 9),
           (-1, -2, -3, -4, 5, 6, -7, -8, -9), (-1, -2, -3, -4, 5, -6, 7, 8, -9), (-1, -2, -3, -4, 5, -6, 7, -8, 9),
           (-1, -2, -3, -4, 5, -6, 7, -8, -9), (-1, -2, -3, -4, 5, -6, -7, 8, -9), (-1, -2, -3, -4, 5, -6, -7, -8, 9),
           (-1, -2, -3, -4, 5, -6, -7, -8, -9), (-1, -2, -3, -4, -5, 6, 7, 8, 9), (-1, -2, -3, -4, -5, 6, 7, 8, -9),
           (-1, -2, -3, -4, -5, 6, 7, -8, 9), (-1, -2, -3, -4, -5, 6, 7, -8, -9), (-1, -2, -3, -4, -5, 6, -7, 8, 9),
           (-1, -2, -3, -4, -5, 6, -7, 8, -9), (-1, -2, -3, -4, -5, 6, -7, -8, 9), (-1, -2, -3, -4, -5, 6, -7, -8, -9),
           (-1, -2, -3, -4, -5, -6, 7, 8, -9), (-1, -2, -3, -4, -5, -6, 7, -8, 9), (-1, -2, -3, -4, -5, -6, 7, -8, -9),
           (-1, -2, -3, -4, -5, -6, -7, 8, -9), (-1, -2, -3, -4, -5, -6, -7, -8, 9),
           (-1, -2, -3, -4, -5, -6, -7, -8, -9)]

    n = 9
    m = len(cnf)

    print(bits(sat_equation(cnf, n), 2 ** n))

    print("""
    (a|b|c|d|e|f|g|h|i)&(a|b|c|d|e|f|g|h|~i)&(a|b|c|d|e|f|g|~h|i)&(a|b|c|d|e|f|g|~h|~i)&(a|b|c|d|e|f|~g|h|i)&(a|b|c|d|e|f|~g|h|~i)&(a|b|c|d|e|f|~g|~h|i)&(a|b|c|d|e|f|~g|~h|~i)&(a|b|c|d|e|~f|g|h|i)&(a|b|c|d|e|~f|g|h|~i)&(a|b|c|d|e|~f|g|~h|i)&(a|b|c|d|e|~f|g|~h|~i)&(a|b|c|d|e|~f|~g|h|i)&(a|b|c|d|e|~f|~g|h|~i)&(a|b|c|d|e|~f|~g|~h|i)&(a|b|c|d|e|~f|~g|~h|~i)&(a|b|c|d|~e|f|g|h|i)&(a|b|c|d|~e|f|g|h|~i)&(a|b|c|d|~e|f|g|~h|i)&(a|b|c|d|~e|f|g|~h|~i)&(a|b|c|d|~e|f|~g|h|i)&(a|b|c|d|~e|f|~g|h|~i)&(a|b|c|d|~e|f|~g|~h|i)&(a|b|c|d|~e|f|~g|~h|~i)&(a|b|c|d|~e|~f|g|h|i)&(a|b|c|d|~e|~f|g|h|~i)&(a|b|c|d|~e|~f|g|~h|i)&(a|b|c|d|~e|~f|g|~h|~i)&(a|b|c|d|~e|~f|~g|h|i)&(a|b|c|d|~e|~f|~g|h|~i)&(a|b|c|d|~e|~f|~g|~h|i)&(a|b|c|d|~e|~f|~g|~h|~i)&(a|b|c|~d|e|f|g|h|i)&(a|b|c|~d|e|f|g|h|~i)&(a|b|c|~d|e|f|g|~h|i)&(a|b|c|~d|e|f|g|~h|~i)&(a|b|c|~d|e|f|~g|h|i)&(a|b|c|~d|e|f|~g|h|~i)&(a|b|c|~d|e|f|~g|~h|i)&(a|b|c|~d|e|f|~g|~h|~i)&(a|b|c|~d|e|~f|g|h|i)&(a|b|c|~d|e|~f|g|h|~i)&(a|b|c|~d|e|~f|g|~h|i)&(a|b|c|~d|e|~f|g|~h|~i)&(a|b|c|~d|e|~f|~g|h|i)&(a|b|c|~d|e|~f|~g|h|~i)&(a|b|c|~d|e|~f|~g|~h|i)&(a|b|c|~d|e|~f|~g|~h|~i)&(a|b|c|~d|~e|f|g|h|i)&(a|b|c|~d|~e|f|g|h|~i)&(a|b|c|~d|~e|f|g|~h|i)&(a|b|c|~d|~e|f|g|~h|~i)&(a|b|c|~d|~e|f|~g|h|i)&(a|b|c|~d|~e|f|~g|h|~i)&(a|b|c|~d|~e|f|~g|~h|i)&(a|b|c|~d|~e|f|~g|~h|~i)&(a|b|c|~d|~e|~f|g|h|i)&(a|b|c|~d|~e|~f|g|h|~i)&(a|b|c|~d|~e|~f|g|~h|i)&(a|b|c|~d|~e|~f|g|~h|~i)&(a|b|c|~d|~e|~f|~g|h|i)&(a|b|c|~d|~e|~f|~g|h|~i)&(a|b|c|~d|~e|~f|~g|~h|i)&(a|b|c|~d|~e|~f|~g|~h|~i)&(a|b|~c|d|e|f|g|h|i)&(a|b|~c|d|e|f|g|h|~i)&(a|b|~c|d|e|f|g|~h|i)&(a|b|~c|d|e|f|g|~h|~i)&(a|b|~c|d|e|f|~g|h|i)&(a|b|~c|d|e|f|~g|h|~i)&(a|b|~c|d|e|f|~g|~h|i)&(a|b|~c|d|e|f|~g|~h|~i)&(a|b|~c|d|e|~f|g|h|i)&(a|b|~c|d|e|~f|g|h|~i)&(a|b|~c|d|e|~f|g|~h|i)&(a|b|~c|d|e|~f|g|~h|~i)&(a|b|~c|d|e|~f|~g|h|i)&(a|b|~c|d|e|~f|~g|h|~i)&(a|b|~c|d|e|~f|~g|~h|i)&(a|b|~c|d|e|~f|~g|~h|~i)&(a|b|~c|d|~e|f|g|h|i)&(a|b|~c|d|~e|f|g|h|~i)&(a|b|~c|d|~e|f|g|~h|i)&(a|b|~c|d|~e|f|g|~h|~i)&(a|b|~c|d|~e|f|~g|h|i)&(a|b|~c|d|~e|f|~g|h|~i)&(a|b|~c|d|~e|f|~g|~h|i)&(a|b|~c|d|~e|f|~g|~h|~i)&(a|b|~c|d|~e|~f|g|h|i)&(a|b|~c|d|~e|~f|g|h|~i)&(a|b|~c|d|~e|~f|g|~h|i)&(a|b|~c|d|~e|~f|g|~h|~i)&(a|b|~c|d|~e|~f|~g|h|i)&(a|b|~c|d|~e|~f|~g|h|~i)&(a|b|~c|d|~e|~f|~g|~h|i)&(a|b|~c|d|~e|~f|~g|~h|~i)&(a|b|~c|~d|e|f|g|h|i)&(a|b|~c|~d|e|f|g|h|~i)&(a|b|~c|~d|e|f|g|~h|i)&(a|b|~c|~d|e|f|g|~h|~i)&(a|b|~c|~d|e|f|~g|h|i)&(a|b|~c|~d|e|f|~g|h|~i)&(a|b|~c|~d|e|f|~g|~h|i)&(a|b|~c|~d|e|f|~g|~h|~i)&(a|b|~c|~d|e|~f|g|h|i)&(a|b|~c|~d|e|~f|g|h|~i)&(a|b|~c|~d|e|~f|g|~h|i)&(a|b|~c|~d|e|~f|g|~h|~i)&(a|b|~c|~d|e|~f|~g|h|i)&(a|b|~c|~d|e|~f|~g|h|~i)&(a|b|~c|~d|e|~f|~g|~h|i)&(a|b|~c|~d|e|~f|~g|~h|~i)&(a|b|~c|~d|~e|f|g|h|i)&(a|b|~c|~d|~e|f|g|h|~i)&(a|b|~c|~d|~e|f|g|~h|i)&(a|b|~c|~d|~e|f|g|~h|~i)&(a|b|~c|~d|~e|f|~g|h|i)&(a|b|~c|~d|~e|f|~g|h|~i)&(a|b|~c|~d|~e|f|~g|~h|i)&(a|b|~c|~d|~e|f|~g|~h|~i)&(a|b|~c|~d|~e|~f|g|h|i)&(a|b|~c|~d|~e|~f|g|h|~i)&(a|b|~c|~d|~e|~f|g|~h|i)&(a|b|~c|~d|~e|~f|g|~h|~i)&(a|b|~c|~d|~e|~f|~g|h|i)&(a|b|~c|~d|~e|~f|~g|h|~i)&(a|b|~c|~d|~e|~f|~g|~h|i)&(a|b|~c|~d|~e|~f|~g|~h|~i)&(a|~b|c|d|e|f|g|h|i)&(a|~b|c|d|e|f|g|h|~i)&(a|~b|c|d|e|f|g|~h|i)&(a|~b|c|d|e|f|g|~h|~i)&(a|~b|c|d|e|f|~g|h|i)&(a|~b|c|d|e|f|~g|h|~i)&(a|~b|c|d|e|f|~g|~h|i)&(a|~b|c|d|e|f|~g|~h|~i)&(a|~b|c|d|e|~f|g|h|i)&(a|~b|c|d|e|~f|g|h|~i)&(a|~b|c|d|e|~f|g|~h|i)&(a|~b|c|d|e|~f|g|~h|~i)&(a|~b|c|d|e|~f|~g|h|i)&(a|~b|c|d|e|~f|~g|h|~i)&(a|~b|c|d|e|~f|~g|~h|i)&(a|~b|c|d|e|~f|~g|~h|~i)&(a|~b|c|d|~e|f|g|h|i)&(a|~b|c|d|~e|f|g|h|~i)&(a|~b|c|d|~e|f|g|~h|i)&(a|~b|c|d|~e|f|g|~h|~i)&(a|~b|c|d|~e|f|~g|h|i)&(a|~b|c|d|~e|f|~g|h|~i)&(a|~b|c|d|~e|f|~g|~h|i)&(a|~b|c|d|~e|f|~g|~h|~i)&(a|~b|c|d|~e|~f|g|h|i)&(a|~b|c|d|~e|~f|g|h|~i)&(a|~b|c|d|~e|~f|g|~h|i)&(a|~b|c|d|~e|~f|g|~h|~i)&(a|~b|c|d|~e|~f|~g|h|i)&(a|~b|c|d|~e|~f|~g|h|~i)&(a|~b|c|d|~e|~f|~g|~h|i)&(a|~b|c|d|~e|~f|~g|~h|~i)&(a|~b|c|~d|e|f|g|h|i)&(a|~b|c|~d|e|f|g|h|~i)&(a|~b|c|~d|e|f|g|~h|i)&(a|~b|c|~d|e|f|g|~h|~i)&(a|~b|c|~d|e|f|~g|h|i)&(a|~b|c|~d|e|f|~g|h|~i)&(a|~b|c|~d|e|f|~g|~h|i)&(a|~b|c|~d|e|f|~g|~h|~i)&(a|~b|c|~d|e|~f|g|h|i)&(a|~b|c|~d|e|~f|g|h|~i)&(a|~b|c|~d|e|~f|g|~h|i)&(a|~b|c|~d|e|~f|g|~h|~i)&(a|~b|c|~d|e|~f|~g|h|i)&(a|~b|c|~d|e|~f|~g|h|~i)&(a|~b|c|~d|e|~f|~g|~h|i)&(a|~b|c|~d|e|~f|~g|~h|~i)&(a|~b|c|~d|~e|f|g|h|i)&(a|~b|c|~d|~e|f|g|h|~i)&(a|~b|c|~d|~e|f|g|~h|i)&(a|~b|c|~d|~e|f|g|~h|~i)&(a|~b|c|~d|~e|f|~g|h|i)&(a|~b|c|~d|~e|f|~g|h|~i)&(a|~b|c|~d|~e|f|~g|~h|i)&(a|~b|c|~d|~e|f|~g|~h|~i)&(a|~b|c|~d|~e|~f|g|h|i)&(a|~b|c|~d|~e|~f|g|h|~i)&(a|~b|c|~d|~e|~f|g|~h|i)&(a|~b|c|~d|~e|~f|g|~h|~i)&(a|~b|c|~d|~e|~f|~g|h|i)&(a|~b|c|~d|~e|~f|~g|h|~i)&(a|~b|c|~d|~e|~f|~g|~h|i)&(a|~b|c|~d|~e|~f|~g|~h|~i)&(a|~b|~c|d|e|f|g|h|i)&(a|~b|~c|d|e|f|g|h|~i)&(a|~b|~c|d|e|f|g|~h|i)&(a|~b|~c|d|e|f|g|~h|~i)&(a|~b|~c|d|e|f|~g|h|i)&(a|~b|~c|d|e|f|~g|h|~i)&(a|~b|~c|d|e|f|~g|~h|i)&(a|~b|~c|d|e|f|~g|~h|~i)&(a|~b|~c|d|e|~f|g|h|i)&(a|~b|~c|d|e|~f|g|h|~i)&(a|~b|~c|d|e|~f|g|~h|i)&(a|~b|~c|d|e|~f|g|~h|~i)&(a|~b|~c|d|e|~f|~g|h|i)&(a|~b|~c|d|e|~f|~g|h|~i)&(a|~b|~c|d|e|~f|~g|~h|i)&(a|~b|~c|d|e|~f|~g|~h|~i)&(a|~b|~c|d|~e|f|g|h|i)&(a|~b|~c|d|~e|f|g|h|~i)&(a|~b|~c|d|~e|f|g|~h|i)&(a|~b|~c|d|~e|f|g|~h|~i)&(a|~b|~c|d|~e|f|~g|h|i)&(a|~b|~c|d|~e|f|~g|h|~i)&(a|~b|~c|d|~e|f|~g|~h|i)&(a|~b|~c|d|~e|f|~g|~h|~i)&(a|~b|~c|d|~e|~f|g|h|i)&(a|~b|~c|d|~e|~f|g|h|~i)&(a|~b|~c|d|~e|~f|g|~h|i)&(a|~b|~c|d|~e|~f|g|~h|~i)&(a|~b|~c|d|~e|~f|~g|h|i)&(a|~b|~c|d|~e|~f|~g|h|~i)&(a|~b|~c|d|~e|~f|~g|~h|i)&(a|~b|~c|d|~e|~f|~g|~h|~i)&(a|~b|~c|~d|e|f|g|h|i)&(a|~b|~c|~d|e|f|g|h|~i)&(a|~b|~c|~d|e|f|g|~h|i)&(a|~b|~c|~d|e|f|g|~h|~i)&(a|~b|~c|~d|e|f|~g|h|i)&(a|~b|~c|~d|e|f|~g|h|~i)&(a|~b|~c|~d|e|f|~g|~h|i)&(a|~b|~c|~d|e|f|~g|~h|~i)&(a|~b|~c|~d|e|~f|g|h|i)&(a|~b|~c|~d|e|~f|g|h|~i)&(a|~b|~c|~d|e|~f|g|~h|i)&(a|~b|~c|~d|e|~f|g|~h|~i)&(a|~b|~c|~d|e|~f|~g|h|i)&(a|~b|~c|~d|e|~f|~g|h|~i)&(a|~b|~c|~d|e|~f|~g|~h|i)&(a|~b|~c|~d|e|~f|~g|~h|~i)&(a|~b|~c|~d|~e|f|g|h|i)&(a|~b|~c|~d|~e|f|g|h|~i)&(a|~b|~c|~d|~e|f|g|~h|i)&(a|~b|~c|~d|~e|f|g|~h|~i)&(a|~b|~c|~d|~e|f|~g|h|i)&(a|~b|~c|~d|~e|f|~g|h|~i)&(a|~b|~c|~d|~e|f|~g|~h|i)&(a|~b|~c|~d|~e|f|~g|~h|~i)&(a|~b|~c|~d|~e|~f|g|h|i)&(a|~b|~c|~d|~e|~f|g|h|~i)&(a|~b|~c|~d|~e|~f|g|~h|i)&(a|~b|~c|~d|~e|~f|g|~h|~i)&(a|~b|~c|~d|~e|~f|~g|h|i)&(a|~b|~c|~d|~e|~f|~g|h|~i)&(a|~b|~c|~d|~e|~f|~g|~h|i)&(a|~b|~c|~d|~e|~f|~g|~h|~i)&(~a|b|c|d|e|f|g|h|i)&(~a|b|c|d|e|f|g|h|~i)&(~a|b|c|d|e|f|g|~h|i)&(~a|b|c|d|e|f|g|~h|~i)&(~a|b|c|d|e|f|~g|h|i)&(~a|b|c|d|e|f|~g|h|~i)&(~a|b|c|d|e|f|~g|~h|i)&(~a|b|c|d|e|f|~g|~h|~i)&(~a|b|c|d|e|~f|g|h|~i)&(~a|b|c|d|e|~f|g|~h|i)&(~a|b|c|d|e|~f|g|~h|~i)&(~a|b|c|d|e|~f|~g|h|~i)&(~a|b|c|d|e|~f|~g|~h|i)&(~a|b|c|d|e|~f|~g|~h|~i)&(~a|b|c|d|~e|f|g|h|i)&(~a|b|c|d|~e|f|g|h|~i)&(~a|b|c|d|~e|f|g|~h|i)&(~a|b|c|d|~e|f|g|~h|~i)&(~a|b|c|d|~e|f|~g|h|i)&(~a|b|c|d|~e|f|~g|h|~i)&(~a|b|c|d|~e|f|~g|~h|i)&(~a|b|c|d|~e|f|~g|~h|~i)&(~a|b|c|d|~e|~f|g|h|~i)&(~a|b|c|d|~e|~f|g|~h|i)&(~a|b|c|d|~e|~f|g|~h|~i)&(~a|b|c|d|~e|~f|~g|h|~i)&(~a|b|c|d|~e|~f|~g|~h|i)&(~a|b|c|d|~e|~f|~g|~h|~i)&(~a|b|c|~d|e|f|g|h|i)&(~a|b|c|~d|e|f|g|h|~i)&(~a|b|c|~d|e|f|g|~h|i)&(~a|b|c|~d|e|f|g|~h|~i)&(~a|b|c|~d|e|f|~g|h|i)&(~a|b|c|~d|e|f|~g|h|~i)&(~a|b|c|~d|e|f|~g|~h|i)&(~a|b|c|~d|e|f|~g|~h|~i)&(~a|b|c|~d|e|~f|g|h|~i)&(~a|b|c|~d|e|~f|g|~h|i)&(~a|b|c|~d|e|~f|g|~h|~i)&(~a|b|c|~d|e|~f|~g|h|~i)&(~a|b|c|~d|e|~f|~g|~h|i)&(~a|b|c|~d|e|~f|~g|~h|~i)&(~a|b|c|~d|~e|f|g|h|i)&(~a|b|c|~d|~e|f|g|h|~i)&(~a|b|c|~d|~e|f|g|~h|i)&(~a|b|c|~d|~e|f|g|~h|~i)&(~a|b|c|~d|~e|f|~g|h|i)&(~a|b|c|~d|~e|f|~g|h|~i)&(~a|b|c|~d|~e|f|~g|~h|i)&(~a|b|c|~d|~e|f|~g|~h|~i)&(~a|b|c|~d|~e|~f|g|h|~i)&(~a|b|c|~d|~e|~f|g|~h|i)&(~a|b|c|~d|~e|~f|g|~h|~i)&(~a|b|c|~d|~e|~f|~g|h|~i)&(~a|b|c|~d|~e|~f|~g|~h|i)&(~a|b|c|~d|~e|~f|~g|~h|~i)&(~a|b|~c|d|e|f|g|h|i)&(~a|b|~c|d|e|f|g|h|~i)&(~a|b|~c|d|e|f|g|~h|i)&(~a|b|~c|d|e|f|g|~h|~i)&(~a|b|~c|d|e|f|~g|h|i)&(~a|b|~c|d|e|f|~g|h|~i)&(~a|b|~c|d|e|f|~g|~h|i)&(~a|b|~c|d|e|f|~g|~h|~i)&(~a|b|~c|d|e|~f|g|h|~i)&(~a|b|~c|d|e|~f|g|~h|i)&(~a|b|~c|d|e|~f|g|~h|~i)&(~a|b|~c|d|e|~f|~g|h|~i)&(~a|b|~c|d|e|~f|~g|~h|i)&(~a|b|~c|d|e|~f|~g|~h|~i)&(~a|b|~c|d|~e|f|g|h|i)&(~a|b|~c|d|~e|f|g|h|~i)&(~a|b|~c|d|~e|f|g|~h|i)&(~a|b|~c|d|~e|f|g|~h|~i)&(~a|b|~c|d|~e|f|~g|h|i)&(~a|b|~c|d|~e|f|~g|h|~i)&(~a|b|~c|d|~e|f|~g|~h|i)&(~a|b|~c|d|~e|f|~g|~h|~i)&(~a|b|~c|d|~e|~f|g|h|~i)&(~a|b|~c|d|~e|~f|g|~h|i)&(~a|b|~c|d|~e|~f|g|~h|~i)&(~a|b|~c|d|~e|~f|~g|h|~i)&(~a|b|~c|d|~e|~f|~g|~h|i)&(~a|b|~c|d|~e|~f|~g|~h|~i)&(~a|b|~c|~d|e|f|g|h|i)&(~a|b|~c|~d|e|f|g|h|~i)&(~a|b|~c|~d|e|f|g|~h|i)&(~a|b|~c|~d|e|f|g|~h|~i)&(~a|b|~c|~d|e|f|~g|h|i)&(~a|b|~c|~d|e|f|~g|h|~i)&(~a|b|~c|~d|e|f|~g|~h|i)&(~a|b|~c|~d|e|f|~g|~h|~i)&(~a|b|~c|~d|e|~f|g|h|~i)&(~a|b|~c|~d|e|~f|g|~h|i)&(~a|b|~c|~d|e|~f|g|~h|~i)&(~a|b|~c|~d|e|~f|~g|h|~i)&(~a|b|~c|~d|e|~f|~g|~h|i)&(~a|b|~c|~d|e|~f|~g|~h|~i)&(~a|b|~c|~d|~e|f|g|h|i)&(~a|b|~c|~d|~e|f|g|h|~i)&(~a|b|~c|~d|~e|f|g|~h|i)&(~a|b|~c|~d|~e|f|g|~h|~i)&(~a|b|~c|~d|~e|f|~g|h|i)&(~a|b|~c|~d|~e|f|~g|h|~i)&(~a|b|~c|~d|~e|f|~g|~h|i)&(~a|b|~c|~d|~e|f|~g|~h|~i)&(~a|b|~c|~d|~e|~f|g|h|~i)&(~a|b|~c|~d|~e|~f|g|~h|i)&(~a|b|~c|~d|~e|~f|g|~h|~i)&(~a|b|~c|~d|~e|~f|~g|h|~i)&(~a|b|~c|~d|~e|~f|~g|~h|i)&(~a|b|~c|~d|~e|~f|~g|~h|~i)&(~a|~b|c|d|e|f|g|h|i)&(~a|~b|c|d|e|f|g|h|~i)&(~a|~b|c|d|e|f|g|~h|i)&(~a|~b|c|d|e|f|g|~h|~i)&(~a|~b|c|d|e|f|~g|h|i)&(~a|~b|c|d|e|f|~g|h|~i)&(~a|~b|c|d|e|f|~g|~h|i)&(~a|~b|c|d|e|f|~g|~h|~i)&(~a|~b|c|d|e|~f|g|h|~i)&(~a|~b|c|d|e|~f|g|~h|i)&(~a|~b|c|d|e|~f|g|~h|~i)&(~a|~b|c|d|e|~f|~g|h|~i)&(~a|~b|c|d|e|~f|~g|~h|i)&(~a|~b|c|d|e|~f|~g|~h|~i)&(~a|~b|c|d|~e|f|g|h|i)&(~a|~b|c|d|~e|f|g|h|~i)&(~a|~b|c|d|~e|f|g|~h|i)&(~a|~b|c|d|~e|f|g|~h|~i)&(~a|~b|c|d|~e|f|~g|h|i)&(~a|~b|c|d|~e|f|~g|h|~i)&(~a|~b|c|d|~e|f|~g|~h|i)&(~a|~b|c|d|~e|f|~g|~h|~i)&(~a|~b|c|d|~e|~f|g|h|~i)&(~a|~b|c|d|~e|~f|g|~h|i)&(~a|~b|c|d|~e|~f|g|~h|~i)&(~a|~b|c|d|~e|~f|~g|h|~i)&(~a|~b|c|d|~e|~f|~g|~h|i)&(~a|~b|c|d|~e|~f|~g|~h|~i)&(~a|~b|c|~d|e|f|g|h|i)&(~a|~b|c|~d|e|f|g|h|~i)&(~a|~b|c|~d|e|f|g|~h|i)&(~a|~b|c|~d|e|f|g|~h|~i)&(~a|~b|c|~d|e|f|~g|h|i)&(~a|~b|c|~d|e|f|~g|h|~i)&(~a|~b|c|~d|e|f|~g|~h|i)&(~a|~b|c|~d|e|f|~g|~h|~i)&(~a|~b|c|~d|e|~f|g|h|~i)&(~a|~b|c|~d|e|~f|g|~h|i)&(~a|~b|c|~d|e|~f|g|~h|~i)&(~a|~b|c|~d|e|~f|~g|h|~i)&(~a|~b|c|~d|e|~f|~g|~h|i)&(~a|~b|c|~d|e|~f|~g|~h|~i)&(~a|~b|c|~d|~e|f|g|h|i)&(~a|~b|c|~d|~e|f|g|h|~i)&(~a|~b|c|~d|~e|f|g|~h|i)&(~a|~b|c|~d|~e|f|g|~h|~i)&(~a|~b|c|~d|~e|f|~g|h|i)&(~a|~b|c|~d|~e|f|~g|h|~i)&(~a|~b|c|~d|~e|f|~g|~h|i)&(~a|~b|c|~d|~e|f|~g|~h|~i)&(~a|~b|c|~d|~e|~f|g|h|~i)&(~a|~b|c|~d|~e|~f|g|~h|i)&(~a|~b|c|~d|~e|~f|g|~h|~i)&(~a|~b|c|~d|~e|~f|~g|h|~i)&(~a|~b|c|~d|~e|~f|~g|~h|i)&(~a|~b|c|~d|~e|~f|~g|~h|~i)&(~a|~b|~c|d|e|f|g|h|i)&(~a|~b|~c|d|e|f|g|h|~i)&(~a|~b|~c|d|e|f|g|~h|i)&(~a|~b|~c|d|e|f|g|~h|~i)&(~a|~b|~c|d|e|f|~g|h|i)&(~a|~b|~c|d|e|f|~g|h|~i)&(~a|~b|~c|d|e|f|~g|~h|i)&(~a|~b|~c|d|e|f|~g|~h|~i)&(~a|~b|~c|d|e|~f|g|h|~i)&(~a|~b|~c|d|e|~f|g|~h|i)&(~a|~b|~c|d|e|~f|g|~h|~i)&(~a|~b|~c|d|e|~f|~g|h|~i)&(~a|~b|~c|d|e|~f|~g|~h|i)&(~a|~b|~c|d|e|~f|~g|~h|~i)&(~a|~b|~c|d|~e|f|g|h|i)&(~a|~b|~c|d|~e|f|g|h|~i)&(~a|~b|~c|d|~e|f|g|~h|i)&(~a|~b|~c|d|~e|f|g|~h|~i)&(~a|~b|~c|d|~e|f|~g|h|i)&(~a|~b|~c|d|~e|f|~g|h|~i)&(~a|~b|~c|d|~e|f|~g|~h|i)&(~a|~b|~c|d|~e|f|~g|~h|~i)&(~a|~b|~c|d|~e|~f|g|h|~i)&(~a|~b|~c|d|~e|~f|g|~h|i)&(~a|~b|~c|d|~e|~f|g|~h|~i)&(~a|~b|~c|d|~e|~f|~g|h|~i)&(~a|~b|~c|d|~e|~f|~g|~h|i)&(~a|~b|~c|d|~e|~f|~g|~h|~i)&(~a|~b|~c|~d|e|f|g|h|i)&(~a|~b|~c|~d|e|f|g|h|~i)&(~a|~b|~c|~d|e|f|g|~h|i)&(~a|~b|~c|~d|e|f|g|~h|~i)&(~a|~b|~c|~d|e|f|~g|h|i)&(~a|~b|~c|~d|e|f|~g|h|~i)&(~a|~b|~c|~d|e|f|~g|~h|i)&(~a|~b|~c|~d|e|f|~g|~h|~i)&(~a|~b|~c|~d|e|~f|g|h|~i)&(~a|~b|~c|~d|e|~f|g|~h|i)&(~a|~b|~c|~d|e|~f|g|~h|~i)&(~a|~b|~c|~d|e|~f|~g|h|~i)&(~a|~b|~c|~d|e|~f|~g|~h|i)&(~a|~b|~c|~d|e|~f|~g|~h|~i)&(~a|~b|~c|~d|~e|f|g|h|i)&(~a|~b|~c|~d|~e|f|g|h|~i)&(~a|~b|~c|~d|~e|f|g|~h|i)&(~a|~b|~c|~d|~e|f|g|~h|~i)&(~a|~b|~c|~d|~e|f|~g|h|i)&(~a|~b|~c|~d|~e|f|~g|h|~i)&(~a|~b|~c|~d|~e|f|~g|~h|i)&(~a|~b|~c|~d|~e|f|~g|~h|~i)&(~a|~b|~c|~d|~e|~f|g|h|~i)&(~a|~b|~c|~d|~e|~f|g|~h|i)&(~a|~b|~c|~d|~e|~f|g|~h|~i)&(~a|~b|~c|~d|~e|~f|~g|h|~i)&(~a|~b|~c|~d|~e|~f|~g|~h|i)&(~a|~b|~c|~d|~e|~f|~g|~h|~i)
    a      b      c      d      e      f      g      h      i      value
    False  False  False  False  False  False  False  False  False  False
    False  False  False  False  False  False  False  False  True   False
    False  False  False  False  False  False  False  True   False  False
    False  False  False  False  False  False  False  True   True   False
    False  False  False  False  False  False  True   False  False  False
    False  False  False  False  False  False  True   False  True   False
    False  False  False  False  False  False  True   True   False  False
    False  False  False  False  False  False  True   True   True   False
    False  False  False  False  False  True   False  False  False  False
    False  False  False  False  False  True   False  False  True   False
    False  False  False  False  False  True   False  True   False  False
    False  False  False  False  False  True   False  True   True   False
    False  False  False  False  False  True   True   False  False  False
    False  False  False  False  False  True   True   False  True   False
    False  False  False  False  False  True   True   True   False  False
    False  False  False  False  False  True   True   True   True   False
    False  False  False  False  True   False  False  False  False  False
    False  False  False  False  True   False  False  False  True   False
    False  False  False  False  True   False  False  True   False  False
    False  False  False  False  True   False  False  True   True   False
    False  False  False  False  True   False  True   False  False  False
    False  False  False  False  True   False  True   False  True   False
    False  False  False  False  True   False  True   True   False  False
    False  False  False  False  True   False  True   True   True   False
    False  False  False  False  True   True   False  False  False  False
    False  False  False  False  True   True   False  False  True   False
    False  False  False  False  True   True   False  True   False  False
    False  False  False  False  True   True   False  True   True   False
    False  False  False  False  True   True   True   False  False  False
    False  False  False  False  True   True   True   False  True   False
    False  False  False  False  True   True   True   True   False  False
    False  False  False  False  True   True   True   True   True   False
    False  False  False  True   False  False  False  False  False  False
    False  False  False  True   False  False  False  False  True   False
    False  False  False  True   False  False  False  True   False  False
    False  False  False  True   False  False  False  True   True   False
    False  False  False  True   False  False  True   False  False  False
    False  False  False  True   False  False  True   False  True   False
    False  False  False  True   False  False  True   True   False  False
    False  False  False  True   False  False  True   True   True   False
    False  False  False  True   False  True   False  False  False  False
    False  False  False  True   False  True   False  False  True   False
    False  False  False  True   False  True   False  True   False  False
    False  False  False  True   False  True   False  True   True   False
    False  False  False  True   False  True   True   False  False  False
    False  False  False  True   False  True   True   False  True   False
    False  False  False  True   False  True   True   True   False  False
    False  False  False  True   False  True   True   True   True   False
    False  False  False  True   True   False  False  False  False  False
    False  False  False  True   True   False  False  False  True   False
    False  False  False  True   True   False  False  True   False  False
    False  False  False  True   True   False  False  True   True   False
    False  False  False  True   True   False  True   False  False  False
    False  False  False  True   True   False  True   False  True   False
    False  False  False  True   True   False  True   True   False  False
    False  False  False  True   True   False  True   True   True   False
    False  False  False  True   True   True   False  False  False  False
    False  False  False  True   True   True   False  False  True   False
    False  False  False  True   True   True   False  True   False  False
    False  False  False  True   True   True   False  True   True   False
    False  False  False  True   True   True   True   False  False  False
    False  False  False  True   True   True   True   False  True   False
    False  False  False  True   True   True   True   True   False  False
    False  False  False  True   True   True   True   True   True   False
    False  False  True   False  False  False  False  False  False  False
    False  False  True   False  False  False  False  False  True   False
    False  False  True   False  False  False  False  True   False  False
    False  False  True   False  False  False  False  True   True   False
    False  False  True   False  False  False  True   False  False  False
    False  False  True   False  False  False  True   False  True   False
    False  False  True   False  False  False  True   True   False  False
    False  False  True   False  False  False  True   True   True   False
    False  False  True   False  False  True   False  False  False  False
    False  False  True   False  False  True   False  False  True   False
    False  False  True   False  False  True   False  True   False  False
    False  False  True   False  False  True   False  True   True   False
    False  False  True   False  False  True   True   False  False  False
    False  False  True   False  False  True   True   False  True   False
    False  False  True   False  False  True   True   True   False  False
    False  False  True   False  False  True   True   True   True   False
    False  False  True   False  True   False  False  False  False  False
    False  False  True   False  True   False  False  False  True   False
    False  False  True   False  True   False  False  True   False  False
    False  False  True   False  True   False  False  True   True   False
    False  False  True   False  True   False  True   False  False  False
    False  False  True   False  True   False  True   False  True   False
    False  False  True   False  True   False  True   True   False  False
    False  False  True   False  True   False  True   True   True   False
    False  False  True   False  True   True   False  False  False  False
    False  False  True   False  True   True   False  False  True   False
    False  False  True   False  True   True   False  True   False  False
    False  False  True   False  True   True   False  True   True   False
    False  False  True   False  True   True   True   False  False  False
    False  False  True   False  True   True   True   False  True   False
    False  False  True   False  True   True   True   True   False  False
    False  False  True   False  True   True   True   True   True   False
    False  False  True   True   False  False  False  False  False  False
    False  False  True   True   False  False  False  False  True   False
    False  False  True   True   False  False  False  True   False  False
    False  False  True   True   False  False  False  True   True   False
    False  False  True   True   False  False  True   False  False  False
    False  False  True   True   False  False  True   False  True   False
    False  False  True   True   False  False  True   True   False  False
    False  False  True   True   False  False  True   True   True   False
    False  False  True   True   False  True   False  False  False  False
    False  False  True   True   False  True   False  False  True   False
    False  False  True   True   False  True   False  True   False  False
    False  False  True   True   False  True   False  True   True   False
    False  False  True   True   False  True   True   False  False  False
    False  False  True   True   False  True   True   False  True   False
    False  False  True   True   False  True   True   True   False  False
    False  False  True   True   False  True   True   True   True   False
    False  False  True   True   True   False  False  False  False  False
    False  False  True   True   True   False  False  False  True   False
    False  False  True   True   True   False  False  True   False  False
    False  False  True   True   True   False  False  True   True   False
    False  False  True   True   True   False  True   False  False  False
    False  False  True   True   True   False  True   False  True   False
    False  False  True   True   True   False  True   True   False  False
    False  False  True   True   True   False  True   True   True   False
    False  False  True   True   True   True   False  False  False  False
    False  False  True   True   True   True   False  False  True   False
    False  False  True   True   True   True   False  True   False  False
    False  False  True   True   True   True   False  True   True   False
    False  False  True   True   True   True   True   False  False  False
    False  False  True   True   True   True   True   False  True   False
    False  False  True   True   True   True   True   True   False  False
    False  False  True   True   True   True   True   True   True   False
    False  True   False  False  False  False  False  False  False  False
    False  True   False  False  False  False  False  False  True   False
    False  True   False  False  False  False  False  True   False  False
    False  True   False  False  False  False  False  True   True   False
    False  True   False  False  False  False  True   False  False  False
    False  True   False  False  False  False  True   False  True   False
    False  True   False  False  False  False  True   True   False  False
    False  True   False  False  False  False  True   True   True   False
    False  True   False  False  False  True   False  False  False  False
    False  True   False  False  False  True   False  False  True   False
    False  True   False  False  False  True   False  True   False  False
    False  True   False  False  False  True   False  True   True   False
    False  True   False  False  False  True   True   False  False  False
    False  True   False  False  False  True   True   False  True   False
    False  True   False  False  False  True   True   True   False  False
    False  True   False  False  False  True   True   True   True   False
    False  True   False  False  True   False  False  False  False  False
    False  True   False  False  True   False  False  False  True   False
    False  True   False  False  True   False  False  True   False  False
    False  True   False  False  True   False  False  True   True   False
    False  True   False  False  True   False  True   False  False  False
    False  True   False  False  True   False  True   False  True   False
    False  True   False  False  True   False  True   True   False  False
    False  True   False  False  True   False  True   True   True   False
    False  True   False  False  True   True   False  False  False  False
    False  True   False  False  True   True   False  False  True   False
    False  True   False  False  True   True   False  True   False  False
    False  True   False  False  True   True   False  True   True   False
    False  True   False  False  True   True   True   False  False  False
    False  True   False  False  True   True   True   False  True   False
    False  True   False  False  True   True   True   True   False  False
    False  True   False  False  True   True   True   True   True   False
    False  True   False  True   False  False  False  False  False  False
    False  True   False  True   False  False  False  False  True   False
    False  True   False  True   False  False  False  True   False  False
    False  True   False  True   False  False  False  True   True   False
    False  True   False  True   False  False  True   False  False  False
    False  True   False  True   False  False  True   False  True   False
    False  True   False  True   False  False  True   True   False  False
    False  True   False  True   False  False  True   True   True   False
    False  True   False  True   False  True   False  False  False  False
    False  True   False  True   False  True   False  False  True   False
    False  True   False  True   False  True   False  True   False  False
    False  True   False  True   False  True   False  True   True   False
    False  True   False  True   False  True   True   False  False  False
    False  True   False  True   False  True   True   False  True   False
    False  True   False  True   False  True   True   True   False  False
    False  True   False  True   False  True   True   True   True   False
    False  True   False  True   True   False  False  False  False  False
    False  True   False  True   True   False  False  False  True   False
    False  True   False  True   True   False  False  True   False  False
    False  True   False  True   True   False  False  True   True   False
    False  True   False  True   True   False  True   False  False  False
    False  True   False  True   True   False  True   False  True   False
    False  True   False  True   True   False  True   True   False  False
    False  True   False  True   True   False  True   True   True   False
    False  True   False  True   True   True   False  False  False  False
    False  True   False  True   True   True   False  False  True   False
    False  True   False  True   True   True   False  True   False  False
    False  True   False  True   True   True   False  True   True   False
    False  True   False  True   True   True   True   False  False  False
    False  True   False  True   True   True   True   False  True   False
    False  True   False  True   True   True   True   True   False  False
    False  True   False  True   True   True   True   True   True   False
    False  True   True   False  False  False  False  False  False  False
    False  True   True   False  False  False  False  False  True   False
    False  True   True   False  False  False  False  True   False  False
    False  True   True   False  False  False  False  True   True   False
    False  True   True   False  False  False  True   False  False  False
    False  True   True   False  False  False  True   False  True   False
    False  True   True   False  False  False  True   True   False  False
    False  True   True   False  False  False  True   True   True   False
    False  True   True   False  False  True   False  False  False  False
    False  True   True   False  False  True   False  False  True   False
    False  True   True   False  False  True   False  True   False  False
    False  True   True   False  False  True   False  True   True   False
    False  True   True   False  False  True   True   False  False  False
    False  True   True   False  False  True   True   False  True   False
    False  True   True   False  False  True   True   True   False  False
    False  True   True   False  False  True   True   True   True   False
    False  True   True   False  True   False  False  False  False  False
    False  True   True   False  True   False  False  False  True   False
    False  True   True   False  True   False  False  True   False  False
    False  True   True   False  True   False  False  True   True   False
    False  True   True   False  True   False  True   False  False  False
    False  True   True   False  True   False  True   False  True   False
    False  True   True   False  True   False  True   True   False  False
    False  True   True   False  True   False  True   True   True   False
    False  True   True   False  True   True   False  False  False  False
    False  True   True   False  True   True   False  False  True   False
    False  True   True   False  True   True   False  True   False  False
    False  True   True   False  True   True   False  True   True   False
    False  True   True   False  True   True   True   False  False  False
    False  True   True   False  True   True   True   False  True   False
    False  True   True   False  True   True   True   True   False  False
    False  True   True   False  True   True   True   True   True   False
    False  True   True   True   False  False  False  False  False  False
    False  True   True   True   False  False  False  False  True   False
    False  True   True   True   False  False  False  True   False  False
    False  True   True   True   False  False  False  True   True   False
    False  True   True   True   False  False  True   False  False  False
    False  True   True   True   False  False  True   False  True   False
    False  True   True   True   False  False  True   True   False  False
    False  True   True   True   False  False  True   True   True   False
    False  True   True   True   False  True   False  False  False  False
    False  True   True   True   False  True   False  False  True   False
    False  True   True   True   False  True   False  True   False  False
    False  True   True   True   False  True   False  True   True   False
    False  True   True   True   False  True   True   False  False  False
    False  True   True   True   False  True   True   False  True   False
    False  True   True   True   False  True   True   True   False  False
    False  True   True   True   False  True   True   True   True   False
    False  True   True   True   True   False  False  False  False  False
    False  True   True   True   True   False  False  False  True   False
    False  True   True   True   True   False  False  True   False  False
    False  True   True   True   True   False  False  True   True   False
    False  True   True   True   True   False  True   False  False  False
    False  True   True   True   True   False  True   False  True   False
    False  True   True   True   True   False  True   True   False  False
    False  True   True   True   True   False  True   True   True   False
    False  True   True   True   True   True   False  False  False  False
    False  True   True   True   True   True   False  False  True   False
    False  True   True   True   True   True   False  True   False  False
    False  True   True   True   True   True   False  True   True   False
    False  True   True   True   True   True   True   False  False  False
    False  True   True   True   True   True   True   False  True   False
    False  True   True   True   True   True   True   True   False  False
    False  True   True   True   True   True   True   True   True   False
    True   False  False  False  False  False  False  False  False  False
    True   False  False  False  False  False  False  False  True   False
    True   False  False  False  False  False  False  True   False  False
    True   False  False  False  False  False  False  True   True   False
    True   False  False  False  False  False  True   False  False  False
    True   False  False  False  False  False  True   False  True   False
    True   False  False  False  False  False  True   True   False  False
    True   False  False  False  False  False  True   True   True   False
    True   False  False  False  False  True   False  False  False  True
    True   False  False  False  False  True   False  False  True   False
    True   False  False  False  False  True   False  True   False  False
    True   False  False  False  False  True   False  True   True   False
    True   False  False  False  False  True   True   False  False  True
    True   False  False  False  False  True   True   False  True   False
    True   False  False  False  False  True   True   True   False  False
    True   False  False  False  False  True   True   True   True   False
    True   False  False  False  True   False  False  False  False  False
    True   False  False  False  True   False  False  False  True   False
    True   False  False  False  True   False  False  True   False  False
    True   False  False  False  True   False  False  True   True   False
    True   False  False  False  True   False  True   False  False  False
    True   False  False  False  True   False  True   False  True   False
    True   False  False  False  True   False  True   True   False  False
    True   False  False  False  True   False  True   True   True   False
    True   False  False  False  True   True   False  False  False  True
    True   False  False  False  True   True   False  False  True   False
    True   False  False  False  True   True   False  True   False  False
    True   False  False  False  True   True   False  True   True   False
    True   False  False  False  True   True   True   False  False  True
    True   False  False  False  True   True   True   False  True   False
    True   False  False  False  True   True   True   True   False  False
    True   False  False  False  True   True   True   True   True   False
    True   False  False  True   False  False  False  False  False  False
    True   False  False  True   False  False  False  False  True   False
    True   False  False  True   False  False  False  True   False  False
    True   False  False  True   False  False  False  True   True   False
    True   False  False  True   False  False  True   False  False  False
    True   False  False  True   False  False  True   False  True   False
    True   False  False  True   False  False  True   True   False  False
    True   False  False  True   False  False  True   True   True   False
    True   False  False  True   False  True   False  False  False  True
    True   False  False  True   False  True   False  False  True   False
    True   False  False  True   False  True   False  True   False  False
    True   False  False  True   False  True   False  True   True   False
    True   False  False  True   False  True   True   False  False  True
    True   False  False  True   False  True   True   False  True   False
    True   False  False  True   False  True   True   True   False  False
    True   False  False  True   False  True   True   True   True   False
    True   False  False  True   True   False  False  False  False  False
    True   False  False  True   True   False  False  False  True   False
    True   False  False  True   True   False  False  True   False  False
    True   False  False  True   True   False  False  True   True   False
    True   False  False  True   True   False  True   False  False  False
    True   False  False  True   True   False  True   False  True   False
    True   False  False  True   True   False  True   True   False  False
    True   False  False  True   True   False  True   True   True   False
    True   False  False  True   True   True   False  False  False  True
    True   False  False  True   True   True   False  False  True   False
    True   False  False  True   True   True   False  True   False  False
    True   False  False  True   True   True   False  True   True   False
    True   False  False  True   True   True   True   False  False  True
    True   False  False  True   True   True   True   False  True   False
    True   False  False  True   True   True   True   True   False  False
    True   False  False  True   True   True   True   True   True   False
    True   False  True   False  False  False  False  False  False  False
    True   False  True   False  False  False  False  False  True   False
    True   False  True   False  False  False  False  True   False  False
    True   False  True   False  False  False  False  True   True   False
    True   False  True   False  False  False  True   False  False  False
    True   False  True   False  False  False  True   False  True   False
    True   False  True   False  False  False  True   True   False  False
    True   False  True   False  False  False  True   True   True   False
    True   False  True   False  False  True   False  False  False  True
    True   False  True   False  False  True   False  False  True   False
    True   False  True   False  False  True   False  True   False  False
    True   False  True   False  False  True   False  True   True   False
    True   False  True   False  False  True   True   False  False  True
    True   False  True   False  False  True   True   False  True   False
    True   False  True   False  False  True   True   True   False  False
    True   False  True   False  False  True   True   True   True   False
    True   False  True   False  True   False  False  False  False  False
    True   False  True   False  True   False  False  False  True   False
    True   False  True   False  True   False  False  True   False  False
    True   False  True   False  True   False  False  True   True   False
    True   False  True   False  True   False  True   False  False  False
    True   False  True   False  True   False  True   False  True   False
    True   False  True   False  True   False  True   True   False  False
    True   False  True   False  True   False  True   True   True   False
    True   False  True   False  True   True   False  False  False  True
    True   False  True   False  True   True   False  False  True   False
    True   False  True   False  True   True   False  True   False  False
    True   False  True   False  True   True   False  True   True   False
    True   False  True   False  True   True   True   False  False  True
    True   False  True   False  True   True   True   False  True   False
    True   False  True   False  True   True   True   True   False  False
    True   False  True   False  True   True   True   True   True   False
    True   False  True   True   False  False  False  False  False  False
    True   False  True   True   False  False  False  False  True   False
    True   False  True   True   False  False  False  True   False  False
    True   False  True   True   False  False  False  True   True   False
    True   False  True   True   False  False  True   False  False  False
    True   False  True   True   False  False  True   False  True   False
    True   False  True   True   False  False  True   True   False  False
    True   False  True   True   False  False  True   True   True   False
    True   False  True   True   False  True   False  False  False  True
    True   False  True   True   False  True   False  False  True   False
    True   False  True   True   False  True   False  True   False  False
    True   False  True   True   False  True   False  True   True   False
    True   False  True   True   False  True   True   False  False  True
    True   False  True   True   False  True   True   False  True   False
    True   False  True   True   False  True   True   True   False  False
    True   False  True   True   False  True   True   True   True   False
    True   False  True   True   True   False  False  False  False  False
    True   False  True   True   True   False  False  False  True   False
    True   False  True   True   True   False  False  True   False  False
    True   False  True   True   True   False  False  True   True   False
    True   False  True   True   True   False  True   False  False  False
    True   False  True   True   True   False  True   False  True   False
    True   False  True   True   True   False  True   True   False  False
    True   False  True   True   True   False  True   True   True   False
    True   False  True   True   True   True   False  False  False  True
    True   False  True   True   True   True   False  False  True   False
    True   False  True   True   True   True   False  True   False  False
    True   False  True   True   True   True   False  True   True   False
    True   False  True   True   True   True   True   False  False  True
    True   False  True   True   True   True   True   False  True   False
    True   False  True   True   True   True   True   True   False  False
    True   False  True   True   True   True   True   True   True   False
    True   True   False  False  False  False  False  False  False  False
    True   True   False  False  False  False  False  False  True   False
    True   True   False  False  False  False  False  True   False  False
    True   True   False  False  False  False  False  True   True   False
    True   True   False  False  False  False  True   False  False  False
    True   True   False  False  False  False  True   False  True   False
    True   True   False  False  False  False  True   True   False  False
    True   True   False  False  False  False  True   True   True   False
    True   True   False  False  False  True   False  False  False  True
    True   True   False  False  False  True   False  False  True   False
    True   True   False  False  False  True   False  True   False  False
    True   True   False  False  False  True   False  True   True   False
    True   True   False  False  False  True   True   False  False  True
    True   True   False  False  False  True   True   False  True   False
    True   True   False  False  False  True   True   True   False  False
    True   True   False  False  False  True   True   True   True   False
    True   True   False  False  True   False  False  False  False  False
    True   True   False  False  True   False  False  False  True   False
    True   True   False  False  True   False  False  True   False  False
    True   True   False  False  True   False  False  True   True   False
    True   True   False  False  True   False  True   False  False  False
    True   True   False  False  True   False  True   False  True   False
    True   True   False  False  True   False  True   True   False  False
    True   True   False  False  True   False  True   True   True   False
    True   True   False  False  True   True   False  False  False  True
    True   True   False  False  True   True   False  False  True   False
    True   True   False  False  True   True   False  True   False  False
    True   True   False  False  True   True   False  True   True   False
    True   True   False  False  True   True   True   False  False  True
    True   True   False  False  True   True   True   False  True   False
    True   True   False  False  True   True   True   True   False  False
    True   True   False  False  True   True   True   True   True   False
    True   True   False  True   False  False  False  False  False  False
    True   True   False  True   False  False  False  False  True   False
    True   True   False  True   False  False  False  True   False  False
    True   True   False  True   False  False  False  True   True   False
    True   True   False  True   False  False  True   False  False  False
    True   True   False  True   False  False  True   False  True   False
    True   True   False  True   False  False  True   True   False  False
    True   True   False  True   False  False  True   True   True   False
    True   True   False  True   False  True   False  False  False  True
    True   True   False  True   False  True   False  False  True   False
    True   True   False  True   False  True   False  True   False  False
    True   True   False  True   False  True   False  True   True   False
    True   True   False  True   False  True   True   False  False  True
    True   True   False  True   False  True   True   False  True   False
    True   True   False  True   False  True   True   True   False  False
    True   True   False  True   False  True   True   True   True   False
    True   True   False  True   True   False  False  False  False  False
    True   True   False  True   True   False  False  False  True   False
    True   True   False  True   True   False  False  True   False  False
    True   True   False  True   True   False  False  True   True   False
    True   True   False  True   True   False  True   False  False  False
    True   True   False  True   True   False  True   False  True   False
    True   True   False  True   True   False  True   True   False  False
    True   True   False  True   True   False  True   True   True   False
    True   True   False  True   True   True   False  False  False  True
    True   True   False  True   True   True   False  False  True   False
    True   True   False  True   True   True   False  True   False  False
    True   True   False  True   True   True   False  True   True   False
    True   True   False  True   True   True   True   False  False  True
    True   True   False  True   True   True   True   False  True   False
    True   True   False  True   True   True   True   True   False  False
    True   True   False  True   True   True   True   True   True   False
    True   True   True   False  False  False  False  False  False  False
    True   True   True   False  False  False  False  False  True   False
    True   True   True   False  False  False  False  True   False  False
    True   True   True   False  False  False  False  True   True   False
    True   True   True   False  False  False  True   False  False  False
    True   True   True   False  False  False  True   False  True   False
    True   True   True   False  False  False  True   True   False  False
    True   True   True   False  False  False  True   True   True   False
    True   True   True   False  False  True   False  False  False  True
    True   True   True   False  False  True   False  False  True   False
    True   True   True   False  False  True   False  True   False  False
    True   True   True   False  False  True   False  True   True   False
    True   True   True   False  False  True   True   False  False  True
    True   True   True   False  False  True   True   False  True   False
    True   True   True   False  False  True   True   True   False  False
    True   True   True   False  False  True   True   True   True   False
    True   True   True   False  True   False  False  False  False  False
    True   True   True   False  True   False  False  False  True   False
    True   True   True   False  True   False  False  True   False  False
    True   True   True   False  True   False  False  True   True   False
    True   True   True   False  True   False  True   False  False  False
    True   True   True   False  True   False  True   False  True   False
    True   True   True   False  True   False  True   True   False  False
    True   True   True   False  True   False  True   True   True   False
    True   True   True   False  True   True   False  False  False  True
    True   True   True   False  True   True   False  False  True   False
    True   True   True   False  True   True   False  True   False  False
    True   True   True   False  True   True   False  True   True   False
    True   True   True   False  True   True   True   False  False  True
    True   True   True   False  True   True   True   False  True   False
    True   True   True   False  True   True   True   True   False  False
    True   True   True   False  True   True   True   True   True   False
    True   True   True   True   False  False  False  False  False  False
    True   True   True   True   False  False  False  False  True   False
    True   True   True   True   False  False  False  True   False  False
    True   True   True   True   False  False  False  True   True   False
    True   True   True   True   False  False  True   False  False  False
    True   True   True   True   False  False  True   False  True   False
    True   True   True   True   False  False  True   True   False  False
    True   True   True   True   False  False  True   True   True   False
    True   True   True   True   False  True   False  False  False  True
    True   True   True   True   False  True   False  False  True   False
    True   True   True   True   False  True   False  True   False  False
    True   True   True   True   False  True   False  True   True   False
    True   True   True   True   False  True   True   False  False  True
    True   True   True   True   False  True   True   False  True   False
    True   True   True   True   False  True   True   True   False  False
    True   True   True   True   False  True   True   True   True   False
    True   True   True   True   True   False  False  False  False  False
    True   True   True   True   True   False  False  False  True   False
    True   True   True   True   True   False  False  True   False  False
    True   True   True   True   True   False  False  True   True   False
    True   True   True   True   True   False  True   False  False  False
    True   True   True   True   True   False  True   False  True   False
    True   True   True   True   True   False  True   True   False  False
    True   True   True   True   True   False  True   True   True   False
    True   True   True   True   True   True   False  False  False  True
    True   True   True   True   True   True   False  False  True   False
    True   True   True   True   True   True   False  True   False  False
    True   True   True   True   True   True   False  True   True   False
    True   True   True   True   True   True   True   False  False  True
    True   True   True   True   True   True   True   False  True   False
    True   True   True   True   True   True   True   True   False  False
     True   True   True   True   True   True   True   True   True   False
     """)

    print()
    print("=" * 60)
    print("Generalized SAT Equation (non-balanced CNF examples)")
    print("=" * 60)

    # Example 1: single clause with one missing variable
    # (a | ~b), variable c absent -> subcube of size 2
    cnf = [(1, -2)]
    n = 3
    S = sat_equation_generalized(cnf, n)
    print("CNF: (a | ~b),  n = 3")
    print("S =", S)
    print("bits(S, 8) =", bits(S, 2 ** n))
    print("""
    (a|~b)
    a      b      c      value
    False  False  False  True
    False  False  True   True
    False  True   False  False
    False  True   True   False
    True   False  False  True
    True   False  True   True
    True   True   False  True
    True   True   True   True
    """)

    # Example 2: two clauses, different sizes
    # (a | ~b) & (~a | b | c)
    cnf = [(1, -2), (-1, 2, 3)]
    n = 3
    S = sat_equation_generalized(cnf, n)
    print("CNF: (a | ~b) & (~a | b | c),  n = 3")
    print("S =", S)
    print("bits(S, 8) =", bits(S, 2 ** n))
    print("""
    (a|~b)&(~a|b|c)
    a      b      c      value
    False  False  False  True
    False  False  True   True
    False  True   False  True
    False  True   True   False
    True   False  False  False
    True   False  True   False
    True   True   False  True
    True   True   True   True
    """)

    # Example 3: generalized function produces same result as balanced version
    cnf_balanced = [(1, -2, 3), (1, -2, -3), (-1, 2, -3)]
    n = 3
    S_bal = sat_equation(cnf_balanced, n)
    S_gen = sat_equation_generalized(cnf_balanced, n)
    print("Balanced CNF: (a|~b|c)&(a|~b|~c)&(~a|b|~c)")
    print("  balanced:   S =", S_bal, " bits =", bits(S_bal, 8))
    print("  generalized: S =", S_gen, " bits =", bits(S_gen, 8))
    print("  match:", S_bal == S_gen)
