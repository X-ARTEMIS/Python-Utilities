def open_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print("File content:\n")
            print(content)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = input("Enter the path to the file you want to open: ")
    open_file(file_path)
