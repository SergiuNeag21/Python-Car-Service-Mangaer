from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiDelete(UndoRedoOperation):
    def __init__(self, repository: Repository, obiecteSterse: list):
        self.__repository = repository
        self.__obiecteSterse = obiecteSterse

    def doUndo(self):
        for entitate in self.__obiecteSterse:
            self.__repository.adauga(entitate)

    def doRedo(self):
        for entitate in self.__obiecteSterse:
            self.__repository.sterge(entitate.idEntitate)
