
"""
Rail Fence Cipher
Cryptographic Systems Simulator

Provides:
    encrypt(text, key)
    decrypt(text, key)

The key represents the number of rails.
"""


def _validate_key(key):
    """Convert and validate the number of rails."""
    try:
        key = int(key)
    except (TypeError, ValueError):
        raise ValueError("The Rail Fence key must be a whole number.")

    if key < 1:
        raise ValueError("The Rail Fence key must be at least 1.")

    return key


def encrypt(text, key):
    """
    Encrypt text using the Rail Fence cipher.

    Args:
        text: The plaintext string.
        key: Number of rails.

    Returns:
        The encrypted ciphertext string.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    key = _validate_key(key)

    if key == 1 or key >= len(text) or len(text) <= 1:
        return text

    rails = [""] * key
    rail = 0
    direction = 1

    for character in text:
        rails[rail] += character

        if rail == 0:
            direction = 1
        elif rail == key - 1:
            direction = -1

        rail += direction

    return "".join(rails)


def decrypt(ciphertext, key):
    """
    Decrypt text encrypted using the Rail Fence cipher.

    Args:
        ciphertext: The encrypted string.
        key: Number of rails used during encryption.

    Returns:
        The original plaintext string.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext must be a string.")

    key = _validate_key(key)

    length = len(ciphertext)

    if key == 1 or key >= length or length <= 1:
        return ciphertext

    # Determine which rail each character belongs to.
    rail_pattern = []
    rail = 0
    direction = 1

    for _ in range(length):
        rail_pattern.append(rail)

        if rail == 0:
            direction = 1
        elif rail == key - 1:
            direction = -1

        rail += direction

    # Count the number of characters in each rail.
    rail_counts = [rail_pattern.count(r) for r in range(key)]

    # Split the ciphertext into the corresponding rail segments.
    rails = []
    position = 0

    for count in rail_counts:
        rails.append(list(ciphertext[position:position + count]))
        position += count

    # Reconstruct the original text by following the rail pattern.
    rail_positions = [0] * key
    plaintext = []

    for rail_number in rail_pattern:
        plaintext.append(rails[rail_number][rail_positions[rail_number]])
        rail_positions[rail_number] += 1

    return "".join(plaintext)


if __name__ == "__main__":
    # Simple test
    message = "WE ARE LEARNING CRYPTOGRAPHY"
    key = 3

    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)

    print("Original text :", message)
    print("Key           :", key)
    print("Encrypted text:", encrypted)
    print("Decrypted text:", decrypted)

    assert decrypted == message
    print("Test passed!")
