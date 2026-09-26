"""
factorial_stack.py
-------------------
Re-implements "factorial using a Stack" from the lecture, with comments
explaining WHY a stack is the natural fit.

Two ways a stack shows up in factorial:

(A) EXPLICIT stack -- we build our own ArrayStack, push the numbers
    1, 2, 3, ..., n onto it, then pop them back off one at a time,
    multiplying as we go. This mirrors exactly how you'd do it by hand
    with a physical stack of plates numbered 1..n.

(B) IMPLICIT stack -- the recursive definition
        n! = n * (n-1)!
    relies on the CALL STACK the language runtime keeps automatically.
    Each recursive call is "pushed" onto the call stack; when the base
    case (0! = 1) is hit, the calls are "popped" back off in reverse
    order and multiplied together as each call returns.

Both approaches are shown below, plus a plain iterative version for
comparison.
"""

from stack import ArrayStack


def factorial_explicit_stack(n: int) -> int:
    """(A) Compute n! by pushing 1..n onto a Stack, then popping+multiplying."""
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")

    s = ArrayStack()

    # Push phase: load the stack with 1, 2, 3, ..., n
    for i in range(1, n + 1):
        s.push(i)

    # Pop phase: unwind the stack, multiplying as we go
    result = 1
    while not s.is_empty():
        result *= s.pop()

    return result


def factorial_recursive(n: int) -> int:
    """(B) Compute n! recursively -- relies on the language's own call stack."""
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)   # each call waits on the call stack


def factorial_iterative(n: int) -> int:
    """Plain iterative version, for comparison -- no stack needed at all."""
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    for n in [0, 1, 5, 7, 10]:
        a = factorial_explicit_stack(n)
        b = factorial_recursive(n)
        c = factorial_iterative(n)
        assert a == b == c, f"Mismatch for n={n}: {a}, {b}, {c}"
        print(f"{n}! = {a}   (explicit stack / recursive call-stack / iterative all agree)")
