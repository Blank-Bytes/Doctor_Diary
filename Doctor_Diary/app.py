from services.choice_controller import ChoiceController
from services.model_manager import ModelManager
from services.user_interface import UserInterface


class App:
    """
    A class to manage the app running and dependencies.

    Attributes
    ----------
        model_manager: ModelManager
            Service for managing patients and appointments (Model)
        user_interface: UserInterface
            Service for user-app communication (View)
        choice_controller: ChoiceController
            Service for executing app functions based on user choices (Controller)


    ! WARNING !
    The app is hard-coded to read specified named and structured (JSON array) files.
    You shouldn't change the data/patients.json and data/appointments.json files.
    If the files are corrupted, create new 'patients.json' and 'appointments.json' files
    in the data directory and fill them only with '[]'.

    The app architecture tries to follow the MVC pattern.
    """

    def __init__(self):
        self.model_manager = ModelManager("data/patients.json",
                                          "data/appointments.json")
        self.user_interface = UserInterface()
        self.choice_controller = ChoiceController(self.model_manager, self.user_interface)
        self.start_app()

    def start_app(self):
        """Start and stop the app."""

        run_app = True
        while run_app:
            run_app = self.choice_controller.start()
