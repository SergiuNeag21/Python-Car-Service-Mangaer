from Domain.CardValidator import CardClientValidator
from Domain.MasinaValidator import MasinaValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from Tests.test_all import test_all
from UI.consola import Consola


def main():
    test_all()
    undoRedoService = UndoRedoService()
    carService = MasinaService

    masinaRepositoryJson = RepositoryJson("masini.json")
    masinaValidator = MasinaValidator()
    masinaService = MasinaService(masinaRepositoryJson,
                                  masinaValidator, undoRedoService)

    cardClientRepositoryJson = RepositoryJson("carduri.json")
    cardClientValidator = CardClientValidator()
    cardClientService = \
        CardClientService(cardClientRepositoryJson,
                          cardClientValidator, undoRedoService)

    tranzactieRepositoryJson = RepositoryJson("tranzactii.json")
    tranzactieService = TranzactieService(
        tranzactieRepositoryJson,
        masinaRepositoryJson,
        cardClientRepositoryJson,
        undoRedoService, carService)

    consola = Consola(masinaService, cardClientService,
                      tranzactieService, undoRedoService)

    consola.runMenu()


main()
