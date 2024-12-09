word = input("Enter the text you would like to check: ")

vowels = "aeiou"

count=0

for letter in word:
    if letter in vowels:
        count = count + 1

print("There are ",count, "vowels in the word" ,word)