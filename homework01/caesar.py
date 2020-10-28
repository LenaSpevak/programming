import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
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
    ciphertext = ""
    # PUT YOUR CODE HERE
    for i in plaintext:
        ucode = ord(i)
        if 'a' <= i <= 'w' or 'A' <= i <= 'W':
            ucode += 3 
        elif 'x' <= i <= 'z' or 'X' <= i <= 'Z':
            ucode -= 23
        ciphertext += chr(ucode)    
    return ciphertest

def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
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
    plaintext = ""
    # PUT YOUR CODE HERE
    for i in ciphertext :
        ucode = ord(i)
        if 'a' <= i <= 'c' or 'A' <= i <= 'C':
            ucode += 23
        elif 'd' <= i <= 'z' or 'D' <= i <= 'Z':
            ucode -= 3 
        plaintext += chr(ucode)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
