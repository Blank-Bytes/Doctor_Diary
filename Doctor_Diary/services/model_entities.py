class Patient:
    """
    A class that represents a patient.

    Attributes
    ----------
        number: str
            Personal Identification Number (number) of the patient
        firstname: str
            First name of the patient
        lastname: str
            Last name of the patient
    """

    def __init__(self, number, firstname, lastname):
        self.number = number
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return f"{self.firstname} {self.lastname},\tnumber: {self.number}"


class Appointment:
    """
    A class that represents an appointment.
    Every instance is related to the specified patient with a unique number.

    Attributes
    ----------
        patient_number: str
            Unique number of the appointed patient
        date: date
            Date of the appointment formatted as [YYYY-MM-DD]
        time: time
            Time of the appointment formatted as [HH:MM:SS]
        description: str
            Short description of the appointment
    """

    def __init__(self, patient_number, date, time, description):
        self.patient_number = patient_number
        self.date = date
        self.time = time
        self.description = description

    def __str__(self):
        return f"[{self.date}\t{self.time.strftime('%H:%M')}] \n\t{self.description}"
