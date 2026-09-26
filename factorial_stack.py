from stack import ArrayStack


def factorial_explicit_stack(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")

    s = ArrayStack()

    for i in range(1, n + 1):
        s.push(i)

    result = 1
    while not s.is_empty():
        result *= s.pop()

    return result


def factorial_recursive(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
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
        print(f"{n}! = {a}")
