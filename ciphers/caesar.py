
def _validate_shift(shift):
    """Validate and normalize the Caesar shift."""
    if isinstance(shift, bool):
        raise ValueError("The shift must be an integer.")

    try:
        shift = int(shift)
    except (TypeError, ValueError):
        raise ValueError("Enter a valid integer shift.")

    return shift % 26


def encrypt(text, shift):
    """Encrypt text using the Caesar cipher."""
    if not isinstance(text, str):
        raise TypeError("Plaintext must be a string.")

    shift = _validate_shift(shift)
    result = []

    for char in text:
        if "A" <= char <= "Z":
            result.append(
                chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            )
        elif "a" <= char <= "z":
            result.append(
                chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            )
        else:
            result.append(char)

    return "".join(result)


def decrypt(ciphertext, shift):
    """Decrypt Caesar ciphertext using the same shift."""
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext must be a string.")

    shift = _validate_shift(shift)
    return encrypt(ciphertext, -shift)


if __name__ == "__main__":
    message = "aa"
    key = 3

    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)

    print("Original: ", repr(message))
    print("Encrypted:", repr(encrypted))
    print("Decrypted:", repr(decrypted))

    assert encrypted == "dd"
    assert decrypted == message

    print("Caesar cipher test passed!")
