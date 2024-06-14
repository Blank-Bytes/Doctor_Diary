import datetime
from enum import Enum


class Choice(Enum):
    """
    An Enum class to represent user choices in if/switch statements.

    Possible values:
        - EXIT: exit app
        - ADD_PATIENT: add new patient
        - ADD_APPOINTMENT: add new appointment for a registered patient
        - PRINT_PATIENTS: print all registered patients
        - PRINT_DAILY_APPOINTMENTS: print all appointments for the specified date [YYYY-MM-DD]
        - PRINT_PATIENT_APPOINTMENTS: print all appointments for the specified patient
        - DELETE_PATIENT: delete a registered patient
        - CANCEL_APPOINTMENT: cancel a booked appointment
        - PRINT_ALL_APPOINTMENTS: print all booked appointments in the app
    """

    EXIT = 0
    ADD_PATIENT = 1
    ADD_APPOINTMENT = 2
    PRINT_PATIENTS = 3
    PRINT_DAILY_APPOINTMENTS = 4
    PRINT_PATIENT_APPOINTMENTS = 5
    DELETE_PATIENT = 6
    CANCEL_APPOINTMENT = 7
    PRINT_ALL_APPOINTMENTS = 8


class UserInterface:
    """
    A class to represent the interface between the user and the controller.
    Send data from the user to the controller and display data on the console.

    Attributes
    ----------
        welcome: str
            welcome text printed on the console
        menu_choices: str
            menu text printed on the console
    """

    def __init__(self):
        self.welcome = """
        |=============================================|
        |             WELCOME TO THE APP!             |
        |         CHOOSE FROM AVAILABLE OPTIONS.      |
        |=============================================| """

        self.menu_choices = """
        |=============================================|
        | 1 |   ADD NEW PATIENT                        |
        | 2 |   SCHEDULE APPOINTMENT                   |
        | 3 |   DISPLAY ALL PATIENTS                   |
        | 4 |   DISPLAY APPOINTMENTS FOR A DATE        |
        | 5 |   DISPLAY APPOINTMENTS FOR A PATIENT     |
        | 6 |   DELETE A PATIENT                       |
        | 7 |   CANCEL AN APPOINTMENT                  |
        | 8 |   DISPLAY ALL APPOINTMENTS               |
        |---------------------------------------------|
        | 0 |   EXIT                                   |
        |=============================================|"""

    def print_welcome(self):
        """Print welcome text on the console."""

        print(self.welcome)

    def menu(self):
        """
        Display the menu interface to get user choice and return it as an enum Choice object.

        Returns:
            user_choice (Choice): enum object which represents user choice
        """

        print(self.menu_choices)
        user_choice = input("\nCHOOSE AN OPTION: ")
        user_choice = int(user_choice)
        return Choice(user_choice)

    def get_patient_number(self):
        """
        Display the interface to get the patient's number from the user.

        Returns:
            number (str): patient's number
        """

        number = input("\nPATIENT'S number: ")
        return number

    def get_patient_name(self):
        """
        Display the interface to get the patient's first name and last name from the user.

        Returns:
            name_tuple (str, str): patient's first name and last name in a tuple
        """

        firstname = input("PATIENT'S FIRST NAME: ")
        lastname = input("PATIENT'S LAST NAME: ")
        return firstname, lastname

    def get_date(self):
        """
        Display the interface to get the appointment date from the user.

        Returns:
            date (date): [YYYY-MM-DD] formatted date of the appointment
        """

        print("\nENTER APPOINTMENT DATE")
        year = int(input("YEAR [YYYY]: "))
        month = int(input("MONTH [MM]: "))
        day = int(input("DAY [DD]: "))
        date = datetime.date(year, month, day)
        return date

    def get_time(self):
        """
        Display the interface to get the appointment time from the user.

        Returns:
            time (time): [HH:MM:SS] formatted time of the appointment
        """

        print("\nENTER APPOINTMENT TIME: ")
        hour = int(input("HOUR [HH]: "))
        minute = int(input("MINUTE [MM]: "))
        time = datetime.time(hour, minute, 0)
        return time

    def get_appointment_description(self):
        """
        Display the interface to get the appointment description.

        Returns:
            description (str): description of the appointment
        """

        description = input("\nAPPOINTMENT DESCRIPTION: ")
        return description

    def print_patients(self, patients):
        """
        Print a list of patients received in the function argument.

        Arguments:
            patients (Patient[]): list of patients printed for the user
        """

        if len(patients) == 0:
            self.print_info("NO REGISTERED PATIENTS")
            return

        print("\nREGISTERED PATIENTS IN THE FACILITY: ")
        for patient in patients:
            print(patient)

    def print_appointments(self, appointments):
        """
        Print a list of appointments received in the function argument.

        Arguments:
            appointments (Appointment[]): list of appointments printed for the user
        """

        if len(appointments) == 0:
            self.print_info("NO SCHEDULED APPOINTMENTS")
            return

        print("\nSCHEDULED APPOINTMENTS: ")
        for appointment in appointments:
            print(appointment)

    def print_info(self, info: str):
        """Print extra information for the user."""

        print(f"[---{info.upper()}---]")
