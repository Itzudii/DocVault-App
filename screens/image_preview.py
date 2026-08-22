from pathlib import Path

import fitz

from kivymd.uix.screen import MDScreen


class ImagePreviewScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pdf_document = None
        self.pdf_path = None
        self.current_page = 0

    def show_image(self, file_path):

        self.close_pdf()

        self.ids.preview_image.source = str(file_path)
        self.ids.preview_image.reload()

        self.ids.page_label.text = ""

        self.ids.previous_button.disabled = True
        self.ids.next_button.disabled = True

    def show_pdf(self, file_path):

        self.close_pdf()

        pdf_path = Path(file_path)

        if not pdf_path.exists():
            print("PDF NOT FOUND:", pdf_path)
            return

        try:
            self.pdf_document = fitz.open(str(pdf_path))
            self.pdf_path = pdf_path
            self.current_page = 0

            print("PDF pages:", self.pdf_document.page_count)

            self.show_pdf_page()

        except Exception as e:
            print("PDF ERROR:", e)

    def show_pdf_page(self):

        if not self.pdf_document:
            return

        page = self.pdf_document[self.current_page]

        pixmap = page.get_pixmap(
            dpi=150,
            colorspace=fitz.csRGB,
            alpha=False
        )

        preview_dir = (
            Path(__file__).resolve().parent.parent
            / "app_storage"
            / "previews"
        )

        preview_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        preview_path = (
            preview_dir /
            f"pdf_page_{self.current_page}.png"
        )

        pixmap.save(str(preview_path))

        self.ids.preview_image.source = ""
        self.ids.preview_image.source = str(preview_path)
        self.ids.preview_image.reload()

        total = self.pdf_document.page_count

        self.ids.page_label.text = (
            f"Page {self.current_page + 1} / {total}"
        )

        self.ids.previous_button.disabled = (
            self.current_page == 0
        )

        self.ids.next_button.disabled = (
            self.current_page == total - 1
        )

    def next_page(self):

        if not self.pdf_document:
            return

        if self.current_page < self.pdf_document.page_count - 1:

            self.current_page += 1

            self.show_pdf_page()

    def previous_page(self):

        if not self.pdf_document:
            return

        if self.current_page > 0:

            self.current_page -= 1

            self.show_pdf_page()

    def close_pdf(self):

        if self.pdf_document:

            self.pdf_document.close()

            self.pdf_document = None
            self.pdf_path = None