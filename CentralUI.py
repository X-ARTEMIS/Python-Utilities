import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import os
import requests
import zipfile
import tempfile
import json
from PIL import Image, ImageTk  # Ensure you have Pillow installed

def install_packages(packages):
    """
    Install a list of packages using pip.

    Args:
    packages (list): List of package names to install.
    """
    for package in packages:
        try:
            # Check if package is already installed
            subprocess.check_call([sys.executable, '-m', 'pip', 'show', package])
            print(f"{package} is already installed.")
        except subprocess.CalledProcessError:
            # If package is not installed, install it
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

class FileExecutorApp:
    def __init__(self, root):
        self.root = root

        self.default_config = {
            "theme": "vista",  # Default UI theme
            "color_scheme": "light",  # Default color scheme
            "default_download_path": "~/Downloads",
            "default_extracted_path": "/tmp",
            "window_geometry": "600x400",
            "window_state": "zoomed"
        }

        self.latest_release_name = self.get_latest_release_name()
        if not self.latest_release_name:
            messagebox.showerror("Error", "Could not fetch the latest release name.")
            self.root.destroy()
            return

        self.zip_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'Python-Utilities-{self.latest_release_name}.zip')
        if not os.path.exists(self.zip_file_path):
            messagebox.showerror("Error", f"The file '{self.zip_file_path}' does not exist.")
            self.root.destroy()
            return

        self.extracted_folder_path = os.path.join(tempfile.gettempdir(), f'Python-Utilities-{self.latest_release_name}')
        self.extract_zip_file()

        self.config_file_path = os.path.join(self.extracted_folder_path, "config.json")

        self.create_config_if_not_exists()
        self.load_config()

        self.messages = {
            "error_fetch_release": "Could not fetch the latest release name.",
            "error_file_not_found": "The file '{file_path}' does not exist.",
            "execution_error": "Execution Error",
            "no_file_selected": "Please select a file to execute",
            "delete_confirmation": "Are you sure you want to delete '{file_path}'?",
            "deleted_message": "File '{file_path}' has been deleted.",
            "no_folder_selected": "Please select a folder containing Python utilities"
        }

        self.root.title("Python Utilities Executor")
        self.root.geometry(self.config["window_geometry"])
        if self.config["window_state"] == "zoomed":
            self.root.state('zoomed')

        self.style = ttk.Style()

        self.create_widgets()
        self.set_theme(self.config["theme"])
        self.apply_color_scheme(self.config["color_scheme"])

        self.selected_folder_path = None
        self.update_folder_list()

    def set_theme(self, theme):
        available_themes = self.style.theme_names()
        if theme not in available_themes:
            theme = "clam"  # Fallback theme
        self.style.theme_use(theme)

    def apply_color_scheme(self, scheme):
        if scheme == "dark":
            self.style.configure('TLabel', background='#2e2e2e', foreground='white')  # Dark grey background, white text
            self.style.configure('TButton', background='#5a5a5a', foreground='black')  # Lighter grey background, black text
            self.style.configure('TFrame', background='#2e2e2e')  # Dark grey background
            self.style.map('TButton', background=[('active', '#5a5a5a')], foreground=[('active', 'black')])
            self.root.configure(background='#2e2e2e')  # Dark grey background

            # Configure Listbox for dark mode
            self.folder_listbox.configure(background='#2e2e2e', foreground='white')
            self.file_listbox.configure(background='#2e2e2e', foreground='white')
        else:
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TButton', background='white', foreground='black')
            self.style.configure('TFrame', background='white')
            self.style.map('TButton', background=[('active', 'white')], foreground=[('active', 'black')])
            self.root.configure(background='white')

            # Configure Listbox for light mode
            self.folder_listbox.configure(background='white', foreground='black')
            self.file_listbox.configure(background='white', foreground='black')

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Select a folder containing Python utilities")
        self.label.pack(pady=10)

        self.folder_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.folder_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.folder_listbox.bind('<<ListboxSelect>>', self.on_folder_select)

        self.label_files = ttk.Label(self.root, text="Select a file to execute")
        self.label_files.pack(pady=10)

        self.file_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.file_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.file_listbox.bind('<<ListboxSelect>>', self.update_buttons_state)

        self.execute_button = ttk.Button(self.root, text="Open in CMD", command=self.open_in_cmd, style='Bottom.TButton', state=tk.DISABLED)
        self.execute_button.pack(pady=5)

        self.open_location_button = ttk.Button(self.root, text="Open in File Location", command=self.open_in_file_location, style='Bottom.TButton', state=tk.DISABLED)
        self.open_location_button.pack(pady=5)

        self.delete_button = ttk.Button(self.root, text="Delete", command=self.delete_file, style='Bottom.TButton', state=tk.DISABLED)
        self.delete_button.pack(pady=5)

        self.close_button = ttk.Button(self.root, text="Close", command=self.root.destroy, style='Bottom.TButton')
        self.close_button.pack(pady=5)

        self.install_button = ttk.Button(self.root, text="Install Packages", command=self.install_required_packages, style='Bottom.TButton')
        self.install_button.pack(side=tk.LEFT, anchor='sw', pady=5, padx=5)

        # Define a custom style for the bottom buttons
        self.style.configure('Bottom.TButton', foreground='black', background='white')

        # Search for Settings.png in the extracted folder path
        settings_image_path = self.find_file(self.extracted_folder_path, "Settings.png")
        if settings_image_path:
            try:
                self.settings_image = ImageTk.PhotoImage(Image.open(settings_image_path).resize((30, 30), Image.Resampling.LANCZOS))
            except Exception as e:
                messagebox.showerror("Error", f"Could not load Settings.png: {e}")
                self.settings_image = self.create_default_image()
        else:
            # Use a default image if Settings.png is not found
            self.settings_image = self.create_default_image()

        self.settings_button = tk.Button(self.root, image=self.settings_image, command=self.open_settings)
        self.settings_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    def find_file(self, root_folder, filename):
        """
        Recursively search for a file starting from the root_folder.
        Return the full path if found, otherwise return None.
        """
        for root, _, files in os.walk(root_folder):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def get_latest_release_name(self):
        try:
            response = requests.get("https://api.github.com/repos/Stari-Div/Python-Utilities/releases/latest")
            response.raise_for_status()
            latest_release = response.json()
            return latest_release['tag_name']
        except requests.RequestException as e:
            print(f"Error fetching latest release: {e}")
            return None

    def create_config_if_not_exists(self):
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as config_file:
                json.dump(self.default_config, config_file, indent=4)
        else:
            with open(self.config_file_path, 'r+') as config_file:
                config = json.load(config_file)
                # Add missing keys from default_config if they are not present
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                config_file.seek(0)
                json.dump(config, config_file, indent=4)
                config_file.truncate()

    def load_config(self):
        try:
            with open(self.config_file_path, "r") as config_file:
                self.config = json.load(config_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load configuration file: {e}")
            self.root.destroy()
            return

    def save_config(self):
        try:
            with open(self.config_file_path, "w") as config_file:
                json.dump(self.config, config_file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save configuration file: {e}")

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
        self.update_buttons_state()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for root, _, files in os.walk(self.selected_folder_path):
            for file in files:
                self.file_listbox.insert(tk.END, os.path.join(root, file))

    def update_buttons_state(self, event=None):
        if self.folder_listbox.curselection() or self.file_listbox.curselection():
            self.execute_button.config(state=tk.NORMAL)
            self.open_location_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.execute_button.config(state=tk.DISABLED)
            self.open_location_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def open_in_cmd(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            try:
                script_dir = os.path.dirname(selected_file)
                script_name = os.path.basename(selected_file)
                cmd_command = f'start cmd /K "cd /d {script_dir} && echo Press Enter to execute {script_name} && pause && python {script_name}"'
                subprocess.run(cmd_command, shell=True)
            except Exception as e:
                messagebox.showerror(self.messages["execution_error"], str(e))
        else:
            messagebox.showwarning("No File Selected", self.messages["no_file_selected"])

    def open_in_file_location(self):
        selected_file_index = self.file_listbox.curselection()
        selected_folder_index = self.folder_listbox.curselection()
        if selected_file_index:
            selected_file = self.file_listbox.get(selected_file_index)
            try:
                file_dir = os.path.dirname(selected_file)
                subprocess.run(f'explorer {file_dir}', shell=True)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif selected_folder_index:
            selected_folder = self.folder_listbox.get(selected_folder_index)
            try:
                folder_path = os.path.join(self.extracted_folder_path, selected_folder)
                subprocess.run(f'explorer {folder_path}', shell=True)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("No Selection", "Please select a file or folder first")

    def delete_file(self):
        selected_file_index = self.file_listbox.curselection()
        selected_folder_index = self.folder_listbox.curselection()
        if selected_file_index:
            selected_file = self.file_listbox.get(selected_file_index)
            try:
                confirm = messagebox.askyesno("Delete File", self.messages["delete_confirmation"].format(file_path=selected_file))
                if confirm:
                    os.remove(selected_file)
                    self.update_file_list()
                    messagebox.showinfo("Deleted", self.messages["deleted_message"].format(file_path=selected_file))
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file: {e}")
        elif selected_folder_index:
            selected_folder = self.folder_listbox.get(selected_folder_index)
            try:
                folder_path = os.path.join(self.extracted_folder_path, selected_folder)
                confirm = messagebox.askyesno("Delete Folder", self.messages["delete_confirmation"].format(file_path=folder_path))
                if confirm:
                    os.rmdir(folder_path)
                    self.update_folder_list()
                    self.file_listbox.delete(0, tk.END)
                    messagebox.showinfo("Deleted", self.messages["deleted_message"].format(file_path=folder_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete folder: {e}")
        else:
            messagebox.showwarning("No Selection", "Please select a file or folder to delete")

    def install_required_packages(self):
        packages_to_install = ["requests", "Pillow"]
        install_packages(packages_to_install)
        messagebox.showinfo("Installation Complete", "Required packages have been installed.")

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        if self.config["color_scheme"] == "dark":
            settings_window.configure(background='#2e2e2e')
        
        ttk.Label(settings_window, text="UI Theme:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        theme_var = tk.StringVar(value=self.config["theme"])
        theme_combobox = ttk.Combobox(settings_window, textvariable=theme_var, values=["clam", "alt", "default", "vista", "xpnative"])
        theme_combobox.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(settings_window, text="Color Scheme:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        color_scheme_var = tk.StringVar(value=self.config["color_scheme"])
        color_scheme_combobox = ttk.Combobox(settings_window, textvariable=color_scheme_var, values=["light", "dark"])
        color_scheme_combobox.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(settings_window, text="Default Download Path:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        default_download_path_var = tk.StringVar(value=self.config["default_download_path"])
        default_download_path_entry = ttk.Entry(settings_window, textvariable=default_download_path_var, width=50)
        default_download_path_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(settings_window, text="Default Extracted Path:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        default_extracted_path_var = tk.StringVar(value=self.config["default_extracted_path"])
        default_extracted_path_entry = ttk.Entry(settings_window, textvariable=default_extracted_path_var, width=50)
        default_extracted_path_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(settings_window, text="Window Geometry:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        window_geometry_var = tk.StringVar(value=self.config["window_geometry"])
        window_geometry_entry = ttk.Entry(settings_window, textvariable=window_geometry_var, width=50)
        window_geometry_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(settings_window, text="Window State:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        window_state_var = tk.StringVar(value=self.config["window_state"])
        window_state_combobox = ttk.Combobox(settings_window, textvariable=window_state_var, values=["normal", "zoomed", "iconic"])
        window_state_combobox.grid(row=5, column=1, padx=10, pady=5)

        if self.config["color_scheme"] == "dark":
            for widget in settings_window.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(foreground='white')
                else:
                    widget.configure(background='#2e2e2e', foreground='black')

        def save_settings():
            self.config["theme"] = theme_var.get()
            self.config["color_scheme"] = color_scheme_var.get()
            self.config["default_download_path"] = default_download_path_var.get()
            self.config["default_extracted_path"] = default_extracted_path_var.get()
            self.config["window_geometry"] = window_geometry_var.get()
            self.config["window_state"] = window_state_var.get()
            self.save_config()
            self.set_theme(self.config["theme"])
            self.apply_color_scheme(self.config["color_scheme"])
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
            settings_window.destroy()

        save_button = ttk.Button(settings_window, text="Save", command=save_settings)
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def create_default_image(self):
        # Create a simple default image (e.g., a grey square) if Settings.png is not found
        image = Image.new('RGB', (30, 30), color='grey')
        return ImageTk.PhotoImage(image)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExecutorApp(root)
    root.mainloop()
