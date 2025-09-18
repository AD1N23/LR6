# fermat_cython.pyx
from math import isqrt

def is_perfect_square(n: int) -> bool:
    """Checks if a number is a perfect square."""
    if n < 0:
        return False
    root: int = isqrt(n)
    return root * root == n

def fermat_factorization(N: int) -> tuple[int, int]:
    """Factorizes N using Fermat's method."""
    if N % 2 == 0:
        return 2, N // 2

    x: int = isqrt(N) + 1
    while True:
        y_squared: int = x * x - N
        if is_perfect_square(y_squared):
            y: int = isqrt(y_squared)
            return (x - y, x + y)
        x += 1