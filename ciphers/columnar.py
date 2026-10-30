
"""
Columnar Transposition Cipher
Encrypts and decrypts text using a keyword.

Features:
- Supports uppercase and lowercase text.
- Preserves spaces, punctuation, and numbers.
- Supports repeated letters in the keyword.
- Handles messages shorter than the keyword.
- Restores the original message without adding padding.
"""


def _validate_key(key):
    """Validate and normalize the keyword."""
    if not isinstance(key, str):
        raise TypeError("The keyword must be a string.")

    key = key.strip()

    if not key:
        raise ValueError("The keyword must not be empty.")

    return key


def _validate_text(text, name):
    """Ensure the input text is a string."""
    if not isinstance(text, str):
        raise TypeError(f"{name} must be a string.")

    return text


def _column_order(key):
    """
    Return column indexes in alphabetical keyword order.

    If keyword letters repeat, their original column order
    is preserved to make encryption and decryption consistent.
    """
    return sorted(
        range(len(key)),
        key=lambda index: (key[index].lower(), index)
    )


def encrypt(text, key):
    """Encrypt a message using Columnar Transposition."""
    text = _validate_text(text, "Plaintext")
    key = _validate_key(key)

    if not text:
        return ""

    columns = len(key)
    order = _column_order(key)
    result = []

    # Read each column from top to bottom, following keyword order.
    for col in order:
        for position in range(col, len(text), columns):
            result.append(text[position])

    return "".join(result)


def decrypt(ciphertext, key):
    """Decrypt a message encrypted with this implementation."""
    ciphertext = _validate_text(ciphertext, "Ciphertext")
    key = _validate_key(key)

    if not ciphertext:
        return ""

    text_length = len(ciphertext)
    columns = len(key)

    # Determine the original length of every column.
    full_rows, extra_chars = divmod(text_length, columns)

    column_lengths = [
        full_rows + (1 if col < extra_chars else 0)
        for col in range(columns)
    ]

    order = _column_order(key)

    # Restore the columns in their original positions.
    restored_columns = [""] * columns
    position = 0

    for col in order:
        length = column_lengths[col]

        restored_columns[col] = ciphertext[
            position:position + length
        ]

        position += length

    # Read the restored columns row by row.
    result = []

    for row in range(full_rows + (1 if extra_chars else 0)):
        for col in range(columns):
            if row < len(restored_columns[col]):
                result.append(restored_columns[col][row])

    return "".join(result)


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    test_cases = [
        ("HELLO WORLD", "ZEBRA"),
        ("ager", "ZEBRA"),
        ("how are you?", "KEY"),
        ("Hello, World! 123", "BALLOON"),
        ("A", "LONGKEYWORD"),
        ("AB", "ZEBRA"),
        ("", "ZEBRA"),
        ("THIS IS A LONGER MESSAGE", "LETTER"),
        ("Repeated letters in a keyword", "BALLOON"),
    ]

    print("=" * 55)
    print("COLUMNAR TRANSPOSITION CIPHER TESTS")
    print("=" * 55)

    for original, keyword in test_cases:
        encrypted = encrypt(original, keyword)
        decrypted = decrypt(encrypted, keyword)

        print(f"\nOriginal:  {original!r}")
        print(f"Keyword:   {keyword!r}")
        print(f"Encrypted: {encrypted!r}")
        print(f"Decrypted: {decrypted!r}")

        assert decrypted == original, (
            f"FAILED: {original!r} did not restore correctly."
        )

    print("\nAll Columnar Transposition tests passed!")
