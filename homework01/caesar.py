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
    for i in range(len(plaintext)):
        if ord('a') <= ord(plaintext[i]) <= ord('z'):
            ciphertext += chr(((ord(plaintext[i]) - ord('a') + shift) % 26) + ord('a'))
        elif ord('A') <= ord(plaintext[i]) <= ord('Z'):
            ciphertext += chr(((ord(plaintext[i]) - ord('A') + shift) % 26) + ord('A'))
        else:
            ciphertext += plaintext[i]
    return ciphertext


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
    for i in range(len(ciphertext)):
        if ord('a') <= ord(ciphertext[i]) <= ord('z'):
            plaintext += chr(((ord(ciphertext[i]) - ord('a') - shift) % 26) + ord('a'))
        elif ord('A') <= ord(ciphertext[i]) <= ord('Z'):
            plaintext += chr(((ord(ciphertext[i]) - ord('A') - shift) % 26) + ord('A'))
        else:
            plaintext += ciphertext[i]
    return plaintext


def caesar_breaker(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker("python", d)
    0
    >>> caesar_breaker("sbwkrq", d)
    3
    """
    best_shift = 0
    ltrs = ciphertext.split()
    for ltr in ltrs:
        for i in range(26):
            decrypted_word = decrypt_caesar(ltr, i)
            if decrypted_word in dictionary:
                best_shift = i
    return best_shift