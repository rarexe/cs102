
def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    plaintext = input('Введите текст для шифрования: ')
    key = input('Введите ключ: ')
    for i, a in enumerate(plaintext):
        if ord('a') <= ord(a) <= ord('z'):
            x = ord(a) + ord(key[i % len(key)]) - ord('a')
        if x > ord('z'):
            x -= 26
            ciphertext = chr(x)
        else :
             ord('A') <= ord(a) <= ord('Z')
             x = ord(a) + ord(key[i % len(key)]) - ord('a')
        if x > ord('z'):
             x -= 26
             ciphertext = chr(x)
    return ciphertext



def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    ciphertext = input('\n' 'Введите текст для расшифровки: ')
    key = input('Введите ключ: ')
    for i, a in enumerate(ciphertext):
        if ord('a') <= ord(a) <= ord('z'):
            x = ord(a) - ord(key[i % len(key)]) + ord('a')
        if x < ord('a'):
            x += 26
            plaintext = chr(x)
        else:
            ord('A') <= ord(a) <= ord('Z')
            x = ord(a) - ord(key[i % len(key)]) + ord('a')
        if x < ord('A'):
            x += 26
            plaintext = chr(x)
    return plaintext