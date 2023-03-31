from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    nume: str
    prenume: str
    CNP: int
    dataNasterii: str
    dataInregistrarii: str
