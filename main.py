import sys
import os
import h2o
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox,
                             QVBoxLayout, QWidget, QCalendarWidget, QHBoxLayout, QDialog,
                             QFileDialog, QMessageBox, QProgressBar)
from PyQt6.QtCore import QDate, Qt, QTimer, QPoint
from PyQt6.QtGui import QColor, QFont, QPainter, QLinearGradient, QMouseEvent


class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setFixedSize(300, 100)
        layout = QVBoxLayout(self)

        self.label = QLabel("Loading...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)  # Update every 30 ms

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #16e0bd;
                font-size: 16px;
            }
            QProgressBar {
                border: 2px solid #16e0bd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #16e0bd;
            }
        """)

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.progress_bar.setValue(0)


# Initialize H2O
try:
    h2o.init()
    best_model = h2o.get_model('Grid_GBM_Key_Frame__upload_844656a837ea4e0ab84a8aa29bbb4832.hex_model_python_1724201234848_21_model_72')
except Exception as e:
    best_model = None
    print(f"Error loading model: {e}")


def load_hospital_levels(filename='hospital_levels.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return ['Sons and Miller', 'Kim Inc', 'Cook PLC', 'and Williams, Brown Mckenzie', 'Moreno Murphy, Griffith and']


# Load hospital levels
hospital_levels = load_hospital_levels()


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)
        self.calendar.clicked.connect(self.accept)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout(self)

        title_label = QLabel("Patient Risk Predictor")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)

        info_label = QLabel("Programmer: Ahmed Atef\nUnder supervised: Abd Elrahman Yehiya")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Risk Predictor")
        self.setGeometry(100, 100, 400, 800)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add close button
        self.close_button = QPushButton("X", self)
        self.close_button.setGeometry(370, 10, 20, 20)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)

        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

        QTimer.singleShot(2000, self.initialize_ui)  # Simulate loading time

        # Variables for dragging
        self.dragging = False
        self.offset = QPoint()

    def initialize_ui(self):
        self.loading_dialog.close()
        self.init_ui()

    def init_ui(self):
        self.add_input_fields()
        self.add_predict_button()
        self.add_result_label()
        self.add_about_button()

        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #1a1a2e;
                font-family: Arial, sans-serif;
            }
            QLineEdit, QComboBox {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 5px;
                padding: 5px;
                color: white;
                min-height: 25px;
            }
            QPushButton {
                background-color: #0f3460;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #1f5c8a;
            }
            QLabel {
                color: white;
            }
            #test_result_label {
                color: black;
            }
        """

    def add_input_fields(self):
        fields = [
            ("name_input", "Enter Patient Name", QLineEdit),
            ("age_input_field", "Enter Age", QLineEdit),
            ("gender_dropdown", "Select Gender", QComboBox, ['Male', 'Female']),
            ("blood_type_dropdown", "Select Blood Type", QComboBox, ['B-', 'A+', 'A-', 'O+', 'AB+', 'AB-', 'B+', 'O-']),
            ("medical_condition_dropdown", "Select Medical Condition", QComboBox, ['Cancer', 'Obesity', 'Diabetes', 'Asthma', 'Hypertension', 'Arthritis']),
            ("doctor_dropdown", "Select Doctor", QComboBox, ['Matthew Smith', 'Samantha Davies', 'Tiffany Mitchell', 'Deborah Sutton', 'Mary Bartlett', 'Alec May']),
            ("hospital_dropdown", "Select Hospital", QComboBox, hospital_levels),
            ("insurance_provider_dropdown", "Select Insurance Provider", QComboBox, ['Blue Cross', 'Medicare', 'Aetna', 'UnitedHealthcare', 'Cigna']),
            ("billing_amount_field", "Enter Billing Amount", QLineEdit),
            ("room_number_field", "Enter Room Number", QLineEdit),
            ("admission_type_dropdown", "Select Admission Type", QComboBox, ['Urgent', 'Emergency', 'Elective']),
            ("discharge_date_input", "Discharge Date", QLineEdit),
            ("medication_dropdown", "Select Medication", QComboBox, ['Paracetamol', 'Ibuprofen', 'Aspirin', 'Penicillin', 'Lipitor'])
        ]

        for field_name, placeholder, widget_type, *args in fields:
            layout = QHBoxLayout()
            widget = widget_type()
            setattr(self, field_name, widget)

            if isinstance(widget, QLineEdit):
                widget.setPlaceholderText(placeholder)
            elif isinstance(widget, QComboBox):
                widget.addItems(args[0])
                widget.setCurrentText(placeholder)

            layout.addWidget(widget)

            if "date" in field_name.lower():
                date_button = QPushButton("Select Date")
                date_button.clicked.connect(lambda _, w=widget: self.show_calendar(w))
                layout.addWidget(date_button)

            self.layout.addLayout(layout)

    def add_predict_button(self):
        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.predict_result)
        self.layout.addWidget(self.predict_button)

    def add_result_label(self):
        self.test_result_label = QLabel("Test Result:")
        self.test_result_label.setObjectName("test_result_label")
        self.layout.addWidget(self.test_result_label)

    def add_about_button(self):
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        self.layout.addWidget(self.about_button)

    def show_calendar(self, target_input):
        calendar_dialog = CalendarDialog(self)
        if calendar_dialog.exec():
            selected_date = calendar_dialog.calendar.selectedDate()
            target_input.setText(selected_date.toString("yyyy-MM-dd"))

    def predict_result(self):
        if best_model is None:
            QMessageBox.critical(self, "Error", "Model could not be loaded. Please check the model path.")
            return

        self.loading_dialog.label.setText("Predicting...")
        self.loading_dialog.progress_bar.setValue(0)
        self.loading_dialog.show()

        QTimer.singleShot(100, self.perform_prediction)

    def perform_prediction(self):
        # Collecting data from GUI input fields
        user_input = {
            'Age': self.age_input_field.text(),
            'Gender': self.gender_dropdown.currentText(),
            'Blood Type': self.blood_type_dropdown.currentText(),
            'Medical Condition': self.medical_condition_dropdown.currentText(),
            'Doctor': self.doctor_dropdown.currentText(),
            'Hospital': self.hospital_dropdown.currentText(),
            'Insurance Provider': self.insurance_provider_dropdown.currentText(),
            'Billing Amount': self.billing_amount_field.text(),
            'Room Number': self.room_number_field.text(),
            'Admission Type': self.admission_type_dropdown.currentText(),
            'Discharge Date': self.discharge_date_input.text(),
            'Medication': self.medication_dropdown.currentText(),
        }

        # Convert to a DataFrame
        import pandas as pd
        user_input_df = pd.DataFrame([user_input])

        try:
            # Convert to H2OFrame
            input_h2o_frame = h2o.H2OFrame(user_input_df)

            # Predict using the loaded model
            prediction = best_model.predict(input_h2o_frame)
            predicted_category = prediction['predict'][0, 0]  # Get the predicted category
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {e}")
            self.loading_dialog.close()
            return

        # Determine danger level based on the predicted category
        if predicted_category == 'Normal':
            color = QColor(0, 255, 0)  # Green
            danger_level = "Low"
        elif predicted_category == 'Moderate':
            color = QColor(255, 255, 0)  # Yellow
            danger_level = "Moderate"
        else:  # Assuming 'High' or any other category
            color = QColor(255, 0, 0)  # Red
            danger_level = "High"

        # Display the prediction result in the GUI
        result_text = f"Patient: {self.name_input.text()}\nPredicted Category: {predicted_category}\nDanger Level: {danger_level}"
        self.test_result_label.setText(result_text)
        self.test_result_label.setStyleSheet(f"background-color: {color.name()}; padding: 10px;")

        self.loading_dialog.close()

    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.move(self.mapToGlobal(event.position().toPoint() - self.offset))

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(26, 26, 46))
        gradient.setColorAt(1, QColor(15, 52, 96))
        painter.fillRect(self.rect(), gradient)


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
