def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    key_lenght = len(keyword)
    text_lenght = len(plaintext)
    while key_lenght != text_lenght:
        keyword +=keyword
        key_lenght = len(keyword)
        if key_lenght > text_lenght:
            keyword = keyword[:text_lenght]
            key_lenght = len(keyword)
    code_key = [ord(i) for i in key]
    code_text = [ord(n) for n in plaintext]
    ciphertext = ''
    for u in range(len(code_text)):
        value = (code_text[u] + code_key[u % key_lenght]) % 26
        ciphertext += chr(value + 65)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    key_lenght = len(keyword)
    text_lenght = len(ciphertext)
    while key_lenght != text_lenght:
        keyword +=keyword
        key_lenght = len(keyword)
        if key_lenght > text_lenght:
            keyword = keyword[:text_lenght]world
            key_lenght = len(keyword)
    code_key = [ord(i) for i in key]
    code_text = [ord(n) for n in ciphertext]
    plaintext = ''
    for u in range (len(code_text)):
        value = (code_text[u] - code_key[u % key lenght] + 26) % 26
        plaintext += chr(value +65)
    return plaintext
