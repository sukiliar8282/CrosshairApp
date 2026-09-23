import sys
import ctypes
import json
import os

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QFont, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QColorDialog,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)


class ColorSettings(QWidget):

    def __init__(self, crosshair):
        super().__init__()

        self.crosshair = crosshair

        self.setWindowTitle("Crosshair Settings")
        self.setFixedSize(320, 180)
        self.setWindowFlag(
            Qt.WindowType.WindowStaysOnTopHint
        )

        title = QLabel("Crosshair Color")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.color_label = QLabel("Current Color")
        self.color_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.update_color_preview()

        self.pick_button = QPushButton(
            "Choose Color"
        )
        self.pick_button.clicked.connect(
            self.choose_color
        )

        self.close_button = QPushButton(
            "Close"
        )
        self.close_button.clicked.connect(
            self.close
        )

        button_layout = QHBoxLayout()
        button_layout.addWidget(
            self.pick_button
        )
        button_layout.addWidget(
            self.close_button
        )

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.color_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_color_preview(self):
        self.color_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {
                self.crosshair.crosshair_color
            };
                color: black;
                border: 1px solid white;
                padding: 15px;
                font-weight: bold;
            }}
            """
        )

        self.color_label.setText(
            self.crosshair.crosshair_color
        )

    def choose_color(self):
        current_color = QColor(
            self.crosshair.crosshair_color
        )

        color = QColorDialog.getColor(
            current_color,
            self,
            "Choose Crosshair Color"
        )

        if color.isValid():
            self.crosshair.set_color(
                color.name()
            )

            self.update_color_preview()


class ShortcutGuide(QWidget):

    def __init__(self, crosshair):
        super().__init__()

        self.crosshair = crosshair

        self.setFixedSize(250, 220)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.move_to_top_right()

        # Tombol X
        self.close_button = QPushButton(
            "×",
            self
        )

        self.close_button.setFixedSize(
            28,
            28
        )

        self.close_button.move(
            self.width() - 34,
            5
        )

        self.close_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 210);
                border: none;
                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:hover {
                color: white;
                background-color: rgba(255, 70, 70, 150);
                border-radius: 6px;
            }
            """
        )

        self.close_button.clicked.connect(
            self.close_application
        )

    def move_to_top_right(self):
        screen = QApplication.primaryScreen()
        geometry = screen.geometry()

        margin = 20

        x = (
            geometry.x()
            + geometry.width()
            - self.width()
            - margin
        )

        y = (
            geometry.y()
            + margin
        )

        self.move(x, y)

    def close_application(self):
        QApplication.quit()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # Background
        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QColor(15, 15, 15, 185)
        )

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            12,
            12
        )

        # Border
        painter.setPen(
            QPen(
                QColor(255, 255, 255, 45),
                1
            )
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawRoundedRect(
            0,
            0,
            self.width() - 1,
            self.height() - 1,
            12,
            12
        )

        # Title
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)

        painter.setFont(title_font)

        painter.setPen(
            QColor(255, 255, 255, 230)
        )

        painter.drawText(
            15,
            28,
            "CROSSHAIR SHORTCUT"
        )

        # Shortcut text
        text_font = QFont()
        text_font.setPointSize(9)

        painter.setFont(text_font)

        shortcuts = [
            ("F6", "Show / Hide Guide"),
            ("F7", "Crosshair Color"),
            ("F8", "Edit Mode"),
            ("Shift + Alt + 1", "Model 1"),
            ("Shift + Alt + 2", "Model 2"),
            ("Shift + Alt + 3", "Model 3"),
            ("Shift + Alt + 4", "Model 4"),
            ("+ / −", "Change Size"),
        ]

        y = 55

        for key, description in shortcuts:

            painter.setPen(
                QColor(255, 255, 255, 235)
            )

            painter.drawText(
                15,
                y,
                key
            )

            painter.setPen(
                QColor(200, 200, 200, 210)
            )

            painter.drawText(
                105,
                y,
                description
            )

            y += 20


class CrosshairOverlay(QWidget):

    def __init__(self):
        super().__init__()

        screen = QApplication.primaryScreen()
        geometry = screen.geometry()

        self.setGeometry(geometry)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.crosshair_x = (
            geometry.width() // 2
        )

        self.crosshair_y = (
            geometry.height() // 2
        )

        self.size = 20

        self.min_size = 5
        self.max_size = 100

        self.crosshair_style = 1
        self.crosshair_color = "#ff0000"

        self.edit_mode = False
        self.dragging = False

        self.show_status = False
        self.status_text = ""

        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)

        self.status_timer.timeout.connect(
            self.hide_status
        )

        self.color_settings = None

        self.last_keys = set()

        self.hotkey_timer = QTimer()
        self.hotkey_timer.timeout.connect(
            self.check_hotkeys
        )

        self.hotkey_timer.start(30)

        self.load_settings()

        # Selalu kembali ke tengah saat aplikasi dibuka
        self.crosshair_x = (
            geometry.width() // 2
        )

        self.crosshair_y = (
            geometry.height() // 2
        )

        # Crosshair normal click-through
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        # Shortcut Guide
        self.shortcut_guide = ShortcutGuide(
            self
        )

        self.shortcut_guide.show()

    def get_config_path(self):
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(
                sys.executable
            )
        else:
            base_path = os.path.dirname(
                os.path.abspath(__file__)
            )

        return os.path.join(
            base_path,
            "config.json"
        )

    def save_settings(self):
        settings = {
            "crosshair_x": self.crosshair_x,
            "crosshair_y": self.crosshair_y,
            "size": self.size,
            "crosshair_style": self.crosshair_style,
            "crosshair_color": self.crosshair_color
        }

        try:
            with open(
                self.get_config_path(),
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    settings,
                    file,
                    indent=4
                )

        except Exception as e:
            print(
                "Gagal menyimpan settings:",
                e
            )

    def load_settings(self):
        config_path = self.get_config_path()

        if not os.path.exists(config_path):
            return

        try:
            with open(
                config_path,
                "r",
                encoding="utf-8"
            ) as file:

                settings = json.load(file)

            self.crosshair_x = int(
                settings.get(
                    "crosshair_x",
                    self.crosshair_x
                )
            )

            self.crosshair_y = int(
                settings.get(
                    "crosshair_y",
                    self.crosshair_y
                )
            )

            self.size = int(
                settings.get(
                    "size",
                    self.size
                )
            )

            self.crosshair_style = int(
                settings.get(
                    "crosshair_style",
                    self.crosshair_style
                )
            )

            self.crosshair_color = settings.get(
                "crosshair_color",
                self.crosshair_color
            )

            self.size = max(
                self.min_size,
                min(
                    self.size,
                    self.max_size
                )
            )

            if self.crosshair_style not in (
                1,
                2,
                3,
                4
            ):
                self.crosshair_style = 1

            test_color = QColor(
                self.crosshair_color
            )

            if not test_color.isValid():
                self.crosshair_color = "#ff0000"

        except Exception as e:
            print(
                "Gagal membaca settings:",
                e
            )

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        pen = QPen(
            QColor(self.crosshair_color)
        )

        pen.setWidth(3)

        painter.setPen(pen)

        x = int(self.crosshair_x)
        y = int(self.crosshair_y)
        size = int(self.size)

        # Model 1 - Plus
        if self.crosshair_style == 1:

            painter.drawLine(
                x - size,
                y,
                x + size,
                y
            )

            painter.drawLine(
                x,
                y - size,
                x,
                y + size
            )

        # Model 2 - T
        elif self.crosshair_style == 2:

            painter.drawLine(
                x - size,
                y,
                x + size,
                y
            )

            painter.drawLine(
                x,
                y,
                x,
                y + size
            )

        # Model 3 - Dot
        elif self.crosshair_style == 3:

            dot_size = max(
                2,
                int(size * 0.25)
            )

            painter.drawEllipse(
                x - dot_size,
                y - dot_size,
                dot_size * 2,
                dot_size * 2
            )

        # Model 4 - Circle + Dot
        elif self.crosshair_style == 4:

            circle_size = size

            painter.drawEllipse(
                x - circle_size,
                y - circle_size,
                circle_size * 2,
                circle_size * 2
            )

            dot_size = max(
                2,
                int(size * 0.2)
            )

            painter.drawEllipse(
                x - dot_size,
                y - dot_size,
                dot_size * 2,
                dot_size * 2
            )

        # Status Edit Mode
        if self.show_status:

            font = QFont()
            font.setPointSize(12)
            font.setBold(True)

            painter.setFont(font)

            if self.edit_mode:
                painter.setPen(
                    Qt.GlobalColor.green
                )
            else:
                painter.setPen(
                    Qt.GlobalColor.red
                )

            painter.drawText(
                20,
                35,
                self.status_text
            )

    def mousePressEvent(self, event):
        if not self.edit_mode:
            return

        if event.button() == (
            Qt.MouseButton.LeftButton
        ):

            self.dragging = True

            self.crosshair_x = int(
                event.position().x()
            )

            self.crosshair_y = int(
                event.position().y()
            )

            self.save_settings()

            self.update()

    def mouseMoveEvent(self, event):
        if not self.edit_mode:
            return

        if self.dragging:

            self.crosshair_x = int(
                event.position().x()
            )

            self.crosshair_y = int(
                event.position().y()
            )

            self.save_settings()

            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == (
            Qt.MouseButton.LeftButton
        ):

            self.dragging = False

            self.save_settings()

    def set_color(self, color):
        self.crosshair_color = color

        self.save_settings()

        self.update()

        print(
            f"Crosshair color: {color}"
        )

    def open_color_settings(self):
        if self.color_settings is None:
            self.color_settings = ColorSettings(
                self
            )

        self.color_settings.update_color_preview()

        self.color_settings.show()

        self.color_settings.raise_()

        self.color_settings.activateWindow()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

        self.dragging = False

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            not self.edit_mode
        )

        self.show_status = True

        if self.edit_mode:
            self.status_text = "EDIT MODE: ON"
        else:
            self.status_text = "EDIT MODE: OFF"

        self.status_timer.start(2000)

        self.update()

        print(
            self.status_text
        )

    def toggle_shortcut_guide(self):
        if self.shortcut_guide.isVisible():

            self.shortcut_guide.hide()

            print(
                "Shortcut Guide: HIDDEN"
            )

        else:

            self.shortcut_guide.move_to_top_right()

            self.shortcut_guide.show()

            self.shortcut_guide.raise_()

            print(
                "Shortcut Guide: SHOWN"
            )

    def hide_status(self):
        self.show_status = False

        self.update()

    def check_hotkeys(self):
        VK_SHIFT = 0x10
        VK_ALT = 0x12

        keys = {
            0x75: "guide",   # F6
            0x76: "color",   # F7
            0x77: "edit",    # F8

            0x31: 1,
            0x32: 2,
            0x33: 3,
            0x34: 4,

            0xBB: "plus",
            0x6B: "plus",

            0xBD: "minus",
            0x6D: "minus",
        }

        current_keys = set()

        shift_pressed = bool(
            ctypes.windll.user32.GetAsyncKeyState(
                VK_SHIFT
            ) & 0x8000
        )

        alt_pressed = bool(
            ctypes.windll.user32.GetAsyncKeyState(
                VK_ALT
            ) & 0x8000
        )

        for vk, action in keys.items():

            if (
                ctypes.windll.user32.GetAsyncKeyState(
                    vk
                ) & 0x8000
            ):

                current_keys.add(vk)

                if vk not in self.last_keys:

                    # F6
                    if action == "guide":

                        self.toggle_shortcut_guide()

                    # F7
                    elif action == "color":

                        self.open_color_settings()

                    # F8
                    elif action == "edit":

                        self.toggle_edit_mode()

                    # Model
                    elif action in (
                        1,
                        2,
                        3,
                        4
                    ):

                        if (
                            shift_pressed
                            and alt_pressed
                        ):

                            self.crosshair_style = action

                            self.save_settings()

                            print(
                                f"Crosshair model: {action}"
                            )

                    # Size +
                    elif action == "plus":

                        self.size += 5

                        if self.size > self.max_size:
                            self.size = self.max_size

                        self.save_settings()

                    # Size -
                    elif action == "minus":

                        self.size -= 5

                        if self.size < self.min_size:
                            self.size = self.min_size

                        self.save_settings()

                    self.update()

        self.last_keys = current_keys


app = QApplication(sys.argv)

app.setQuitOnLastWindowClosed(False)

window = CrosshairOverlay()

window.show()

sys.exit(app.exec())
