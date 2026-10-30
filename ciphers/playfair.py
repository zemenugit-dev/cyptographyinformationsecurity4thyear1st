
def create_matrix(key):
    """Create the 5x5 Playfair matrix."""
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Please enter a Playfair keyword.")

    key = key.upper()

    if not key.isascii() or not key.isalpha():
        raise ValueError("The keyword must contain English letters only.")

    key = key.replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    letters = []
    for char in key + alphabet:
        if char not in letters:
            letters.append(char)

    matrix = [letters[i:i + 5] for i in range(0, 25, 5)]

    positions = {
        char: (row, col)
        for row, line in enumerate(matrix)
        for col, char in enumerate(line)
    }

    return matrix, positions


def prepare_text(text):
    """Prepare plaintext into pairs, inserting filler letters."""
    if not isinstance(text, str):
        raise TypeError("Plaintext must be a string.")

    text = "".join(
        char.upper()
        for char in text
        if char.isascii() and char.isalpha()
    ).replace("J", "I")

    pairs = []
    i = 0

    while i < len(text):
        first = text[i]

        if i + 1 >= len(text):
            second = "X" if first != "X" else "Q"
            i += 1
        elif text[i] == text[i + 1]:
            second = "X" if first != "X" else "Q"
            i += 1
        else:
            second = text[i + 1]
            i += 2

        pairs.append((first, second))

    return pairs


def encrypt(plaintext, key):
    """Encrypt plaintext using the Playfair cipher."""
    matrix, positions = create_matrix(key)
    pairs = prepare_text(plaintext)
    result = []

    for first, second in pairs:
        row1, col1 = positions[first]
        row2, col2 = positions[second]

        if row1 == row2:
            result.append(matrix[row1][(col1 + 1) % 5])
            result.append(matrix[row2][(col2 + 1) % 5])

        elif col1 == col2:
            result.append(matrix[(row1 + 1) % 5][col1])
            result.append(matrix[(row2 + 1) % 5][col2])

        else:
            result.append(matrix[row1][col2])
            result.append(matrix[row2][col1])

    return "".join(result)


def decrypt(ciphertext, key):
    """Decrypt Playfair ciphertext."""
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext must be a string.")

    matrix, positions = create_matrix(key)

    text = "".join(
        char.upper()
        for char in ciphertext
        if char.isascii() and char.isalpha()
    ).replace("J", "I")

    if len(text) % 2 != 0:
        raise ValueError(
            "Playfair ciphertext must contain an even number of letters."
        )

    result = []

    for i in range(0, len(text), 2):
        first, second = text[i], text[i + 1]
        row1, col1 = positions[first]
        row2, col2 = positions[second]

        if row1 == row2:
            result.append(matrix[row1][(col1 - 1) % 5])
            result.append(matrix[row2][(col2 - 1) % 5])

        elif col1 == col2:
            result.append(matrix[(row1 - 1) % 5][col1])
            result.append(matrix[(row2 - 1) % 5][col2])

        else:
            result.append(matrix[row1][col2])
            result.append(matrix[row2][col1])

    return "".join(result)


if __name__ == "__main__":
    message = "ager"
    key = "MONARCHY"

    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)

    print("Original: ", message)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print("Note: Playfair removes spaces and capitalization.")
