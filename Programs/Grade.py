grade = float(input("Please enter your grade: "))
if 100 >= grade >= 85:
    print("You get an A")
elif 70 <= grade <= 84:
    print("You get a B")
elif 60 <= grade <= 69:
    print("You get a C")
elif 50 <= grade <= 59:
    print("You get a D")
else:
    print("You failed")
