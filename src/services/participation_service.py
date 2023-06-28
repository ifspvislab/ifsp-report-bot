"""Service regarding input issues"""

from datetime import date
from uuid import uuid4

from data import Participation
from data.participation_data import ParticipationData
from data.projects_data import ProjectData
from data.students_data import StudentData


class InputAlreadyExists(Exception):
    """
    Class regarding the error when the input already exists.
    """

    print(Exception)


class StudentError(Exception):
    """
    Class regarding the error when the student isn't in the database.
    """

    print(Exception)


class ProjectError(Exception):
    """
    Class regarding the error when the project isn't in the database.
    """

    print(Exception)


class DateError(Exception):
    """
    Class regarding the error when the date inputed is invalid.
    """

    print(Exception)


class RegistrationError(Exception):
    """
    Class regarding the error when the registration is invalid.
    """

    print(Exception)


class ParticipationService:
    """
    A service for managing participations.
    """

    def __init__(self, participation_data: ParticipationData) -> None:
        self.database = []
        self.participation_data = participation_data
        self.student_data = StudentData
        self.project_data = ProjectData

    def find_participation_by_discord_id(self, discord_id: int) -> list | None:
        """
        Find a participation in the database with the user discord ID.

        :param discord_id: The discord ID of the user.
        :return: The participation of the student.
        :rtype: Dataclass
        """

        students = self.student_data.load_students(self)
        if not self.database:
            self.database = self.participation_data.load_participations(self)

        for participation in self.database:
            for student in students:
                if int(student.discord_id) == discord_id:
                    if participation.registration == student.registration:
                        student_participations = list[participation]
                        return student_participations
                    break
                break
        return None

    def date_validation(self, value):
        """
        Validates the input of date.

        :param value: The date to be verified.
        :raises DateError: If the date is invalid.
        """

        input_date = date(int(value.year), int(value.month), int(value.day))
        for project in self.project_data.load_projects(self):
            referencial_date = project.start_date
            final_date = project.final_date
            if input_date < referencial_date:
                raise DateError(
                    "A data inserida é inválida, pois é anterior ao início do projeto."
                )

            if final_date < input_date:
                raise DateError(
                    "A data inserida é inválida, pois é após o fim do projeto."
                )

    def project_validation(self, value):
        """
        Validates the input of the project.
        :param value: The project name inputed.
        :raises ProjectError: If the project doesn't exists.
        """

        for project in self.project_data.load_projects(self):
            if str(value) != project.title:
                raise ProjectError("O projeto inserido inexiste nos registros.")

    def student_validation(self, value):
        """
        Validates the input of the student.
        :param value: The student registration inputed.
        :raises StudentError: If the student isn't in the database.
        """
        for student in self.student_data.load_students(self):
            if str(value) != student.registration:
                raise StudentError("O aluno inserido inexiste nos registros.")

    def modal_input_verification(self, value, _value):
        """
        Verifies if the participation already exists in the database.
        :param value: The project name inputed.
        :param _value: The student registration inputed.
        :raises InputAlreadyExists: If the participation already exists.
        """

        for project in self.project_data.load_projects(self):
            for participation in self.participation_data.load_participations(self):
                if value == project.title and _value == participation.registration:
                    raise InputAlreadyExists(
                        "O aluno já está registrado nesse projeto."
                    )
                break

    def registration_validation(self, value: str):
        """
        Verifies if the registration is valid.
        :param value: The registration to be verified.
        :type value: str
        :raises RegistrationError: If the registration is incorrect.
        """

        if not (
            value[:1].isalpha()
            and value[2:-2].isnumeric()
            and value[-1].isalnum()
            and value[:1] == "SP"
        ):
            raise RegistrationError("Prontuário Inválido!")

    def create(self, participation: Participation):
        """
        Realize the validation and adds the participation to the database.
        :param value: The dataclass with the participation info.
        :raises DateError: If the date is invalid.
        :raises ProjectError: If the project doesn't exists.
        :raises StudentError: If the student isn't in the database.
        :raises InputAlreadyExists: If the participation already exists.
        """
        self.date_validation(participation.initial_date)
        self.project_validation(participation.project)
        self.student_validation(participation.registration)
        self.modal_input_verification(participation.project, participation.registration)
        self.registration_validation(participation.registration)

        p_id = self.project_data.project_name_to_id(self, title=participation.project)
        final_date = self.project_data.project_name_to_final_date(
            self, title=participation.project
        )
        uuid = uuid4()
        with open("assets/data/participations.csv", "a", encoding="utf-8") as data:
            data.write(
                f"{uuid},{data.registration},{p_id},{data.inital_date},{final_date}\n"
            )
