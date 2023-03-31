import jsonpickle

from Domain.entitate import Entitate
from Repository.repositoryInMemory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __readFile(self):
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __writeFile(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati))

    def read(self, idEntitate=None):
        self.entitati = self.__readFile()
        return super().read(idEntitate)

    def adauga(self, entitate: Entitate):
        self.entitati = self.__readFile()
        super().adauga(entitate)
        self.__writeFile()

    def sterge(self, idEntitate):
        self.entitati = self.__readFile()
        super().sterge(idEntitate)
        self.__writeFile()

    def modifica(self, entitate: Entitate):
        self.entitati = self.__readFile()
        super().modifica(entitate)
        self.__writeFile()
