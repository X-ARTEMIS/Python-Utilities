import sys
import os
import requests
import zipfile
import tempfile
import subprocess
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QVBoxLayout,
    QWidget, QPushButton, QLabel, QListWidget, QComboBox, QLineEdit, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

def install_packages(packages):
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'show', package])
            print(f"{package} is already installed.")
        except subprocess.CalledProcessError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

class SettingsDialog(QDialog):
    def __init__(self, config, save_callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.config = config
        self.save_callback = save_callback

        layout = QVBoxLayout()

        # Color Scheme
        layout.addWidget(QLabel("Color Scheme:"))
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["dark"])
        self.color_scheme_combo.setCurrentText(self.config["color_scheme"])
        layout.addWidget(self.color_scheme_combo)

        # Default Download Path
        layout.addWidget(QLabel("Default Download Path:"))
        self.download_path_edit = QLineEdit(self.config["default_download_path"])
        layout.addWidget(self.download_path_edit)

        # Default Extracted Path
        layout.addWidget(QLabel("Default Extracted Path:"))
        self.extracted_path_edit = QLineEdit(self.config["default_extracted_path"])
        layout.addWidget(self.extracted_path_edit)

        # Window Geometry
        layout.addWidget(QLabel("Window Geometry:"))
        self.geometry_edit = QLineEdit(self.config["window_geometry"])
        layout.addWidget(self.geometry_edit)

        # Save Button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.config["color_scheme"] = self.color_scheme_combo.currentText()
        self.config["default_download_path"] = self.download_path_edit.text()
        self.config["default_extracted_path"] = self.extracted_path_edit.text()
        self.config["window_geometry"] = self.geometry_edit.text()
        self.save_callback(self.config)
        self.accept()

class FileExecutorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.default_config = {
            "color_scheme": "dark",
            "default_download_path": "~/Downloads",
            "default_extracted_path": "/tmp",
            "window_geometry": "800x600"
        }

        self.latest_release_name = self.get_latest_release_name()
        if not self.latest_release_name:
            QMessageBox.critical(self, "Error", "Could not fetch the latest release name.")
            sys.exit(1)

        self.zip_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'Python-Utilities-{self.latest_release_name}.zip')
        if not os.path.exists(self.zip_file_path):
            QMessageBox.critical(self, "Error", f"The file '{self.zip_file_path}' does not exist.")
            sys.exit(1)

        self.extracted_folder_path = os.path.join(tempfile.gettempdir(), f'Python-Utilities-{self.latest_release_name}')
        self.extract_zip_file()

        self.config_file_path = os.path.join(self.extracted_folder_path, "config.json")
        self.create_config_if_not_exists()
        self.load_config()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Python Utilities Executor")
        self.resize(*map(int, self.config["window_geometry"].split("x")))

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Folder Selector
        layout.addWidget(QLabel("Select a folder containing Python utilities"))
        self.folder_list = QListWidget()
        self.folder_list.itemSelectionChanged.connect(self.on_folder_select)
        layout.addWidget(self.folder_list)

        # File Selector
        layout.addWidget(QLabel("Select a file to execute"))
        self.file_list = QListWidget()
        self.file_list.itemSelectionChanged.connect(self.update_buttons_state)
        layout.addWidget(self.file_list)

        # Buttons
        self.execute_button = QPushButton("Open in CMD")
        self.execute_button.clicked.connect(self.open_in_cmd)
        self.execute_button.setEnabled(False)
        layout.addWidget(self.execute_button)

        self.open_location_button = QPushButton("Open in File Location")
        self.open_location_button.clicked.connect(self.open_in_file_location)
        self.open_location_button.setEnabled(False)
        layout.addWidget(self.open_location_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_file)
        self.delete_button.setEnabled(False)
        layout.addWidget(self.delete_button)

        install_button = QPushButton("Install Packages")
        install_button.clicked.connect(self.install_required_packages)
        layout.addWidget(install_button)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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

    def create_config_if_not_exists(self):
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as config_file:
                json.dump(self.default_config, config_file, indent=4)
        else:
            with open(self.config_file_path, 'r+') as config_file:
                config = json.load(config_file)
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
            QMessageBox.critical(self, "Error", f"Could not load configuration file: {e}")
            sys.exit(1)

    def save_config(self, config):
        try:
            with open(self.config_file_path, "w") as config_file:
                json.dump(config, config_file, indent=4)
            self.config = config
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save configuration file: {e}")

    def extract_zip_file(self):
        if not os.path.exists(self.extracted_folder_path):
            os.makedirs(self.extracted_folder_path)
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_folder_path)

    def update_folder_list(self):
        self.folder_list.clear()
        for item in os.listdir(self.extracted_folder_path):
            item_path = os.path.join(self.extracted_folder_path, item)
            if os.path.isdir(item_path):
                self.folder_list.addItem(item)

    def on_folder_select(self):
        self.file_list.clear()
        selected_folder = self.folder_list.currentItem()
        if selected_folder:
            folder_path = os.path.join(self.extracted_folder_path, selected_folder.text())
            for root, _, files in os.walk(folder_path):
                for file in files:
                    self.file_list.addItem(os.path.join(root, file))
        self.update_buttons_state()

    def update_buttons_state(self):
        has_selection = self.file_list.currentItem() is not None
        self.execute_button.setEnabled(has_selection)
        self.open_location_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def open_in_cmd(self):
        selected_file = self.file_list.currentItem().text()
        if selected_file:
            try:
                script_dir = os.path.dirname(selected_file)
                script_name = os.path.basename(selected_file)
                cmd_command = f'start cmd /K "cd /d {script_dir} && echo Press Enter to execute {script_name} && pause && python {script_name}"'
                subprocess.run(cmd_command, shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Execution Error", str(e))

    def open_in_file_location(self):
        selected_file = self.file_list.currentItem().text()
        if selected_file:
            try:
                file_dir = os.path.dirname(selected_file)
                subprocess.run(f'explorer {file_dir}', shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def delete_file(self):
        selected_file = self.file_list.currentItem().text()
        if selected_file:
            confirm = QMessageBox.question(
                self, "Delete File", f"Are you sure you want to delete '{selected_file}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                try:
                    os.remove(selected_file)
                    self.on_folder_select()
                    QMessageBox.information(self, "Deleted", f"File '{selected_file}' has been deleted.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not delete file: {e}")

    def install_required_packages(self):
        packages_to_install = ["requests", "PySide6"]
        install_packages(packages_to_install)
        QMessageBox.information(self, "Installation Complete", "Required packages have been installed.")

    def open_settings(self):
        dialog = SettingsDialog(self.config, self.save_config, self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExecutorApp()
    window.show()
    sys.exit(app.exec())
    root = tk.Tk()
    app = FileExecutorApp(root)
    root.mainloop()
