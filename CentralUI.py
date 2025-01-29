import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import requests
import zipfile
import tempfile

class FileExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Utilities Executor")

        # Fetch the latest release name
        self.latest_release_name = self.get_latest_release_name()
        if not self.latest_release_name:
            messagebox.showerror("Error", "Could not fetch the latest release name.")
            self.root.destroy()
            return

        self.zip_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'Python-Utilities-{self.latest_release_name}.zip')
        self.extracted_folder_path = os.path.join(tempfile.gettempdir(), f'Python-Utilities-{self.latest_release_name}')

        if not os.path.exists(self.zip_file_path):
            messagebox.showerror("Error", f"The file '{self.zip_file_path}' does not exist.")
            self.root.destroy()
            return

        # Extract the ZIP file
        self.extract_zip_file()

        self.label = tk.Label(root, text="Select a folder containing Python utilities")
        self.label.pack(pady=10)

        self.folder_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.folder_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.folder_listbox.bind('<<ListboxSelect>>', self.on_folder_select)

        self.label_files = tk.Label(root, text="Select a Python file to execute")
        self.label_files.pack(pady=10)

        self.file_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.file_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.execute_button = tk.Button(root, text="Open in CMD", command=self.open_in_cmd, state=tk.DISABLED)
        self.execute_button.pack(pady=5)

        self.selected_folder_path = None

        self.update_folder_list()

    def get_latest_release_name(self):
        try:
            response = requests.get("https://api.github.com/repos/Stari-Div/Python-Utilities/releases/latest")
            response.raise_for_status()
            latest_release = response.json()
            return latest_release['tag_name']
        except requests.RequestException as e:
            print(f"Error fetching latest release: {e}")
            return None

    def extract_zip_file(self):
        if not os.path.exists(self.extracted_folder_path):
            os.makedirs(self.extracted_folder_path)
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_folder_path)

    def update_folder_list(self):
        self.folder_listbox.delete(0, tk.END)
        for item in os.listdir(self.extracted_folder_path):
            item_path = os.path.join(self.extracted_folder_path, item)
            if os.path.isdir(item_path):
                self.folder_listbox.insert(tk.END, item)

    def on_folder_select(self, event):
        selected_index = self.folder_listbox.curselection()
        if selected_index:
            selected_folder = self.folder_listbox.get(selected_index)
            self.selected_folder_path = os.path.join(self.extracted_folder_path, selected_folder)
            self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for root, _, files in os.walk(self.selected_folder_path):
            for file in files:
                if file.endswith(".py"):
                    self.file_listbox.insert(tk.END, os.path.join(root, file))
        if self.file_listbox.size() > 0:
            self.execute_button.config(state=tk.NORMAL)
        else:
            self.execute_button.config(state=tk.DISABLED)

    def open_in_cmd(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            try:
                # Open a command prompt window and navigate to the directory of the selected file
                script_dir = os.path.dirname(selected_file)
                script_name = os.path.basename(selected_file)
                cmd_command = f'start cmd /K "cd /d {script_dir} && echo Press Enter to execute {script_name} && pause && python {script_name}"'
                subprocess.run(cmd_command, shell=True)
            except Exception as e:
                messagebox.showerror("Execution Error", str(e))
        else:
            messagebox.showwarning("No File Selected", "Please select a Python file to execute")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExecutorApp(root)
    root.mainloop()
