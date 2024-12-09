while 1==1:
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))
    operation = input("Enter an operation: ")
    if operation=="+":
        answer = num1 + num2
    elif operation=="-":
        answer = num1 - num2
    elif operation=="*":
        answer = num1 * num2
    elif operation=="/":
        answer = num1 / num2
    else:
        answer = "ERROR: non-existent operation entered."
    print("Your answer is", answer)

    if answer=="ERROR: non-existent operation entered.":
        print(answer)
