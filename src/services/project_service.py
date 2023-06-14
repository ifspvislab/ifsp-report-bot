from dataclasses import dataclass

from data import _load_projects, add_projects


class ProjectAlreadyExists(Excpetion):
    print(Excpetion)


class DiscordServerIdError(Exception):
    print(Exception)


@dataclass
class Project:
    coordenador: str
    discord_server_id: int
    titulo: str
    data_inicio: int
    data_fim: int


class ProjectService:
    def __init__(self, data: Project):
        self._coordenador = data.coordenador
        self._discord_server_id = data.discord_server_id
        self._titulo = data.titulo
        self._data_inicio = data.data_inicio
        self._data_fim = data.data_fim

    # def verify_coordenador(self, value):

    # def verify_titulo(self, value):

    def verify_discord_server_id(self, value):
        if not value.isnumeric():
            raise DiscordServerIdError("Discord Server ID inválido")

        print("O Discord Server ID foi verificado")
        self._discord_server_id = value

        def check_ocurrance(self):
            for projeto in load_projects():
                if (
                    self.titulo == projeto["titulo"]
                    and self.data_inicio == projeto["data_inicio"]
                    and self.data_fim == projeto["data_fim"]
                ):
                    raise ProjectAlreadyExists("Esse projeto já existe!")

            print("Novo projeto")

    def verify_standards(self, projeto):
        # self.verify_coordenador(projeto.coordenador) // pensar .conferir se o coordenador existe //
        self.verify_discord_server_id(projeto.discord_server_id)
        self.verify_titulo(projeto.titulo)
        self.verify_data_inicio(projeto.data_inicio)
        self.verify_data_fim(projeto.data_fim)
        self.check_ocurrance()
        add_projects(
            projeto.coordenador,
            projeto.discord_server_id,
            projeto.titulo,
            projeto.data_inicio,
            projeto.data_fim,
        )
