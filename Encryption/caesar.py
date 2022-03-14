def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    plaintext = ''
    for c in plaintext:
        if ord('a') <= ord(c) <= ord('w') or ord('A') <= ord(c) <= ord('W'):
            ciphertext = chr(ord(c) + 3)
        if ord('x') <= ord(c) <= ord('z') or ord('X') <= ord(c) <= ord('Z'):
            ciphertext = chr(ord(c) + 3 - 26)
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    ciphertext = ''
    for c in ciphertext:
        if ord('d') <= ord(c) <= ord('z') or ord('D') <= ord(c) <= ord('Z'):
            plaintext = chr(ord(c) - 3)
        if ord('a') <= ord(c) <= ord('c') or ord('A') <= ord(c) <= ord('C'):
            plaintext = chr(ord(c) - 3 + 26)
    return plaintext
