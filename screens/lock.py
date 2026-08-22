from kivymd.uix.screen import MDScreen

from services.security import (
    pin_exists,
    set_pin,
    verify_pin
)


class LockScreen(MDScreen):

    def on_pre_enter(self, *args):

        if pin_exists():

            self.ids.title.text = "Unlock DocVault"
            self.ids.pin_field.hint_text = "Enter PIN"
            self.ids.action_button.text = "UNLOCK"

        else:

            self.ids.title.text = "Create PIN"
            self.ids.pin_field.hint_text = "Create 4-digit PIN"
            self.ids.action_button.text = "SAVE PIN"

        self.ids.pin_field.text = ""
        self.ids.error_label.text = ""

    def process_pin(self):

        pin = self.ids.pin_field.text.strip()

        if len(pin) != 4 or not pin.isdigit():

            self.ids.error_label.text = "PIN must be 4 digits"
            return

        if pin_exists():

            if verify_pin(pin):

                self.ids.error_label.text = ""
                self.manager.current = "home"

            else:

                self.ids.error_label.text = "Incorrect PIN"

        else:

            set_pin(pin)

            self.ids.error_label.text = ""

            self.manager.current = "home"