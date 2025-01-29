def encrypt(text, shift):
    """
    Encrypts the input text using Caesar Cipher with the given shift.
    
    Args:
    text (str): The input text to encrypt.
    shift (int): The number of positions to shift each character.
    
    Returns:
    str: The encrypted text.
    """
    result = ""

    # Traverse through the given text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Encrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)

        # Leave non-alphabet characters unchanged
        else:
            result += char

    return result

def main():
    print("Welcome to the Text Encrypter!")
    text = input("Enter the text to encrypt: ")
    shift = int(input("Enter the shift value: "))
    
    encrypted_text = encrypt(text, shift)
    print(f"Encrypted Text: {encrypted_text}")

if __name__ == "__main__":
    main()
