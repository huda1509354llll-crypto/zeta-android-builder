"""Zeta App - Python Android Application built with BeeWare"""

import toga

def main():
    app = toga.App("Zeta App", "com.zeta.androidapp")

    def startup(app):
        main_window = toga.MainWindow(title="Zeta App")
        main_window.app = app

        # Create main box container
        main_box = toga.Box(style=Pack(flex=1, direction=COLUMN, padding=20))

        # Title label
        title = toga.Label(
            "🚀 Zeta Python Android App",
            style=Pack(font_size=24, padding_bottom=10)
        )

        # Description
        desc = toga.Label(
            "Aplikasi dibuat dengan Python + BeeWare",
            style=Pack(font_size=16, padding_bottom=20)
        )

        # Button with handler
        def say_hello(widget):
            main_window.info_dialog("Hello!", "Tombol berhasil ditekan! 🎉")

        button = toga.Button(
            "Klik Saya!",
            on_press=say_hello,
            style=Pack(padding=10)
        )

        # Status
        status = toga.Label(
            "Status: App berjalan sempurna ✅",
            style=Pack(font_size=12, padding_top=20)
        )

        # Add widgets
        main_box.add(title)
        main_box.add(desc)
        main_box.add(button)
        main_box.add(status)

        main_window.content = main_box
        main_window.show()

    app.startup = startup
    return app
