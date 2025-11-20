import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    """Load settings from JSON file or create defaults."""
    defaults = {"temp_threshold": 25, "hum_threshold": 50}
    if not os.path.exists(SETTINGS_FILE) or os.stat(SETTINGS_FILE).st_size == 0:
        save_settings(defaults)
        return defaults
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return defaults
            return data
    except json.JSONDecodeError:
        return defaults

def save_settings(settings):
    """Save settings dictionary to JSON file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
