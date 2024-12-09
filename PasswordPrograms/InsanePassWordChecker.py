import re
import math

# List of commonly used passwords (you can expand this list as needed)
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345", "12345678", "qwerty", "abc123", "password1"
]

# Function to evaluate password strength
def check_password_strength(password):
    # Password strength criteria
    length_criteria = len(password) >= 8
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    digit_criteria = re.search(r'[0-9]', password) is not None
    special_char_criteria = re.search(r'[\W_]', password) is not None  # Non-alphanumeric characters
    common_password_criteria = password.lower() not in COMMON_PASSWORDS  # Check against common passwords

    # Calculate entropy for randomness check
    entropy = calculate_entropy(password)
    entropy_criteria = entropy >= 40  # A reasonable threshold for entropy

    # Count the number of conditions the password meets
    score = 0
    if length_criteria:
        score += 1
    if uppercase_criteria:
        score += 1
    if lowercase_criteria:
        score += 1
    if digit_criteria:
        score += 1
    if special_char_criteria:
        score += 1
    if common_password_criteria:
        score += 1
    if entropy_criteria:
        score += 1

    # Determine the strength based on score
    if score == 7:
        return "Very Strong"
    elif score == 6:
        return "Strong"
    elif score == 5:
        return "Medium"
    else:
        return "Weak"

# Function to calculate the entropy of the password
def calculate_entropy(password):
    # Total possible characters for the password
    possible_characters = 0

    if re.search(r'[a-z]', password):
        possible_characters += 26  # Lowercase letters
    if re.search(r'[A-Z]', password):
        possible_characters += 26  # Uppercase letters
    if re.search(r'[0-9]', password):
        possible_characters += 10  # Digits
    if re.search(r'[\W_]', password):
        possible_characters += 32  # Special characters (simple estimation)

    # Calculate entropy: entropy = log2(possible_characters^length)
    entropy = len(password) * math.log2(possible_characters) if possible_characters > 0 else 0
    return entropy

# Function to prompt user for password and check strength
def main():
    password = input("Enter your password: ")
    strength = check_password_strength(password)
    print(f"Password strength: {strength}")

if __name__ == "__main__":
    main()
