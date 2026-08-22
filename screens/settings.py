from kivymd.uix.screen import MDScreen

from services.security import (
    lock_enabled,
    set_lock_enabled,
    pin_exists
)


class SettingsScreen(MDScreen):

    def on_pre_enter(self, *args):

        self.ids.lock_switch.active = lock_enabled()

    def toggle_lock(self, enabled):

        if enabled:

            if not pin_exists():

                self.ids.lock_switch.active = False
                self.manager.current = "lock"

                return

            set_lock_enabled(True)

        else:

            set_lock_enabled(False)

        print("Lock enabled:", enabled)