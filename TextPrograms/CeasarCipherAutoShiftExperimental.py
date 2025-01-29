# This uses a rough estimate. If it isn't correct use the normal manual shift and start from 1 until you get words :)
from collections import Counter

def get_shift(encrypted_text):
    """
    Estimates the shift value used in Caesar Cipher by analyzing the most frequent letter.
    
    Args:
    encrypted_text (str): The encrypted text to analyze.
    
    Returns:
    int: The estimated shift value.
    """
    # Count the frequency of each letter in the encrypted text
    frequency = Counter(encrypted_text)
    
    # Find the most common letter in the encrypted text
    most_common_letter, _ = frequency.most_common(1)[0]
    
    # Assuming the most common letter should be 'E', calculate the shift
    shift = (ord(most_common_letter) - ord('E')) % 26
    
    return shift

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
    encrypted_text = input("Enter the text to decrypt: ")
    
    # Estimate the shift value
    shift = get_shift(encrypted_text)
    print(f"Estimated Shift: {shift}")
    
    # Decrypt the text using the estimated shift
    decrypted_text = decrypt(encrypted_text, shift)
    print(f"Decrypted Text: {decrypted_text}")

if __name__ == "__main__":
    main()
