def create_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)
    print(f"File '{filename}' created successfully.")

def main():
    filename = "Edit4.txt" # Edit this to be your file name, be sure to include a file extension
    content = "dog dog dog dog dog" # This will be the content of the file. Edit this as well

    # Create the file
    create_file(filename, content)

if __name__ == "__main__":
    main()