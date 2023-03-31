from typing import Protocol

from Domain.entitate import Entitate


class Repository(Protocol):
    def read(self, idEntitate=None):
        ...

    def adauga(self, entitate: Entitate):
        ...

    def sterge(self, idEntitate: str):
        ...

    def modifica(self, entitate: Entitate):
        ...
