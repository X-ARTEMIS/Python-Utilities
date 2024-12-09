word = input("Enter the text you would like to check: ")

consonants = "bcdfghjklmnpqrstvwxyz"

count=0

for letter in word:
    if letter in consonants:
        count = count + 1

print("There are",count, "consonants in the word" ,word)
