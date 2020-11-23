def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a",)
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE

    key_lenght = len(keyword)
    text_lenght = len(plaintext)
    while key_lenght != text_lenght:
        keyword += keyword
        key_lenght = len(keyword)
        if key_lenght > text_lenght:
            keyword = keyword[:text_lenght]
            key_lenght = len(keyword)
    code_key = []
    ord_A = ord('A')
    ord_a = ord('a')

    if plaintext.islower():
        for i in range(key_lenght):
            if plaintext[i] == " ":
                code_key.append(" ")
            else:
                code_key.append(ord(keyword[i]) - ord_a)
        code_text = []
        for n in range(text_lenght):
            if plaintext[n] == " ":
                code_text.append(" ")
            else:
                code_text.append(ord(plaintext[n]) - ord_a)
        ciphertext = ''
        for u in range(len(plaintext)):
            if plaintext[u] == " ":
                ciphertext += " "
            else:
                value = (code_key[u] + code_text[u]) % 26 + ord_a
                ciphertext += chr(value)
    else:
        for i in range(key_lenght):
            if plaintext[i] == " ":
                code_key.append(" ")
            else:
                code_key.append(ord(keyword[i]) - ord_A)
        code_text = []
        for n in range(text_lenght):
            if plaintext[n] == " ":
                code_text.append(" ")
            else:
                code_text.append(ord(plaintext[n]) - ord_A)
        ciphertext = ''
        for u in range(len(plaintext)):
            if plaintext[u] == " ":
                value = ord(" ")
            else:
                value = (code_key[u] + code_text[u]) % 26 + ord_A
            ciphertext += chr(value)
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
    plaintext = ""
    # PUT YOUR CODE HERE
    key_lenght = len(keyword)
    text_lenght = len(ciphertext)

    while key_lenght != text_lenght:
        keyword += keyword
        key_lenght = len(keyword)
        if key_lenght > text_lenght:
            keyword = keyword[:text_lenght]
            key_lenght = len(keyword)
    code_key = []
    ord_a = ord('a')
    ord_A = ord('A')

    if ciphertext.islower():
        for i in range(key_lenght):
            if ciphertext[i] == " ":
                code_key.append(" ")
            else:
                code_key.append(ord(keyword[i]) - ord_a)
        code_text = []
        for n in range(text_lenght):
            if ciphertext[n] == " ":
                code_text.append(" ")
            else:
                code_text.append(ord(ciphertext[n]) - ord_a)
        for u in range(text_lenght):
            if ciphertext[u] == " ":
                value = ord(" ")
            else:

                value = ((code_text[u] - code_key[u] + 26) % 26) + ord_a
            plaintext += chr(value)
    else:
        for i in range(key_lenght):
            if ciphertext[i] == " ":
                code_key.append(" ")
            else:
                code_key.append(ord(keyword[i]) - ord_A)
        code_text = []
        for n in range(text_lenght):
            if ciphertext[n] == " ":
                code_text.append(" ")
            else:
                code_text.append(ord(ciphertext[n]) - ord_A)
        for u in range(text_lenght):
            if ciphertext[u] == " ":
                value = ord(" ")
            else:
                value = ((code_text[u] - code_key[u] + 26) % 26) + ord_A
            plaintext += chr(value)

    return plaintext

   
