import random

minimum_number = int(input("Enter the minimum number that you want to be generated(Recommended:0): "))
maximum_number = int(input("Enter the maximum number you want generated: "))

randomNumber = random.randint(minimum_number,maximum_number) # Change the first number to set the minimum number, and the second number to change the maximum number
print(randomNumber)
