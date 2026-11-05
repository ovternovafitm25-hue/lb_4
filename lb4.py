from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QCheckBox,
    QRadioButton, QSlider, QSpinBox, QProgressBar,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
    QFileDialog, QInputDialog, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
import sys

class InputWidget(QWidget):

    textSent = pyqtSignal(str)
    valueSent = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введіть текст")

        self.spin = QSpinBox()
        self.spin.setRange(0, 100)

        self.send_button = QPushButton("Надіслати")

        layout.addWidget(self.line_edit)
        layout.addWidget(self.spin)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_data)

    def send_data(self):
        self.textSent.emit(self.line_edit.text())
        self.valueSent.emit(
            self.spin.value(),
            self.line_edit.text()
        )


class DisplayWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("Очікування даних...")
        self.label.setWordWrap(True)

        layout.addWidget(self.label)

        self.setLayout(layout)

    def show_text(self, text):
        self.label.setText(f"Текст: {text}")

    def show_complex(self, value, text):
        self.label.setText(
            f"Число: {value}\nТекст: {text}"
        )

class CustomDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Власний діалог")

        layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.age_spin = QSpinBox()

        self.age_spin.setRange(1, 120)

        layout.addRow("Ім'я:", self.name_edit)
        layout.addRow("Вік:", self.age_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return self.name_edit.text(), self.age_spin.value()


def simple_slot():
    print("Виконано звичайну функцію-слот")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лабораторна робота PyQt6")
        self.setMinimumSize(900, 700)

        self.create_widgets()
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.apply_styles()

    def create_widgets(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.label = QLabel("Введіть дані")
        self.label.setToolTip("Інформаційна мітка")

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Ваше ім'я")

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Коментар")

        self.combo = QComboBox()
        self.combo.addItems([
            "Python",
            "Java",
            "C++"
        ])

        self.checkbox = QCheckBox(
            "Погоджуюся з умовами"
        )

        self.radio = QRadioButton(
            "Отримувати повідомлення"
        )

        self.slider = QSlider(
            Qt.Orientation.Horizontal
        )
        self.slider.setRange(0, 100)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(18, 100)
        self.spinbox.setValue(18)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.result_label = QLabel("Результат")

        self.confirm_button = QPushButton(
            "Підтвердити"
        )

        self.reset_button = QPushButton(
            "Скинути"
        )

        self.confirm_button.setEnabled(False)

        form_layout.addRow("Ім'я:", self.line_edit)
        form_layout.addRow("Вік:", self.spinbox)
        form_layout.addRow("Мова:", self.combo)
        form_layout.addRow("Коментар:", self.text_edit)

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.confirm_button
        )

        button_layout.addWidget(
            self.reset_button
        )

        main_layout.addWidget(self.label)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.checkbox)
        main_layout.addWidget(self.radio)
        main_layout.addWidget(self.slider)
        main_layout.addWidget(self.progress)
        main_layout.addWidget(self.result_label)
        main_layout.addLayout(button_layout)

        self.input_component = InputWidget()
        self.display_component = DisplayWidget()

        main_layout.addWidget(
            self.input_component
        )

        main_layout.addWidget(
            self.display_component
        )

        central.setLayout(main_layout)

        self.line_edit.textChanged.connect(
            self.update_name
        )

        self.slider.valueChanged.connect(
            self.progress.setValue
        )

        self.slider.valueChanged.connect(
            lambda value:
            self.result_label.setText(
                f"Повзунок: {value}"
            )
        )

        self.combo.currentTextChanged.connect(
            simple_slot
        )

        self.checkbox.stateChanged.connect(
            self.toggle_button
        )

        self.confirm_button.clicked.connect(
            self.validate_data
        )

        self.reset_button.clicked.connect(
            self.reset_form
        )

        self.input_component.textSent.connect(
            self.display_component.show_text
        )

        self.input_component.valueSent.connect(
            self.display_component.show_complex
        )

    def create_menu(self):

        file_menu = self.menuBar().addMenu("Файл")

        open_action = QAction(
            "Відкрити",
            self
        )

        open_action.setShortcut("Ctrl+O")

        about_action = QAction(
            "Про програму",
            self
        )

        about_action.setShortcut("Ctrl+A")

        exit_action = QAction(
            "Вихід",
            self
        )

        exit_action.setShortcut("Ctrl+Q")

        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu(
            "Довідка"
        )

        help_menu.addAction(about_action)

        input_action = QAction(
            "Ввести дані",
            self
        )

        help_menu.addAction(input_action)

        open_action.triggered.connect(
            self.open_file
        )

        about_action.triggered.connect(
            self.show_about
        )

        exit_action.triggered.connect(
            self.close
        )

        input_action.triggered.connect(
            self.show_input_dialog
        )

        self.open_action = open_action
        self.about_action = about_action

    def create_toolbar(self):

        toolbar = self.addToolBar(
            "Основна панель"
        )

        toolbar.addAction(
            self.open_action
        )

        toolbar.addAction(
            self.about_action
        )

    def create_statusbar(self):

        self.statusBar().showMessage(
            "Готово"
        )

    def update_name(self, text):

        self.label.setText(
            f"Користувач: {text}"
        )

        self.statusBar().showMessage(
            f"Символів: {len(text)}"
        )

    def toggle_button(self, state):

        self.confirm_button.setEnabled(
            state == 2
        )

    def validate_data(self):

        if not self.line_edit.text().strip():

            QMessageBox.warning(
                self,
                "Помилка",
                "Введіть ім'я"
            )

            return

        if self.spinbox.value() < 18:

            QMessageBox.warning(
                self,
                "Помилка",
                "Мінімальний вік 18 років"
            )

            return

        self.result_label.setText(
            "Дані коректні"
        )

    def reset_form(self):

        self.line_edit.clear()
        self.text_edit.clear()
        self.combo.setCurrentIndex(0)
        self.checkbox.setChecked(False)
        self.radio.setChecked(False)
        self.slider.setValue(0)
        self.spinbox.setValue(18)
        self.progress.setValue(0)

    def open_file(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Вибір файлу"
        )

        if file_name:
            self.statusBar().showMessage(
                f"Відкрито: {file_name}"
            )

    def show_about(self):

        QMessageBox.about(
            self,
            "Про програму",
            "Лабораторна робота PyQt6"
        )

    def show_input_dialog(self):

        text, ok = QInputDialog.getText(
            self,
            "Введення",
            "Введіть текст:"
        )

        if ok:
            self.result_label.setText(text)

    def open_custom_dialog(self):

        dialog = CustomDialog()

        if dialog.exec():

            name, age = dialog.get_data()

            self.result_label.setText(
                f"{name}, {age}"
            )

    def apply_styles(self):

        self.setStyleSheet("""

        QLabel {
            font-size: 14px;
            color: navy;
        }

        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #45a049;
        }

        QPushButton:pressed {
            background-color: #2e7d32;
        }

        QLineEdit {
            border: 2px solid gray;
            padding: 4px;
        }

        QLineEdit:focus {
            border: 2px solid blue;
        }

        #specialLabel {
            color: red;
            font-weight: bold;
        }

        """)


app = QApplication(sys.argv)

window = MainWindow()

window.input_component.blockSignals(True)
window.input_component.blockSignals(False)

window.show()

sys.exit(app.exec())
