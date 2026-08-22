from pathlib import Path
import shutil

# Project root (DocVault folder)
from kivy.utils import platform

if platform == "android":

    from android.storage import app_storage_path

    APP_STORAGE = Path(app_storage_path()) / "app_storage"

else:

    BASE_DIR = Path(__file__).resolve().parent.parent
    APP_STORAGE = BASE_DIR / "app_storage"

# app_storage folder inside the project
APP_STORAGE.mkdir(parents=True, exist_ok=True)


def copy_to_app(source_path):
    source = Path(source_path)

    destination = APP_STORAGE / source.name

    counter = 1
    while destination.exists():
        destination = APP_STORAGE / f"{source.stem}_{counter}{source.suffix}"
        counter += 1

    shutil.copy2(str(source), str(destination))

    return destination