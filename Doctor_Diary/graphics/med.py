import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QDateEdit, QTimeEdit, QTextEdit, QListWidget, QMessageBox, QWidget
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QPixmap
from enum import Enum

DATA_DIR = "data"
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.json")

class Choice(Enum):
    EXIT = 0
    ADD_PATIENT = 1
    ADD_APPOINTMENT = 2
    PRINT_PATIENTS = 3
    PRINT_DAILY_APPOINTMENTS = 4
    PRINT_PATIENT_APPOINTMENTS = 5
    DELETE_PATIENT = 6
    CANCEL_APPOINTMENT = 7
    PRINT_ALL_APPOINTMENTS = 8

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Appointment Scheduler")
        self.setGeometry(100, 100, 800, 600)

        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)

        # Ensure JSON files exist
        self.ensure_json_file(PATIENTS_FILE)
        self.ensure_json_file(APPOINTMENTS_FILE)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Set background image
        background_image = QLabel(self)
        pixmap = QPixmap("background_image.jpg")
        background_image.setPixmap(pixmap)
        background_image.setGeometry(0, 0, self.width(), self.height())

        # Welcome message
        welcome_label = QLabel("Welcome to the App!\nChoose from Available Options.", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet(
            "QLabel {"
            "   font-size: 20px;"
            "   font-weight: normal;"
            "   color: #333;"
            "   text-align: center;"
            "   background-color: rgba(255, 255, 255, 0.7);"  # Semi-transparent white background
            "   border-radius: 10px;"
            "   padding: 10px;"
            "}"
        )
        main_layout.addWidget(welcome_label)

        # Add the background image widget to the main layout
        main_layout.addWidget(background_image)

        # Buttons for each action
        action_buttons = [
            ("ADD NEW PATIENT", self.add_patient),
            ("SCHEDULE APPOINTMENT", self.add_appointment),
            ("DISPLAY ALL PATIENTS", self.show_patient_window),
            ("DISPLAY APPOINTMENTS FOR A DATE", self.show_daily_appointments_window),
            ("DISPLAY APPOINTMENTS FOR A PATIENT", self.show_patient_appointments_window),
            ("DELETE A PATIENT", self.delete_patient),
            ("CANCEL AN APPOINTMENT", self.cancel_appointment),
            ("DISPLAY ALL APPOINTMENTS", self.print_all_appointments),
            ("EXIT", self.close)
        ]
        for text, func in action_buttons:
            button = QPushButton(text)
            button.clicked.connect(func)
            button.setStyleSheet(
                "QPushButton {"
                "   background-color: #4CAF50;"
                "   border: none;"
                "   color: white;"
                "   padding: 15px 32px;"
                "   text-align: center;"
                "   text-decoration: none;"
                "   display: inline-block;"
                "   font-size: 16px;"
                "   margin: 4px 2px;"
                "   cursor: pointer;"
                "   border-radius: 8px;"
                "}"
                "QPushButton:hover {background-color: #45a049;}"
                "QPushButton:pressed {background-color: #39803d;}"
            )
            main_layout.addWidget(button)

        self.setCentralWidget(main_widget)


    def ensure_json_file(self, filepath):
        if not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                json.dump([], file)

    def read_json(self, filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def write_json(self, filepath, data):
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def add_patient(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Patient")

        layout = QVBoxLayout()

        first_name_label = QLabel("Patient's First Name:")
        layout.addWidget(first_name_label)
        self.first_name_input = QLineEdit()
        layout.addWidget(self.first_name_input)

        last_name_label = QLabel("Patient's Last Name:")
        layout.addWidget(last_name_label)
        self.last_name_input = QLineEdit()
        layout.addWidget(self.last_name_input)

        number_label = QLabel("Patient's NUMBER:")
        layout.addWidget(number_label)
        self.number_input = QLineEdit()
        layout.addWidget(self.number_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_patient(dialog))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_patient(self, dialog):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        number = self.number_input.text()

        patients = self.read_json(PATIENTS_FILE)
        if any(patient['number'] == number for patient in patients):
            QMessageBox.warning(self, "Error", "NUMBER already exists.")
            return

        patients.append({
            'first_name': first_name,
            'last_name': last_name,
            'number': number
        })
        self.write_json(PATIENTS_FILE, patients)
        QMessageBox.information(self, "Patient Added", f"Patient {first_name} {last_name} added successfully.")
        dialog.accept()

    def add_appointment(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Schedule Appointment")

        layout = QVBoxLayout()

        number_label = QLabel("Patient's NUMBER:")
        layout.addWidget(number_label)
        self.number_input = QLineEdit()
        layout.addWidget(self.number_input)

        date_label = QLabel("Appointment Date:")
        layout.addWidget(date_label)
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        time_label = QLabel("Appointment Time:")
        layout.addWidget(time_label)
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        layout.addWidget(self.time_input)
        description_label = QLabel("Appointment Description:")
        layout.addWidget(description_label)
        self.description_input = QTextEdit()
        layout.addWidget(self.description_input)

        save_button = QPushButton("Schedule")
        save_button.clicked.connect(lambda: self.save_appointment(dialog))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_appointment(self, dialog):
        number = self.number_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm:ss")
        description = self.description_input.toPlainText()

        patients = self.read_json(PATIENTS_FILE)
        if not any(patient['number'] == number for patient in patients):
            QMessageBox.warning(self, "Error", "Patient not found.")
            return

        appointments = self.read_json(APPOINTMENTS_FILE)
        appointments.append({
            'patient_number': number,
            'appointment_date': date,
            'appointment_time': time,
            'description': description
        })
        self.write_json(APPOINTMENTS_FILE, appointments)
        QMessageBox.information(self, "Appointment Scheduled", f"Appointment for {number} scheduled on {date} at {time}.")
        dialog.accept()

    def print_all_appointments(self):
        appointments = self.read_json(APPOINTMENTS_FILE)

        dialog = QDialog(self)
        dialog.setWindowTitle("All Appointments")

        layout = QVBoxLayout()
        if appointments:
            list_widget = QListWidget()
            for appt in appointments:
                number = appt['patient_number']
                date = appt['appointment_date']
                time = appt['appointment_time']
                description = appt['description']
                list_widget.addItem(f"NUMBER: {number}, Date: {date}, Time: {time}, Description: {description}")
            layout.addWidget(list_widget)
        else:
            layout.addWidget(QLabel("No scheduled appointments."))

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_patient_window(self):
        patients = self.read_json(PATIENTS_FILE)
        dialog = PatientDialog(patients)
        dialog.exec_()

    def show_daily_appointments_window(self):
        dialog = DailyAppointmentsDialog()
        dialog.exec_()

    def show_patient_appointments_window(self):
        dialog = PatientAppointmentsDialog()
        dialog.exec_()

    def delete_patient(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Patient")

        layout = QVBoxLayout()

        number_label = QLabel("Patient's NUMBER:")
        layout.addWidget(number_label)
        self.number_input = QLineEdit()
        layout.addWidget(self.number_input)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.remove_patient(dialog))
        layout.addWidget(delete_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def remove_patient(self, dialog):
        number = self.number_input.text()

        patients = self.read_json(PATIENTS_FILE)
        appointments = self.read_json(APPOINTMENTS_FILE)

        patients = [patient for patient in patients if patient['number'] != number]
        appointments = [appt for appt in appointments if appt['patient_number'] != number]

        self.write_json(PATIENTS_FILE, patients)
        self.write_json(APPOINTMENTS_FILE, appointments)

        QMessageBox.information(self, "Patient Deleted", f"Patient with NUMBER {number} and their appointments have been deleted.")
        dialog.accept()

    def cancel_appointment(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Cancel Appointment")

        layout = QVBoxLayout()

        number_label = QLabel("Patient's NUMBER:")
        layout.addWidget(number_label)
        self.number_input = QLineEdit()
        layout.addWidget(self.number_input)

        date_label = QLabel("Appointment Date:")
        layout.addWidget(date_label)
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        time_label = QLabel("Appointment Time (HH:MM:SS):")
        layout.addWidget(time_label)
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.time_input.setDisplayFormat("HH:mm:ss")  # Include seconds
        layout.addWidget(self.time_input)

        delete_button = QPushButton("Cancel Appointment")
        delete_button.clicked.connect(lambda: self.remove_appointment(dialog))
        layout.addWidget(delete_button)

        dialog.setLayout(layout)
        dialog.exec_()


    def remove_appointment(self, dialog):
        number = self.number_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm:ss")

        appointments = self.read_json(APPOINTMENTS_FILE)
        appointments = [appt for appt in appointments if not (appt['patient_number'] == number and appt['appointment_date'] == date and appt['appointment_time'] == time)]

        self.write_json(APPOINTMENTS_FILE, appointments)

        QMessageBox.information(self, "Appointment Canceled", f"Appointment for {number} on {date} at {time} has been canceled.")
        dialog.accept()

class PatientDialog(QDialog):
    def __init__(self, patients):
        super().__init__()
        self.setWindowTitle("Registered Patients")

        layout = QVBoxLayout()
        list_widget = QListWidget()

        if patients:
            for patient in patients:
                first_name = patient['first_name']
                last_name = patient['last_name']
                number = patient['number']
                list_widget.addItem(f"{first_name} {last_name}, NUMBER: {number}")
        else:
            list_widget.addItem("No registered patients.")

        layout.addWidget(list_widget)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    
class PatientAppointmentsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Patient")
        layout = QVBoxLayout()

        number_label = QLabel("Patient's NUMBER:")
        layout.addWidget(number_label)
        self.number_input = QLineEdit()
        layout.addWidget(self.number_input)

        fetch_button = QPushButton("Fetch Appointments")
        fetch_button.clicked.connect(self.show_patient_appointments)
        layout.addWidget(fetch_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def show_patient_appointments(self):
        number = self.number_input.text()
        appointments = UserInterface().read_json(APPOINTMENTS_FILE)
        patient_appointments = [appt for appt in appointments if appt['patient_number'] == number]

        appointment_dialog = QDialog(self)
        appointment_dialog.setWindowTitle(f"Appointments for {number}")

        layout = QVBoxLayout()
        if patient_appointments:
            list_widget = QListWidget()
            for appt in patient_appointments:
                date = appt['appointment_date']
                time = appt['appointment_time']
                description = appt['description']
                list_widget.addItem(f"Date: {date}, Time: {time}, Description: {description}")
            layout.addWidget(list_widget)
        else:
            layout.addWidget(QLabel("No appointments for this patient."))

        close_button = QPushButton("Close")
        close_button.clicked.connect(appointment_dialog.accept)
        layout.addWidget(close_button)

        appointment_dialog.setLayout(layout)
        appointment_dialog.exec_()
        self.accept()

        
class DailyAppointmentsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Date")

        layout = QVBoxLayout()

        date_label = QLabel("Appointment Date:")
        layout.addWidget(date_label)
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        fetch_button = QPushButton("Fetch Appointments")
        fetch_button.clicked.connect(self.show_appointments)
        layout.addWidget(fetch_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def show_appointments(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        appointments = UserInterface().read_json(APPOINTMENTS_FILE)
        daily_appointments = [appt for appt in appointments if appt['appointment_date'] == date]

        appointment_dialog = QDialog(self)
        appointment_dialog.setWindowTitle(f"Appointments on {date}")

        layout = QVBoxLayout()
        if daily_appointments:
            list_widget = QListWidget()
            for appt in daily_appointments:
                number = appt['patient_number']
                time = appt['appointment_time']
                description = appt['description']
                list_widget.addItem(f"NUMBER: {number}, Time: {time}, Description: {description}")
            layout.addWidget(list_widget)
        else:
            layout.addWidget(QLabel("No appointments for this date."))

        close_button = QPushButton("Close")
        close_button.clicked.connect(appointment_dialog.accept)
        layout.addWidget(close_button)

        appointment_dialog.setLayout(layout)
        appointment_dialog.exec_()
        self.accept()
        
def main():
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()