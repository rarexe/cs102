def encrypt_caesar(plaintext: str) -> str:
"""
»> encrypt_caesar("PYTHON")
'SBWKRQ'
»> encrypt_caesar("python")
'sbwkrq'
»> encrypt_caesar("Python3.6")
'Sbwkrq3.6'
»> encrypt_caesar("")
''
"""


plaintext = input("введите текст для зашифровки: ")
for c in plaintext:
    if ord('a') <= ord(c) <= ord('w') or ord('A') <= ord(c) <= ord('W'):
        ciphhertext = chr(ord(c) + 3)
        print(ciphhertext, end='')
    if ord('x') <= ord(c) <= ord('z') or ord('X') <= ord(c) <= ord('Z'):
        ciphertext = chr(ord(c) + 3 - 26)
        print(ciphertext, end='')



def decrypt_caesar(ciphertext: str) -> str:
"""
»> decrypt_caesar("SBWKRQ")
'PYTHON'
»> decrypt_caesar("sbwkrq")
'python'
»> decrypt_caesar("Sbwkrq3.6")
'Python3.6'
»> decrypt_caesar("")
''
"""


ciphhertext = input('\n' 'введите текст для расшифровки: ')
for c in ciphhertext:
    if ord('d') <= ord(c) <= ord('z') or ord('D') <= ord(c) <= ord('Z') :
        plaintext = chr(ord(c) - 3)
        print(plaintext, end='')
    if ord('a') <= ord(c) <= ord('c') or ord('A') <= ord(c) <= ord('C'):
        plaintext = chr(ord(c) - 3 + 26)
        print(plaintext, end='')