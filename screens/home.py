import os

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button

import shutil

from pathlib import Path

from kivymd.uix.dialog import MDDialog

from database.db import Database


class HomeScreen(MDScreen):

    def on_pre_enter(self, *args):
        self.load_documents()

    def open_document(self, file_path):
        try:
            if not os.path.exists(file_path):
                print("File not found:", file_path)
                return

            os.startfile(file_path)

        except Exception as e:
            print("Error opening file:", e)

    def load_documents(self):

        container = self.ids.documents_container
        container.clear_widgets()

        documents = Database.get_documents()
        count = Database.get_document_count()

        self.ids.document_count.text = (
            f"{count} Document" if count == 1
            else f"{count} Documents"
        )

        if not documents:
            container.add_widget(
                MDLabel(
                    text="No documents saved yet",
                    halign="center",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height="50dp"
                )
            )
            return

        for document_id, name, original_name, file_path, file_type in documents:

            card = MDCard(
                orientation="horizontal",
                size_hint_x=1,
                size_hint_y=None,
                height="75dp",
                padding="10dp",
                spacing="5dp",
            )

            info = MDBoxLayout(
                orientation="vertical",
                size_hint_x=1
            )

            info.add_widget(
                MDLabel(
                    text=name,
                    bold=True,
                    theme_text_color="Primary"
                )
            )

            info.add_widget(
                MDLabel(
                    text=file_type.upper(),
                    theme_text_color="Secondary"
                )
            )

            card.add_widget(info)

            menu_button = MDIconButton(
                icon="dots-vertical"
            )

            save_button = MDIconButton(
                icon="content-save"
            )

            save_button.bind(
                on_release=lambda instance,
                path=file_path:
                self.save_to_downloads(path)
            )

            menu_button.bind(
                on_release=lambda instance,
                doc_id=document_id,
                doc_name=name,
                path=file_path:
                self.show_document_menu(
                    doc_id,
                    doc_name,
                    path
                )
            )


            card.add_widget(save_button)
            card.add_widget(menu_button)

            card.bind(
                on_release=lambda instance,
                path=file_path:
                self.preview_document(path,file_type)
            )

            container.add_widget(card)

    def show_document_menu(self, doc_id, name, file_path):

        self.selected_document_id = doc_id
        self.selected_document_name = name
        self.selected_document_path = file_path

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            adaptive_height=True
        )

        open_button = Button(
            text="Open",
            size_hint_y=None,
            height="50dp"
        )

        rename_button = Button(
            text="Rename",
            size_hint_y=None,
            height="50dp"
        )

        details_button = Button(
            text="Details",
            size_hint_y=None,
            height="50dp"
        )

        delete_button = Button(
            text="Delete",
            size_hint_y=None,
            height="50dp"
        )

        content.add_widget(open_button)
        content.add_widget(rename_button)
        content.add_widget(details_button)
        content.add_widget(delete_button)

        self.dialog = MDDialog(
            title=name,
            type="custom",
            content_cls=content
        )

        open_button.bind(
            on_release=lambda x: (
                self.dialog.dismiss(),
                self.open_document(self.selected_document_path)
            )
        )

        rename_button.bind(
            on_release=lambda x: self.rename_document()
        )

        details_button.bind(
            on_release=lambda x: (
                self.dialog.dismiss(),
                self.show_document_details(
                    self.selected_document_id
                )
            )
        )

        delete_button.bind(
            on_release=lambda x: self.delete_document()
        )

        self.dialog.open()

    def rename_document(self):

        self.dialog.dismiss()

        self.rename_field = MDTextField(
            hint_text="Document name",
            text=self.selected_document_name,
            size_hint_y=None,
            height="50dp"
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            adaptive_height=True
        )

        content.add_widget(self.rename_field)

        save_button = Button(
            text="Save",
            size_hint_y=None,
            height="50dp"
        )

        cancel_button = Button(
            text="Cancel",
            size_hint_y=None,
            height="50dp"
        )

        content.add_widget(save_button)
        content.add_widget(cancel_button)

        self.rename_dialog = MDDialog(
            title="Rename Document",
            type="custom",
            content_cls=content
        )

        save_button.bind(
            on_release=lambda x: self.save_rename()
        )

        cancel_button.bind(
            on_release=lambda x: self.rename_dialog.dismiss()
        )

        self.rename_dialog.open()

    def save_rename(self):

        new_name = self.rename_field.text.strip()

        if not new_name:
            return

        Database.rename_document(
            self.selected_document_id,
            new_name
        )

        self.rename_dialog.dismiss()

        self.load_documents()

    # def delete_document(self):

    #     self.dialog.dismiss()

    #     file_path = self.selected_document_path
    #     doc_id = self.selected_document_id

    #     try:

    #         if os.path.exists(file_path):
    #             os.remove(file_path)

    #         Database.delete_document(doc_id)

    #         self.load_documents()

    #     except Exception as e:
    #         print("Error deleting document:", e)
    def delete_document(self):

        self.dialog.dismiss()

        content = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            adaptive_height=True
        )

        content.add_widget(
            MDLabel(
                text=(
                    f'Are you sure you want to delete '
                    f'"{self.selected_document_name}"?'
                ),
                size_hint_y=None,
                height="60dp"
            )
        )

        cancel_button = Button(
            text="Cancel",
            size_hint_y=None,
            height="50dp"
        )

        delete_button = Button(
            text="Delete",
            size_hint_y=None,
            height="50dp"
        )

        content.add_widget(cancel_button)
        content.add_widget(delete_button)

        self.delete_dialog = MDDialog(
            title="Delete Document?",
            type="custom",
            content_cls=content
        )

        cancel_button.bind(
            on_release=lambda x: self.delete_dialog.dismiss()
        )

        delete_button.bind(
            on_release=lambda x: self.confirm_delete()
        )

        self.delete_dialog.open()

    def confirm_delete(self):

        self.delete_dialog.dismiss()

        file_path = self.selected_document_path
        doc_id = self.selected_document_id

        try:

            # Delete copied file from app_storage
            if os.path.exists(file_path):
                os.remove(file_path)

            # Delete database record
            Database.delete_document(doc_id)

            # Refresh Home screen
            self.load_documents()

            print("Document deleted successfully")

        except Exception as e:
            print("Error deleting document:", e)

    def show_document_details(self, doc_id):

        document = Database.get_document(doc_id)

        if not document:
            return

        (
            document_id,
            custom_name,
            original_name,
            file_path,
            file_type,
            created_at
        ) = document

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="10dp",
            adaptive_height=True
        )

        content.add_widget(
            MDLabel(
                text=f"[b]Name:[/b] {custom_name}",
                markup=True,
                size_hint_y=None,
                height="35dp"
            )
        )

        content.add_widget(
            MDLabel(
                text=f"[b]Original File:[/b] {original_name}",
                markup=True,
                size_hint_y=None,
                height="35dp"
            )
        )

        content.add_widget(
            MDLabel(
                text=f"[b]Type:[/b] {file_type.upper()}",
                markup=True,
                size_hint_y=None,
                height="35dp"
            )
        )

        content.add_widget(
            MDLabel(
                text=f"[b]Created:[/b] {created_at}",
                markup=True,
                size_hint_y=None,
                height="35dp"
            )
        )

        content.add_widget(
            MDLabel(
                text=f"[b]Path:[/b] {file_path}",
                markup=True,
                size_hint_y=None,
                height="70dp"
            )
        )

        self.details_dialog = MDDialog(
            title="Document Details",
            type="custom",
            content_cls=content
        )

        self.details_dialog.open()

    def search_documents(self, text):

        text = text.strip().lower()

        container = self.ids.documents_container
        container.clear_widgets()

        documents = Database.get_documents()

        if not text:
            self.load_documents()
            return

        found = False

        for document_id, name, original_name, file_path, file_type in documents:

            if (
                text in name.lower()
                or text in original_name.lower()
            ):

                found = True

                card = MDCard(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="75dp",
                    padding="15dp",
                    spacing="10dp",
                    ripple_behavior=True
                )

                info = MDBoxLayout(
                    orientation="vertical"
                )

                info.add_widget(
                    MDLabel(
                        text=name,
                        bold=True,
                        theme_text_color="Primary"
                    )
                )

                info.add_widget(
                    MDLabel(
                        text=file_type.upper(),
                        theme_text_color="Secondary"
                    )
                )

                card.add_widget(info)

                menu_button = MDIconButton(
                    icon="dots-vertical"
                )

                menu_button.bind(
                    on_release=lambda instance,
                    doc_id=document_id,
                    doc_name=name,
                    path=file_path:
                    self.show_document_menu(
                        doc_id,
                        doc_name,
                        path
                    )
                )

                card.add_widget(menu_button)

                card.bind(
                    on_release=lambda instance,
                    path=file_path,
                    ftype=file_type:
                    self.preview_document(path, ftype)
                )

                container.add_widget(card)

        if not found:

            container.add_widget(
                MDLabel(
                    text="No documents found",
                    halign="center",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height="50dp"
                )
            )

    def preview_document(self, file_path, file_type):
    
        print("Preview:", file_path)
        print("Type:", file_type)
    
        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return
    
        preview_screen = self.manager.get_screen("image_preview")
    
        if file_type == "image":
        
            preview_screen.show_image(file_path)
    
        elif file_type == "pdf":
        
            preview_screen.show_pdf(file_path)
    
        else:
        
            print("Unsupported file type:", file_type)
            return
    
        self.manager.current = "image_preview"

    def save_to_downloads(self, file_path):

        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return

        downloads = Path.home() / "Downloads/docValt"
        downloads.mkdir(parents=True, exist_ok=True)

        source = Path(file_path)

        destination = downloads / source.name

        counter = 1

        while destination.exists():
            destination = downloads / f"{source.stem}_{counter}{source.suffix}"
            counter += 1

        shutil.copy2(
            str(source),
            str(destination)
        )

        print("Saved to:", destination) 