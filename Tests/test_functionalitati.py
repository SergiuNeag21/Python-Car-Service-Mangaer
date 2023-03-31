from Domain.CardClient import CardClient
from Domain.CardValidator import CardClientValidator
from Domain.MasinaValidator import MasinaValidator
from Domain.masina import Masina
from Domain.tranzactie import Tranzactie
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from utils import clear_file


def test_cautare_full_text():
    """
    Functie de test pentru cautarea full text
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
    card_validator = CardClientValidator()
    card_repository = RepositoryJson(filename_card)
    card_service = CardClientService(card_repository,
                                     card_validator, undoRedoService)

    tranzactie_service = TranzactieService(
        tranzactie_repository,
        car_repository,
        card_repository, undoRedoService, masinaService)

    car_service.adauga('1', 'Mercedes', 2011, 3000, 'da')
    car_service.adauga('2', "Audi", 2015, 3000, "nu")

    card_service.adauga('1', 'Neag', 'Sergiu',
                        1234567890111, "05.02.2000", "06.04.2021")
    card_service.adauga("2", "Abc", "Def", 1231231231234,
                        "07.12.2005", "07.09.2010")

    tranzactie_service.adauga('1', '1', '1', 420, 350, '19.11.2021.16.24')
    tranzactie_service.adauga('2', '2', '2', 670, 530, '12.01.2006.10.12')

    text = "11"
    rez = tranzactie_service.cautareFullText(text)
    assert rez == [Masina(idEntitate='1', model='Mercedes', anAchizitie=2011,
                          km=3000, garantie='da'),
                   CardClient(idEntitate='1', nume='Neag', prenume='Sergiu',
                              CNP=1234567890111, dataNasterii='05.02.2000',
                              dataInregistrarii='06.04.2021')]


def test_stergere_casacada():
    """
    Functie de test pentru stergere in cascada
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
    card_validator = CardClientValidator()
    card_repository = RepositoryJson(filename_card)
    card_service = CardClientService(card_repository,
                                     card_validator, undoRedoService)

    tranzactie_service = TranzactieService(
        tranzactie_repository,
        car_repository,
        card_repository, undoRedoService, masinaService)

    car_service.adauga('1', 'Mercedes', 2011, 3000, 'da')
    car_service.adauga('2', "Audi", 2015, 3000, "nu")

    card_service.adauga('1', 'Neag', 'Sergiu',
                        1234567890111, "05.02.2000", "06.04.2021")
    card_service.adauga("2", "Abc", "Def", 1231231231234,
                        "07.12.2005", "07.09.2010")

    tranzactie_service.adauga('1', '1', '1', 420, 350, '19.11.2021.16.24')
    tranzactie_service.adauga('2', '2', '2', 670, 530, '12.01.2006.10.12')

    tranzactie_service.stergeInCascada("1")
    stergere_cascada = tranzactie_service.getAll()
    assert stergere_cascada == [Tranzactie(idEntitate='2', id_masina='2',
                                           id_card_client='2', suma_piese=670,
                                           suma_manopera=477.0,
                                           data='12.01.2006.10.12')]
    tranzactie_service.stergeInCascada("2")
    stergere_cascada = tranzactie_service.getAll()
    assert stergere_cascada == []


def test_generator_masini():
    """
    Functie de test pentru genrtorul de masini
    """
    undoRedoService = UndoRedoService()
    car_validator = MasinaValidator()
    filename_car = 'test_car.json'
    clear_file(filename_car)
    car_repository = RepositoryJson(filename_car)
    car_service = MasinaService(car_repository, car_validator, undoRedoService)

    masini = car_service.getAll()
    assert len(masini) == 0
    car_service.generareMasini(5)
    masini = car_service.getAll()
    assert len(masini) == 5
    car_service.generareMasini(2)
    masini = car_service.getAll()
    assert len(masini) == 7


def test_ordoneaza_dupa_manopera():
    """
    Functie de test pentru ordonarea dupa manopera
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
    card_validator = CardClientValidator()
    card_repository = RepositoryJson(filename_card)
    card_service = CardClientService(card_repository,
                                     card_validator, undoRedoService)

    tranzactie_service = TranzactieService(
        tranzactie_repository,
        car_repository,
        card_repository, undoRedoService, masinaService)

    car_service.adauga('1', 'Mercedes', 2011, 3000, 'da')
    car_service.adauga('2', "Audi", 2015, 3000, "nu")

    card_service.adauga('1', 'Neag', 'Sergiu',
                        1234567890111, "05.02.2000", "06.04.2021")
    card_service.adauga("2", "Abc", "Def", 1231231231234,
                        "07.12.2005", "07.09.2010")

    tranzactie_service.adauga('1', '1', '1', 420, 350, '19.11.2021.16.24')
    tranzactie_service.adauga('2', '2', '2', 670, 530, '12.01.2006.10.12')

    tranzactii = tranzactie_service.orodonareMasiniDupaManopera()
    assert tranzactii == [{'masina': Masina(idEntitate='2', model='Audi',
                                            anAchizitie=2015, km=3000,
                                            garantie='nu'),
                           'suma manopera': 477.0},
                          {'masina': Masina(idEntitate='1', model='Mercedes',
                                            anAchizitie=2011, km=3000,
                                            garantie='da'),
                           'suma manopera': 315.0}]


def test_afisare_card_client_dupa_reducere():
    """
    Functie de test pentru ordonarea cardurilor dupa reducere
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
    card_validator = CardClientValidator()
    card_repository = RepositoryJson(filename_card)
    card_service = CardClientService(card_repository,
                                     card_validator, undoRedoService)

    tranzactie_service = TranzactieService(
        tranzactie_repository,
        car_repository,
        card_repository, undoRedoService, masinaService)

    car_service.adauga('1', 'Mercedes', 2011, 3000, 'da')
    car_service.adauga('2', "Audi", 2015, 3000, "nu")

    card_service.adauga('1', 'Neag', 'Sergiu',
                        1234567890111, "05.02.2000", "06.04.2021")
    card_service.adauga("2", "Abc", "Def", 1231231231234,
                        "07.12.2005", "07.09.2010")

    tranzactie_service.adauga('1', '1', '1', 420, 350, '19.11.2021.16.24')
    tranzactie_service.adauga('2', '2', '2', 670, 530, '12.01.2006.10.12')

    card_ord = tranzactie_service.afisareCarduriDupaReduceri()
    assert card_ord == [{'Card Client': CardClient(idEntitate='2',
                                                   nume='Abc',
                                                   prenume='Def',
                                                   CNP=1231231231234,
                                                   dataNasterii='07.12.2005',
                                                   dataInregistrarii='07.09.'
                                                                     '2010'),
                         'Reduceri': 53.0},
                        {'Card Client': CardClient(idEntitate='1', nume='Neag',
                                                   prenume='Sergiu',
                                                   CNP=1234567890111,
                                                   dataNasterii='05.02.2000',
                                                   dataInregistrarii='06.04.'
                                                                     '2021'),
                         'Reduceri': 35.0}]


def test_all_functionalitati():
    test_cautare_full_text()
    test_stergere_casacada()
    test_ordoneaza_dupa_manopera()
    test_afisare_card_client_dupa_reducere()
