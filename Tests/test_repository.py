from Domain.CardClient import CardClient
from Domain.masina import Masina
from Domain.tranzactie import Tranzactie
from Repository.repositoryJson import RepositoryJson
from utils import clear_file


def test_tranzactie_repository():
    """
    Functie de test tranzactie repository
    """
    filename = 'test_tranzactie.json'
    clear_file(filename)
    tranzactie_repository = RepositoryJson(filename)
    added = Tranzactie('1', '1', '1',
                       200, 250,
                       '11.10.2020,15.51')
    tranzactie_repository.adauga(added)
    assert tranzactie_repository.read(added.idEntitate) == added


def test_masina_repository():
    """
    Functie de test masina repository
    """
    filename = "test_car.json"
    clear_file(filename)
    masina_repository = RepositoryJson(filename)
    added = Masina('1', '1', 200, 250, '11')
    masina_repository.adauga(added)
    assert masina_repository.read(added.idEntitate) == added


def test_card_repository():
    """
    Functie de test card repository
    """
    filename = "test_card.json"
    clear_file(filename)
    card_repository = RepositoryJson(filename)
    added = \
        CardClient('1', '1', '1', 1231231231235, '10.02.2002', '10.02.2021')
    card_repository.adauga(added)
    assert card_repository.read(added.idEntitate) == added


def test_repository():
    """
    Toate testele din repository
    """
    test_tranzactie_repository()
    test_masina_repository()
    test_masina_repository()
