import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QSlider, QPushButton, QFileDialog, QGroupBox)
from PyQt5.QtCore import Qt
import sys

# Directory to save profiles
PROFILES_DIR = os.path.join(os.path.dirname(__file__), "profiles")
if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

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
        main_layout.addWidget(self.create_script_group("Breath Hold on ADS", "Hold breath when ADS", no_slider=True))
        main_layout.addWidget(self.create_script_group("Bunny Hop", "Enable bunny hop"))
        main_layout.addWidget(self.create_script_group("Constant R2 Hold Down", "Hold down R2 continuously", no_slider=True))

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

    def create_script_group(self, title, description, no_slider=False):
        """Creates a group box with a toggle for each script. Optionally omits the slider."""
        group_box = QGroupBox(title)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(description))
        enable_combo = QComboBox()
        enable_combo.addItems(["Disabled", "Enabled"])
        layout.addWidget(enable_combo)

        if not no_slider:
            if title == "Switch Like Rapid Fire":
                layout.addWidget(QLabel("Fire duration (iterations)"))
                fire_duration_slider = QSlider(Qt.Horizontal)
                fire_duration_slider.setRange(1, 10)
                fire_duration_slider.setValue(1)
                fire_duration_label = QLabel("1 iteration")
                fire_duration_slider.valueChanged.connect(lambda value: fire_duration_label.setText(f"{value} iterations"))
                layout.addWidget(fire_duration_slider)
                layout.addWidget(fire_duration_label)

            elif title == "Bunny Hop":
                layout.addWidget(QLabel("Hop cycle duration (seconds)"))
                hop_duration_slider = QSlider(Qt.Horizontal)
                hop_duration_slider.setRange(1, 10)
                hop_duration_slider.setValue(1)
                hop_duration_label = QLabel("1 second")
                hop_duration_slider.valueChanged.connect(lambda value: hop_duration_label.setText(f"{value} seconds"))
                layout.addWidget(hop_duration_slider)
                layout.addWidget(hop_duration_label)

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
    main_app = ScriptSettingsApp()  # Open the main application directly
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
