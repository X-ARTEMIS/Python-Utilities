filename = input("Enter a name for the new file (Be sure to include the file extension)")
content = input("Enter the content for the file.")

def create_file(filename, content): # This is a script that can overwrite or create a new file depending on if the file already exists.
    with open(filename, "w") as file:
        file.write(content)
    print("File '{filename}' created successfully.")

def main():
    filename = "Edit4.txt" # Edit this to be your file name, be sure to include a file extension
    content = "dog dog dog dog dog" # This will be the content of the file. Edit this as well

    # Create the file
    create_file(filename, content)

if __name__ == "__main__":
    main()
