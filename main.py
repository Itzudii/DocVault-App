from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from services.security import lock_enabled
from screens.home import HomeScreen
from screens.add_document import AddDocumentScreen
from screens.image_preview import ImagePreviewScreen
from screens.lock import LockScreen
from screens.settings import SettingsScreen


Window.clearcolor = (0.05, 0.05, 0.07, 1)


class DocVaultApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"

        Builder.load_file("kv/home.kv")
        Builder.load_file("kv/add_document.kv")
        Builder.load_file("kv/image_preview.kv")
        Builder.load_file("kv/lock.kv")
        Builder.load_file("kv/settings.kv")
        sm = MDScreenManager()

        sm.add_widget(HomeScreen())
        sm.add_widget(AddDocumentScreen())
        sm.add_widget(ImagePreviewScreen())
        sm.add_widget(LockScreen())
        sm.add_widget(SettingsScreen())
        if lock_enabled():
            sm.current = "lock"
        else:
            sm.current = "home"
                
        return sm


DocVaultApp().run()