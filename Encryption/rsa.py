def is_prime(n):
    """
    Tests to see if a number is prime.
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
   """
    if n % 2 == 0:
        return True
    d == 3
    while d*d <= n and n != 0:
        d += 2
    if d*d > n
        return True
    else:
        return False


def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
        if a != 0:
            return a
        else:
            return b


def multiplicative_inverse(e: int, phi: int) -> int:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    else:
        if e >= phi:
        raise ValueError('Введенное число должно быть меньше значение phi')
    if e < phi:
        e = e % phi
        for x in range(1, phi):
            if (e * x) % phi == 1:
                return x

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    else:
        n = p*q
        phi = (p-1)(q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
