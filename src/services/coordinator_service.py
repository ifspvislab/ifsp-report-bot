from dataclasses import dataclass

from data import add_coordinator, load_coordinators


class CoordinatorAlreadyExists(Exception):
    print(Exception)


class ProntuarioError(Exception):
    print(Exception)


class EmailError(Exception):
    print(Exception)


class DiscordIdError(Exception):
    print(Exception)


@dataclass
class Coordinator:
    prontuario: str
    discord_id: int
    name: str
    email: str


class CoordinatorService:
    def __init__(self, data: Coordinator):
        self._prontuario = data.prontuario
        self._name = data.name
        self._email = data.email
        self._discord_id = data.discord_id

    def verify_prontuario(self, value):
        if not (
            value[:1].isalpha()
            and value[2:-2].isnumeric()
            and value[-1].isalnum()
            and len(value) == 9
        ):
            raise ProntuarioError("Prontuario incorreto")

        print("Prontuario correto")
        self._prontuario = value

    def verify_email(self, value):
        if value.count("@") != 1:
            raise EmailError("Email inválido")

        print("Email correto")
        self._email = value

    def verify_discord_id(self, value):
        if not value.isnumeric():
            raise DiscordIdError("Discord ID inválido")

        print("Discord ID correto")
        self._discord_id = value

    def check_ocurrance(self):
        for coordinator in load_coordinators():
            if self.prontuario == coordinator["prontuario"]:
                raise ValueError("Já existe esse membro")

        print("Novo membro")

    def verify_standards(self, coordenador):
        self.verify_prontuario(coordenador.prontuario)
        self.verify_email(coordenador.email)
        self.verify_discord_id(coordenador.discord_id)
        self.check_ocurrance()
        add_coordinator(
            coordenador.prontuario,
            coordenador.name,
            coordenador.email,
            coordenador.discord_id,
        )
