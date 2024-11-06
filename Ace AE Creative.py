import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QCheckBox, QSlider, QPushButton, QTabWidget, QFileDialog, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt
import sys
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://fmjkuxaklulgxxudyeue.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZtamt1eGFrbHVsZ3h4dWR5ZXVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA4Njg2NTEsImV4cCI6MjA0NjQ0NDY1MX0.7SoGBP4Gw5vsUYOXpg1zXUA_smU_LClRzb01Z-hVElo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Directory to save profiles
PROFILES_DIR = os.path.join(os.path.dirname(__file__), "profiles")
if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("License Key Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        self.label = QLabel("Enter License Key:")
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("License Key")
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.validate_license)

        layout.addWidget(self.label)
        layout.addWidget(self.license_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def validate_license(self):
        entered_key = self.license_input.text()
        response = supabase.table("licenses").select("*").eq("license_key", entered_key).execute()
        if response.data and response.data[0]["is_active"]:
            self.open_main_app()
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid or inactive license key.")

    def open_main_app(self):
        self.close()
        self.main_app = ScriptSettingsApp()
        self.main_app.show()

class ScriptSettingsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Script Settings")
        self.setGeometry(100, 100, 600, 700)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.create_script_group("Switch Like Rapid Fire", "Enable rapid-fire mode"))
        main_layout.addWidget(self.create_script_group("Anti Knife Lunge", "Enable anti-lunge behavior"))
        main_layout.addWidget(self.create_script_group("Breath Hold on ADS", "Hold breath when ADS"))
        main_layout.addWidget(self.create_script_group("Bunny Hop", "Enable bunny hop"))
        main_layout.addWidget(self.create_script_group("Constant R2 Hold Down", "Hold down R2 continuously"))

        # Save and Profile Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        profile_button = QPushButton("Load Profile")
        profile_button.clicked.connect(self.load_profile)

        button_layout.addWidget(save_button)
        button_layout.addWidget(profile_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_script_group(self, title, description):
        """Creates a group box with a toggle for each script."""
        group_box = QGroupBox(title)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(description))
        enable_combo = QComboBox()
        enable_combo.addItems(["Disabled", "Enabled"])
        layout.addWidget(enable_combo)

        # Additional specific sliders based on the script requirements
        if title == "Switch Like Rapid Fire":
            layout.addWidget(QLabel("Fire duration (iterations)"))
            fire_duration_slider = QSlider(Qt.Horizontal)
            fire_duration_slider.setRange(1, 10)
            fire_duration_slider.setValue(1)
            fire_duration_label = QLabel("1 iteration")
            fire_duration_slider.valueChanged.connect(lambda value: fire_duration_label.setText(f"{value} iterations"))
            layout.addWidget(fire_duration_slider)
            layout.addWidget(fire_duration_label)

        elif title == "Breath Hold on ADS":
            layout.addWidget(QLabel("Hold duration (seconds)"))
            hold_duration_slider = QSlider(Qt.Horizontal)
            hold_duration_slider.setRange(1, 10)
            hold_duration_slider.setValue(5)
            hold_duration_label = QLabel("5 seconds")
            hold_duration_slider.valueChanged.connect(lambda value: hold_duration_label.setText(f"{value} seconds"))
            layout.addWidget(hold_duration_slider)
            layout.addWidget(hold_duration_label)

        elif title == "Bunny Hop":
            layout.addWidget(QLabel("Hop cycle duration (seconds)"))
            hop_duration_slider = QSlider(Qt.Horizontal)
            hop_duration_slider.setRange(1, 10)
            hop_duration_slider.setValue(1)
            hop_duration_label = QLabel("1 second")
            hop_duration_slider.valueChanged.connect(lambda value: hop_duration_label.setText(f"{value} seconds"))
            layout.addWidget(hop_duration_slider)
            layout.addWidget(hop_duration_label)

        elif title == "Constant R2 Hold Down":
            layout.addWidget(QLabel("Hold R2 duration (seconds)"))
            hold_duration_slider = QSlider(Qt.Horizontal)
            hold_duration_slider.setRange(1, 10)
            hold_duration_slider.setValue(1)
            hold_duration_label = QLabel("1 second")
            hold_duration_slider.valueChanged.connect(lambda value: hold_duration_label.setText(f"{value} seconds"))
            layout.addWidget(hold_duration_slider)
            layout.addWidget(hold_duration_label)

        group_box.setLayout(layout)
        return group_box

    def save_settings(self):
        """Save settings to a profile."""
        profile_path, _ = QFileDialog.getSaveFileName(self, "Save Profile", PROFILES_DIR, "JSON Files (*.json)")
        if profile_path:
            settings = {"sample_setting": "example_value"}  # Replace with actual settings
            with open(profile_path, "w") as f:
                json.dump(settings, f)
            print(f"Settings saved to {profile_path}")

    def load_profile(self):
        """Load settings from a profile."""
        profile_path, _ = QFileDialog.getOpenFileName(self, "Open Profile", PROFILES_DIR, "JSON Files (*.json)")
        if profile_path:
            with open(profile_path, "r") as f:
                settings = json.load(f)
                print(f"Settings loaded from {profile_path}: {settings}")
                # Apply loaded settings here

# Main Application
def main():
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
