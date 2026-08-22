from pathlib import Path

from kivymd.uix.screen import MDScreen
from plyer import filechooser

from database.db import Database
from services.storage import copy_to_app


class AddDocumentScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_file = None

    def choose_file(self):
        filechooser.open_file(
            filters=[
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.pdf"
            ],
            on_selection=self.file_selected
        )

    def file_selected(self, selection):
        if not selection:
            return

        self.selected_file = selection[0]

        filename = Path(self.selected_file).name

        self.ids.file_name.text = filename
        self.ids.save_btn.disabled = False

    def save_document(self):

        if not self.selected_file:
            return

        custom_name = self.ids.custom_name.text.strip()

        if not custom_name:
            custom_name = Path(self.selected_file).stem

        new_path = copy_to_app(self.selected_file)

        ext = new_path.suffix.lower()

        file_type = "pdf" if ext == ".pdf" else "image"

        Database.add_document(
            custom_name,
            Path(self.selected_file).name,
            str(new_path),
            file_type
        )

        self.selected_file = None

        self.ids.file_name.text = "No File Selected"
        self.ids.custom_name.text = ""
        self.ids.save_btn.disabled = True

        self.manager.current = "home"