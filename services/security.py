from pathlib import Path
import hashlib
import json

from kivy.utils import platform

if platform == "android":

    from android.storage import app_storage_path

    SETTINGS_FILE = Path(app_storage_path()) / "settings.json"

else:

    BASE_DIR = Path(__file__).resolve().parent.parent
    SETTINGS_FILE = BASE_DIR / "settings.json"



def load_settings():

    if not SETTINGS_FILE.exists():
        return {}

    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return {}


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def hash_pin(pin):

    return hashlib.sha256(
        pin.encode("utf-8")
    ).hexdigest()


def pin_exists():

    settings = load_settings()

    return "pin_hash" in settings

def set_pin(pin):

    settings = load_settings()

    settings["pin_hash"] = hash_pin(pin)
    settings["lock_enabled"] = True

    save_settings(settings)


def verify_pin(pin):

    settings = load_settings()

    stored_hash = settings.get("pin_hash")

    if not stored_hash:
        return False

    return hash_pin(pin) == stored_hash


def lock_enabled():

    settings = load_settings()

    return settings.get("lock_enabled", False)


def set_lock_enabled(enabled):

    settings = load_settings()

    settings["lock_enabled"] = enabled

    save_settings(settings)