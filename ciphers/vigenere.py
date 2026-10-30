
def validate_key(key):
    """Validate the Vigenere keyword."""
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Please enter a Vigenere keyword.")

    if not key.isascii() or not key.isalpha():
        raise ValueError(
            "The key must contain English letters only, without spaces."
        )

    return key.upper()


def encrypt(plaintext, key):
    """
    Encrypt using the Vigenere cipher.
    Preserves letter case, spaces, punctuation, and digits.
    """
    if not isinstance(plaintext, str):
        raise TypeError("Plaintext must be a string.")

    key = validate_key(key)
    result = []
    key_index = 0

    for char in plaintext:
        if "A" <= char <= "Z":
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(
                chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            )
            key_index += 1

        elif "a" <= char <= "z":
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(
                chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            )
            key_index += 1

        else:
            result.append(char)

    return "".join(result)


def decrypt(ciphertext, key):
    """Decrypt Vigenere ciphertext using the same keyword."""
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext must be a string.")

    key = validate_key(key)
    result = []
    key_index = 0

    for char in ciphertext:
        if "A" <= char <= "Z":
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(
                chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            )
            key_index += 1

        elif "a" <= char <= "z":
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(
                chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            )
            key_index += 1

        else:
            result.append(char)

    return "".join(result)


if __name__ == "__main__":
    message = "Hello, how are you?"
    key = "LEMON"

    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)

    print("Original: ", message)
    print("Key:      ", key)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

    assert decrypted == message
    print("Vigenere cipher test passed!")
