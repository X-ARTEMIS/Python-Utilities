def decrypt(text, shift):
    """
    Decrypts the input text using Caesar Cipher with the given shift.
    
    Args:
    text (str): The encrypted text to decrypt.
    shift (int): The number of positions to shift each character back.
    
    Returns:
    str: The decrypted text.
    """
    result = ""

    # Traverse through the given text
    for i in range(len(text)):
        char = text[i]

        # Decrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) - shift - 65) % 26 + 65)

        # Decrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) - shift - 97) % 26 + 97)

        # Leave non-alphabet characters unchanged
        else:
            result += char

    return result

def main():
    print("Welcome to the Text Decrypter!")
    text = input("Enter the text to decrypt: ")
    shift = int(input("Enter the shift value: "))
    
    decrypted_text = decrypt(text, shift)
    print(f"Decrypted Text: {decrypted_text}")

if __name__ == "__main__":
    main()
