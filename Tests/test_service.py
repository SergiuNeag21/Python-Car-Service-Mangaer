from Domain.CardValidator import CardClientValidator
from Domain.MasinaValidator import MasinaValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from utils import clear_file


def test_car_service():
    """
    Functie test service car
    """
    undoRedoService = UndoRedoService()
    car_validator = MasinaValidator()
    filename = 'test_car.json'
    clear_file(filename)
    car_repository = RepositoryJson(filename)
    car_service = MasinaService(car_repository, car_validator, undoRedoService)
    car_service.adauga('3', 'Mercedes', 2011, 3000, 'da')
    assert len(car_service.getAll()) == 1
    car_service.modifica('3', 'Mercedes', 2011, 3000, 'nu')
    assert len(car_service.getAll()) == 1
    car_service.sterge('3')
    assert len(car_service.getAll()) == 0


def test_card_service():
    """
    Functie test service card
    """
    undoRedoService = UndoRedoService()
    card_validator = CardClientValidator()
    filename = 'test_card.json'
    clear_file(filename)
    card_repository = RepositoryJson(filename)
    card_service = CardClientService(card_repository,
                                     card_validator, undoRedoService)
    card_service.adauga('3', 'Neag', 'Sergiu',
                        1234567890111, "05.02.2000", "06.04.2021")
    assert len(card_service.getAll()) == 1
    card_service.sterge('3')
    assert len(card_service.getAll()) == 0


def test_tranzactie_service():
    """
    Functie test service tranzactie
    """
    masinaService = MasinaService
    undoRedoService = UndoRedoService()
    filename_tranzactie = 'test_tranzactie.json'
    clear_file(filename_tranzactie)
    tranzactie_repository = RepositoryJson(filename_tranzactie)

    car_validator = MasinaValidator()
    filename_car = 'test_car.json'
    clear_file(filename_car)
    car_repository = RepositoryJson(filename_car)
    car_service = MasinaService(car_repository, car_validator, undoRedoService)

    filename_card = 'test_card.json'
    clear_file(filename_card)
    card_repository = RepositoryJson(filename_card)

    car_service.adauga('1', 'Mercedes', 2011, 3000, 'da')

    tranzactie_service = TranzactieService(
        tranzactie_repository,
        car_repository,
        card_repository,
        undoRedoService,
        masinaService)
    tranzactie_service.adauga('1', '1', '1', 420, 350, '19.11.2021.16.24')

    assert len(tranzactie_service.getAll()) == 1
    tranzactie_service.sterge('1')
    assert len(tranzactie_service.getAll()) == 0


def test_service():
    """
    Funcite test tot service-ul
    """
    test_car_service()
    test_card_service()
    test_tranzactie_service()
