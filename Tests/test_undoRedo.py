from Domain.CardClient import CardClient
from Domain.CardValidator import CardClientValidator
from Domain.MasinaValidator import MasinaValidator
from Domain.masina import Masina
from Repository.repositoryInMemory import RepositoryInMemory
from Service.cardClientService import CardClientService
from Service.masinaService import MasinaService
from Service.undoRedoService import UndoRedoService


def test_undo():
    """
    Functie de test pentru undo
    """
    masinaRepository = RepositoryInMemory()
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(masinaRepository,
                                  masinaValidator,
                                  undoRedoService)

    masinaService.adauga("1", "Mercedes", 2021, 12000, "da")
    undoRedoService.undo()

    assert len(masinaRepository.read()) == 0

    masinaService.adauga("2", "Mercedes", 2021, 12000, "da")
    masinaService.adauga("3", "Audi", 22012, 130000, "nu")
    undoRedoService.undo()

    assert masinaRepository.read() == [Masina(idEntitate='2',
                                              model='Mercedes',
                                              anAchizitie=2021,
                                              km=12000, garantie='da')]

    undoRedoService.undo()
    assert masinaRepository.read() == []


def test_redo():
    """
    Functie de test pentru redo
    """
    cardClientRepository = RepositoryInMemory()
    cardClientValidator = CardClientValidator()
    undoRedoService = UndoRedoService()
    cardClientService = CardClientService(cardClientRepository,
                                          cardClientValidator,
                                          undoRedoService)

    card1 = CardClient("1", "Neag", "Sergiu",
                       1231231231235, "12.05.2002", "12.12.2002")
    card2 = CardClient("2", "BBB", "LLL",
                       1231231231236, "12.05.2002", "12.12.2002")
    card3 = CardClient("3", "AAA", "MMM",
                       1231231231237, "12.05.2002", "12.12.2002")

    cardClientService.adauga(
        "1", "Neag", "Sergiu", 1231231231235, "12.05.2002", "12.12.2002"
    )
    cardClientService.adauga(
        "2", "BBB", "LLL", 1231231231236, "12.05.2002", "12.12.2002"
    )
    cardClientService.adauga(
        "3", "AAA", "MMM", 1231231231237, "12.05.2002", "12.12.2002"
    )

    undoRedoService.undo()
    assert cardClientRepository.read() == [card1, card2]
    undoRedoService.redo()
    assert cardClientRepository.read() == [card1, card2, card3]

    undoRedoService.undo()
    undoRedoService.undo()
    assert cardClientRepository.read() == [card1]
    undoRedoService.redo()
    assert cardClientRepository.read() == [card1, card2]
